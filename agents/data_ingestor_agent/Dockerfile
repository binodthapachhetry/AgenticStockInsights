FROM python:3.9-slim                                                                                                                                        
                                                                                                                                                             
# Install system dependencies                                                                                                                              
RUN apt-get update && apt-get install -y \                                                                                                                 
    curl \                                                                                                                                                 
    gcc \                                                                                                                                                  
    libssl-dev \                                                                                                                                           
    && rm -rf /var/lib/apt/lists/*                                                                                                                         
                                                                                                                                                           
WORKDIR /app                                                                                                                                               
                                                                                                                                                           
# Install Python dependencies first for layer caching                                                                                                      
COPY requirements.txt .                                                                                                                                    
RUN pip install --no-cache-dir -r requirements.txt                                                                                                         
                                                                                                                                                           
# Copy application code                                                                                                                                    
COPY . .                                                                                                                                                   
                                                                                                                                                           
# Health check configuration                                                                                                                               
HEALTHCHECK --interval=30s --timeout=10s --retries=3 --start-period=30s \                                                                                  
    CMD curl -f http://localhost:8000/health || exit 1                                                                                                     
                                                                                                                                                           
# Production server with timeout and graceful shutdown                                                                                                     
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", \                                                                                                  
    "--bind", "0.0.0.0:8000", "--timeout", "120", \                                                                                                        
    "--preload", "main:app"]  
