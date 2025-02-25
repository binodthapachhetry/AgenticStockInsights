from pydantic import BaseModel, Field                                                                                                                   
from datetime import datetime                                                                                                                           
                                                                                                                                                        
class StockDataSchema(BaseModel):                                                                                                                       
    symbol: str = Field(..., pattern=r'^[A-Z]{1,5}$')                                                                                                   
    open_price: float = Field(..., gt=0)    # Changed from 'price'                                                                                      
    close_price: float = Field(..., gt=0)   # New required field                                                                                        
    volume: int = Field(..., ge=0)                                                                                                                      
    timestamp: datetime                                                                                                                                 
    source: str = "yfinance" 