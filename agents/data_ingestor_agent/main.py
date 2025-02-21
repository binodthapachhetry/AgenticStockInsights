from fastapi import FastAPI, BackgroundTasks
import os
from google.cloud import pubsub_v1

app = FastAPI()

# Example: publish data to Pub/Sub
PROJECT_ID = os.getenv("GCP_PROJECT", "your-gcp-project")
TOPIC_ID = os.getenv("DATA_INGEST_TOPIC", "finance-docs-ingest")

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)

@app.get("/health")
def health():
    return {"status": "ok", "service": "data-ingestor-agent"}

@app.post("/fetch_data")
def fetch_data(bg: BackgroundTasks):
    """
    Example endpoint to fetch new data (e.g., from SEC) 
    and push to Pub/Sub for further processing
    """
    # You'd have a real function that fetches new filings/news
    # For demo, let's simulate a doc
    doc = {
        "text": "Sample SEC Filing content about Company X...",
        "metadata": {"ticker": "COMPX", "date": "2025-02-20"}
    }
    bg.add_task(_publish_to_pubsub, doc)
    return {"status": "fetching"}

def _publish_to_pubsub(document):
    data = str(document).encode("utf-8")
    future = publisher.publish(topic_path, data)
    print("Published message ID:", future.result())