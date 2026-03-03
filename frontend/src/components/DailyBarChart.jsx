import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Paper, Typography } from '@mui/material';

const DailyBarChart = ({ data }) => {
  if (!data || data.length === 0) return null;

  const chartData = data.map(day => ({
    date: day.date,
    ...day.categories
  }));

  return (
    <Paper elevation={3} sx={{ p: 3, mt: 3 }}>
      <Typography variant="h6" gutterBottom>
        Ежедневная активность
      </Typography>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="date" />
          <YAxis tickFormatter={(value) => `${(value / 3600).toFixed(0)}ч`} />
          <Tooltip formatter={(value) => `${(value / 3600).toFixed(1)} часов`} />
          <Legend />
          <Bar dataKey="productive" name="Продуктивно" stackId="a" fill="#4CAF50" />
          <Bar dataKey="neutral" name="Нейтрально" stackId="a" fill="#FFC107" />
          <Bar dataKey="wasteful" name="Бесполезно" stackId="a" fill="#F44336" />
        </BarChart>
      </ResponsiveContainer>
    </Paper>
  );
};

export default DailyBarChart;