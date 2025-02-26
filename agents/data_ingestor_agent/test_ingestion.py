import os    
import time                                                                                                                                           
import pytest
import requests
from unittest.mock import Mock                                                                                                                                        
from datetime import datetime                                                                                                                           
from clients.sec_client import SECClient                                                                                                                
from clients.yfinance_client import YFinanceClient                                                                                                      
from schemas.stock import StockDataSchema      
from requests.exceptions import RequestException                                                                                                         
                                                                                                                                                        
@pytest.fixture                                                                                                                                         
def live_sec_client():                                                                                                                                       
    return SECClient(api_key=os.getenv("SEC_API_KEY", "dummy-key"))     

@pytest.fixture                                                                                                                                         
def sec_client(mocker):                                                                                                                                 
    client = SECClient(api_key="dummy-key")                                                                                                             
    mocker.patch.object(client, '_refresh_cik_mapping')  # Disable initial CIK download                                                                 
    return client                                                                                    
                                                                                                                                                        
@pytest.fixture                                                                                                                                         
def yfinance_client():                                                                                                                                  
    return YFinanceClient()    

                                                                                                                                                                                                                                                                         
def test_sec_filing(live_sec_client, mocker):                                                                                                                        

    filings = live_sec_client.get_company_filings("AAPL")                                                                                                    
    assert isinstance(filings, list)                                                                                                                    
    assert len(filings) > 0                                                                                                                             
    assert all(f["form"] == "10-K" for f in filings)                                                                                                    
                                                                                                                                                        
def test_sec_filing_invalid_ticker_live(live_sec_client): 
    try:
        time.sleep(1)                                                                                              
        # Ensure CIK mapping is loaded                                                                                                                      
        live_sec_client._refresh_cik_mapping()  # Force refresh                                                                                             

        with pytest.raises(ValueError) as exc_info:                                                                                                         
            live_sec_client.get_company_filings("INVALIDTICKER")                                                                                            

        assert "CIK not found" in str(exc_info.value)  
    except RequestException:
            pytest.skip("SEC API unavailable")                                                                                             

def test_sec_filing_invalid_ticker(sec_client, mocker):     
    print("CIK MAP:", sec_client.ticker_cik_map)                                                                                            
    # Force CIK lookup to fail                                                                                                                          
    mocker.patch.object(                                                                                                                                
        sec_client,                                                                                                                                     
        '_get_cik',                                                                                                                                     
        side_effect=ValueError("CIK not found for ticker: INVALIDTICKER")                                                                               
    )                                                                                                                                                

    with pytest.raises(ValueError) as exc_info:                                                                                                         
        sec_client.get_company_filings("INVALIDTICKER")                                                                                                 
                                                                                                                                                        
    # Verify error message                                                                                                                              
    assert "CIK not found" in str(exc_info.value)

def test_stock_validation(yfinance_client):                                                                                                             
    # Test valid data                                                                                                                                   
    raw_data = yfinance_client.get_stock_data("AAPL")                                                                                                   
    validated = StockDataSchema(**raw_data)  # Now matches fields                                                                                       
    assert validated.source == "yfinance"                                                                                                               
                                                                                                                                                        
    # Test invalid data                                                                                                                                 
    invalid_data = raw_data.copy()                                                                                                                      
    invalid_data["open_price"] = -1  # Changed from 'price'                                                                                             
    with pytest.raises(ValueError):                                                                                                                     
        StockDataSchema(**invalid_data)                                                                                                                 
                                                                                                                                                        
def test_stock_data_types(yfinance_client):                                                                                                             
    data = yfinance_client.get_stock_data("MSFT")                                                                                                       
    assert isinstance(data["timestamp"], datetime)                                                                                                      
    assert isinstance(data["volume"], int)   