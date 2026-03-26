import React from 'react';
import { Grid, Paper, Typography, Box } from '@mui/material';

const CATEGORY_LABELS = {
  productive: 'Продуктивно',
  neutral: 'Нейтрально',
  wasteful: 'Бесполезно',
  unknown: 'Прочее',
};

const CATEGORY_COLORS = {
  productive: '#4CAF50',
  neutral: '#42A5F5',
  wasteful: '#EF5350',
  unknown: '#78909C',
};

const fmtHours = (seconds) => {
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  if (h === 0) return `${m} мин`;
  if (m === 0) return `${h} ч`;
  return `${h} ч ${m} мин`;
};

function StatCard({ title, value, subtitle, accent }) {
  return (
    <Paper
      elevation={0}
      sx={{
        p: 2.5,
        borderRadius: 3,
        borderLeft: `3px solid ${accent}`,
        height: '100%',
      }}
    >
      <Typography variant="caption" color="text.secondary" sx={{ textTransform: 'uppercase', letterSpacing: 1, fontSize: 10 }}>
        {title}
      </Typography>
      <Typography variant="h5" sx={{ mt: 0.5, mb: 0.25, fontWeight: 700, color: accent }}>
        {value}
      </Typography>
      {subtitle && (
        <Typography variant="body2" color="text.secondary">
          {subtitle}
        </Typography>
      )}
    </Paper>
  );
}

const StatsCards = ({ categoryStats, topApps, days }) => {
  const totalSeconds = categoryStats?.total_seconds ?? 0;
  const categories = categoryStats?.categories ?? {};

  const productiveSeconds = categories.productive?.seconds ?? 0;
  const productivePct = totalSeconds > 0
    ? ((productiveSeconds / totalSeconds) * 100).toFixed(0)
    : 0;

  const topApp = topApps?.[0];

  const dominantCategory = Object.entries(categories).sort(
    (a, b) => b[1].seconds - a[1].seconds
  )[0];

  return (
    <Grid container spacing={2}>
      <Grid item xs={12} sm={6} md={3}>
        <StatCard
          title={`Всего за ${days} дней`}
          value={fmtHours(totalSeconds)}
          subtitle={`≈ ${(totalSeconds / 3600 / days).toFixed(1)} ч/день`}
          accent="#6C63FF"
        />
      </Grid>

      <Grid item xs={12} sm={6} md={3}>
        <StatCard
          title="Продуктивное время"
          value={fmtHours(productiveSeconds)}
          subtitle={`${productivePct}% от всего времени`}
          accent="#4CAF50"
        />
      </Grid>

      <Grid item xs={12} sm={6} md={3}>
        <StatCard
          title="Топ приложение"
          value={topApp?.app_name ?? '—'}
          subtitle={topApp ? fmtHours(topApp.total_seconds) : 'Нет данных'}
          accent="#FFA726"
        />
      </Grid>

      <Grid item xs={12} sm={6} md={3}>
        <StatCard
          title="Доминирующая категория"
          value={dominantCategory ? CATEGORY_LABELS[dominantCategory[0]] ?? dominantCategory[0] : '—'}
          subtitle={dominantCategory ? fmtHours(dominantCategory[1].seconds) : 'Нет данных'}
          accent={dominantCategory ? CATEGORY_COLORS[dominantCategory[0]] ?? '#78909C' : '#78909C'}
        />
      </Grid>
    </Grid>
  );
};

export default StatsCards;
