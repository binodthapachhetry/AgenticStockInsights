import axios, { AxiosError, AxiosRequestConfig } from 'axios';                                                                                              
import { auth } from '../firebase/config';                                                                                                                  
                                                                                                                                                            
// Get the API URL from environment variables, with a fallback                                                                                              
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8001';                                                                                   
                                                                                                                                                            
console.log('API URL configured as:', API_URL);                                                                                                             
                                                                                                                                                            
const apiClient = axios.create({                                                                                                                            
  baseURL: API_URL,                                                                                                                                         
  headers: {                                                                                                                                                
    'Content-Type': 'application/json'                                                                                                                      
  },                                                                                                                                                        
  timeout: 10000 // 10 seconds timeout                                                                                                                      
});                                                                                                                                                         
                                                                                                                                                            
// Add auth token to requests                                                                                                                               
apiClient.interceptors.request.use(                                                                                                                         
  async (config) => {                                                                                                                                       
    console.log(`Making ${config.method?.toUpperCase()} request to: ${config.baseURL}${config.url}`);                                                       
                                                                                                                                                            
    const user = auth.currentUser;                                                                                                                          
    if (user) {                                                                                                                                             
      const token = await user.getIdToken();                                                                                                                
      config.headers.Authorization = `Bearer ${token}`;                                                                                                     
    }                                                                                                                                                       
    return config;                                                                                                                                          
  },                                                                                                                                                        
  (error) => {                                                                                                                                              
    console.error('Request interceptor error:', error);                                                                                                     
    return Promise.reject(error);                                                                                                                           
  }                                                                                                                                                         
);                                                                                                                                                          
                                                                                                                                                            
// Add response interceptor for logging                                                                                                                     
apiClient.interceptors.response.use(                                                                                                                        
  (response) => {                                                                                                                                           
    console.log(`Response from ${response.config.url}: Status ${response.status}`);                                                                         
    return response;                                                                                                                                        
  },                                                                                                                                                        
  (error: AxiosError) => {                                                                                                                                  
    if (error.response) {                                                                                                                                   
      console.error(`API Error: ${error.response.status} - ${error.response.statusText}`);                                                                  
      console.error('Error data:', error.response.data);                                                                                                    
    } else if (error.request) {                                                                                                                             
      console.error('No response received from API');                                                                                                       
    } else {                                                                                                                                                
      console.error('Error setting up request:', error.message);                                                                                            
    }                                                                                                                                                       
    return Promise.reject(error);                                                                                                                           
  }                                                                                                                                                         
);                                                                                                                                                          
                                                                                                                                                            
export default apiClient;