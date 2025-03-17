import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { 
  Typography, 
  Box, 
  Paper, 
  Grid, 
  CircularProgress,
  Tabs,
  Tab,
  Divider
} from '@mui/material';
import { getStockData, getStockSentiment } from '../api/stocksApi';
import StockPriceChart from '../components/stocks/StockPriceChart';
import SentimentAnalysis from '../components/stocks/SentimentAnalysis';

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`stock-tabpanel-${index}`}
      aria-labelledby={`stock-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box sx={{ p: 3 }}>
          {children}
        </Box>
      )}
    </div>
  );
}

const StockDetail: React.FC = () => {
  const { ticker } = useParams<{ ticker: string }>();
  const [stockData, setStockData] = useState<any>(null);
  const [sentimentData, setSentimentData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [tabValue, setTabValue] = useState(0);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        if (ticker) {
          const stockResponse = await getStockData(ticker);
          setStockData(stockResponse);
          
          try {
            const sentimentResponse = await getStockSentiment(ticker);
            setSentimentData(sentimentResponse);
          } catch (sentimentError) {
            console.error('Error fetching sentiment data:', sentimentError);
            // Don't fail the whole page if sentiment data fails
          }
        }
      } catch (err) {
        console.error('Error fetching stock data:', err);
        setError('Failed to load stock data. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [ticker]);

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Box sx={{ mt: 4 }}>
        <Typography color="error">{error}</Typography>
      </Box>
    );
  }

  return (
    <Box>
      <Paper sx={{ p: 3, mb: 3 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          {ticker}
        </Typography>
        {stockData && (
          <>
            <Typography variant="h6" component="div">
              ${stockData.close_price.toFixed(2)}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Volume: {stockData.volume.toLocaleString()}
            </Typography>
          </>
        )}
      </Paper>

      <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
        <Tabs value={tabValue} onChange={handleTabChange} aria-label="stock information tabs">
          <Tab label="Overview" />
          <Tab label="Sentiment" />
          <Tab label="News" />
        </Tabs>
      </Box>

      <TabPanel value={tabValue} index={0}>
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <Paper sx={{ p: 2 }}>
              <Typography variant="h6" gutterBottom>Price Information</Typography>
              <Divider sx={{ mb: 2 }} />
              <Grid container spacing={2}>
                <Grid item xs={6} md={3}>
                  <Typography variant="body2" color="text.secondary">Open</Typography>
                  <Typography variant="body1">${stockData?.open_price.toFixed(2)}</Typography>
                </Grid>
                <Grid item xs={6} md={3}>
                  <Typography variant="body2" color="text.secondary">Close</Typography>
                  <Typography variant="body1">${stockData?.close_price.toFixed(2)}</Typography>
                </Grid>
                <Grid item xs={6} md={3}>
                  <Typography variant="body2" color="text.secondary">Volume</Typography>
                  <Typography variant="body1">{stockData?.volume.toLocaleString()}</Typography>
                </Grid>
                <Grid item xs={6} md={3}>
                  <Typography variant="body2" color="text.secondary">Date</Typography>
                  <Typography variant="body1">
                    {new Date(stockData?.timestamp).toLocaleDateString()}
                  </Typography>
                </Grid>
              </Grid>
            </Paper>
          </Grid>
          <Grid item xs={12}>
            <Paper sx={{ p: 2 }}>
              <Typography variant="h6" gutterBottom>Price Chart</Typography>
              <Divider sx={{ mb: 2 }} />
              <StockPriceChart ticker={ticker || ''} />
            </Paper>
          </Grid>
        </Grid>
      </TabPanel>

      <TabPanel value={tabValue} index={1}>
        <Paper sx={{ p: 2 }}>
          <Typography variant="h6" gutterBottom>Sentiment Analysis</Typography>
          <Divider sx={{ mb: 2 }} />
          {sentimentData ? (
            <SentimentAnalysis data={sentimentData} />
          ) : (
            <Typography>Sentiment data not available</Typography>
          )}
        </Paper>
      </TabPanel>

      <TabPanel value={tabValue} index={2}>
        <Paper sx={{ p: 2 }}>
          <Typography variant="h6" gutterBottom>Latest News</Typography>
          <Divider sx={{ mb: 2 }} />
          <Typography>News feature coming soon</Typography>
        </Paper>
      </TabPanel>
    </Box>
  );
};

export default StockDetail;