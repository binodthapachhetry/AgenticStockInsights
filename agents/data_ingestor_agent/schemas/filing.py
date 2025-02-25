from pydantic import BaseModel, Field                                                                                                                   
from datetime import datetime                                                                                                                           
from typing import List                                                                                                                                 
                                                                                                                                                        
class SECFilingSchema(BaseModel):                                                                                                                       
    cik: str = Field(..., pattern=r'^\d{10}$')                                                                                                          
    form_type: str = Field(..., min_length=1)                                                                                                           
    filing_date: datetime                                                                                                                               
    report_date: datetime                                                                                                                               
    primary_doc: str = Field(..., pattern=r'^https://www.sec.gov/Archives/edgar/data/\d+/\d+/.*\.htm$')                                                 
    entities: List[str] = [] 