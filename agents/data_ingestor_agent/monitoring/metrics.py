from prometheus_client import Counter, Histogram, Gauge, Summary
import time
from functools import wraps

# Metrics definitions
REQUEST_COUNT = Counter(
    'data_ingestor_requests_total',
    'Total number of requests by endpoint and status',
    ['endpoint', 'status', 'source']
)

REQUEST_LATENCY = Histogram(
    'data_ingestor_request_latency_seconds',
    'Request latency in seconds',
    ['endpoint', 'source']
)

CIRCUIT_STATE = Gauge(
    'data_ingestor_circuit_state',
    'Circuit breaker state (0=closed, 1=open, 2=half-open)',
    ['service']
)

# New metrics
DATA_SIZE = Summary(
    'data_ingestor_data_size_bytes',
    'Size of ingested data in bytes',
    ['source', 'data_type']
)

INGEST_COUNT = Counter(
    'data_ingestor_ingest_operations_total',
    'Total number of data ingestion operations',
    ['source', 'status']
)

DEPENDENCY_UP = Gauge(
    'data_ingestor_dependency_up',
    'Indicates if a dependency is available (1) or not (0)',
    ['dependency']
)

# Decorator for metrics
def track_metrics(source: str):
    """
    Decorator to track metrics for an endpoint
    """
    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            endpoint = func.__name__
            start_time = time.time()
            
            try:
                result = await func(*args, **kwargs)
                REQUEST_COUNT.labels(
                    endpoint=endpoint,
                    status="success",
                    source=source
                ).inc()
                INGEST_COUNT.labels(source=source, status="success").inc()
                
                # Track data size if result has a size attribute or is a dict/list
                if hasattr(result, 'size'):
                    DATA_SIZE.labels(source=source, data_type=type(result).__name__).observe(result.size)
                elif isinstance(result, (dict, list)):
                    DATA_SIZE.labels(source=source, data_type=type(result).__name__).observe(len(str(result)))
                
                return result
            except Exception as e:
                REQUEST_COUNT.labels(
                    endpoint=endpoint,
                    status="error",
                    source=source
                ).inc()
                INGEST_COUNT.labels(source=source, status="error").inc()
                raise e
            finally:
                REQUEST_LATENCY.labels(
                    endpoint=endpoint,
                    source=source
                ).observe(time.time() - start_time)
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            endpoint = func.__name__
            start_time = time.time()
            
            try:
                result = func(*args, **kwargs)
                REQUEST_COUNT.labels(
                    endpoint=endpoint,
                    status="success",
                    source=source
                ).inc()
                INGEST_COUNT.labels(source=source, status="success").inc()
                
                # Track data size if result has a size attribute or is a dict/list
                if hasattr(result, 'size'):
                    DATA_SIZE.labels(source=source, data_type=type(result).__name__).observe(result.size)
                elif isinstance(result, (dict, list)):
                    DATA_SIZE.labels(source=source, data_type=type(result).__name__).observe(len(str(result)))
                
                return result
            except Exception as e:
                REQUEST_COUNT.labels(
                    endpoint=endpoint,
                    status="error",
                    source=source
                ).inc()
                INGEST_COUNT.labels(source=source, status="error").inc()
                raise e
            finally:
                REQUEST_LATENCY.labels(
                    endpoint=endpoint,
                    source=source
                ).observe(time.time() - start_time)
        
        # Choose the appropriate wrapper based on whether the function is async or not
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        return sync_wrapper
    
    return decorator

# Import asyncio at the top to avoid reference errors
import asyncio
