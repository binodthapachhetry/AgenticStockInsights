import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Container, 
  Typography, 
  Grid, 
  Paper, 
  Box,
  Button,
  Card,
  CardContent,
  CardActionArea,
  CircularProgress,
  Divider
} from '@mui/material';
import { useAuth } from '../contexts/AuthContext';

// This would be replaced with actual API calls
const mockWatchlist = [
  { ticker: 'AAPL', name: 'Apple Inc.', price: 182.63, change: 1.25 },
  { ticker: 'MSFT', name: 'Microsoft Corporation', price: 337.42, change: -0.87 },
  { ticker: 'GOOGL', name: 'Alphabet Inc.', price: 131.86, change: 0.54 }
];

const Dashboard: React.FC = () => {
  const { currentUser } = useAuth();
  const [loading, setLoading] = useState(true);
  const [watchlist, setWatchlist] = useState<any[]>([]);
  const navigate = useNavigate();

  useEffect(() => {
    // This would be an API call in a real implementation
    const fetchWatchlist = async () => {
      try {
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 1000));
        setWatchlist(mockWatchlist);
      } catch (error) {
        console.error('Error fetching watchlist:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchWatchlist();
  }, []);

  const handleStockClick = (ticker: string) => {
    navigate(`/stock/${ticker}`);
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Container maxWidth="lg">
      <Box sx={{ mt: 4, mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Dashboard
        </Typography>
        <Typography variant="subtitle1" gutterBottom>
          Welcome back, {currentUser?.email}
        </Typography>
      </Box>

      <Grid container spacing={3}>
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 3, mb: 3 }}>
            <Typography variant="h5" gutterBottom>
              Your Watchlist
            </Typography>
            <Divider sx={{ mb: 2 }} />
            
            {watchlist.length === 0 ? (
              <Typography>You haven't added any stocks to your watchlist yet.</Typography>
            ) : (
              <Grid container spacing={2}>
                {watchlist.map((stock) => (
                  <Grid item xs={12} sm={6} md={4} key={stock.ticker}>
                    <Card>
                      <CardActionArea onClick={() => handleStockClick(stock.ticker)}>
                        <CardContent>
                          <Typography variant="h6" component="div">
                            {stock.ticker}
                          </Typography>
                          <Typography variant="body2" color="text.secondary" gutterBottom>
                            {stock.name}
                          </Typography>
                          <Typography variant="h6" component="div">
                            ${stock.price.toFixed(2)}
                          </Typography>
                          <Typography 
                            variant="body2" 
                            color={stock.change >= 0 ? "success.main" : "error.main"}
                          >
                            {stock.change >= 0 ? "+" : ""}{stock.change.toFixed(2)}%
                          </Typography>
                        </CardContent>
                      </CardActionArea>
                    </Card>
                  </Grid>
                ))}
              </Grid>
            )}
            
            <Button 
              variant="outlined" 
              sx={{ mt: 2 }}
              onClick={() => navigate('/')}
            >
              Add Stocks
            </Button>
          </Paper>
        </Grid>
        
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3, mb: 3 }}>
            <Typography variant="h5" gutterBottom>
              Recent Activity
            </Typography>
            <Divider sx={{ mb: 2 }} />
            <Typography variant="body2" color="text.secondary">
              No recent activity to display.
            </Typography>
          </Paper>
          
          <Paper sx={{ p: 3 }}>
            <Typography variant="h5" gutterBottom>
              Market Overview
            </Typography>
            <Divider sx={{ mb: 2 }} />
            <Typography variant="body2" gutterBottom>
              <strong>S&P 500:</strong> 4,783.45 (+0.32%)
            </Typography>
            <Typography variant="body2" gutterBottom>
              <strong>NASDAQ:</strong> 15,003.22 (+0.58%)
            </Typography>
            <Typography variant="body2" gutterBottom>
              <strong>DOW:</strong> 38,239.98 (+0.17%)
            </Typography>
            <Button 
              variant="text" 
              sx={{ mt: 1 }}
              size="small"
            >
              View More
            </Button>
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
};

export default Dashboard;
