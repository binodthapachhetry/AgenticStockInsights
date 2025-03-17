import json
import logging
from google.cloud import pubsub_v1
from typing import Dict, Any, Optional, Callable
import os

logger = logging.getLogger(__name__)

class PubSubManager:
    """
    Manages Google Cloud Pub/Sub operations for the data ingestor agent.
    Handles publishing messages to topics and subscribing to topics.
    """
    
    def __init__(self, project_id: Optional[str] = None):
        """
        Initialize the Pub/Sub manager
        
        Args:
            project_id: Google Cloud project ID (defaults to GCP_PROJECT env var)
        """
        self.project_id = project_id or os.getenv("GCP_PROJECT", "your-gcp-project")
        self.publisher = pubsub_v1.PublisherClient()
        self.subscriber = pubsub_v1.SubscriberClient()
        self.subscriptions = {}
        
        logger.info(f"PubSubManager initialized for project {self.project_id}")
    
    def publish_message(self, topic_id: str, data: Dict[str, Any], attributes: Optional[Dict[str, str]] = None) -> str:
        """
        Publish a message to a Pub/Sub topic
        
        Args:
            topic_id: The Pub/Sub topic ID
            data: The message data (will be converted to JSON)
            attributes: Optional message attributes
            
        Returns:
            The published message ID
        """
        topic_path = self.publisher.topic_path(self.project_id, topic_id)
        
        # Convert dict to JSON string and then to bytes
        data_bytes = json.dumps(data).encode("utf-8")
        
        # Add attributes if provided
        message_future = self.publisher.publish(
            topic_path, 
            data=data_bytes,
            **attributes if attributes else {}
        )
        
        # Get the message ID
        message_id = message_future.result()
        logger.debug(f"Published message with ID: {message_id} to {topic_id}")
        
        return message_id
    
    def subscribe_to_topic(self, topic_id: str, subscription_id: str, callback: Callable) -> None:
        """
        Subscribe to a Pub/Sub topic
        
        Args:
            topic_id: The Pub/Sub topic ID
            subscription_id: The subscription ID
            callback: Function to call when a message is received
        """
        subscription_path = self.subscriber.subscription_path(
            self.project_id, subscription_id
        )
        
        # Define the callback wrapper
        def callback_wrapper(message):
            try:
                # Parse the message data
                data = json.loads(message.data.decode("utf-8"))
                
                # Call the user callback
                callback(data, message.attributes)
                
                # Acknowledge the message
                message.ack()
                
            except Exception as e:
                logger.error(f"Error processing message: {e}")
                # Don't acknowledge to allow retry
        
        # Subscribe to the topic
        streaming_pull_future = self.subscriber.subscribe(
            subscription_path, callback=callback_wrapper
        )
        
        # Store the subscription
        self.subscriptions[subscription_id] = streaming_pull_future
        
        logger.info(f"Subscribed to {topic_id} with subscription {subscription_id}")
    
    def close(self):
        """Close all subscriptions"""
        for subscription_id, future in self.subscriptions.items():
            future.cancel()
            logger.info(f"Cancelled subscription {subscription_id}")
