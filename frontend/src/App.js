// src/App.js

import React, { useState } from 'react';
import { ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { darkTheme } from './theme';
import lightTheme from './themeLight'; // Import the light theme
import Sidebar from './components/Sidebar';
import LexicalAnalyzer from './components/LexicalAnalyzer';
import { Box, IconButton } from '@mui/material';
import Brightness4Icon from '@mui/icons-material/Brightness4'; // Icon for dark mode
import Brightness7Icon from '@mui/icons-material/Brightness7'; // Icon for light mode

const App = () => {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [themeMode, setThemeMode] = useState('dark'); // State to manage theme mode

  const toggleDrawer = () => {
    setSidebarOpen(!sidebarOpen);
  };

  // Function to toggle between light and dark mode
  const toggleTheme = () => {
    setThemeMode((prevMode) => (prevMode === 'dark' ? 'light' : 'dark'));
  };

  return (
    <ThemeProvider theme={themeMode === 'dark' ? darkTheme : lightTheme}>
      <CssBaseline />
      <Box sx={{ display: 'flex' }}>
        <Sidebar open={sidebarOpen} toggleDrawer={toggleDrawer} />
        <Box component="main" sx={{ flexGrow: 1, padding: 0 }}>
          {/* Theme Toggle Button */}
          {/* <IconButton
            sx={{ position: 'fixed', top: 16, right: 16 }}
            onClick={toggleTheme}
            color="inherit"
          >
            {themeMode === 'dark' ? <Brightness7Icon /> : <Brightness4Icon />}
          </IconButton> */}

          <LexicalAnalyzer 
            toggleSidebar={toggleDrawer} 
            themeMode={themeMode}      // Pass themeMode
            toggleTheme={toggleTheme} // Pass toggleTheme
          />
          {/* Other components can go here */}
        </Box>
      </Box>
    </ThemeProvider>
  );
};

export default App;