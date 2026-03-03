import axios from 'axios';

const API_BASE = 'http://localhost:8000/api/v1';

export const api = {
  // Активности
  getActivities: (page = 1, size = 10) => 
    axios.get(`${API_BASE}/activities?page=${page}&size=${size}`),
  
  createActivity: (data) => 
    axios.post(`${API_BASE}/activities`, data),
  
  // Статистика [citation:3][citation:6]
  getCategoryStats: (startDate, endDate) => 
    axios.get(`${API_BASE}/stats/categories`, { params: { start_date: startDate, end_date: endDate } }),
  
  getDailyStats: (days = 7) => 
    axios.get(`${API_BASE}/stats/daily?days=${days}`),
  
  getTopApps: (limit = 10, category = null) => 
    axios.get(`${API_BASE}/stats/top-apps`, { params: { limit, category } })
};