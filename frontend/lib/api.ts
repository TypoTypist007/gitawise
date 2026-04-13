import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: { 'Content-Type': 'application/json' },
});

export const askQuestion = (question: string, language: string = 'english') =>
  api.post('/chat/ask', { question, language });

export const getChapters = () => api.get('/verse/chapters');

export default api;
