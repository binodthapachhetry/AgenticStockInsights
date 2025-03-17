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


import os
import requests
import json
import logging
import aiohttp
from datetime import datetime
from pathlib import Path
from tenacity import retry, retry_if_exception_type, wait_exponential, stop_after_attempt

class SECClient:
    """Client for interacting with the SEC EDGAR API"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://data.sec.gov"
        self.submissions_url = "https://data.sec.gov/submissions"
        self.ticker_cik_map = {}  # Initialize empty map
        
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "StockInsightsPlatform admin@stockinsights.com",
            "Accept-Encoding": "gzip, deflate"
        })
        
        if api_key:
            self.session.headers.update({"Authorization": f"Bearer {api_key}"})
            
        self.logger = logging.getLogger(__name__)
        self._refresh_cik_mapping()  # Load initial data
    
    @retry(
        wait=wait_exponential(multiplier=1),
        stop=stop_after_attempt(3),
        retry=retry_if_exception_type((requests.exceptions.RequestException,)),
        reraise=True
    )
    def get_company_filings(self, ticker: str, form_type="10-K", limit=5):
        """
        Get recent company filings from SEC EDGAR
        
        Args:
            ticker: Company ticker symbol
            form_type: Type of form to retrieve (10-K, 10-Q, 8-K, etc.)
            limit: Maximum number of filings to return
            
        Returns:
            List of filing information
        """
        try:
            cik = self._get_cik(ticker)
            
            # Get company submissions
            url = f"{self.base_url}/submissions/CIK{cik}.json"
            self.logger.info(f"Fetching filings for {ticker} (CIK: {cik})")
            
            response = self.session.get(url)
            response.raise_for_status()
            
            return self._filter_filings(response.json(), form_type, limit)
            
        except Exception as e:
            self.logger.error(f"Error fetching filings for {ticker}: {str(e)}")
            raise
    
    def _filter_filings(self, response_data: dict, form_type="10-K", limit=5) -> list:
        """Filter filings by form type"""
        filings = response_data.get('filings', {}).get('recent', {})
        
        if not filings:
            return []
            
        filtered = []
        
        # Get the relevant data arrays
        form_types = filings.get('form', [])
        filing_dates = filings.get('filingDate', [])
        descriptions = filings.get('primaryDocDescription', [])
        accession_numbers = filings.get('accessionNumber', [])
        
        # Zip and filter
        for i, (form, date, desc) in enumerate(zip(
            form_types, filing_dates, 
            descriptions if descriptions else [""] * len(form_types)
        )):
            if form == form_type and len(filtered) < limit:
                filing_info = {
                    "form": form,
                    "filing_date": date,
                    "description": desc
                }
                
                # Add accession number if available
                if accession_numbers and i < len(accession_numbers):
                    filing_info["accession_number"] = accession_numbers[i]
                
                filtered.append(filing_info)
        
        return filtered
                                                                                                                                                     
    def _get_cik(self, ticker: str) -> str:
        """Get the CIK for a ticker symbol"""
        ticker = ticker.upper()
        if ticker in self.ticker_cik_map:
            return self.ticker_cik_map[ticker]
                                                                                                                  
        # If not found, try refreshing the mapping
        self._refresh_cik_mapping()
        
        if ticker in self.ticker_cik_map:
            return self.ticker_cik_map[ticker]
            
        raise ValueError(f"CIK not found for ticker: {ticker}")

    def _refresh_cik_mapping(self):
        """Load the CIK to ticker mapping from SEC"""
        try:
            # Check if we have a cached version
            cache_file = Path("cik_cache.json")
            
            if cache_file.exists() and (datetime.now().timestamp() - cache_file.stat().st_mtime < 86400):
                # Use cached version if less than 24 hours old
                self.logger.info("Loading CIK mapping from cache")
                with open(cache_file, "r") as f:
                    self.ticker_cik_map = json.load(f)
                return
            
            # Otherwise fetch from SEC
            self.logger.info("Fetching fresh CIK mapping from SEC")
            response = self.session.get("https://www.sec.gov/files/company_tickers.json")
            response.raise_for_status()
            
            companies = response.json()
            
            self.ticker_cik_map = {
                company["ticker"]: str(company["cik_str"]).zfill(10)
                for company in companies.values()
            }
            
            # Cache the results
            with open(cache_file, "w") as f:
                json.dump(self.ticker_cik_map, f)
                
        except Exception as e:
            self.logger.error(f"Error refreshing CIK mapping: {str(e)}")
            # Fallback to local cache if available
            if os.path.exists("cik_cache.json"):
                with open("cik_cache.json") as f:
                    self.ticker_cik_map = json.load(f)
            else:
                self.ticker_cik_map = {}  # Empty if no cache
    
    async def check_connection(self):
        """Check if the SEC API is accessible"""
        async with aiohttp.ClientSession() as session:
            async with session.head(f"{self.base_url}/submissions", headers=self.session.headers) as response:
                if response.status != 200:
                    raise Exception(f"SEC API returned status code {response.status}")
                return True
