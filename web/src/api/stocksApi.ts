import axios from 'axios'; 
import apiClient from './apiClient';

export const getStockData = async (ticker: string) => {

  try {                                                                                                                                                     
    console.log(`Fetching data for ${ticker}`);                                                                                                             
    console.log(`API URL: ${process.env.REACT_APP_API_URL}/ingest/yfinance/${ticker}`);                                                                     
                                                                                                                                                            
    const response = await apiClient.get(`/ingest/yfinance/${ticker}`);                                                                                     
    console.log('API Response:', response.data);                                                                                                            
    return response.data;                                                                                                                                   
  } catch (error: unknown) {                                                                                                                                         
    if (axios.isAxiosError(error)) {                                                                                                                  
      if (error.response) {                                                                                                                                   
        // The request was made and the server responded with a status code                                                                                   
        // that falls out of the range of 2xx                                                                                                                 
        console.error('Response data:', error.response.data);                                                                                                 
        console.error('Response status:', error.response.status);                                                                                             
        console.error('Response headers:', error.response.headers);                                                                                           
      } else if (error.request) {                                                                                                                             
        // The request was made but no response was received                                                                                                  
        console.error('No response received:', error.request);                                                                                                
      } else {                                                                                                                                                
        // Something happened in setting up the request that triggered an Error                                                                               
        console.error('Error message:', error.message);                                                                                                       
      }  
    } else {                                                                                                                                                
      // Handle non-Axios errors                                                                                                                            
      console.error('Unexpected error:', error);                                                                                                            
    }                                                                                                                                                      
    throw error;                                                                                                                                            
  }    

};

export const getStockSentiment = async (ticker: string) => {
  const response = await apiClient.get(`/stock_sentiment_correlations?ticker=${ticker}`);
  return response.data;
};

export const askQuestion = async (question: string) => {
  const response = await apiClient.get(`/ask?q=${encodeURIComponent(question)}`);
  return response.data;
};