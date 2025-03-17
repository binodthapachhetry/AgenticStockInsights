import React, { useState, useEffect } from 'react';
import { 
  LineChart, 
  Line, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  Legend
} from 'recharts';
import { Typography, Box, CircularProgress } from '@mui/material';

interface StockPriceChartProps {
  ticker: string;
  timeRange?: '1d' | '5d' | '1m' | '3m' | '6m' | '1y';
}

// For MVP, we'll use mock data until we connect to the real API
const generateMockData = (ticker: string, days: number) => {
  const data = [];
  const today = new Date();
  let basePrice = 150 + Math.random() * 50; // Random starting price between 150-200
  
  for (let i = days; i >= 0; i--) {
    const date = new Date(today);
    date.setDate(date.getDate() - i);
    
    // Add some random movement to the price
    const change = (Math.random() - 0.5) * 5;
    basePrice += change;
    
    data.push({
      date: date.toISOString().split('T')[0],
      price: parseFloat(basePrice.toFixed(2)),
      volume: Math.floor(Math.random() * 10000000) + 1000000
    });
  }
  
  return data;
};

const StockPriceChart: React.FC<StockPriceChartProps> = ({ ticker, timeRange = '1m' }) => {
  const [chartData, setChartData] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  useEffect(() => {
    const fetchChartData = async () => {
      try {
        setLoading(true);
        
        // In a real implementation, this would be an API call
        // const response = await axios.get(`/api/stocks/${ticker}/history?range=${timeRange}`);
        // setChartData(response.data);
        
        // For MVP, use mock data
        let days = 30; // Default to 1 month
        if (timeRange === '1d') days = 1;
        else if (timeRange === '5d') days = 5;
        else if (timeRange === '3m') days = 90;
        else if (timeRange === '6m') days = 180;
        else if (timeRange === '1y') days = 365;
        
        // Simulate API delay
        await new Promise(resolve => setTimeout(resolve, 500));
        setChartData(generateMockData(ticker, days));
      } catch (err) {
        console.error('Error fetching chart data:', err);
        setError('Failed to load chart data');
      } finally {
        setLoading(false);
      }
    };
    
    fetchChartData();
  }, [ticker, timeRange]);
  
  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', p: 3 }}>
        <CircularProgress />
      </Box>
    );
  }
  
  if (error) {
    return (
      <Typography color="error">{error}</Typography>
    );
  }
  
  return (
    <Box sx={{ width: '100%', height: 300 }}>
      <ResponsiveContainer>
        <LineChart
          data={chartData}
          margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis 
            dataKey="date" 
            tick={{ fontSize: 12 }}
            tickFormatter={(value) => {
              // Format date based on time range
              if (timeRange === '1d' || timeRange === '5d') {
                return new Date(value).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
              }
              return value;
            }}
          />
          <YAxis 
            domain={['auto', 'auto']}
            tick={{ fontSize: 12 }}
            tickFormatter={(value) => `$${value}`}
          />
          <Tooltip 
            formatter={(value) => [`$${value}`, 'Price']}
            labelFormatter={(label) => `Date: ${label}`}
          />
          <Legend />
          <Line 
            type="monotone" 
            dataKey="price" 
            stroke="#8884d8" 
            activeDot={{ r: 8 }} 
            name={`${ticker} Price`}
          />
        </LineChart>
      </ResponsiveContainer>
    </Box>
  );
};

export default StockPriceChart;
