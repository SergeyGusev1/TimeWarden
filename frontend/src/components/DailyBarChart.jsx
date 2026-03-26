import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid,
  Tooltip, Legend, ResponsiveContainer, ReferenceLine,
} from 'recharts';
import { Paper, Typography, Box } from '@mui/material';

const BARS = [
  { key: 'productive', label: 'Продуктивно', color: '#4CAF50' },
  { key: 'neutral',    label: 'Нейтрально',  color: '#42A5F5' },
  { key: 'wasteful',   label: 'Бесполезно',  color: '#EF5350' },
];

const fmtAxisHours = (s) => `${(s / 3600).toFixed(0)}ч`;

const fmtDate = (dateStr) => {
  if (!dateStr) return '';
  const d = new Date(dateStr);
  return d.toLocaleDateString('ru-RU', { day: 'numeric', month: 'short' });
};

const CustomTooltip = ({ active, payload, label }) => {
  if (!active || !payload?.length) return null;
  const total = payload.reduce((sum, p) => sum + (p.value || 0), 0);
  return (
    <Box sx={{ bgcolor: '#1E2530', border: '1px solid rgba(255,255,255,0.1)', borderRadius: 2, p: 1.5, minWidth: 160 }}>
      <Typography variant="body2" fontWeight={600} sx={{ mb: 1 }}>
        {fmtDate(label)}
      </Typography>
      {payload.map((p) => (
        <Box key={p.name} sx={{ display: 'flex', justifyContent: 'space-between', gap: 3 }}>
          <Typography variant="caption" sx={{ color: p.fill }}>{p.name}</Typography>
          <Typography variant="caption" color="text.secondary">
            {(p.value / 3600).toFixed(1)} ч
          </Typography>
        </Box>
      ))}
      <Box sx={{ borderTop: '1px solid rgba(255,255,255,0.1)', mt: 1, pt: 1, display: 'flex', justifyContent: 'space-between' }}>
        <Typography variant="caption" fontWeight={600}>Итого</Typography>
        <Typography variant="caption" fontWeight={600}>{(total / 3600).toFixed(1)} ч</Typography>
      </Box>
    </Box>
  );
};

const DailyBarChart = ({ data, days }) => {
  if (!data || data.length === 0) return null;

  const chartData = data.map(day => ({
    date: day.date,
    productive: day.categories?.productive ?? 0,
    neutral:    day.categories?.neutral    ?? 0,
    wasteful:   day.categories?.wasteful   ?? 0,
  }));

  const avgTotal = chartData.reduce((sum, d) =>
    sum + d.productive + d.neutral + d.wasteful, 0) / chartData.length;

  return (
    <Paper elevation={0} sx={{ p: 3, borderRadius: 3 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', mb: 2 }}>
        <Typography variant="h6">Ежедневная активность</Typography>
        <Typography variant="body2" color="text.secondary">
          За {days} дней · среднее {(avgTotal / 3600).toFixed(1)} ч/день
        </Typography>
      </Box>

      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={chartData} barCategoryGap="30%">
          <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
          <XAxis
            dataKey="date"
            tickFormatter={fmtDate}
            tick={{ fontSize: 12, fill: '#888' }}
            axisLine={false}
            tickLine={false}
          />
          <YAxis
            tickFormatter={fmtAxisHours}
            tick={{ fontSize: 12, fill: '#888' }}
            axisLine={false}
            tickLine={false}
            width={36}
          />
          <Tooltip content={<CustomTooltip />} cursor={{ fill: 'rgba(255,255,255,0.04)' }} />
          <Legend
            wrapperStyle={{ paddingTop: 16, fontSize: 13 }}
            formatter={(value) => <span style={{ color: '#aaa' }}>{value}</span>}
          />
          <ReferenceLine
            y={avgTotal}
            stroke="#6C63FF"
            strokeDasharray="4 4"
            label={{ value: 'среднее', position: 'insideTopRight', fill: '#6C63FF', fontSize: 11 }}
          />
          {BARS.map(({ key, label, color }) => (
            <Bar key={key} dataKey={key} name={label} stackId="a" fill={color} radius={key === 'wasteful' ? [4, 4, 0, 0] : [0, 0, 0, 0]} />
          ))}
        </BarChart>
      </ResponsiveContainer>
    </Paper>
  );
};

export default DailyBarChart;
