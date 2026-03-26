import React from 'react';
import { Grid, Paper, Skeleton } from '@mui/material';

function CardSkeleton({ height = 120 }) {
  return (
    <Paper elevation={0} sx={{ p: 2.5, borderRadius: 3, height }}>
      <Skeleton variant="text" width="50%" height={16} />
      <Skeleton variant="text" width="70%" height={40} sx={{ mt: 0.5 }} />
      <Skeleton variant="text" width="40%" height={16} />
    </Paper>
  );
}

function ChartSkeleton({ height = 340 }) {
  return (
    <Paper elevation={0} sx={{ p: 3, borderRadius: 3, height }}>
      <Skeleton variant="text" width="40%" height={28} sx={{ mb: 2 }} />
      <Skeleton variant="rounded" width="100%" height={height - 80} />
    </Paper>
  );
}

const SkeletonDashboard = () => (
  <Grid container spacing={3}>
    <Grid item xs={12}>
      <Grid container spacing={2}>
        {[0, 1, 2, 3].map(i => (
          <Grid item xs={12} sm={6} md={3} key={i}>
            <CardSkeleton />
          </Grid>
        ))}
      </Grid>
    </Grid>
    <Grid item xs={12} md={5}>
      <ChartSkeleton height={380} />
    </Grid>
    <Grid item xs={12} md={7}>
      <ChartSkeleton height={380} />
    </Grid>
    <Grid item xs={12}>
      <ChartSkeleton height={340} />
    </Grid>
  </Grid>
);

export default SkeletonDashboard;
