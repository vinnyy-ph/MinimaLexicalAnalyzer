// src/components/Buttons.js
import React, { useRef } from 'react';
import { Box, Button } from '@mui/material';
import AnalyzeIcon from '@mui/icons-material/PlayArrow';
import ClearIcon from '@mui/icons-material/Clear';
import LoadIcon from '@mui/icons-material/FolderOpen';
import SaveIcon from '@mui/icons-material/Save'; // Import SaveIcon

const Buttons = ({ onAnalyze, onClear, onLoadFile, onSaveFile }) => {
  const fileInputRef = useRef(null);

  const handleLoadClick = () => {
    if (fileInputRef.current) {
      fileInputRef.current.click();
    }
  };

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      onLoadFile(file);
    }
    event.target.value = null;
  };

  return (
    <Box sx={{ marginTop: 3, display: 'flex', gap: 4, paddingX: 1 }}>
      <Button
        variant="contained"
        color="buttonAnalyze"
        startIcon={<AnalyzeIcon />}
        onClick={onAnalyze}
        fullWidth
        sx={{ 
          fontWeight: 700, 
          fontSize: '1rem',
          letterSpacing: '0.5px',
          color: 'buttonAnalyze.contrastText',
          backgroundColor: 'buttonAnalyze.main',
          '&:hover': {
            backgroundColor: 'buttonAnalyze.dark',
          },
        }}
      >
        Analyze
      </Button>
      <Button
        variant="contained"
        color="buttonClear"
        startIcon={<ClearIcon />}
        onClick={onClear}
        fullWidth
        sx={{ 
          fontWeight: 700, 
          fontSize: '1rem',
          letterSpacing: '0.5px',
          color: 'buttonClear.contrastText',
          backgroundColor: 'buttonClear.main',
          '&:hover': {
            backgroundColor: 'buttonClear.dark',
          },
        }}
      >
        Clear
      </Button>
      <Button
        variant="contained"
        color="buttonLoad"
        startIcon={<LoadIcon />}
        onClick={handleLoadClick}
        fullWidth
        sx={{ 
          fontWeight: 700, 
          fontSize: '1rem',
          letterSpacing: '0.5px',
          color: 'buttonLoad.contrastText',
          backgroundColor: 'buttonLoad.main',
          '&:hover': {
            backgroundColor: 'buttonLoad.dark',
          },
        }}
      >
        Load File
      </Button>
      <Button
        variant="contained"
        color="buttonSave"
        startIcon={<SaveIcon />} // Add SaveIcon
        onClick={onSaveFile} // Handle save click
        fullWidth
        sx={{ 
          fontWeight: 700, 
          fontSize: '1rem',
          letterSpacing: '0.5px',
          color: 'buttonSave.contrastText',
          backgroundColor: 'buttonSave.main',
          '&:hover': {
            backgroundColor: 'buttonSave.dark',
          },
        }}
      >
        Save File
      </Button>
      {/* Hidden file input */}
      <input
        type="file"
        accept=".mnm"
        ref={fileInputRef}
        style={{ display: 'none' }}
        onChange={handleFileChange}
      />
    </Box>
  );
};

export default Buttons;