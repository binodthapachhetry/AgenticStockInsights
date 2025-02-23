import requests                                                                                                                                         
from tenacity import retry, wait_exponential 
from circuitbreaker import circuit, CircuitBreakerError                                                                                                 
                                                                                                                                                         
class SECClient:                                                                                                                                        
    def __init__(self, api_key: str):    
         self.circuit_state = "closed"                                                                                                                
         self.base_url = "https://api.sec.gov"                                                                                                           
         self.session = requests.Session()                                                                                                               
         self.session.headers.update({                                                                                                                   
             "User-Agent": "Your Company Name contact@email.com",                                                                                        
             "Authorization": f"Bearer {api_key}"                                                                                                        
         })                                                                                                                                              
    
    @circuit(failure_threshold=3, recovery_timeout=60,                                                                                                  
              expected_exception=requests.exceptions.RequestException,                                                                                   
              fallback_function=_fallback_filings)                                                                                                                                                   
    @retry(wait=wait_exponential(multiplier=1, max=10))                                                                                                 
    def get_filings(self, cik: str, form_type: str):                                                                                                    
         endpoint = f"/submissions/CIK{cik.zfill(10)}.json"                                                                                              
         response = self.session.get(f"{self.base_url}{endpoint}")                                                                                       
         response.raise_for_status()                                                                                                                     
         return self._filter_filings(response.json(), form_type) 
    def _fallback_filings(self, cik: str, form_type: str):                                                                                              
         return {"status": "circuit_open", "cache": get_cached_filings(cik)}                                                                             
                                                                                                                                                         
    def _update_circuit_state(self, error):                                                                                                             
         if isinstance(error, (requests.Timeout, requests.ConnectionError)):                                                                             
             self.circuit_state = "open"  