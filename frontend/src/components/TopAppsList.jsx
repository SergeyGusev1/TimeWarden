import { Paper, Typography, Box, Chip, LinearProgress } from '@mui/material';

const CATEGORY_CONFIG = {
  productive: { label: 'Продуктивно', color: '#4CAF50', bg: 'rgba(76,175,80,0.12)' },
  neutral:    { label: 'Нейтрально',  color: '#42A5F5', bg: 'rgba(66,165,245,0.12)' },
  wasteful:   { label: 'Бесполезно',  color: '#EF5350', bg: 'rgba(239,83,80,0.12)' },
  unknown:    { label: 'Прочее',       color: '#78909C', bg: 'rgba(120,144,156,0.12)' },
};

const fmtTime = (s) => {
  const h = Math.floor(s / 3600);
  const m = Math.floor((s % 3600) / 60);
  if (h === 0) return `${m} мин`;
  if (m === 0) return `${h} ч`;
  return `${h} ч ${m} мин`;
};

const RANK_COLORS = ['#FFD700', '#C0C0C0', '#CD7F32'];

const TopAppsList = ({ data }) => {
  if (!data || data.length === 0) return null;

  const maxSeconds = Math.max(...data.map(a => a.total_seconds));

  return (
    <Paper elevation={0} sx={{ p: 3, borderRadius: 3, height: '100%' }}>
      <Typography variant="h6" gutterBottom>
        Топ приложений
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
        По суммарному времени использования
      </Typography>

      <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1.5 }}>
        {data.map((app, idx) => {
          const cfg = CATEGORY_CONFIG[app.category] ?? CATEGORY_CONFIG.unknown;
          const pct = (app.total_seconds / maxSeconds) * 100;
          return (
            <Box key={app.app_name} sx={{ display: 'flex', alignItems: 'center', gap: 1.5 }}>
              <Typography
                variant="body2"
                sx={{
                  width: 22,
                  textAlign: 'center',
                  fontWeight: 700,
                  color: RANK_COLORS[idx] ?? 'text.secondary',
                  flexShrink: 0,
                }}
              >
                {idx + 1}
              </Typography>

              <Box sx={{ flex: 1, minWidth: 0 }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 0.5 }}>
                  <Typography variant="body2" fontWeight={500} noWrap sx={{ maxWidth: '55%' }}>
                    {app.app_name}
                  </Typography>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <Typography variant="caption" color="text.secondary">
                      {app.sessions} сес.
                    </Typography>
                    <Typography variant="caption" fontWeight={600}>
                      {fmtTime(app.total_seconds)}
                    </Typography>
                  </Box>
                </Box>
                <LinearProgress
                  variant="determinate"
                  value={pct}
                  sx={{
                    height: 6,
                    borderRadius: 3,
                    bgcolor: 'rgba(255,255,255,0.06)',
                    '& .MuiLinearProgress-bar': { bgcolor: cfg.color, borderRadius: 3 },
                  }}
                />
              </Box>

              <Chip
                label={cfg.label}
                size="small"
                sx={{
                  fontSize: 10,
                  height: 20,
                  color: cfg.color,
                  bgcolor: cfg.bg,
                  border: 'none',
                  flexShrink: 0,
                }}
              />
            </Box>
          );
        })}
      </Box>
    </Paper>
  );
};

export default TopAppsList;
