FROM python:3.9-slim                                                                                                                                    
                                                                                                                                                         
# Install system dependencies                                                                                                                           
RUN apt-get update && apt-get install -y \                                                                                                              
    curl \                                                                                                                                              
    gcc \                                                                                                                                               
    libssl-dev \                                                                                                                                        
    && rm -rf /var/lib/apt/lists/*                                                                                                                      
                                                                                                                                                         
WORKDIR /app                                                                                                                                            
                                                                                                                                                         
# Copy requirements file                                                                                                                                
COPY requirements/requirements.txt .                                                                                                                                 
RUN pip install --no-cache-dir -r requirements.txt                                                                                                      
                                                                                                                                                         
# Copy application code                                                                                                                                 
COPY . .                                                                                                                                                
                                                                                                                                                         
# Create metrics directory                                                                                                                              
RUN mkdir -p /app/metrics && chmod 777 /app/metrics                                                                                                     
                                                                                                                                                         
# Health check configuration                                                                                                                            
HEALTHCHECK --interval=30s --timeout=10s --retries=3 --start-period=30s \                                                                               
    CMD curl -f http://localhost:8000/health || exit 1                                                                                                  
                                                                                                                                                         
# Expose port                                                                                                                                           
EXPOSE 8000                                                                                                                                             
                                                                                                                                                         
# Production server with timeout and graceful shutdown                                                                                                  
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
