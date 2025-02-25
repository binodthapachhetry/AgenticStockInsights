import yfinance as yf                                                                                                                                   
from datetime import datetime                                                                                                                           
                                                                                                                                                        
class YFinanceClient:                                                                                                                                   
    def get_stock_data(self, ticker: str, period: str = '1d'):                                                                                          
        stock = yf.Ticker(ticker)                                                                                                                       
        data = stock.history(period=period).iloc[-1].to_dict()                                                                                          
                                                                                                                                                        
        return {                                                                                                                                        
            "symbol": ticker.upper(),                                                                                                                   
            "open_price": data['Open'],                                                                                                                 
            "close_price": data['Close'],                                                                                                               
            "volume": int(data['Volume']),                                                                                                              
            "timestamp": datetime.utcnow(),                                                                                                             
            "source": "yfinance"                                                                                                                        
        } 