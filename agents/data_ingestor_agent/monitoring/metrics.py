from prometheus_client import Counter, Histogram, Gauge                                                                                                 
                                                                                                                                                         
 # Metrics definitions                                                                                                                                   
INGEST_REQUESTS = Counter(                                                                                                                              
     'ingestor_requests_total',                                                                                                                          
     'Total data ingestion requests',                                                                                                                    
     ['source', 'status']                                                                                                                                
 )                                                                                                                                                       
                                                                                                                                                         
PROCESSING_TIME = Histogram(                                                                                                                            
     'ingestor_processing_seconds',                                                                                                                      
     'Data processing latency',                                                                                                                          
     ['pipeline']                                                                                                                                        
 )                                                                                                                                                       
                                                                                                                                                         
CIRCUIT_STATE = Gauge(                                                                                                                                  
     'circuit_breaker_state',                                                                                                                            
     'State of circuit breakers',                                                                                                                        
     ['service']                                                                                                                                         
 )                                                                                                                                                       
                                                                                                                                                         
 # Decorator for metrics                                                                                                                                 
def track_metrics(source: str):                                                                                                                         
    def decorator(func):                                                                                                                                
        async def wrapper(*args, **kwargs):                                                                                                             
            start_time = time.time()                                                                                                                    
            try:                                                                                                                                        
                result = await func(*args, **kwargs)                                                                                                    
                INGEST_REQUESTS.labels(source=source, status="success").inc()                                                                           
                return result                                                                                                                           
            except Exception as e:                                                                                                                      
                INGEST_REQUESTS.labels(source=source, status="failed").inc()                                                                            
                raise                                                                                                                                   
            finally:                                                                                                                                    
                PROCESSING_TIME.labels(pipeline=func.__name__).observe(time.time() - start_time)                                                        
        return wrapper                                                                                                                                  
    return decorator 