import { Paper, Typography, Box, Divider } from '@mui/material';

const CATEGORIES = [
  { key: 'productive', label: 'Продуктивно', color: '#4CAF50' },
  { key: 'neutral',    label: 'Нейтрально',  color: '#42A5F5' },
  { key: 'wasteful',   label: 'Бесполезно',  color: '#EF5350' },
  { key: 'unknown',    label: 'Прочее',       color: '#78909C' },
];

const fmtTime = (s) => {
  const h = Math.floor(s / 3600);
  const m = Math.floor((s % 3600) / 60);
  if (h === 0) return `${m} мин`;
  if (m === 0) return `${h} ч`;
  return `${h} ч ${m} мин`;
};

const todayLabel = () => {
  const d = new Date();
  return d.toLocaleDateString('ru-RU', { weekday: 'long', day: 'numeric', month: 'long' });
};

const TodaySection = ({ data }) => {
  const total = data?.total_seconds ?? 0;
  const cats = data?.categories ?? {};

  const present = CATEGORIES.filter(c => (cats[c.key]?.seconds ?? 0) > 0);
  const productive = cats.productive?.seconds ?? 0;
  const productivePct = total > 0 ? Math.round((productive / total) * 100) : 0;

  return (
    <Paper
      elevation={0}
      sx={{
        p: 3,
        borderRadius: 3,
        background: 'linear-gradient(135deg, rgba(108,99,255,0.12) 0%, rgba(0,217,163,0.07) 100%)',
        border: '1px solid rgba(108,99,255,0.25)',
        display: 'flex',
        gap: 4,
        alignItems: 'center',
        flexWrap: 'wrap',
      }}
    >
      {/* Главная цифра */}
      <Box sx={{ minWidth: 160 }}>
        <Typography variant="caption" color="text.secondary" sx={{ textTransform: 'uppercase', letterSpacing: 1, fontSize: 10 }}>
          Сегодня · {todayLabel()}
        </Typography>
        <Typography variant="h3" sx={{ fontWeight: 800, color: '#fff', lineHeight: 1.1, mt: 0.5 }}>
          {total === 0 ? '—' : fmtTime(total)}
        </Typography>
        {total > 0 && (
          <Typography variant="body2" sx={{ color: '#4CAF50', mt: 0.5 }}>
            {productivePct}% продуктивно
          </Typography>
        )}
      </Box>

      {total > 0 && (
        <>
          {/* Горизонтальный прогресс-бар */}
          <Box sx={{ flex: 1, minWidth: 200 }}>
            <Box sx={{ display: 'flex', height: 12, borderRadius: 6, overflow: 'hidden', mb: 2 }}>
              {CATEGORIES.map(({ key, color }) => {
                const pct = total > 0 ? ((cats[key]?.seconds ?? 0) / total) * 100 : 0;
                if (pct === 0) return null;
                return (
                  <Box
                    key={key}
                    sx={{ width: `${pct}%`, bgcolor: color, transition: 'width 0.5s ease' }}
                  />
                );
              })}
            </Box>

            {/* Детализация по категориям */}
            <Box sx={{ display: 'flex', gap: 3, flexWrap: 'wrap' }}>
              {present.map(({ key, label, color }) => (
                <Box key={key} sx={{ display: 'flex', alignItems: 'center', gap: 0.75 }}>
                  <Box sx={{ width: 8, height: 8, borderRadius: '50%', bgcolor: color, flexShrink: 0 }} />
                  <Typography variant="caption" color="text.secondary">{label}</Typography>
                  <Typography variant="caption" fontWeight={600} sx={{ color }}>
                    {fmtTime(cats[key].seconds)}
                  </Typography>
                </Box>
              ))}
            </Box>
          </Box>

          <Divider orientation="vertical" flexItem sx={{ borderColor: 'rgba(255,255,255,0.1)' }} />

          {/* Мотивационный блок */}
          <Box sx={{ minWidth: 120, textAlign: 'center' }}>
            <Typography variant="h4" sx={{ fontWeight: 800 }}>
              {productivePct >= 70 ? '🔥' : productivePct >= 40 ? '⚡' : '💤'}
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mt: 0.5 }}>
              {productivePct >= 70 ? 'Продуктивный день!' : productivePct >= 40 ? 'Хорошее начало' : 'Можно лучше'}
            </Typography>
          </Box>
        </>
      )}

      {total === 0 && (
        <Typography variant="body2" color="text.secondary">
          Данных за сегодня пока нет. Запусти агент для сбора активности.
        </Typography>
      )}
    </Paper>
  );
};

export default TodaySection;
