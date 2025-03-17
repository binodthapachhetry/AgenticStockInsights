import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Typography, 
  TextField, 
  Button, 
  Box, 
  Paper, 
  Grid,
  Card,
  CardContent,
  CardActionArea
} from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';

const popularStocks = [
  { ticker: 'AAPL', name: 'Apple Inc.' },
  { ticker: 'MSFT', name: 'Microsoft Corporation' },
  { ticker: 'GOOGL', name: 'Alphabet Inc.' },
  { ticker: 'AMZN', name: 'Amazon.com, Inc.' },
  { ticker: 'META', name: 'Meta Platforms, Inc.' },
  { ticker: 'TSLA', name: 'Tesla, Inc.' }
];

const Home: React.FC = () => {
  const [ticker, setTicker] = useState('');
  const navigate = useNavigate();

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (ticker.trim()) {
      navigate(`/stock/${ticker.toUpperCase()}`);
    }
  };

  return (
    <Box>
      <Paper sx={{ p: 4, mb: 4, textAlign: 'center' }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Get Insights on Your Favorite Stocks
        </Typography>
        <Typography variant="subtitle1" gutterBottom>
          Search for a stock to see real-time data, sentiment analysis, and more
        </Typography>
        
        <Box component="form" onSubmit={handleSearch} sx={{ mt: 3, display: 'flex', justifyContent: 'center' }}>
          <TextField
            label="Enter Stock Ticker"
            variant="outlined"
            value={ticker}
            onChange={(e) => setTicker(e.target.value)}
            sx={{ width: '300px', mr: 1 }}
          />
          <Button 
            type="submit" 
            variant="contained" 
            startIcon={<SearchIcon />}
          >
            Search
          </Button>
        </Box>
      </Paper>
      
      <Typography variant="h5" component="h2" gutterBottom>
        Popular Stocks
      </Typography>
      <Grid container spacing={2}>
        {popularStocks.map((stock) => (
          <Grid item xs={12} sm={6} md={4} key={stock.ticker}>
            <Card>
              <CardActionArea onClick={() => navigate(`/stock/${stock.ticker}`)}>
                <CardContent>
                  <Typography variant="h6" component="div">
                    {stock.ticker}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    {stock.name}
                  </Typography>
                </CardContent>
              </CardActionArea>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
};

export default Home;