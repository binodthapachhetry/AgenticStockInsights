import apiClient from './apiClient';

export const getStockData = async (ticker: string) => {
  const response = await apiClient.get(`/ingest/yfinance/${ticker}`);
  return response.data;
};

export const getStockSentiment = async (ticker: string) => {
  const response = await apiClient.get(`/stock_sentiment_correlations?ticker=${ticker}`);
  return response.data;
};

export const askQuestion = async (question: string) => {
  const response = await apiClient.get(`/ask?q=${encodeURIComponent(question)}`);
  return response.data;
};