import React from 'react';
import { 
  Paper, Typography, List, ListItem, 
  ListItemText, LinearProgress, Box, Chip 
} from '@mui/material';

const TopAppsList = ({ data }) => {
  if (!data || data.length === 0) return null;

  const maxSeconds = Math.max(...data.map(app => app.total_seconds));

  return (
    <Paper elevation={3} sx={{ p: 3, mt: 3 }}>
      <Typography variant="h6" gutterBottom>
        Топ приложений
      </Typography>
      <List>
        {data.map((app) => (
          <ListItem key={app.app_name} divider>
            <ListItemText
              primary={app.app_name}
              secondary={
                <Box sx={{ width: '100%', mt: 1 }}>
                  <LinearProgress 
                    variant="determinate" 
                    value={(app.total_seconds / maxSeconds) * 100} 
                    sx={{ height: 10, borderRadius: 5 }}
                  />
                  <Box display="flex" justifyContent="space-between" mt={0.5}>
                    <span>{(app.total_seconds / 3600).toFixed(1)} часов</span>
                    <span>{app.sessions} сессий</span>
                  </Box>
                </Box>
              }
            />
          </ListItem>
        ))}
      </List>
    </Paper>
  );
};

export default TopAppsList;