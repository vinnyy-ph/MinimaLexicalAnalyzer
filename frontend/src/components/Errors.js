import React, { useRef, useEffect, useState } from 'react';
import { Alert, AlertTitle, Box, Typography, Tabs, Tab, useTheme } from '@mui/material';

const Errors = ({ errors }) => {
  const theme = useTheme();
  const boxRef = useRef(null);
  // 0: Lexical, 1: Syntax, 2: Semantic
  const [tabIndex, setTabIndex] = useState(0);

  useEffect(() => {
    if (boxRef.current) {
      boxRef.current.scrollTop = 0;
    }
  }, [errors, tabIndex]);

  // Separate errors into lexical, syntax, and semantic categories
  const lexicalErrors = errors.filter((error) => error.type === 'lexical');
  const syntaxErrors = errors.filter((error) => error.type === 'syntax');
  const semanticErrors = errors.filter((error) => error.type === 'semantic');

  const handleTabChange = (event, newIndex) => {
    setTabIndex(newIndex);
  };

  const currentErrors =
    tabIndex === 0 ? lexicalErrors : tabIndex === 1 ? syntaxErrors : semanticErrors;
  const hasErrors = currentErrors.length > 0;

  // Dynamically choose colors based on whether there are errors
  const arrowColor = hasErrors ? '#ff5555' : '#66ff66';
  const alertTitleColor = hasErrors ? '#ff5555' : '#66ff66';
  const secondaryTextColor = hasErrors ? '#ffcccc' : '#ccffcc';

  // Renders the separate bullet points for each category
  const renderExpectedCategories = (error) => {
    const { literals, keywords, symbols, others } = error;
    if (!literals?.length && !keywords?.length && !symbols?.length && !others?.length) {
      return null;
    }

    return (
      <ul style={{ listStyleType: 'disc', paddingLeft: '20px', marginTop: '4px' }}>
        {literals?.length > 0 && (
          <li>
            <Typography variant="body2" sx={{ color: secondaryTextColor }}>
              <strong>Literals:</strong> {literals.join(', ')}
            </Typography>
          </li>
        )}
        {keywords?.length > 0 && (
          <li>
            <Typography variant="body2" sx={{ color: secondaryTextColor }}>
              <strong>Keywords:</strong> {keywords.join(', ')}
            </Typography>
          </li>
        )}
        {symbols?.length > 0 && (
          <li>
            <Typography variant="body2" sx={{ color: secondaryTextColor }}>
              <strong>Symbols:</strong> {symbols.join(', ')}
            </Typography>
          </li>
        )}
        {others?.length > 0 && (
          <li>
            <Typography variant="body2" sx={{ color: secondaryTextColor }}>
              <strong>Others:</strong> {others.join(', ')}
            </Typography>
          </li>
        )}
      </ul>
    );
  };

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
        backgroundColor: '#001524',
        color: '#d4d4d4',
        fontFamily: 'Menlo, Monaco, Consolas, "Courier New", monospace',
        boxShadow: 1,
        '&::-webkit-scrollbar': { width: '10px' },
        '&::-webkit-scrollbar-track': { background: '#2e2e2e', borderRadius: '4px' },
        '&::-webkit-scrollbar-thumb': {
          backgroundColor: '#555',
          borderRadius: '10px',
          border: '2px solid #2e2e2e',
        },
        '&::-webkit-scrollbar-thumb:hover': { backgroundColor: '#777' },
      }}
    >
      {/* Tabs for Lexical, Syntax & Semantic Errors */}
      <Tabs
        value={tabIndex}
        onChange={handleTabChange}
        textColor="inherit"
        indicatorColor="primary"
        centered
        sx={{
          marginBottom: 2,
          '.MuiTabs-flexContainer': {
            borderBottom: '1px solid #444',
          },
          '.MuiTab-root': {
            fontWeight: 'bold',
            textTransform: 'none',
          },
        }}
      >
        <Tab label={`Lexical Errors (${lexicalErrors.length})`} />
        <Tab label={`Syntax Errors (${syntaxErrors.length})`} />
        <Tab label={`Semantic Errors (${semanticErrors.length})`} />
      </Tabs>

      {/* Error Display */}
      <Alert
        severity={hasErrors ? 'error' : 'success'}
        sx={{
          background: 'transparent',
          color: theme.palette.text.primary,
          width: '100%',
        }}
      >
        <AlertTitle sx={{ fontWeight: 'bold', color: alertTitleColor }}>
          {hasErrors
            ? tabIndex === 0
              ? 'Lexical Errors'
              : tabIndex === 1
              ? 'Syntax Errors'
              : 'Semantic Errors'
            : 'You understand Minima, Good Job!'}
        </AlertTitle>

        {hasErrors ? (
          <ul style={{ listStyleType: 'none', paddingLeft: 0, margin: 0 }}>
            {currentErrors.map((error, index) => {
              // Ensure error.message is a string.
              const message =
                error.message && typeof error.message === 'object'
                  ? JSON.stringify(error.message)
                  : error.message || 'Error';
              return (
                <li key={index} style={{ marginBottom: '0.5rem' }}>
                  <Typography variant="body1">
                    <span style={{ color: arrowColor, marginRight: '8px' }}>➜</span>
                    <strong>{message}:</strong>{' '}
                    (Line {error.line || '??'}, Col {error.column || '??'})
                  </Typography>

                  {error.unexpected && (
                    <Typography
                      variant="body2"
                      sx={{ marginLeft: '16px', fontSize: '0.9rem', color: secondaryTextColor }}
                    >
                      <span style={{ color: arrowColor, marginRight: '8px' }}>•</span>
                      Unexpected token: {error.unexpected}
                    </Typography>
                  )}

                  {renderExpectedCategories(error)}
                </li>
              );
            })}
          </ul>
        ) : (
          <Typography variant="body2" sx={{ color: secondaryTextColor }}>
            No errors detected in this category.
          </Typography>
        )}
      </Alert>
    </Box>
  );
};

export default Errors;