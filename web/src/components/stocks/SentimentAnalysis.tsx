import React from 'react';
import { 
  Typography, 
  Box, 
  Grid,
  LinearProgress,
  Chip
} from '@mui/material';
import { 
  PieChart, 
  Pie, 
  Cell, 
  ResponsiveContainer,
  Tooltip,
  Legend
} from 'recharts';

interface SentimentAnalysisProps {
  data: any;
}

// Add these new interfaces                                                                                                                                 
interface SentimentSource {                                                                                                                                 
  name: string;                                                                                                                                             
  positive: number;                                                                                                                                         
  negative: number;                                                                                                                                         
  neutral: number;                                                                                                                                          
}                                                                                                                                                           
                                                                                                                                                            
interface SentimentKeyword {                                                                                                                                
  word: string;                                                                                                                                             
  sentiment: string;                                                                                                                                        
  count: number;                                                                                                                                            
}                                                                                                                                                           
                                                                                                                                                            
interface SentimentData {                                                                                                                                   
  overall: {                                                                                                                                                
    positive: number;                                                                                                                                       
    negative: number;                                                                                                                                       
    neutral: number;                                                                                                                                        
  };                                                                                                                                                        
  sources: SentimentSource[];                                                                                                                               
  keywords: SentimentKeyword[];                                                                                                                             
} 


// For MVP, we'll use mock data if real data isn't available
const generateMockSentimentData = () => {
  return {
    overall: {
      positive: 0.65,
      negative: 0.15,
      neutral: 0.20
    },
    sources: [
      { name: 'News Articles', positive: 0.70, negative: 0.10, neutral: 0.20 },
      { name: 'SEC Filings', positive: 0.55, negative: 0.25, neutral: 0.20 },
      { name: 'Social Media', positive: 0.60, negative: 0.30, neutral: 0.10 }
    ],
    keywords: [
      { word: 'growth', sentiment: 'positive', count: 28 },
      { word: 'innovation', sentiment: 'positive', count: 22 },
      { word: 'revenue', sentiment: 'positive', count: 19 },
      { word: 'competition', sentiment: 'neutral', count: 15 },
      { word: 'challenges', sentiment: 'negative', count: 12 }
    ]
  };
};

const SentimentAnalysis: React.FC<SentimentAnalysisProps> = ({ data }) => {
  // Use provided data or generate mock data if it's empty
  const sentimentData = data && Object.keys(data).length > 0 ? data : generateMockSentimentData();
  
  const pieChartData = [
    { name: 'Positive', value: sentimentData.overall.positive * 100 },
    { name: 'Negative', value: sentimentData.overall.negative * 100 },
    { name: 'Neutral', value: sentimentData.overall.neutral * 100 }
  ];
  
  const COLORS = ['#4caf50', '#f44336', '#9e9e9e'];
  
  const getSentimentColor = (sentiment: string) => {
    switch (sentiment) {
      case 'positive': return '#4caf50';
      case 'negative': return '#f44336';
      case 'neutral': return '#9e9e9e';
      default: return '#9e9e9e';
    }
  };
  
  return (
    <Box>
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Typography variant="h6" gutterBottom>Overall Sentiment</Typography>
          <Box sx={{ height: 250 }}>
            <ResponsiveContainer>
              <PieChart>
                <Pie
                  data={pieChartData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                  label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                >
                  {pieChartData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip formatter={(value) => `${value.toString}%`} />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </Box>
        </Grid>
        
        <Grid item xs={12} md={6}>
          <Typography variant="h6" gutterBottom>Sentiment by Source</Typography>
          {sentimentData.sources.map((source: SentimentSource, index: number) => (
            <Box key={index} sx={{ mb: 2 }}>
              <Typography variant="body2" gutterBottom>{source.name}</Typography>
              <Grid container spacing={1} alignItems="center">
                <Grid item xs={3}>
                  <Typography variant="caption" color="text.secondary">Positive</Typography>
                </Grid>
                <Grid item xs={9}>
                  <LinearProgress 
                    variant="determinate" 
                    value={source.positive * 100} 
                    sx={{ 
                      height: 10, 
                      borderRadius: 5,
                      backgroundColor: '#e0e0e0',
                      '& .MuiLinearProgress-bar': {
                        backgroundColor: '#4caf50'
                      }
                    }} 
                  />
                  <Typography variant="caption" sx={{ pl: 1 }}>
                    {(source.positive * 100).toFixed(0)}%
                  </Typography>
                </Grid>
                
                <Grid item xs={3}>
                  <Typography variant="caption" color="text.secondary">Negative</Typography>
                </Grid>
                <Grid item xs={9}>
                  <LinearProgress 
                    variant="determinate" 
                    value={source.negative * 100} 
                    sx={{ 
                      height: 10, 
                      borderRadius: 5,
                      backgroundColor: '#e0e0e0',
                      '& .MuiLinearProgress-bar': {
                        backgroundColor: '#f44336'
                      }
                    }} 
                  />
                  <Typography variant="caption" sx={{ pl: 1 }}>
                    {(source.negative * 100).toFixed(0)}%
                  </Typography>
                </Grid>
              </Grid>
            </Box>
          ))}
        </Grid>
        
        <Grid item xs={12}>
          <Typography variant="h6" gutterBottom>Key Topics</Typography>
          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
            {sentimentData.keywords.map((keyword: SentimentKeyword, index: number) => (
              <Chip 
                key={index}
                label={`${keyword.word} (${keyword.count})`}
                sx={{ 
                  backgroundColor: getSentimentColor(keyword.sentiment),
                  color: 'white'
                }}
              />
            ))}
          </Box>
        </Grid>
      </Grid>
    </Box>
  );
};

export default SentimentAnalysis;
