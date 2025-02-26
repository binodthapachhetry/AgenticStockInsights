# import requests                                                                                                                                         
# from tenacity import retry, wait_exponential 
# from circuitbreaker import circuit, CircuitBreakerError                                                                                                 

# class SECClient:                                                                                                                                       
#      def __init__(self, api_key: str):    
#           self.circuit_state = "closed"                                                                                                                
#           self.base_url = "https://api.sec.gov"                                                                                                           
#           self.session = requests.Session()                                                                                                               
#           self.session.headers.update({                                                                                                                   
#                "User-Agent": "Your Company Name contact@email.com",                                                                                        
#                "Authorization": f"Bearer {api_key}"                                                                                                        
#           })                                                                                                                                              
    
#      @circuit(failure_threshold=3, recovery_timeout=60,                                                                                                  
#               expected_exception=requests.exceptions.RequestException,                                                                                   
#               fallback_function=_fallback_filings)  
                                                                                                                                                     
#      @retry(wait=wait_exponential(multiplier=1, max=10))                                                                                                 
#      def get_filings(self, cik: str, form_type: str):                                                                                                    
#           endpoint = f"/submissions/CIK{cik.zfill(10)}.json"                                                                                              
#           response = self.session.get(f"{self.base_url}{endpoint}")                                                                                       
#           response.raise_for_status()                                                                                                                     
#           return self._filter_filings(response.json(), form_type) 
     
#      def _fallback_filings(self, cik: str, form_type: str):                                                                                              
#           return {"status": "circuit_open", "cache": get_cached_filings(cik)}                                                                             
                                                                                                                                                         
#      def _update_circuit_state(self, error):                                                                                                             
#           if isinstance(error, (requests.Timeout, requests.ConnectionError)):                                                                             
#                self.circuit_state = "open"  


import requests
import os
import json    
import time                                                                                                                           
from tenacity import retry, retry_if_exception_type, wait_exponential, stop_after_attempt                                                                                        
                                                                                                                                                      
class SECClient:                                                                                                                                        
     def __init__(self, api_key: str):  
          self.ticker_cik_map = {}  # Initialize empty map                                                                                                
          self._refresh_cik_mapping()  # Load initial data 
          # self.ticker_cik_map = self._load_cik_mapping()                                                                                                                 
          self.base_url = "https://data.sec.gov"  

          self.session = requests.Session()                                                                                                               
          self.session.headers.update({                                                                                                                   
               "User-Agent": "EducationalPurpose thapachhetry.binod@gmail.com",   
               "Accept-Encoding": "gzip, deflate",                                                                                     
               "Authorization": f"Bearer {api_key}"                                                                                                        
          })                                                                                                                                              
                                                                                                                                                           
     @retry(                                                                                                                                                 
               wait=wait_exponential(multiplier=1),                                                                                                                
               stop=stop_after_attempt(3),                                                                                                                         
               retry=retry_if_exception_type((requests.exceptions.RequestException,)),  # Only retry on network errors                                             
               reraise=True  # Re-raise original error after retries                                                                                               
     )                                                                            
     def get_company_filings(self, ticker: str):                                                                                                         
          """Get latest 10-K filings for a company"""                                                                                                     
          cik = self._get_cik(ticker)                                                                                                                     
          url = f"{self.base_url}/submissions/CIK{cik}.json"  
          print("URL:", url)      
          response = self.session.get(url)                                                                                                                
          response.raise_for_status()                                                                                                                     
          return self._filter_10k_filings(response.json())                                                                                                

     def _filter_10k_filings(self, response_data: dict) -> list:                                                                                             
          filings = response_data.get('filings', {}).get('recent', {})                                                                                                                                                                                                                         
          filtered = []                                                                                                                                       
          for form, date, desc in zip(filings.get('form', []),                                                                                                
                                   filings.get('filingDate', []),                                                                                          
                                   filings.get('primaryDocDescription', [])):                                                                              
               if form == '10-K':                                                                                                                              
                    filtered.append({                                                                                                                           
                         "form": form,                                                                                                                           
                         "filing_date": date,                                                                                                                    
                         "description": desc                                                                                                                     
                    })                                                                                                                                          
                                                                                                                                                           
          return filtered
                                                                                                                                                     
     def _get_cik(self, ticker: str) -> str:                                                                                                             
          if ticker in self.ticker_cik_map:                                                                                                               
               return self.ticker_cik_map[ticker]  
                                                                                                                  
          raise ValueError(f"CIK not found for ticker: {ticker}")
                                                                                                                                                    
          # url = f"https://www.sec.gov/files/company_tickers.json"                                                                                         
          # response = requests.get(url)                                                                                                                    
          # response.raise_for_status()                                                                                                                     
                                                                                                                                                           
          # companies = response.json()                                                                                                                     
          # for company in companies.values():                                                                                                              
          #      if company["ticker"] == ticker.upper():                                                                                                     
          #           cik = str(company["cik_str"]).zfill(10)                                                                                                 
          #           self.ticker_cik_map[ticker] = cik                                                                                                       
          #           return cik                                                                                                                              
                                                                                                                                                           
          # raise ValueError(f"CIK not found for ticker: {ticker}")   

     def _refresh_cik_mapping(self):  # Was previously _load_cik_mapping                                                                                 
          try: 
               time.sleep(10)                                                                                                                                             
               print("Attempting SEC API call...")                                                                                                             
               response = self.session.get("https://www.sec.gov/files/company_tickers.json")                                                                       
               response.raise_for_status()                                                                                                                     
               print(f"API Status: {response.status_code}")                                                                                                    
                                                                                                                                                                
               companies = response.json()                                                                                                                     
               print(f"Received {len(companies)} companies")                                                                                                   
                                                                                                                                                                
               self.ticker_cik_map = {                                                                                                                         
                    company["ticker"]: str(company["cik_str"]).zfill(10)                                                                                        
                    for company in companies.values()                                                                                                           
               }                                                                                                                                               
               print(f"Mapped {len(self.ticker_cik_map)} tickers")                                                                                             
                                                                                                                                                                
               with open("cik_cache.json", "w") as f:                                                                                                          
                    json.dump(self.ticker_cik_map, f)                                                                                                           
               print("Cache updated successfully")                                                                                                             
                                                                                                                                                           
          except Exception as e:                                                                                                                              
               print(f"Refresh failed: {str(e)}")                                                                                                               
               # Fallback to local cache if available                                                                                                      
               if os.path.exists("cik_cache.json"):                                                                                                        
                    with open("cik_cache.json") as f:                                                                                                       
                         self.ticker_cik_map = json.load(f)                                                                                                  
               else:                                                                                                                                       
                    self.ticker_cik_map = {}  # Empty if no cache   