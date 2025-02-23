from pydantic import BaseModel, Field                                                                                                                   
from datetime import datetime                                                                                                                           
                                                                                                                                                         
 class StockDataSchema(BaseModel):                                                                                                                       
     symbol: str = Field(..., pattern=r'^[A-Z]{1,5}$')                                                                                                   
     price: float = Field(..., gt=0)                                                                                                                     
     volume: int = Field(..., ge=0)                                                                                                                      
     timestamp: datetime                                                                                                                                 
     source: str = "yfinance" 