from confluent_kafka import Producer   
from prometheus_client import Counter                                                                                                                 
import json    

KAFKA_ERRORS = Counter(                                                                                                                                 
     'kafka_producer_errors_total',                                                                                                                      
     'Total Kafka producer errors',                                                                                                                      
     ['topic']                                                                                                                                           
 ) 
                                                                                                                                                         
class PubSubManager:                                                                                                                                    
    def __init__(self, bootstrap_servers: str):                                                                                                         
         self.conf = {                                                                                                                                   
             'bootstrap.servers': bootstrap_servers,                                                                                                     
             'message.max.bytes': 15728640,  # 15MB for large filings                                                                                    
             'compression.type': 'lz4'                                                                                                                   
         }                                                                                                                                               
         self.producer = Producer(self.conf)                                                                                                             

    def _delivery_report(self, err, msg):                                                                                                               
        if err:                                                                                                                                         
            KAFKA_ERRORS.labels(topic=msg.topic()).inc()   


    def publish(self, topic: str, validated_data: dict):  
        try:                                                                                              
            self.producer.produce(                                                                                                                          
                topic=topic,                                                                                                                                
                value=json.dumps(validated_data),                                                                                                           
                callback=self._delivery_report 
                self.producer.poll(0)                                                                                                              
            )
        except BufferError as e:                                                                                                                        
             KAFKA_ERRORS.labels(topic=topic).inc()                                                                                                      
             raise  
                                                                                                                          
                                