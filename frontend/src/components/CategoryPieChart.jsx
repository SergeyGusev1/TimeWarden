import React from 'react';
import { PieChart, Pie, Cell, Tooltip, Legend } from 'recharts';
import { Paper, Typography, Box } from '@mui/material';

const COLORS = ['#4CAF50', '#FFC107', '#F44336', '#9E9E9E'];

const CategoryPieChart = ({ data }) => {
  if (!data || !data.categories) return null;

  const chartData = Object.entries(data.categories).map(([name, values]) => ({
    name: name.charAt(0).toUpperCase() + name.slice(1),
    value: values.seconds,
    percentage: values.percentage
  }));

  return (
    <Paper elevation={3} sx={{ p: 3, height: '100%' }}>
      <Typography variant="h6" gutterBottom>
        Распределение по категориям
      </Typography>
      <Box display="flex" justifyContent="center">
        <PieChart width={400} height={300}>
          <Pie
            data={chartData}
            cx="50%"
            cy="50%"
            labelLine={false}
            label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(1)}%`}
            outerRadius={100}
            fill="#8884d8"
            dataKey="value"
          >
            {chartData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip formatter={(value) => `${(value / 3600).toFixed(1)} часов`} />
          <Legend />
        </PieChart>
      </Box>
      <Typography variant="body2" color="text.secondary" align="center">
        Всего: {(data.total_seconds / 3600).toFixed(1)} часов
      </Typography>
    </Paper>
  );
};

export default CategoryPieChart;