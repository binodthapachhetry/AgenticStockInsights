from fastapi import FastAPI, BackgroundTasks, status, Response
import os
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST, multiprocess, CollectorRegistry 
from .monitoring.metrics import track_metrics
from google.cloud import pubsub_v1


app = FastAPI()

# Example: publish data to Pub/Sub
PROJECT_ID = os.getenv("GCP_PROJECT", "your-gcp-project")
TOPIC_ID = os.getenv("DATA_INGEST_TOPIC", "finance-docs-ingest")

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)

@app.get("/health", status_code=status.HTTP_200_OK)                                                                                                     
async def health():                                                                                                                                     
    health_status = {                                                                                                                                   
         "service": "data-ingestor",                                                                                                                     
         "version": "1.2.0",                                                                                                                             
         "status": "healthy",                                                                                                                            
         "dependencies": {                                                                                                                               
             "sec_api": await check_sec_health(),                                                                                                        
             "kafka": check_kafka_health(),                                                                                                              
             "cache": check_cache_health()                                                                                                               
         }                                                                                                                                               
     }                                                                                                                                                   
                                                                                                                                                         
    if any(v["status"] != "healthy" for v in health_status["dependencies"].values()):                                                                   
         health_status["status"] = "degraded"                                                                                                            
         return health_status                                                                                                                            
                                                                                                                                                         
    return health_status
async def check_sec_health():                                                                                                                           
     try:                                                                                                                                                
         resp = await self.sec_client.session.head("https://api.sec.gov")                                                                                
         return {"status": "healthy" if resp.ok else "unhealthy"}                                                                                        
     except Exception as e:                                                                                                                              
         return {"status": "unhealthy", "error": str(e)}                                                                                                 
                                                                                                                                                         
def check_kafka_health():                                                                                                                               
     try:                                                                                                                                                
         consumer = Consumer({"bootstrap.servers": KAFKA_BROKERS, "group.id": "health-check"})                                                           
         topics = consumer.list_topics(timeout=5)                                                                                                        
         return {"status": "healthy", "topics": len(topics.topics)}                                                                                      
     except Exception as e:                                                                                                                              
         return {"status": "unhealthy", "error": str(e)} 

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

@app.post("/ingest/stock")                                                                                                                              
@track_metrics(source="yfinance")                                                                                                                       
async def ingest_stock_data(payload: StockDataSchema):                                                                                                  
    try:                                                                                                                                                
         # Processing logic                                                                                                                              
        CIRCUIT_STATE.labels(service="yfinance").set(1 if yfinance_client.circuit_open else 0)                                                          
        return {"status": "success"}                                                                                                                    
    except CircuitBreakerError:                                                                                                                         
        CIRCUIT_STATE.labels(service="yfinance").set(2)                                                                                                 
        raise HTTPException(status_code=503, detail="Service unavailable")  

@app.get("/metrics")                                                                                                                                    
async def metrics():                                                                                                                                    
    return Response(                                                                                                                                    
        content=generate_latest(),                                                                                                                      
        media_type=CONTENT_TYPE_LATEST                                                                                                                  
    ) 
@app.get("/health/liveness")                                                                                                                            
def liveness_probe():                                                                                                                                   
     """Basic container alive check"""                                                                                                                   
     return Response(status_code=204)                                                                                                                    
                                                                                                                                                         
@app.get("/health/readiness")                                                                                                                           
def readiness_probe():                                                                                                                                  
     """Check service dependencies"""                                                                                                                    
     if not kafka_connected.is_set():                                                                                                                    
         return Response("Kafka not connected", status_code=503)                                                                                         
     return Response(status_code=204)                                                                                                                    
                                                                                                                                                         
@app.get("/health/startup")                                                                                                                             
def startup_probe():                                                                                                                                    
     """Initialization completeness check"""                                                                                                             
     if not app.state.initialized:                                                                                                                       
         return Response("Service initializing", status_code=503)                                                                                        
     return Response(status_code=204)                                                                                                                    
                                                                                                                                                         
 # Add shutdown hook for clean metrics collection                                                                                                        
@app.on_event("shutdown")                                                                                                                               
def shutdown_event():                                                                                                                                   
     registry = CollectorRegistry()                                                                                                                      
     multiprocess.MultiProcessCollector(registry)                                                                                                        
     generate_latest(registry)   


def _publish_to_pubsub(document):
    data = str(document).encode("utf-8")
    future = publisher.publish(topic_path, data)
    print("Published message ID:", future.result())