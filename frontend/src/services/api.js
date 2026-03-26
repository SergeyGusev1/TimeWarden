import axios from 'axios';

const API_BASE = process.env.REACT_APP_API_BASE || 'http://localhost:8000/api/v1';

export const api = {
  // Активности
  getActivities: (page = 1, size = 10) =>
    axios.get(`${API_BASE}/activity`, { params: { page, size } }),

  createActivity: (data) =>
    axios.post(`${API_BASE}/activity`, data),

  // Статистика
  getCategoryStats: (startDate, endDate) =>
    axios.get(`${API_BASE}/stats/categories`, { params: { start_date: startDate, end_date: endDate } }),

  getTodayStats: () => {
    const today = new Date().toISOString().split('T')[0];
    return axios.get(`${API_BASE}/stats/categories`, { params: { start_date: today, end_date: today } });
  },

  getDailyStats: (days = 7) =>
    axios.get(`${API_BASE}/stats/daily`, { params: { days } }),

  getTopApps: (limit = 10, category = null) =>
    axios.get(`${API_BASE}/stats/top-apps`, { params: { limit, category } }),
};