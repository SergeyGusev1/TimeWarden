import React, { useState, useEffect } from 'react';
import { Container, Grid, AppBar, Toolbar, Typography, Button, CircularProgress, Box } from '@mui/material';
import { api } from './services/api';
import CategoryPieChart from './components/CategoryPieChart';
import DailyBarChart from './components/DailyBarChart';
import TopAppsList from './components/TopAppsList';

function App() {
  const [categoryStats, setCategoryStats] = useState(null);
  const [dailyStats, setDailyStats] = useState(null);
  const [topApps, setTopApps] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [categories, daily, top] = await Promise.all([
        api.getCategoryStats(),
        api.getDailyStats(7),
        api.getTopApps(10)
      ]);
      setCategoryStats(categories.data);
      setDailyStats(daily.data);
      setTopApps(top.data);
    } catch (error) {
      console.error('Ошибка загрузки данных:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 60000);
    return () => clearInterval(interval);
  }, []);

  return (
    <>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" sx={{ flexGrow: 1 }}>
            TimeWarden Dashboard
          </Typography>
          <Button color="inherit" onClick={fetchData}>
            Обновить
          </Button>
        </Toolbar>
      </AppBar>
      
      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
        {loading ? (
          <Box display="flex" justifyContent="center" alignItems="center" minHeight="60vh">
            <CircularProgress />
          </Box>
        ) : (
          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <CategoryPieChart data={categoryStats} />
            </Grid>
            <Grid item xs={12} md={6}>
              <TopAppsList data={topApps} />
            </Grid>
            <Grid item xs={12}>
              <DailyBarChart data={dailyStats} />
            </Grid>
          </Grid>
        )}
      </Container>
    </>
  );
}

export default App;
