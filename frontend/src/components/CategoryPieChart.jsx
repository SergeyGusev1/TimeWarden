import { PieChart, Pie, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Paper, Typography, Box, Divider } from '@mui/material';

const CATEGORY_CONFIG = {
  productive: { label: 'Продуктивно', color: '#4CAF50' },
  neutral:    { label: 'Нейтрально',  color: '#42A5F5' },
  wasteful:   { label: 'Бесполезно',  color: '#EF5350' },
  unknown:    { label: 'Прочее',       color: '#78909C' },
};

const fmtHours = (s) => `${(s / 3600).toFixed(1)} ч`;

const CustomTooltip = ({ active, payload }) => {
  if (!active || !payload?.length) return null;
  const { name, value, payload: p } = payload[0];
  return (
    <Box sx={{ bgcolor: '#1E2530', border: '1px solid rgba(255,255,255,0.1)', borderRadius: 2, p: 1.5 }}>
      <Typography variant="body2" fontWeight={600}>{name}</Typography>
      <Typography variant="body2" color="text.secondary">{fmtHours(value)}</Typography>
      <Typography variant="caption" color="text.secondary">{p.percentage?.toFixed(1)}%</Typography>
    </Box>
  );
};

const renderLabel = ({ cx, cy, midAngle, innerRadius, outerRadius, percent }) => {
  if (percent < 0.05) return null;
  const RADIAN = Math.PI / 180;
  const r = innerRadius + (outerRadius - innerRadius) * 0.5;
  const x = cx + r * Math.cos(-midAngle * RADIAN);
  const y = cy + r * Math.sin(-midAngle * RADIAN);
  return (
    <text x={x} y={y} fill="white" textAnchor="middle" dominantBaseline="central" fontSize={13} fontWeight={600}>
      {`${(percent * 100).toFixed(0)}%`}
    </text>
  );
};

const CategoryPieChart = ({ data }) => {
  if (!data?.categories) return null;

  const chartData = Object.entries(data.categories)
    .filter(([, v]) => v.seconds > 0)
    .map(([key, values]) => ({
      name: CATEGORY_CONFIG[key]?.label ?? key,
      value: values.seconds,
      percentage: values.percentage,
      color: CATEGORY_CONFIG[key]?.color ?? '#78909C',
    }));

  return (
    <Paper elevation={0} sx={{ p: 3, height: '100%', borderRadius: 3 }}>
      <Typography variant="h6" gutterBottom>
        Распределение по категориям
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
        Всего: <strong>{fmtHours(data.total_seconds)}</strong>
      </Typography>

      <ResponsiveContainer width="100%" height={260}>
        <PieChart>
          <Pie
            data={chartData}
            cx="50%"
            cy="50%"
            labelLine={false}
            label={renderLabel}
            outerRadius={110}
            innerRadius={50}
            dataKey="value"
            strokeWidth={2}
            stroke="#161B22"
          />

          <Tooltip content={<CustomTooltip />} />
          <Legend
            formatter={(value) => (
              <span style={{ color: '#aaa', fontSize: 13 }}>{value}</span>
            )}
          />
        </PieChart>
      </ResponsiveContainer>

      <Divider sx={{ my: 2, borderColor: 'rgba(255,255,255,0.07)' }} />

      <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
        {chartData.map((item) => (
          <Box key={item.name} sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <Box sx={{ width: 10, height: 10, borderRadius: '50%', bgcolor: item.color }} />
              <Typography variant="body2">{item.name}</Typography>
            </Box>
            <Typography variant="body2" color="text.secondary">
              {fmtHours(item.value)} ({item.percentage?.toFixed(1)}%)
            </Typography>
          </Box>
        ))}
      </Box>
    </Paper>
  );
};

export default CategoryPieChart;
