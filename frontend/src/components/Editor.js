// src/components/Editor.js

import React, { useRef, useEffect } from 'react';
import Editor from '@monaco-editor/react';
import { MINIMA, tokenizer, languageConfiguration } from './monacoConfig/languageDefinition';
import { provideCompletionItems } from './monacoConfig/completionProvider';
import { MinimaTheme } from './monacoConfig/theme';
import { MinimaThemeLight } from './monacoConfig/lightTheme'; 
import { useTheme } from '@mui/material/styles';

const CodeEditor = ({ code, setCode }) => {
  const editorRef = useRef(null);
  const theme = useTheme();
  const monacoRef = useRef(null);

  const handleEditorChange = (value) => {
    setCode(value);
  };

  const handleEditorDidMount = (editor, monacoInstance) => {
    monacoRef.current = monacoInstance;
    
    // Register language
    monacoInstance.languages.register({ id: MINIMA });

    // Set tokenizer
    monacoInstance.languages.setMonarchTokensProvider(MINIMA, tokenizer);

    // Set language configuration
    monacoInstance.languages.setLanguageConfiguration(MINIMA, languageConfiguration);

    // Register completion provider
    monacoInstance.languages.registerCompletionItemProvider(MINIMA, provideCompletionItems(monacoInstance));

    // Define and set custom dark theme
    monacoInstance.editor.defineTheme('myMinimaTheme', MinimaTheme);

    // Define and set custom light theme
    monacoInstance.editor.defineTheme('myMinimaThemeLight', MinimaThemeLight);

    // Set the initial theme based on MUI theme
    const initialTheme = theme.palette.mode === 'dark' ? 'myMinimaTheme' : 'myMinimaThemeLight';
    monacoInstance.editor.setTheme(initialTheme);
  };

  // Update editor theme based on MUI theme
  useEffect(() => {
    const monaco = monacoRef.current;
    if (monaco) {
      const themeName = theme.palette.mode === 'dark' ? 'myMinimaTheme' : 'myMinimaThemeLight';
      monaco.editor.setTheme(themeName);
    }
  }, [theme.palette.mode]);

  return (
    <Editor
      height="45vh"
      defaultValue="# Write your code here"
      language={MINIMA}
      theme={theme.palette.mode === 'dark' ? 'myMinimaTheme' : 'myMinimaThemeLight'} // Use custom light theme
      value={code}
      onChange={handleEditorChange}
      onMount={handleEditorDidMount}
      options={{
        minimap: { enabled: false },
        fontSize: 15,
        fontFamily: 'Fira Code, Consolas, "Courier New", monospace', 
        cursorBlinking: 'smooth',
        cursorSmoothCaretAnimation: true,
        wordWrap: 'on',
        scrollbar: {
          verticalScrollbarSize: 10,
          horizontalScrollbarSize: 10,
          arrowSize: 10,
          verticalHasArrows: false,
          horizontalHasArrows: false,
          scrollbarMinSize: 8,
          renderVerticalScrollbar: 'auto',
          renderHorizontalScrollbar: 'auto',
        },
      }}
    />
  );
};

export default CodeEditor;