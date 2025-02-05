// frontend/src/components/WelcomePage.js
import React from 'react';
import { Grid, Typography, Box } from '@mui/material';

const WelcomePage = () => {
  const members = [
    { name: 'Member 1', image: '/assets/member1.jpg' },
    { name: 'Member 2', image: '/assets/member2.jpg' },
    { name: 'Member 3', image: '/assets/member3.jpg' },
    { name: 'Member 4', image: '/assets/member4.jpg' },
    { name: 'Member 5', image: '/assets/member5.jpg' },
    { name: 'Member 6', image: '/assets/member6.jpg' },
  ];

  return (
    <Box sx={{ padding: '2rem', textAlign: 'center' }}>
      <Typography variant="h4" gutterBottom>
        Welcome to the Lexical Analyzer
      </Typography>
      <Grid container spacing={4} justifyContent="center">
        {members.map((member, index) => (
          <Grid item key={index}>
            <Box
              component="img"
              src={member.image}
              alt={member.name}
              sx={{
                width: '150px',
                height: '150px',
                borderRadius: '50%',
                objectFit: 'cover',
                margin: '1rem',
              }}
            />
            <Typography variant="subtitle1">{member.name}</Typography>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
};

export default WelcomePage;