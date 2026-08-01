import React, { useState, useEffect } from 'react';
import {
  Container,
  Paper,
  Typography,
  TextField,
  Button,
  Box,
  MenuItem,
  Alert,
  LinearProgress,
  Grid,
  Chip,
  IconButton,
  Collapse,
  Fade,
  Slide,
  Tooltip,
  Zoom,
  Avatar,
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { codeReviewAPI } from '../../api';
import AceEditor from 'react-ace';
import { motion } from 'framer-motion';
import { toast } from 'react-toastify';
import CloseIcon from '@mui/icons-material/Close';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import PlayArrowIcon from '@mui/icons-material/PlayArrow';
import CodeIcon from '@mui/icons-material/Code';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import AutoAwesomeIcon from '@mui/icons-material/AutoAwesome';
import LanguageIcon from '@mui/icons-material/Language';
import DescriptionIcon from '@mui/icons-material/Description';
import WarningIcon from '@mui/icons-material/Warning';
import InfoIcon from '@mui/icons-material/Info';
import ErrorIcon from '@mui/icons-material/Error';

import 'ace-builds/src-noconflict/mode-python';
import 'ace-builds/src-noconflict/mode-javascript';
import 'ace-builds/src-noconflict/mode-typescript';
import 'ace-builds/src-noconflict/mode-java';
import 'ace-builds/src-noconflict/mode-c_cpp';
import 'ace-builds/src-noconflict/mode-csharp';
import 'ace-builds/src-noconflict/mode-golang';
import 'ace-builds/src-noconflict/mode-rust';
import 'ace-builds/src-noconflict/mode-ruby';
import 'ace-builds/src-noconflict/mode-php';
import 'ace-builds/src-noconflict/mode-html';
import 'ace-builds/src-noconflict/mode-css';
import 'ace-builds/src-noconflict/mode-sql';
import 'ace-builds/src-noconflict/mode-swift';
import 'ace-builds/src-noconflict/mode-kotlin';
import 'ace-builds/src-noconflict/mode-r';
import 'ace-builds/src-noconflict/mode-scala';
import 'ace-builds/src-noconflict/mode-perl';
import 'ace-builds/src-noconflict/mode-sh';
import 'ace-builds/src-noconflict/mode-dart';
import 'ace-builds/src-noconflict/mode-elixir';
import 'ace-builds/src-noconflict/mode-haskell';
import 'ace-builds/src-noconflict/mode-lua';
import 'ace-builds/src-noconflict/mode-julia';
import 'ace-builds/src-noconflict/theme-monokai';
import 'ace-builds/src-noconflict/theme-github';
import 'ace-builds/src-noconflict/theme-dracula';

// Language colors
const languageColors = {
  'Python': '#3776AB',
  'JavaScript': '#F7DF1E',
  'TypeScript': '#3178C6',
  'Java': '#007396',
  'C++': '#00599C',
  'C': '#A8B9CC',
  'C#': '#239120',
  'Go': '#00ADD8',
  'Rust': '#DEA584',
  'Ruby': '#CC342D',
  'PHP': '#777BB4',
  'HTML': '#E34F26',
  'CSS': '#1572B6',
  'SQL': '#336791',
  'Swift': '#FA7343',
  'Kotlin': '#7F52FF',
  'R': '#276DC3',
  'Scala': '#DC322F',
  'Perl': '#39457E',
  'Shell': '#4EAA25',
  'Dart': '#00B4AB',
  'Elixir': '#4B275F',
  'Haskell': '#5E5086',
  'Lua': '#2C2D72',
  'Julia': '#9558B2',
};

const languageEmojis = {
  'Python': '🐍',
  'JavaScript': '🟨',
  'TypeScript': '🔵',
  'Java': '☕',
  'C++': '➕➕',
  'C': '©️',
  'C#': '#️⃣',
  'Go': '🐹',
  'Rust': '🦀',
  'Ruby': '💎',
  'PHP': '🐘',
  'HTML': '🌐',
  'CSS': '🎨',
  'SQL': '🗄️',
  'Swift': '🦅',
  'Kotlin': '🎯',
  'R': '📊',
  'Scala': '🔷',
  'Perl': '🐫',
  'Shell': '💻',
  'Dart': '🎯',
  'Elixir': '💧',
  'Haskell': 'λ',
  'Lua': '🌙',
  'Julia': '🔢',
};

// Language patterns - ONLY used when manually triggering detection
const languagePatterns = {
  'Haskell': {
    patterns: ['module ', 'where', '::', '->', 'data ', 'class ', 'instance', 'deriving', 'do ', '<-', 'putStrLn'],
    keywords: ['haskell', 'hs'],
  },
  'JavaScript': {
    patterns: ['function ', 'const ', 'let ', 'var ', 'console.log', '=>', 'export ', 'import {'],
    keywords: ['javascript', 'js'],
  },
  'TypeScript': {
    patterns: [': string', ': number', ': boolean', 'interface ', 'type ', 'export interface', 'enum ', 'implements'],
    keywords: ['typescript', 'ts'],
  },
  'Java': {
    patterns: ['public class', 'private ', 'protected ', 'public static void', 'System.out.println', 'import java.', '@Override'],
    keywords: ['java'],
  },
  'C': {
    patterns: ['#include', 'int main(', 'printf(', 'scanf(', 'malloc(', 'free(', 'char*'],
    keywords: ['c'],
  },
  'C++': {
    patterns: ['#include', 'std::', 'cout', 'cin', 'class ', 'public:', 'private:', 'virtual ', 'template'],
    keywords: ['cpp', 'c++'],
  },
  'C#': {
    patterns: ['using System', 'namespace ', 'public class', 'private ', 'Console.WriteLine', 'get; set;'],
    keywords: ['csharp', 'c#'],
  },
  'Go': {
    patterns: ['package ', 'func ', 'import ', 'fmt.Println', 'go ', 'chan ', 'func main()'],
    keywords: ['golang', 'go'],
  },
  'Rust': {
    patterns: ['fn ', 'let mut', 'println!', 'match ', 'impl ', 'pub fn', 'fn main()', 'mod ', 'unsafe'],
    keywords: ['rust', 'rs'],
  },
  'Ruby': {
    patterns: ['def ', 'end', 'attr_accessor', 'puts ', 'class ', 'require ', 'module ', 'include '],
    keywords: ['ruby', 'rb'],
  },
  'PHP': {
    patterns: ['<?php', 'echo ', 'function ', 'public function', 'private function', '$_GET', '$_POST', '->'],
    keywords: ['php'],
  },
  'Python': {
    patterns: ['def ', 'import ', 'from ', 'class ', 'print(', 'if __name__', 'self.', 'self,'],
    keywords: ['python', 'py'],
  },
  'Julia': {
    patterns: ['function ', 'end', '::', 'println(', 'using ', 'import ', 'Dict{', 'Array{', 'Vector{'],
    keywords: ['julia', 'jl'],
  },
  'Swift': {
    patterns: ['import UIKit', 'import Foundation', 'func ', 'var ', 'let ', 'class ', 'override', 'init('],
    keywords: ['swift'],
  },
  'Kotlin': {
    patterns: ['fun ', 'var ', 'val ', 'class ', 'data class', 'suspend', 'companion object'],
    keywords: ['kotlin', 'kt'],
  },
  'HTML': {
    patterns: ['<!DOCTYPE html>', '<html>', '<body>', '<div>', '<span>', '<p>', '<head>', '<title>'],
    keywords: ['html'],
  },
  'CSS': {
    patterns: ['{', '}', 'color:', 'margin:', 'padding:', 'font-size:', 'border:', '@media', '@keyframes'],
    keywords: ['css'],
  },
  'SQL': {
    patterns: ['SELECT ', 'INSERT ', 'UPDATE ', 'DELETE ', 'CREATE ', 'DROP ', 'ALTER ', 'FROM ', 'WHERE ', 'JOIN '],
    keywords: ['sql'],
  },
  'R': {
    patterns: ['<-', 'function(', 'library(', 'data.frame', 'ggplot', 'c(', 'list('],
    keywords: ['r'],
  },
  'Scala': {
    patterns: ['def ', 'val ', 'var ', 'object ', 'trait ', 'case class', 'extends', 'implicit'],
    keywords: ['scala'],
  },
  'Perl': {
    patterns: ['my ', 'sub ', 'use strict', 'use warnings', '$', '@', '%', 'print '],
    keywords: ['perl', 'pl'],
  },
  'Shell': {
    patterns: ['#!/bin/', 'echo ', 'export ', 'if [', 'for ', 'then', 'fi', 'done'],
    keywords: ['shell', 'bash', 'sh'],
  },
  'Dart': {
    patterns: ['void main()', 'import ', 'class ', 'extends ', 'Widget', 'StatefulWidget', 'async'],
    keywords: ['dart'],
  },
  'Elixir': {
    patterns: ['defmodule', 'def ', 'defp ', 'do', 'end', 'alias ', 'import ', '|>', '->'],
    keywords: ['elixir', 'ex'],
  },
  'Lua': {
    patterns: ['function ', 'local ', 'end', 'table.', 'pairs', 'require ', 'print('],
    keywords: ['lua'],
  },
};

const CodeSubmission = () => {
  const navigate = useNavigate();
  const [languages, setLanguages] = useState([]);
  const [formData, setFormData] = useState({
    language: '',
    title: '',
    code: '',
    description: '',
    file: null,
  });
  const [loading, setLoading] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [showPreview, setShowPreview] = useState(false);
  const [selectedLanguage, setSelectedLanguage] = useState(null);
  const [charCount, setCharCount] = useState(0);
  const [lineCount, setLineCount] = useState(0);
  const [isDarkTheme, setIsDarkTheme] = useState(true);
  const [detectedLanguage, setDetectedLanguage] = useState(null);
  const [languageMismatch, setLanguageMismatch] = useState(false);

  useEffect(() => {
    fetchLanguages();
  }, []);

  // ==============================================================
  // FIX: Only update char/line count, NO AUTO-DETECTION!
  // ==============================================================
  useEffect(() => {
    if (formData.code) {
      setCharCount(formData.code.length);
      setLineCount(formData.code.split('\n').length);
      // DISABLED: detectCodeLanguage(formData.code);  // ← COMMENTED OUT!
    } else {
      setCharCount(0);
      setLineCount(0);
    }
  }, [formData.code]);

  // ==============================================================
  // FIX: Only check mismatch when language is selected
  // ==============================================================
  useEffect(() => {
    if (detectedLanguage && selectedLanguage) {
      const isMatch = detectedLanguage === selectedLanguage.name;
      setLanguageMismatch(!isMatch);
    } else {
      setLanguageMismatch(false);
    }
  }, [detectedLanguage, selectedLanguage]);

  // ==============================================================
  // DETECT LANGUAGE - ONLY CALLED MANUALLY
  // ==============================================================
  const detectCodeLanguage = (code) => {
    if (!code || code.trim() === '') {
      setDetectedLanguage(null);
      toast.info('Please paste some code first');
      return;
    }

    let bestMatch = null;
    let maxScore = 0;

    for (const [lang, config] of Object.entries(languagePatterns)) {
      let score = 0;
      const codeLower = code.toLowerCase();
      const lines = code.split('\n');

      for (const pattern of config.patterns) {
        if (code.includes(pattern)) {
          score += 2;
        }
      }

      for (const keyword of config.keywords) {
        if (codeLower.includes(keyword)) {
          score += 1;
        }
      }

      for (const line of lines) {
        const trimmed = line.trim();
        if (trimmed) {
          if (trimmed.startsWith('#!')) {
            if (trimmed.includes('python')) score += 3;
            if (trimmed.includes('node')) score += 3;
            if (trimmed.includes('ruby')) score += 3;
            if (trimmed.includes('perl')) score += 3;
            if (trimmed.includes('bash')) score += 3;
            if (trimmed.includes('sh')) score += 3;
            if (trimmed.includes('runhaskell')) score += 5;
          }
          break;
        }
      }

      if (score > maxScore) {
        maxScore = score;
        bestMatch = lang;
      }
    }

    if (maxScore >= 3 && bestMatch) {
      setDetectedLanguage(bestMatch);
      toast.success(`✅ Detected: ${bestMatch}`);
    } else {
      setDetectedLanguage(null);
      toast.warning('Could not detect language. Please select manually.');
    }
  };

  // ==============================================================
  // HANDLE LANGUAGE SELECTION - Auto-detect when selected
  // ==============================================================
  const handleLanguageChange = (e) => {
    const value = e.target.value;
    const lang = languages.find(l => l.id === value);
    setSelectedLanguage(lang);
    setFormData({
      ...formData,
      language: value,
    });
    
    // Check if selected language matches detected language
    if (detectedLanguage && lang) {
      const isMatch = detectedLanguage === lang.name;
      setLanguageMismatch(!isMatch);
      if (!isMatch) {
        toast.warning(`⚠️ Language mismatch: You selected ${lang.name} but code appears to be ${detectedLanguage}`);
      } else {
        toast.success(`✅ Language matched: ${lang.name}`);
      }
    }
    
    toast.info(`Switched to ${lang?.name || 'language'}`);
  };

  // ==============================================================
  // HANDLE DETECT BUTTON CLICK
  // ==============================================================
  const handleDetectLanguage = () => {
    if (!formData.code) {
      toast.error('Please paste some code first');
      return;
    }
    detectCodeLanguage(formData.code);
  };

  const handleCodeChange = (newCode) => {
    setFormData({
      ...formData,
      code: newCode,
    });
    // Clear detection when code changes
    setDetectedLanguage(null);
    setLanguageMismatch(false);
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (event) => {
        const content = event.target.result;
        setFormData({
          ...formData,
          code: content,
          file_name: file.name,
        });
        setDetectedLanguage(null);
        setLanguageMismatch(false);
        toast.success(`✅ File ${file.name} loaded successfully!`);
      };
      reader.readAsText(file);
    }
  };

  const fetchLanguages = async () => {
    setLoading(true);
    try {
      const response = await codeReviewAPI.getLanguages();
      console.log('Languages response:', response.data);
      
      let languagesData = [];
      if (Array.isArray(response.data)) {
        languagesData = response.data;
      } else if (response.data && Array.isArray(response.data.results)) {
        languagesData = response.data.results;
      } else if (response.data && typeof response.data === 'object') {
        languagesData = response.data.data || [];
      }
      
      console.log('Languages data:', languagesData);
      setLanguages(languagesData);
      
      if (languagesData && languagesData.length > 0) {
        setFormData(prev => ({ ...prev, language: languagesData[0].id }));
        setSelectedLanguage(languagesData[0]);
      }
    } catch (error) {
      console.error('Failed to fetch languages:', error);
      toast.error('Failed to load programming languages');
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const validateForm = () => {
    if (!formData.code && !formData.file) {
      setError('Please provide code either by typing or uploading a file');
      toast.error('Please provide code');
      return false;
    }

    if (!formData.title || formData.title.trim() === '') {
      setError('Please provide a title for your code');
      toast.error('Title is required');
      return false;
    }

    if (!formData.language) {
      setError('Please select a programming language');
      toast.error('Language is required');
      return false;
    }

    if (formData.code && formData.code.length > 100000) {
      setError('Code is too large. Please upload a file instead.');
      toast.error('Code too large');
      return false;
    }

    return true;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    
    if (!validateForm()) {
      return;
    }
    
    setSubmitting(true);

    try {
      const selectedLang = languages.find(l => l.id === formData.language);
      const languageName = selectedLang ? selectedLang.name : 'Python';
      
      const submissionData = {
        language: formData.language,
        title: formData.title,
        code: formData.code,
        description: formData.description || '',
        language_name: languageName
      };

      console.log('📤 Submitting:', submissionData);
      console.log('📝 Language selected:', languageName);
      
      const response = await codeReviewAPI.createSubmission(submissionData);
      console.log('✅ Submission response:', response.data);
      
      const submissionId = response.data.id;
      console.log('📝 Submission ID:', submissionId);
      
      if (!submissionId) {
        throw new Error('No submission ID returned');
      }
      
      toast.success('✅ Code submitted successfully!');
      setSuccess('Code submitted successfully!');
      
      try {
        console.log('🤖 Initiating AI review for submission:', submissionId);
        const reviewResponse = await codeReviewAPI.initiateReview(submissionId);
        console.log('✅ Review response:', reviewResponse.data);
        toast.success('🤖 AI review completed successfully!');
      } catch (aiError) {
        console.error('❌ AI review failed:', aiError);
        console.error('Error details:', aiError.response?.data);
        toast.warning('Code submitted but AI review failed to start');
      }
      
      setTimeout(() => {
        navigate('/dashboard');
      }, 3000);
      
    } catch (error) {
      console.error('❌ Submission failed:', error);
      console.error('Error details:', error.response?.data);
      
      let errorMsg = 'Failed to submit code. Please try again.';
      if (error.response?.data?.message) {
        errorMsg = error.response.data.message;
      } else if (error.response?.data?.errors) {
        const errors = error.response.data.errors;
        if (typeof errors === 'string') {
          errorMsg = errors;
        } else if (Array.isArray(errors)) {
          errorMsg = errors[0];
        } else {
          const firstKey = Object.keys(errors)[0];
          if (firstKey && errors[firstKey]) {
            errorMsg = Array.isArray(errors[firstKey]) ? errors[firstKey][0] : errors[firstKey];
          }
        }
      }
      
      setError(errorMsg);
      toast.error(errorMsg);
    } finally {
      setSubmitting(false);
    }
  };

  const getEditorMode = () => {
    const lang = languages.find(l => l.id === formData.language);
    if (!lang) return 'python';
    const modeMap = {
      'Python': 'python',
      'JavaScript': 'javascript',
      'TypeScript': 'typescript',
      'Java': 'java',
      'C++': 'c_cpp',
      'C': 'c_cpp',
      'C#': 'csharp',
      'Go': 'golang',
      'Rust': 'rust',
      'Ruby': 'ruby',
      'PHP': 'php',
      'HTML': 'html',
      'CSS': 'css',
      'SQL': 'sql',
      'Swift': 'swift',
      'Kotlin': 'kotlin',
      'R': 'r',
      'Scala': 'scala',
      'Perl': 'perl',
      'Shell': 'sh',
      'Dart': 'dart',
      'Elixir': 'elixir',
      'Haskell': 'haskell',
      'Lua': 'lua',
      'Julia': 'julia',
    };
    return modeMap[lang.name] || 'text';
  };

  if (loading) {
    return (
      <Container>
        <LinearProgress sx={{ mt: 4 }} />
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <motion.div
        initial={{ y: -20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.5 }}
      >
        <Paper sx={{ 
          p: 4, 
          background: 'rgba(255,255,255,0.05)', 
          backdropFilter: 'blur(10px)', 
          borderRadius: 4, 
          border: '1px solid rgba(255,255,255,0.1)' 
        }}>
          {/* Header */}
          <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 3, flexWrap: 'wrap', gap: 2 }}>
            <Box>
              <Typography variant="h4" sx={{ color: '#fff', fontWeight: 'bold' }}>
                <CodeIcon sx={{ mr: 2, color: '#64ffda' }} />
                Submit Code for Review
              </Typography>
              <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.7)', mt: 1 }}>
                Paste your code or upload a file for AI-powered code review
              </Typography>
            </Box>
            <Zoom in={true}>
              <Chip
                icon={<AutoAwesomeIcon />}
                label="AI Powered"
                sx={{ 
                  background: 'linear-gradient(45deg, #64ffda, #00b4d8)',
                  color: '#000',
                  fontWeight: 'bold',
                  px: 2,
                  py: 1,
                }}
              />
            </Zoom>
          </Box>

          {/* Language Mismatch Error */}
          {languageMismatch && detectedLanguage && (
            <Alert
              severity="error"
              icon={<ErrorIcon />}
              sx={{ 
                mb: 2,
                borderRadius: 2,
                border: '1px solid rgba(255,0,0,0.2)',
                '& .MuiAlert-message': {
                  width: '100%',
                }
              }}
              action={
                <Button 
                  color="error" 
                  size="small"
                  onClick={() => {
                    const detectedLang = languages.find(l => l.name === detectedLanguage);
                    if (detectedLang) {
                      setSelectedLanguage(detectedLang);
                      setFormData({ ...formData, language: detectedLang.id });
                      setLanguageMismatch(false);
                      setError('');
                      toast.success(`✅ Switched to ${detectedLanguage}`);
                    }
                  }}
                  sx={{ mt: 1 }}
                >
                  Switch to {detectedLanguage}
                </Button>
              }
            >
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
                <Typography variant="subtitle1" sx={{ fontWeight: 'bold', color: '#ff1744' }}>
                  ⚠️ Language Mismatch Detected
                </Typography>
                <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
                  <Chip
                    label={`You selected: ${selectedLanguage?.name || 'Unknown'}`}
                    sx={{ backgroundColor: 'rgba(255,0,0,0.1)', color: '#ff1744' }}
                  />
                  <Chip
                    label={`Code appears to be: ${detectedLanguage}`}
                    sx={{ backgroundColor: 'rgba(100,255,218,0.1)', color: '#64ffda' }}
                  />
                </Box>
                <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.7)' }}>
                  Please select the correct language or click "Switch to {detectedLanguage}" to auto-correct.
                </Typography>
              </Box>
            </Alert>
          )}

          {error && !languageMismatch && (
            <Collapse in={!!error}>
              <Alert
                severity="error"
                icon={<WarningIcon />}
                action={
                  <IconButton size="small" onClick={() => setError('')}>
                    <CloseIcon fontSize="small" />
                  </IconButton>
                }
                sx={{ mb: 2 }}
              >
                {error}
              </Alert>
            </Collapse>
          )}

          {success && (
            <Collapse in={!!success}>
              <Alert
                severity="success"
                icon={<CheckCircleIcon />}
                action={
                  <IconButton size="small" onClick={() => setSuccess('')}>
                    <CloseIcon fontSize="small" />
                  </IconButton>
                }
                sx={{ mb: 2 }}
              >
                {success}
              </Alert>
            </Collapse>
          )}

          <form onSubmit={handleSubmit}>
            <Grid container spacing={3}>
              <Grid item xs={12} md={6}>
                <TextField
                  required
                  fullWidth
                  label="Title"
                  name="title"
                  value={formData.title}
                  onChange={handleChange}
                  placeholder="Enter a descriptive title for your code"
                  sx={{
                    '& .MuiOutlinedInput-root': {
                      color: '#fff',
                      '& fieldset': { borderColor: 'rgba(255,255,255,0.2)' },
                      '&:hover fieldset': { borderColor: '#64ffda' },
                      '&.Mui-focused fieldset': { borderColor: '#64ffda' },
                    },
                    '& .MuiInputLabel-root': {
                      color: 'rgba(255,255,255,0.7)',
                      '&.Mui-focused': { color: '#64ffda' },
                    },
                  }}
                />
              </Grid>
              <Grid item xs={12} md={6}>
                <TextField
                  required
                  fullWidth
                  select
                  label="Programming Language"
                  name="language"
                  value={formData.language}
                  onChange={handleLanguageChange}
                  SelectProps={{
                    renderValue: (value) => {
                      const lang = languages.find(l => l.id === value);
                      return (
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                          <Avatar
                            sx={{
                              width: 28,
                              height: 28,
                              bgcolor: lang ? languageColors[lang.name] : '#64ffda',
                              fontSize: '12px',
                              fontWeight: 'bold',
                              color: '#fff',
                            }}
                          >
                            {lang ? lang.name.charAt(0) : '?'}
                          </Avatar>
                          <span style={{ color: '#fff' }}>{lang?.name}</span>
                          <Chip
                            label="AI Supported"
                            size="small"
                            sx={{ 
                              ml: 1, 
                              background: 'rgba(100,255,218,0.2)',
                              color: '#64ffda',
                              fontSize: '0.6rem',
                              height: '18px',
                            }}
                          />
                        </Box>
                      );
                    },
                  }}
                  sx={{
                    '& .MuiOutlinedInput-root': {
                      color: '#fff',
                      '& fieldset': { borderColor: 'rgba(255,255,255,0.2)' },
                      '&:hover fieldset': { borderColor: '#64ffda' },
                      '&.Mui-focused fieldset': { borderColor: '#64ffda' },
                    },
                    '& .MuiInputLabel-root': {
                      color: 'rgba(255,255,255,0.7)',
                      '&.Mui-focused': { color: '#64ffda' },
                    },
                    '& .MuiSelect-select': { color: '#fff' },
                  }}
                >
                  {Array.isArray(languages) && languages.map((lang) => (
                    <MenuItem key={lang.id} value={lang.id}>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, width: '100%' }}>
                        <Avatar
                          sx={{
                            width: 32,
                            height: 32,
                            bgcolor: languageColors[lang.name] || '#64ffda',
                            fontSize: '12px',
                            fontWeight: 'bold',
                            color: '#fff',
                          }}
                        >
                          {lang.name.charAt(0)}
                        </Avatar>
                        <span style={{ flex: 1 }}>{lang.name}</span>
                        {detectedLanguage === lang.name && (
                          <Chip
                            label="✅ Detected"
                            size="small"
                            sx={{ 
                              fontSize: '0.6rem', 
                              height: '18px',
                              backgroundColor: 'rgba(76,175,80,0.2)',
                              color: '#4caf50',
                            }}
                          />
                        )}
                        <Chip
                          label={languageEmojis[lang.name] || lang.extension || '.txt'}
                          size="small"
                          sx={{ 
                            fontSize: '0.6rem', 
                            height: '20px',
                            background: 'rgba(255,255,255,0.05)',
                            color: 'rgba(255,255,255,0.7)',
                          }}
                        />
                      </Box>
                    </MenuItem>
                  ))}
                </TextField>
              </Grid>
            </Grid>

            {/* Language Detection Info - Only show when detected */}
            {detectedLanguage && (
              <Fade in={true}>
                <Box sx={{ 
                  mt: 2, 
                  p: 2, 
                  bgcolor: languageMismatch ? 'rgba(255,0,0,0.05)' : 'rgba(100,255,218,0.05)', 
                  borderRadius: 2,
                  border: languageMismatch ? '1px solid rgba(255,0,0,0.2)' : '1px solid rgba(100,255,218,0.1)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  flexWrap: 'wrap',
                  gap: 1
                }}>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                    <Avatar
                      sx={{
                        width: 32,
                        height: 32,
                        bgcolor: languageColors[detectedLanguage] || '#64ffda',
                        fontSize: '14px',
                        fontWeight: 'bold',
                        color: '#fff',
                      }}
                    >
                      {detectedLanguage.charAt(0)}
                    </Avatar>
                    <Box>
                      <Typography variant="body2" sx={{ color: '#fff', fontWeight: 'bold' }}>
                        {languageMismatch ? '⚠️ Detected Language:' : '✅ Detected Language:'}
                      </Typography>
                      <Typography variant="body2" sx={{ 
                        color: languageMismatch ? '#ff1744' : '#64ffda',
                        fontWeight: 'bold'
                      }}>
                        {detectedLanguage}
                      </Typography>
                    </Box>
                  </Box>
                  <Box sx={{ display: 'flex', gap: 1 }}>
                    <Chip
                      icon={languageMismatch ? <ErrorIcon /> : <CheckCircleIcon />}
                      label={languageMismatch ? 'Mismatch' : 'Match'}
                      size="small"
                      sx={{ 
                        color: languageMismatch ? '#ff1744' : '#4caf50',
                        borderColor: languageMismatch ? '#ff1744' : '#4caf50',
                      }}
                      variant="outlined"
                    />
                    {languageMismatch && (
                      <Button
                        size="small"
                        variant="contained"
                        onClick={() => {
                          const detectedLang = languages.find(l => l.name === detectedLanguage);
                          if (detectedLang) {
                            setSelectedLanguage(detectedLang);
                            setFormData({ ...formData, language: detectedLang.id });
                            setLanguageMismatch(false);
                            setError('');
                            toast.success(`✅ Switched to ${detectedLanguage}`);
                          }
                        }}
                        sx={{
                          backgroundColor: '#64ffda',
                          color: '#000',
                          '&:hover': {
                            backgroundColor: '#00b4d8',
                          },
                        }}
                      >
                        Switch to {detectedLanguage}
                      </Button>
                    )}
                  </Box>
                </Box>
              </Fade>
            )}

            {/* Detect Language Button */}
            <Box sx={{ mt: 2, display: 'flex', gap: 2, flexWrap: 'wrap' }}>
              <Button
                variant="outlined"
                onClick={handleDetectLanguage}
                startIcon={<AutoAwesomeIcon />}
                sx={{
                  borderColor: '#64ffda',
                  color: '#64ffda',
                  '&:hover': {
                    borderColor: '#00b4d8',
                    color: '#00b4d8',
                    backgroundColor: 'rgba(100,255,218,0.05)',
                  },
                }}
              >
                🔍 Detect Language
              </Button>
              <Typography variant="caption" sx={{ color: 'rgba(255,255,255,0.5)', alignSelf: 'center' }}>
                Click to detect language from your code
              </Typography>
            </Box>

            <TextField
              fullWidth
              multiline
              rows={3}
              label="Description (Optional)"
              name="description"
              value={formData.description}
              onChange={handleChange}
              sx={{ mt: 2 }}
              placeholder="Describe what your code does, any issues you're facing, or specific areas you want reviewed"
              InputProps={{
                sx: {
                  color: '#fff',
                  '& fieldset': { borderColor: 'rgba(255,255,255,0.2)' },
                  '&:hover fieldset': { borderColor: '#64ffda' },
                  '&.Mui-focused fieldset': { borderColor: '#64ffda' },
                },
              }}
              InputLabelProps={{
                sx: { color: 'rgba(255,255,255,0.7)', '&.Mui-focused': { color: '#64ffda' } },
              }}
            />

            {formData.code && (
              <Fade in={true}>
                <Box sx={{ display: 'flex', gap: 2, mt: 2, mb: 1, flexWrap: 'wrap' }}>
                  <Chip
                    label={`📝 ${charCount} characters`}
                    size="small"
                    sx={{ color: 'rgba(255,255,255,0.7)' }}
                  />
                  <Chip
                    label={`📄 ${lineCount} lines`}
                    size="small"
                    sx={{ color: 'rgba(255,255,255,0.7)' }}
                  />
                  <Chip
                    label={`🔤 ${selectedLanguage?.name || 'Unknown'}`}
                    size="small"
                    sx={{ color: '#64ffda', borderColor: '#64ffda' }}
                    variant="outlined"
                  />
                  {detectedLanguage && (
                    <Chip
                      label={`🔍 Detected: ${detectedLanguage}`}
                      size="small"
                      sx={{ 
                        color: languageMismatch ? '#ff1744' : '#64ffda',
                        borderColor: languageMismatch ? '#ff1744' : '#64ffda',
                      }}
                      variant="outlined"
                    />
                  )}
                </Box>
              </Fade>
            )}

            <Box sx={{ mt: 3 }}>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
                <Typography variant="subtitle2" sx={{ color: 'rgba(255,255,255,0.7)' }}>
                  Code Editor
                </Typography>
                <Tooltip title={`${isDarkTheme ? 'Switch to Light' : 'Switch to Dark'} Theme`}>
                  <IconButton
                    onClick={() => setIsDarkTheme(!isDarkTheme)}
                    size="small"
                    sx={{ color: '#64ffda' }}
                  >
                    {isDarkTheme ? '🌙' : '☀️'}
                  </IconButton>
                </Tooltip>
              </Box>
              <AceEditor
                mode={getEditorMode()}
                theme={isDarkTheme ? 'monokai' : 'github'}
                onChange={handleCodeChange}
                name="code_editor"
                value={formData.code}
                editorProps={{ $blockScrolling: true }}
                enableBasicAutocompletion={true}
                enableLiveAutocompletion={true}
                enableSnippets={true}
                setOptions={{
                  showLineNumbers: true,
                  tabSize: 4,
                  fontSize: 14,
                  useWorker: false,
                  showPrintMargin: false,
                  fontFamily: 'monospace',
                  highlightActiveLine: true,
                  displayIndentGuides: true,
                  wrap: true,
                }}
                onLoad={(editor) => {
                  editor.setOption('enableBasicAutocompletion', true);
                  editor.setOption('enableLiveAutocompletion', true);
                  editor.setOption('enableSnippets', true);
                }}
                width="100%"
                height="450px"
                style={{
                  border: '1px solid rgba(255,255,255,0.1)',
                  borderRadius: '8px',
                }}
              />
            </Box>

            <Box sx={{ mt: 2, display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: 2 }}>
              <Box sx={{ display: 'flex', gap: 2, alignItems: 'center', flexWrap: 'wrap' }}>
                <Button
                  variant="outlined"
                  component="label"
                  startIcon={<CloudUploadIcon />}
                  sx={{
                    borderColor: 'rgba(255,255,255,0.2)',
                    color: '#fff',
                    '&:hover': {
                      borderColor: '#64ffda',
                      color: '#64ffda',
                    },
                  }}
                >
                  Choose File
                  <input
                    type="file"
                    hidden
                    accept=".py,.js,.ts,.java,.cpp,.c,.cs,.go,.rs,.rb,.php,.html,.css,.sql,.txt,.swift,.kt,.r,.scala,.pl,.sh,.dart,.ex,.hs,.lua,.jl"
                    onChange={handleFileChange}
                  />
                </Button>
                {formData.file_name && (
                  <Chip
                    label={`📄 ${formData.file_name}`}
                    onDelete={() => setFormData({ ...formData, file_name: '', code: '' })}
                    sx={{ color: '#64ffda', borderColor: '#64ffda' }}
                    variant="outlined"
                  />
                )}
              </Box>
              <Box sx={{ display: 'flex', gap: 1 }}>
                <Chip
                  icon={<LanguageIcon />}
                  label={`${languages.length} Languages Available`}
                  size="small"
                  sx={{ color: 'rgba(255,255,255,0.5)' }}
                />
              </Box>
            </Box>

            <Box sx={{ mt: 3, display: 'flex', gap: 2, flexWrap: 'wrap' }}>
              <motion.div whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}>
                <Button
                  type="submit"
                  variant="contained"
                  disabled={submitting || languageMismatch}
                  size="large"
                  startIcon={submitting ? <LinearProgress sx={{ width: 20 }} /> : <PlayArrowIcon />}
                  sx={{
                    background: languageMismatch ? 'rgba(255,0,0,0.3)' : 'linear-gradient(45deg, #64ffda, #00b4d8)',
                    color: languageMismatch ? 'rgba(255,255,255,0.5)' : '#000',
                    fontWeight: 'bold',
                    px: 4,
                    '&:hover': {
                      background: languageMismatch ? 'rgba(255,0,0,0.3)' : 'linear-gradient(45deg, #00b4d8, #64ffda)',
                    },
                    '&:disabled': {
                      background: 'rgba(100,255,218,0.1)',
                      color: 'rgba(255,255,255,0.3)',
                    },
                  }}
                >
                  {languageMismatch ? '⚠️ Fix Language First' : submitting ? 'Submitting...' : 'Submit for Review'}
                </Button>
              </motion.div>
              <motion.div whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}>
                <Button
                  type="button"
                  variant="outlined"
                  onClick={() => navigate('/dashboard')}
                  size="large"
                  sx={{
                    borderColor: 'rgba(255,255,255,0.2)',
                    color: '#fff',
                    '&:hover': {
                      borderColor: '#ff6b6b',
                      color: '#ff6b6b',
                    },
                  }}
                >
                  Cancel
                </Button>
              </motion.div>
              <motion.div whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}>
                <Button
                  type="button"
                  variant="outlined"
                  onClick={() => setShowPreview(!showPreview)}
                  size="large"
                  sx={{
                    borderColor: 'rgba(255,255,255,0.2)',
                    color: '#fff',
                    '&:hover': {
                      borderColor: '#ffd93d',
                      color: '#ffd93d',
                    },
                  }}
                >
                  {showPreview ? 'Hide Preview' : 'Preview Code'}
                </Button>
              </motion.div>
            </Box>

            {showPreview && formData.code && (
              <Slide direction="up" in={showPreview} mountOnEnter unmountOnExit>
                <Paper sx={{ mt: 3, p: 3, background: 'rgba(0,0,0,0.4)', borderRadius: 2 }}>
                  <Typography variant="subtitle2" sx={{ color: '#64ffda', mb: 2 }}>
                    <DescriptionIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                    Code Preview:
                  </Typography>
                  <pre style={{ 
                    color: 'rgba(255,255,255,0.9)', 
                    whiteSpace: 'pre-wrap', 
                    wordWrap: 'break-word',
                    maxHeight: '300px',
                    overflow: 'auto',
                    fontFamily: 'monospace',
                    fontSize: '14px',
                    background: 'rgba(0,0,0,0.3)',
                    padding: '16px',
                    borderRadius: '8px',
                  }}>
                    {formData.code.substring(0, 2000)}
                    {formData.code.length > 2000 && '\n... (truncated)'}
                  </pre>
                  <Box sx={{ mt: 2, display: 'flex', gap: 2, flexWrap: 'wrap' }}>
                    <Chip
                      label={`📝 ${charCount} chars`}
                      size="small"
                      sx={{ color: 'rgba(255,255,255,0.6)' }}
                    />
                    <Chip
                      label={`📄 ${lineCount} lines`}
                      size="small"
                      sx={{ color: 'rgba(255,255,255,0.6)' }}
                    />
                    <Chip
                      label={`🔤 ${selectedLanguage?.name || 'Unknown'}`}
                      size="small"
                      sx={{ color: '#64ffda' }}
                    />
                    {detectedLanguage && (
                      <Chip
                        label={`🔍 Detected: ${detectedLanguage}`}
                        size="small"
                        sx={{ 
                          color: languageMismatch ? '#ff1744' : '#64ffda',
                          borderColor: languageMismatch ? '#ff1744' : '#64ffda',
                        }}
                        variant="outlined"
                      />
                    )}
                  </Box>
                </Paper>
              </Slide>
            )}
          </form>
        </Paper>
      </motion.div>
    </Container>
  );
};

export default CodeSubmission;
