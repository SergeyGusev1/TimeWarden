import { useState, useEffect, useCallback } from 'react';
import {
  Container, Grid, AppBar, Toolbar, Typography, Button,
  Alert, Chip, ToggleButton, ToggleButtonGroup,
  CssBaseline,
} from '@mui/material';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { api } from './services/api';
import CategoryPieChart from './components/CategoryPieChart';
import DailyBarChart from './components/DailyBarChart';
import TopAppsList from './components/TopAppsList';
import StatsCards from './components/StatsCards';
import SkeletonDashboard from './components/SkeletonDashboard';
import TodaySection from './components/TodaySection';

const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: { main: '#6C63FF' },
    secondary: { main: '#00D9A3' },
    background: {
      default: '#0D1117',
      paper: '#161B22',
    },
    error: { main: '#EF5350' },
    warning: { main: '#FFA726' },
    success: { main: '#4CAF50' },
    info: { main: '#42A5F5' },
  },
  typography: {
    fontFamily: '"Inter", "Roboto", sans-serif',
    h5: { fontWeight: 700 },
    h6: { fontWeight: 600 },
  },
  components: {
    MuiPaper: {
      styleOverrides: {
        root: {
          backgroundImage: 'none',
          border: '1px solid rgba(255,255,255,0.07)',
          borderRadius: 12,
        },
      },
    },
    MuiAppBar: {
      styleOverrides: {
        root: {
          backgroundImage: 'none',
          backgroundColor: '#0D1117',
          borderBottom: '1px solid rgba(255,255,255,0.07)',
          boxShadow: 'none',
        },
      },
    },
    MuiToggleButton: {
      styleOverrides: {
        root: {
          border: '1px solid rgba(255,255,255,0.12)',
          '&.Mui-selected': {
            backgroundColor: 'rgba(108, 99, 255, 0.2)',
            color: '#6C63FF',
          },
        },
      },
    },
  },
});

const DAY_OPTIONS = [
  { value: 7, label: '7 дней' },
  { value: 14, label: '14 дней' },
  { value: 30, label: '30 дней' },
];

function App() {
  const [categoryStats, setCategoryStats] = useState(null);
  const [dailyStats, setDailyStats] = useState(null);
  const [topApps, setTopApps] = useState(null);
  const [todayStats, setTodayStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [lastUpdated, setLastUpdated] = useState(null);
  const [days, setDays] = useState(7);
  const [refreshing, setRefreshing] = useState(false);

  const fetchData = useCallback(async (selectedDays, isManual = false) => {
    if (isManual) setRefreshing(true);
    setError(null);
    try {
      const [categories, daily, top, today] = await Promise.all([
        api.getCategoryStats(),
        api.getDailyStats(selectedDays),
        api.getTopApps(10),
        api.getTodayStats(),
      ]);
      setCategoryStats(categories.data);
      setDailyStats(daily.data);
      setTopApps(top.data);
      setTodayStats(today.data);
      setLastUpdated(new Date());
    } catch {
      setError('Не удалось загрузить данные. Убедитесь, что бэкенд запущен на порту 8000.');
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }, []);

  useEffect(() => {
    fetchData(days);
    const interval = setInterval(() => fetchData(days), 60000);
    return () => clearInterval(interval);
  }, [days, fetchData]);

  const handleDaysChange = (_, newDays) => {
    if (!newDays) return;
    setDays(newDays);
    fetchData(newDays);
  };

  const formattedTime = lastUpdated
    ? lastUpdated.toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' })
    : null;

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <AppBar position="sticky">
        <Toolbar sx={{ gap: 2 }}>
          <Typography variant="h6" sx={{ flexGrow: 1, letterSpacing: '-0.5px' }}>
            ⏱ TimeWarden
          </Typography>

          {formattedTime && (
            <Chip
              label={`Обновлено в ${formattedTime}`}
              size="small"
              variant="outlined"
              sx={{ borderColor: 'rgba(255,255,255,0.15)', color: 'text.secondary', fontSize: 12 }}
            />
          )}

          <ToggleButtonGroup
            value={days}
            exclusive
            onChange={handleDaysChange}
            size="small"
          >
            {DAY_OPTIONS.map(({ value, label }) => (
              <ToggleButton key={value} value={value} sx={{ px: 1.5, fontSize: 12 }}>
                {label}
              </ToggleButton>
            ))}
          </ToggleButtonGroup>

          <Button
            variant="contained"
            size="small"
            onClick={() => fetchData(days, true)}
            disabled={refreshing}
            disableElevation
            sx={{ minWidth: 110 }}
          >
            {refreshing ? '⟳ Загрузка…' : '⟳ Обновить'}
          </Button>
        </Toolbar>
      </AppBar>

      <Container maxWidth="xl" sx={{ mt: 3, mb: 5 }}>
        {error && (
          <Alert severity="error" sx={{ mb: 3, borderRadius: 2 }} onClose={() => setError(null)}>
            {error}
          </Alert>
        )}

        {loading ? (
          <SkeletonDashboard />
        ) : (
          <Grid container spacing={3}>
            <Grid item xs={12}>
              <TodaySection data={todayStats} />
            </Grid>

            <Grid item xs={12}>
              <StatsCards categoryStats={categoryStats} topApps={topApps} days={days} />
            </Grid>

            <Grid item xs={12} md={5}>
              <CategoryPieChart data={categoryStats} />
            </Grid>

            <Grid item xs={12} md={7}>
              <TopAppsList data={topApps} />
            </Grid>

            <Grid item xs={12}>
              <DailyBarChart data={dailyStats} days={days} />
            </Grid>
          </Grid>
        )}
      </Container>
    </ThemeProvider>
  );
}

export default App;
