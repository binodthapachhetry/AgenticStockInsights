from prometheus_client import Counter, Histogram, Gauge
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

# Decorator for metrics
def track_metrics(source: str):
    """
    Decorator to track metrics for an endpoint
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            endpoint = func.__name__
            start_time = time.time()
            
            try:
                result = func(*args, **kwargs)
                REQUEST_COUNT.labels(
                    endpoint=endpoint,
                    status="success",
                    source=source
                ).inc()
                return result
            except Exception as e:
                REQUEST_COUNT.labels(
                    endpoint=endpoint,
                    status="error",
                    source=source
                ).inc()
                raise e
            finally:
                REQUEST_LATENCY.labels(
                    endpoint=endpoint,
                    source=source
                ).observe(time.time() - start_time)
                
        return wrapper
    return decorator
