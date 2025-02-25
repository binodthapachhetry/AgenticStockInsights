import os                                                                                                                                               
import pytest
import requests
from unittest.mock import Mock                                                                                                                                        
from datetime import datetime                                                                                                                           
from clients.sec_client import SECClient                                                                                                                
from clients.yfinance_client import YFinanceClient                                                                                                      
from schemas.stock import StockDataSchema                                                                                                               
                                                                                                                                                        
# @pytest.fixture                                                                                                                                         
# def sec_client():                                                                                                                                       
#     return SECClient(api_key=os.getenv("SEC_API_KEY", "dummy-key"))     

@pytest.fixture                                                                                                                                         
def sec_client(mocker):                                                                                                                                 
    client = SECClient(api_key="dummy-key")                                                                                                             
    mocker.patch.object(client, '_refresh_cik_mapping')  # Disable initial CIK download                                                                 
    return client                                                                                    
                                                                                                                                                        
@pytest.fixture                                                                                                                                         
def yfinance_client():                                                                                                                                  
    return YFinanceClient()                                                                                                                             
                                                                                                                                                        
# def test_sec_filing(sec_client, mocker):                                                                                                                        
#     sec_client.ticker_cik_map = {'AAPL': '0000320193'}

#     # filings = sec_client.get_company_filings("AAPL")                                                                                                    
#     # assert isinstance(filings, list)                                                                                                                    
#     # assert len(filings) > 0                                                                                                                             
#     # assert all(f["form"] == "10-K" for f in filings)                                                                                                    
                                                                                                                                                        
#     # # Test invalid ticker                                                                                                                               
#     # with pytest.raises(ValueError):                                                                                                                     
#     #     sec_client.get_company_filings("INVALIDTICKER")

#     # Mock API response                                                                                                                                 
#     mock_response = Mock()                                                                                                                              
#     mock_response.json.return_value = {                                                                                                                 
#         'filings': {                                                                                                                                    
#             'recent': {                                                                                                                                 
#                 'form': ['10-K', '10-Q', '10-K'],                                                                                                       
#                 'filingDate': ['2023-01-01', '2023-04-01', '2022-12-31'],                                                                               
#                 'primaryDocDescription': ['Annual report', 'Quarterly report', 'Annual report']                                                         
#             }                                                                                                                                           
#         }                                                                                                                                               
#     }                                                                                                                                                   
#     mock_response.raise_for_status = Mock()                                                                                                             
                                                                                                                                                        
#     # Patch the session get call                                                                                                                        
#     mocker.patch.object(sec_client.session, 'get', return_value=mock_response)                                                                          
                                                                                                                                                        
#     # Test valid                                                                                                                                        
#     filings = sec_client.get_company_filings("AAPL")                                                                                                    
#     assert len(filings) == 2  # Should filter to only 10-Ks                                                                                             
#     assert all(f["form"] == "10-K" for f in filings)                                                                                              

def test_sec_filing_invalid_ticker(sec_client, mocker):                                                                                                 
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

# def test_stock_validation(yfinance_client):                                                                                                             
#     # Test valid data                                                                                                                                   
#     raw_data = yfinance_client.get_stock_data("AAPL")                                                                                                   
#     validated = StockDataSchema(**raw_data)  # Now matches fields                                                                                       
#     assert validated.source == "yfinance"                                                                                                               
                                                                                                                                                        
#     # Test invalid data                                                                                                                                 
#     invalid_data = raw_data.copy()                                                                                                                      
#     invalid_data["open_price"] = -1  # Changed from 'price'                                                                                             
#     with pytest.raises(ValueError):                                                                                                                     
#         StockDataSchema(**invalid_data)                                                                                                                 
                                                                                                                                                        
# def test_stock_data_types(yfinance_client):                                                                                                             
#     data = yfinance_client.get_stock_data("MSFT")                                                                                                       
#     assert isinstance(data["timestamp"], datetime)                                                                                                      
#     assert isinstance(data["volume"], int)   