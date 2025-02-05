// src/components/Errors.js

import React, { useRef, useEffect } from 'react';
import { Alert, AlertTitle, Box, Typography, useTheme } from '@mui/material';

const Errors = ({ errors }) => {
  const hasErrors = errors.length > 0;
  const theme = useTheme();
  const boxRef = useRef(null);

  useEffect(() => {
    if (boxRef.current) {
      boxRef.current.scrollTop = 0;
    }
  }, [errors]);

  return (
    <Box
      ref={boxRef}
      sx={{
        marginTop: 3,
        height: '21vh',
        overflow: 'auto',
        width: '100%',
        padding: 2,
        borderRadius: 2,
        background: theme.palette.background.paper,
        boxShadow: 1,
        '&::-webkit-scrollbar': {
          width: '10px',
        },
        '&::-webkit-scrollbar-track': {
          background: theme.palette.background.default,
          borderRadius: '4px',
        },
        '&::-webkit-scrollbar-thumb': {
          backgroundColor: theme.palette.action.hover,
          borderRadius: '10px',
          border: `2px solid ${theme.palette.background.default}`,
        },
        '&::-webkit-scrollbar-thumb:hover': {
          backgroundColor: theme.palette.action.selected,
        },
      }}
    >
      <Alert
        severity={hasErrors ? 'error' : 'success'}
        sx={{
          background: 'transparent',
          color: theme.palette.text.primary,
          width: '100%',
        }}
      >
        <AlertTitle>
          {hasErrors ? 'Lexical Errors' : 'You understand Minima, Good Job!'}
        </AlertTitle>
        {hasErrors ? (
          <ul>
            {errors.map((error, index) => (
              <li key={index}>
                <strong>{error.message}</strong> {error.value} (Line {error.line}, Column {error.column})
              </li>
            ))}
          </ul>
        ) : (
          <Typography variant="body2">
            No lexical errors detected.
          </Typography>
        )}
      </Alert>
    </Box>
  );
};

export default Errors;