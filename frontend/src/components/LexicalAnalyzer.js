// src/components/LexicalAnalyzer.js

import React, { useState } from 'react';
import CodeEditor from './Editor';
import Buttons from './Buttons';
import OutputTable from './OutputTable';
import Errors from './Errors';
import axios from 'axios';
import logo from '../assets/logomnm.png'; 
import { Grid, Box, Typography, IconButton, useTheme } from '@mui/material';
import Brightness4Icon from '@mui/icons-material/Brightness4'; // Icon for dark mode
import Brightness7Icon from '@mui/icons-material/Brightness7'; // Icon for light mode

const LexicalAnalyzer = ({ toggleSidebar, themeMode, toggleTheme }) => { // Receive theme props
  const [code, setCode] = useState('');
  const [tokens, setTokens] = useState([]);
  const [errors, setErrors] = useState([]);
  const [loading, setLoading] = useState(false);
  const [fileName, setFileName] = useState('');
  const theme = useTheme();

  const handleAnalyze = () => {
    axios
      .post('http://localhost:5000/analyze', { code })
      .then((response) => {
        setTokens(response.data.tokens);
        setErrors(response.data.errors);
      })
      .catch((error) => {
        console.error('Error analyzing code:', error);
      });
  };

  const handleClear = () => {
    setCode('');
    setTokens([]);
    setErrors([]);
  };

  const handleLoadFile = (file) => {
    setLoading(true);
    setFileName(file.name);
    const reader = new FileReader();
    reader.onload = (event) => {
      const fileContent = event.target.result;
      setCode(fileContent);
      setLoading(false);
    };
    reader.onerror = (error) => {
      console.error('Error reading file:', error);
      alert('An error occurred while reading the file.');
      setLoading(false);
    };
    reader.readAsText(file);
  };

  // Implement the Save File functionality
  const handleSaveFile = async () => {
    if (!code) {
      alert('There is no code to save.');
      return;
    }
  
    // Check if the File System Access API is supported
    if ('showSaveFilePicker' in window) {
      try {
        const options = {
          suggestedName: fileName ? fileName : 'code.mnm',
          types: [
            {
              description: 'Minima Files',
              accept: { 'text/plain': ['.mnm'] },
            },
          ],
        };
        const handle = await window.showSaveFilePicker(options);
        const writable = await handle.createWritable();
        await writable.write(code);
        await writable.close();
        alert('File saved successfully!');
      } catch (err) {
        console.error('Error saving file:', err);
        alert('An error occurred while saving the file.');
      }
    } else {
      // Fallback to download
      const blob = new Blob([code], { type: 'text/plain;charset=utf-8' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      const downloadName = fileName ? fileName : 'code.mnm';
      link.href = url;
      link.download = downloadName;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url);
    }
  };

  return (
    <div style={{ padding: '20px' }}>
      <Grid container spacing={2}>
        {/* Editor */}
        <Grid item xs={12} md={6}>
          {/* Editor Container */}
          <Box 
            sx={{ 
              height: 'calc(65vh - 2rem)', 
              borderRadius: 2, 
              background: theme.palette.background.paper, 
              padding: 3,
              boxShadow: 3,
            }}
          >
            <Box 
              sx={{ 
                display: 'flex', 
                justifyContent: 'space-between', 
                alignItems: 'center', 
                marginBottom: 3 
              }}
            >
              {/* Logo with onClick to toggle sidebar */}
              <IconButton 
                onClick={toggleSidebar} 
                sx={{ 
                  display: 'flex', 
                  alignItems: 'center', 
                  transition: 'transform 0.2s',
                  '&:hover': {
                    backgroundColor: 'transparent',
                    transform: 'scale(1.3)',
                  },
                }}
                disableRipple
              >
                <img
                  src={logo}
                  alt="Logo"
                  style={{
                    height: '35px',
                    marginRight: '15px',
                    borderRadius: '8px',
                    boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
                    cursor: 'pointer',
                  }}
                />
              </IconButton>
              <Typography color='text.primary' fontWeight='bold' variant="subtitle1">
                Loaded File: {fileName || 'None'}
              </Typography>
              {/* Theme Toggle Button */}
              <IconButton
                sx={{ ml: 1 }}
                onClick={toggleTheme}
                color="inherit"
              >
                {themeMode === 'dark' ? <Brightness7Icon /> : <Brightness4Icon />}
              </IconButton>
            </Box>
            <CodeEditor code={code} setCode={setCode} loading={loading} />
          </Box>
          
          {/* Buttons */}
          <Buttons
            onAnalyze={handleAnalyze}
            onClear={handleClear}
            onLoadFile={handleLoadFile}
            onSaveFile={handleSaveFile} // Pass the save handler
          />
          {/* Errors */}
          <Errors errors={errors} />
        </Grid>
        {/* Output Table */}
        <Grid item xs={12} md={6} sx={{ height: '100%' }}>
          <Box 
            sx={{ 
              borderRadius: 2, 
              background: theme.palette.background.paper, 
              padding: 3,
              boxShadow: 3,
              height: '100%',
            }}
          >
            <OutputTable tokens={tokens}/>
          </Box>
        </Grid>
      </Grid>
    </div>
  );
};

export default LexicalAnalyzer;