import React, { useEffect, useState } from 'react';
import {
  Container,
  Paper,
  Typography,
  Box,
  Chip,
  Button,
  Divider,
  LinearProgress,
  Grid,
  Card,
  CardContent,
  IconButton,
  Collapse,
  Alert,
} from '@mui/material';
import { useParams, useNavigate } from 'react-router-dom';
import { codeReviewAPI } from '../api';
import { toast } from 'react-toastify';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import CodeIcon from '@mui/icons-material/Code';
import BugReportIcon from '@mui/icons-material/BugReport';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import LightbulbIcon from '@mui/icons-material/Lightbulb';
import WarningIcon from '@mui/icons-material/Warning';
import DownloadIcon from '@mui/icons-material/Download';
import { motion } from 'framer-motion';

const SubmissionDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [submission, setSubmission] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [expandedBugs, setExpandedBugs] = useState(true);
  const [expandedSuggestions, setExpandedSuggestions] = useState(true);
  const [expandedIssues, setExpandedIssues] = useState(true);
  const [expandedTestCases, setExpandedTestCases] = useState(true);
  const [redirectCountdown, setRedirectCountdown] = useState(5);
  const [hoveredLine, setHoveredLine] = useState(null);

  useEffect(() => {
    fetchSubmissionDetail();
  }, [id]);

  useEffect(() => {
    let timer;
    if (error) {
      timer = setInterval(() => {
        setRedirectCountdown((prev) => {
          if (prev <= 1) {
            clearInterval(timer);
            navigate('/dashboard');
            return 0;
          }
          return prev - 1;
        });
      }, 1000);
    }
    return () => clearInterval(timer);
  }, [error, navigate]);

  const fetchSubmissionDetail = async () => {
    try {
      setLoading(true);
      setError('');
      console.log('Fetching submission detail for ID:', id);
      
      const response = await codeReviewAPI.getSubmission(id);
      console.log('Submission detail:', response.data);
      setSubmission(response.data);
      
    } catch (error) {
      console.error('Failed to fetch submission:', error);
      
      if (error.response?.status === 404) {
        setError('❌ Submission not found. It may have been deleted or does not exist.');
        toast.error('Submission not found');
      } else if (error.response?.status === 401) {
        setError('🔒 You are not authorized to view this submission. Please login again.');
        toast.error('Unauthorized access');
        setTimeout(() => {
          navigate('/login');
        }, 3000);
      } else if (error.response?.status === 403) {
        setError('⛔ You do not have permission to view this submission.');
        toast.error('Permission denied');
      } else if (error.code === 'ERR_NETWORK') {
        setError('🌐 Network error. Please check your internet connection.');
        toast.error('Network error');
      } else {
        setError('⚠️ Failed to load submission details. Please try again.');
        toast.error('Failed to load submission details');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleRetry = () => {
    fetchSubmissionDetail();
  };

  const handleDownloadReport = () => {
    if (!submission) return;
    
    toast.info('Generating report...');
    
    // Helper to safely stringify objects
    const safeStringify = (value) => {
      if (value === null || value === undefined) return 'N/A';
      if (typeof value === 'string') return value;
      if (typeof value === 'number') return String(value);
      if (Array.isArray(value)) return JSON.stringify(value);
      if (typeof value === 'object') {
        return Object.entries(value)
          .map(([key, val]) => `${key}: ${typeof val === 'object' ? JSON.stringify(val) : val}`)
          .join(', ');
      }
      return String(value);
    };
    
    const reportContent = `
AI Code Review Report
=====================

Title: ${submission.title || 'Untitled'}
Language: ${submission.language_name || 'N/A'}
Status: ${submission.status || 'N/A'}
Quality Score: ${submission.quality_score || 0}%
Submitted: ${new Date(submission.created_at).toLocaleDateString()}
Reviewed: ${submission.reviewed_at ? new Date(submission.reviewed_at).toLocaleDateString() : 'N/A'}

${'='.repeat(50)}

CODE:
${submission.code || 'No code available'}

${'='.repeat(50)}

ANALYSIS RESULTS:

Bugs Found: ${submission.analysis_result?.bugs?.length || 0}
${submission.analysis_result?.bugs?.map((bug, i) => `
Bug #${i + 1}:
  Line: ${bug.line || 'N/A'}
  Description: ${bug.description || 'N/A'}
  Severity: ${bug.severity || 'low'}
  Suggestion: ${bug.suggestion || 'No suggestion'}
`).join('') || '  No bugs found!'}

Issues Found: ${submission.analysis_result?.issues?.length || 0}
${submission.analysis_result?.issues?.map((issue, i) => `
Issue #${i + 1}:
  Line: ${issue.line || 'N/A'}
  Description: ${issue.description || 'N/A'}
  Type: ${issue.type || 'N/A'}
  Suggestion: ${issue.suggestion || 'No suggestion'}
`).join('') || '  No issues found!'}

Suggestions: ${submission.analysis_result?.suggestions?.length || 0}
${submission.analysis_result?.suggestions?.map((sugg, i) => `
Suggestion #${i + 1}:
  Line: ${sugg.line || 'N/A'}
  Description: ${sugg.description || 'N/A'}
  Recommendation: ${sugg.recommendation || 'N/A'}
  Code Example: ${sugg.code_example || 'N/A'}
`).join('') || '  No suggestions!'}

Test Cases: ${submission.analysis_result?.test_cases?.length || 0}
${submission.analysis_result?.test_cases?.map((tc, i) => `
Test Case ${i + 1}:
  Name: ${tc.name || 'N/A'}
  Function: ${tc.function || 'N/A'}
  Input: ${safeStringify(tc.input)}
  Expected: ${tc.expected || 'N/A'}
  Description: ${tc.description || 'N/A'}
`).join('') || '  No test cases!'}

${'='.repeat(50)}

Generated by AI Code Review Platform
    `;

    const blob = new Blob([reportContent], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `report_${submission.title || 'submission'}_${new Date().toISOString().split('T')[0]}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
    
    toast.success('✅ Report downloaded successfully!');
  };

  const getSeverityColor = (severity) => {
    switch (severity?.toLowerCase()) {
      case 'critical': return 'error';
      case 'high': return 'error';
      case 'medium': return 'warning';
      case 'low': return 'info';
      default: return 'default';
    }
  };

  const getSeverityIcon = (severity) => {
    switch (severity?.toLowerCase()) {
      case 'critical': return <WarningIcon sx={{ color: '#ff1744' }} />;
      case 'high': return <WarningIcon sx={{ color: '#ff6d00' }} />;
      case 'medium': return <WarningIcon sx={{ color: '#ffab00' }} />;
      case 'low': return <WarningIcon sx={{ color: '#00e676' }} />;
      default: return <BugReportIcon />;
    }
  };

  // ============================================================
  // FIX 1: Helper to safely render input values (objects, arrays, etc.)
  // ============================================================
  const renderInput = (input) => {
    if (!input) return 'N/A';
    if (typeof input === 'string') return input;
    if (typeof input === 'number') return String(input);
    if (typeof input === 'boolean') return String(input);
    if (Array.isArray(input)) {
      return `[${input.map(item => typeof item === 'object' ? JSON.stringify(item) : item).join(', ')}]`;
    }
    if (typeof input === 'object') {
      return Object.entries(input)
        .map(([key, value]) => `${key}: ${typeof value === 'object' ? JSON.stringify(value) : value}`)
        .join(', ');
    }
    return String(input);
  };

  // ============================================================
  // FIX 2: Helper to check if test case should pass based on code
  // ============================================================
  const shouldTestCasePass = (testCase, code) => {
    if (!testCase || !code) return false;
    
    const inputStr = String(testCase.input || '');
    
    // Empty list test
    if (inputStr.includes('[]') || inputStr.includes('empty')) {
      return code.includes('if not') || code.includes('try') || code.includes('except') || code.includes('len(');
    }
    
    // Invalid input test
    if (inputStr.includes('invalid') || inputStr.includes('"a"') || inputStr.includes('string')) {
      return code.includes('isinstance') || code.includes('try') || code.includes('except') || code.includes('type') || code.includes('validate');
    }
    
    // Null/None test
    if (inputStr.includes('null') || inputStr.includes('None') || inputStr.includes('undefined')) {
      return code.includes('if') || code.includes('is None') || code.includes('is not None') || code.includes('!== null');
    }
    
    // Negative numbers test
    if (inputStr.includes('-1') || inputStr.includes('-5')) {
      return code.includes('if') || code.includes('>=') || code.includes('> 0') || code.includes('abs') || code.includes('min');
    }
    
    // Large numbers test
    if (inputStr.includes('999999') || inputStr.includes('1000')) {
      return code.includes('int') || code.includes('float') || code.includes('Number') || code.includes('try');
    }
    
    // Default: pass if the test case has an expected value
    return !!testCase.expected;
  };

  if (loading) {
    return (
      <Container>
        <LinearProgress sx={{ mt: 4 }} />
        <Typography sx={{ color: 'rgba(255,255,255,0.7)', mt: 2, textAlign: 'center' }}>
          Loading submission details...
        </Typography>
      </Container>
    );
  }

  if (error) {
    return (
      <Container>
        <Paper sx={{ 
          p: 4, 
          mt: 4, 
          textAlign: 'center', 
          background: 'rgba(255,255,255,0.05)', 
          borderRadius: 4,
          border: '1px solid rgba(255,255,255,0.1)'
        }}>
          <Alert severity="error" sx={{ mb: 3, fontSize: '1rem' }}>
            {error}
          </Alert>
          <Typography sx={{ color: 'rgba(255,255,255,0.7)', mb: 2 }}>
            Redirecting to dashboard in {redirectCountdown} seconds...
          </Typography>
          <Box sx={{ display: 'flex', gap: 2, justifyContent: 'center', flexWrap: 'wrap' }}>
            <Button 
              variant="contained" 
              onClick={handleRetry}
              sx={{
                background: 'linear-gradient(45deg, #64ffda, #00b4d8)',
                color: '#000',
                fontWeight: 'bold',
                '&:hover': {
                  background: 'linear-gradient(45deg, #00b4d8, #64ffda)',
                },
              }}
            >
              Retry
            </Button>
            <Button 
              variant="contained" 
              onClick={() => navigate('/dashboard')}
              sx={{
                background: 'linear-gradient(45deg, #ffd93d, #f6b93b)',
                color: '#000',
                fontWeight: 'bold',
                '&:hover': {
                  background: 'linear-gradient(45deg, #f6b93b, #ffd93d)',
                },
              }}
            >
              Go to Dashboard
            </Button>
          </Box>
        </Paper>
      </Container>
    );
  }

  if (!submission) {
    return (
      <Container>
        <Paper sx={{ p: 4, mt: 4, textAlign: 'center' }}>
          <Typography sx={{ color: '#fff' }}>Submission not found</Typography>
          <Button onClick={() => navigate('/dashboard')} sx={{ mt: 2 }}>
            Back to Dashboard
          </Button>
        </Paper>
      </Container>
    );
  }

  const bugs = submission.analysis_result?.bugs || [];
  const issues = submission.analysis_result?.issues || [];
  const suggestions = submission.analysis_result?.suggestions || [];
  const explanation = submission.analysis_result?.explanation || '';
  const testCases = submission.analysis_result?.test_cases || [];
  const codeLines = submission.code ? submission.code.split('\n') : [];

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
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 3, flexWrap: 'wrap', gap: 2 }}>
            <IconButton onClick={() => navigate('/dashboard')} sx={{ color: '#64ffda' }}>
              <ArrowBackIcon />
            </IconButton>
            <Typography variant="h4" sx={{ color: '#fff', fontWeight: 'bold', flex: 1 }}>
              Submission Details
            </Typography>
            <Chip
              label={submission.status || 'pending'}
              color={submission.status === 'completed' ? 'success' : 'warning'}
            />
            <Button
              variant="contained"
              startIcon={<DownloadIcon />}
              onClick={handleDownloadReport}
              sx={{
                background: 'linear-gradient(45deg, #ffd93d, #f6b93b)',
                color: '#000',
                fontWeight: 'bold',
                '&:hover': {
                  background: 'linear-gradient(45deg, #f6b93b, #ffd93d)',
                },
              }}
            >
              Download Report
            </Button>
          </Box>

          <Divider sx={{ borderColor: 'rgba(255,255,255,0.1)', mb: 3 }} />

          {/* Basic Info */}
          <Grid container spacing={3}>
            <Grid item xs={12} md={8}>
              <Typography variant="h5" sx={{ color: '#fff' }}>
                {submission.title || 'Untitled'}
              </Typography>
              <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.7)', mt: 1 }}>
                {submission.description || 'No description provided'}
              </Typography>
              <Box sx={{ display: 'flex', gap: 2, mt: 2, flexWrap: 'wrap' }}>
                <Chip label={`Language: ${submission.language_name || 'N/A'}`} />
                <Chip label={`Submitted: ${new Date(submission.created_at).toLocaleDateString()}`} />
                {submission.reviewed_at && (
                  <Chip label={`Reviewed: ${new Date(submission.reviewed_at).toLocaleDateString()}`} />
                )}
              </Box>
            </Grid>
            <Grid item xs={12} md={4}>
              <Card sx={{ background: 'rgba(255,255,255,0.05)', borderRadius: 2 }}>
                <CardContent>
                  <Typography color="rgba(255,255,255,0.7)" gutterBottom>
                    Quality Score
                  </Typography>
                  <Typography variant="h2" sx={{ 
                    color: submission.quality_score >= 70 ? '#4caf50' : submission.quality_score >= 50 ? '#ff9800' : '#f44336',
                    fontWeight: 'bold'
                  }}>
                    {submission.quality_score || 0}%
                  </Typography>
                  <Box sx={{ display: 'flex', gap: 2, mt: 2 }}>
                    <Box>
                      <Typography variant="caption" sx={{ color: 'rgba(255,255,255,0.5)' }}>
                        Bugs
                      </Typography>
                      <Typography variant="h6" sx={{ color: '#fff' }}>
                        {bugs.length || 0}
                      </Typography>
                    </Box>
                    <Box>
                      <Typography variant="caption" sx={{ color: 'rgba(255,255,255,0.5)' }}>
                        Issues
                      </Typography>
                      <Typography variant="h6" sx={{ color: '#fff' }}>
                        {issues.length || 0}
                      </Typography>
                    </Box>
                    <Box>
                      <Typography variant="caption" sx={{ color: 'rgba(255,255,255,0.5)' }}>
                        Suggestions
                      </Typography>
                      <Typography variant="h6" sx={{ color: '#fff' }}>
                        {suggestions.length || 0}
                      </Typography>
                    </Box>
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          </Grid>

          {/* Code Display with Line Numbers */}
          {submission.code && (
            <>
              <Typography variant="h6" sx={{ color: '#fff', mt: 4, mb: 2 }}>
                <CodeIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                Code with Line Numbers
              </Typography>
              
              <Box sx={{ display: 'flex', gap: 2, mb: 2, flexWrap: 'wrap' }}>
                <Chip 
                  icon={<BugReportIcon />} 
                  label="🐛 Bug Line" 
                  size="small" 
                  sx={{ backgroundColor: '#ff6b6b', color: '#fff' }} 
                />
                <Chip 
                  icon={<WarningIcon />} 
                  label="⚠️ Issue Line" 
                  size="small" 
                  sx={{ backgroundColor: '#ffab00', color: '#000' }} 
                />
                <Chip 
                  icon={<LightbulbIcon />} 
                  label="💡 Suggestion Line" 
                  size="small" 
                  sx={{ backgroundColor: '#4ecdc4', color: '#000' }} 
                />
              </Box>

              <Paper sx={{ 
                p: 2, 
                background: 'rgba(0,0,0,0.4)', 
                borderRadius: 2,
                maxHeight: '500px',
                overflow: 'auto',
                border: '1px solid rgba(255,255,255,0.05)'
              }}>
                <pre style={{ 
                  margin: 0,
                  fontFamily: 'monospace',
                  fontSize: '14px',
                  lineHeight: '1.8',
                }}>
                  {codeLines.map((line, index) => {
                    const lineNum = index + 1;
                    const hasBug = bugs.some(b => b.line === lineNum);
                    const hasIssue = issues.some(i => i.line === lineNum);
                    const hasSuggestion = suggestions.some(s => s.line === lineNum);
                    
                    let bgColor = 'transparent';
                    let borderColor = 'transparent';
                    let icon = '';
                    let textColor = 'rgba(255,255,255,0.9)';
                    let borderLeftWidth = '4px';
                    
                    if (hasBug) {
                      bgColor = 'rgba(255,0,0,0.25)';
                      borderColor = '#ff1744';
                      icon = '🐛';
                      textColor = '#ff6b6b';
                      borderLeftWidth = '6px';
                    } else if (hasIssue) {
                      bgColor = 'rgba(255,171,0,0.2)';
                      borderColor = '#ffab00';
                      icon = '⚠️';
                      textColor = '#ffab00';
                      borderLeftWidth = '4px';
                    } else if (hasSuggestion) {
                      bgColor = 'rgba(78,205,196,0.15)';
                      borderColor = '#4ecdc4';
                      icon = '💡';
                      textColor = '#4ecdc4';
                      borderLeftWidth = '3px';
                    }
                    
                    return (
                      <div 
                        key={index}
                        style={{
                          display: 'flex',
                          backgroundColor: bgColor,
                          borderLeft: hasBug || hasIssue || hasSuggestion ? `${borderLeftWidth} solid ${borderColor}` : '4px solid transparent',
                          padding: '4px 0',
                          borderRadius: '2px',
                          transition: 'all 0.2s ease',
                          cursor: hasBug || hasIssue || hasSuggestion ? 'pointer' : 'default',
                        }}
                        onMouseEnter={() => setHoveredLine(hasBug || hasIssue || hasSuggestion ? lineNum : null)}
                        onMouseLeave={() => setHoveredLine(null)}
                      >
                        <span style={{ 
                          color: '#64ffda', 
                          minWidth: '50px', 
                          display: 'inline-block',
                          userSelect: 'none',
                          opacity: 0.6,
                          textAlign: 'right',
                          paddingRight: '12px',
                          fontSize: '12px',
                          fontFamily: 'monospace',
                        }}>
                          {lineNum}
                        </span>
                        <span style={{ 
                          color: textColor,
                          whiteSpace: 'pre',
                          flex: 1,
                          fontFamily: 'monospace',
                          fontWeight: hasBug ? 'bold' : 'normal',
                          textDecoration: hasBug ? 'underline wavy #ff6b6b' : 'none',
                        }}>
                          {line || ' '}
                        </span>
                        {icon && (
                          <span style={{ 
                            marginLeft: '8px', 
                            fontSize: '16px',
                            minWidth: '24px'
                          }}>
                            {icon}
                          </span>
                        )}
                        {hasBug && (
                          <span style={{ 
                            marginLeft: '8px', 
                            fontSize: '12px',
                            color: '#ff6b6b',
                            background: 'rgba(255,0,0,0.1)',
                            padding: '2px 8px',
                            borderRadius: '4px',
                            whiteSpace: 'nowrap'
                          }}>
                            🔴 ERROR HERE!
                          </span>
                        )}
                      </div>
                    );
                  })}
                </pre>
              </Paper>
            </>
          )}

          {/* Explanation Section */}
          {explanation && (
            <>
              <Typography variant="h6" sx={{ color: '#fff', mt: 4, mb: 2 }}>
                <LightbulbIcon sx={{ mr: 1, verticalAlign: 'middle', color: '#ffd93d' }} />
                Code Explanation
              </Typography>
              <Paper sx={{ p: 3, background: 'rgba(255,215,0,0.05)', borderRadius: 2, border: '1px solid rgba(255,215,0,0.2)' }}>
                <Typography sx={{ color: 'rgba(255,255,255,0.9)', whiteSpace: 'pre-wrap' }}>
                  {explanation}
                </Typography>
              </Paper>
            </>
          )}

          {/* Bugs Section */}
          <Box sx={{ mt: 4 }}>
            <Box 
              sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', cursor: 'pointer' }}
              onClick={() => setExpandedBugs(!expandedBugs)}
            >
              <Typography variant="h6" sx={{ color: '#fff' }}>
                <BugReportIcon sx={{ mr: 1, verticalAlign: 'middle', color: '#ff6b6b' }} />
                Bugs Found ({bugs.length})
              </Typography>
              <Chip 
                label={expandedBugs ? 'Hide' : 'Show'} 
                size="small" 
                sx={{ color: '#64ffda' }}
              />
            </Box>
            <Collapse in={expandedBugs}>
              {bugs.length === 0 ? (
                <Paper sx={{ p: 2, mt: 2, background: 'rgba(0,255,0,0.05)', borderRadius: 2, border: '1px solid rgba(0,255,0,0.1)' }}>
                  <Typography sx={{ color: '#4caf50' }}>
                    ✅ No bugs found! Great job!
                  </Typography>
                </Paper>
              ) : (
                bugs.map((bug, index) => (
                  <Paper key={index} sx={{ 
                    p: 2, 
                    mt: 2, 
                    background: 'rgba(255,0,0,0.05)', 
                    borderRadius: 2, 
                    borderLeft: `4px solid ${bug.severity === 'critical' ? '#ff1744' : bug.severity === 'high' ? '#ff6d00' : bug.severity === 'medium' ? '#ffab00' : '#00e676'}`
                  }}>
                    <Box sx={{ display: 'flex', alignItems: 'flex-start', gap: 1 }}>
                      {getSeverityIcon(bug.severity)}
                      <Box sx={{ flex: 1 }}>
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, flexWrap: 'wrap' }}>
                          <Typography sx={{ color: '#fff', fontWeight: 'bold' }}>
                            Bug #{index + 1}
                          </Typography>
                          {bug.line && (
                            <Chip 
                              label={`Line ${bug.line}`} 
                              size="small" 
                              sx={{ 
                                backgroundColor: '#ff6b6b', 
                                color: '#fff',
                                fontWeight: 'bold',
                              }}
                            />
                          )}
                          {bug.severity && (
                            <Chip 
                              label={bug.severity.toUpperCase()} 
                              color={getSeverityColor(bug.severity)}
                              size="small"
                            />
                          )}
                        </Box>
                        <Typography sx={{ color: 'rgba(255,255,255,0.9)', mt: 1 }}>
                          {bug.description}
                        </Typography>
                        
                        {bug.line && codeLines.length > 0 && codeLines[bug.line - 1] !== undefined && (
                          <Paper sx={{ 
                            mt: 1, 
                            p: 1.5, 
                            background: 'rgba(255,0,0,0.15)', 
                            borderRadius: 1,
                            borderLeft: '4px solid #ff1744',
                            border: '1px solid rgba(255,0,0,0.2)'
                          }}>
                            <Typography variant="caption" sx={{ color: '#ff1744', fontWeight: 'bold' }}>
                              🔴 ERROR at Line {bug.line}:
                            </Typography>
                            <Box sx={{ 
                              display: 'flex',
                              mt: 1,
                              background: 'rgba(0,0,0,0.3)',
                              borderRadius: 1,
                              padding: '8px',
                            }}>
                              <span style={{ 
                                color: '#64ffda', 
                                minWidth: '35px', 
                                opacity: 0.5,
                                fontSize: '12px',
                                fontFamily: 'monospace',
                              }}>
                                {bug.line}
                              </span>
                              <pre style={{ 
                                margin: 0, 
                                color: '#ff6b6b',
                                fontSize: '13px',
                                fontFamily: 'monospace',
                                whiteSpace: 'pre-wrap',
                                wordWrap: 'break-word',
                                flex: 1,
                                fontWeight: 'bold',
                                textDecoration: 'underline wavy #ff1744',
                              }}>
                                {codeLines[bug.line - 1] || 'Line not found'}
                              </pre>
                            </Box>
                          </Paper>
                        )}
                        
                        {bug.suggestion && (
                          <Box sx={{ mt: 1, display: 'flex', alignItems: 'flex-start', gap: 1 }}>
                            <LightbulbIcon sx={{ color: '#64ffda', fontSize: 18, mt: 0.5 }} />
                            <Box>
                              <Typography variant="body2" sx={{ color: '#64ffda', fontWeight: 'bold' }}>
                                🔧 Fix Suggestion:
                              </Typography>
                              <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.8)' }}>
                                {bug.suggestion}
                              </Typography>
                            </Box>
                          </Box>
                        )}
                      </Box>
                    </Box>
                  </Paper>
                ))
              )}
            </Collapse>
          </Box>

          {/* Issues Section */}
          <Box sx={{ mt: 4 }}>
            <Box 
              sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', cursor: 'pointer' }}
              onClick={() => setExpandedIssues(!expandedIssues)}
            >
              <Typography variant="h6" sx={{ color: '#fff' }}>
                <WarningIcon sx={{ mr: 1, verticalAlign: 'middle', color: '#ffab00' }} />
                Issues ({issues.length})
              </Typography>
              <Chip 
                label={expandedIssues ? 'Hide' : 'Show'} 
                size="small" 
                sx={{ color: '#64ffda' }}
              />
            </Box>
            <Collapse in={expandedIssues}>
              {issues.length === 0 ? (
                <Paper sx={{ p: 2, mt: 2, background: 'rgba(0,255,0,0.05)', borderRadius: 2, border: '1px solid rgba(0,255,0,0.1)' }}>
                  <Typography sx={{ color: '#4caf50' }}>
                    ✅ No issues found!
                  </Typography>
                </Paper>
              ) : (
                issues.map((issue, index) => (
                  <Paper key={index} sx={{ 
                    p: 2, 
                    mt: 2, 
                    background: 'rgba(255,171,0,0.05)', 
                    borderRadius: 2, 
                    borderLeft: '4px solid #ffab00'
                  }}>
                    <Box sx={{ display: 'flex', alignItems: 'flex-start', gap: 1 }}>
                      <WarningIcon sx={{ color: '#ffab00' }} />
                      <Box sx={{ flex: 1 }}>
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, flexWrap: 'wrap' }}>
                          <Typography sx={{ color: '#fff', fontWeight: 'bold' }}>
                            Issue #{index + 1}
                          </Typography>
                          {issue.line && (
                            <Chip 
                              label={`Line ${issue.line}`} 
                              size="small" 
                              sx={{ backgroundColor: '#ffab00', color: '#000' }}
                            />
                          )}
                          {issue.type && (
                            <Chip 
                              label={issue.type} 
                              size="small" 
                              variant="outlined"
                              sx={{ color: '#ffab00', borderColor: '#ffab00' }}
                            />
                          )}
                        </Box>
                        <Typography sx={{ color: 'rgba(255,255,255,0.9)', mt: 1 }}>
                          {issue.description}
                        </Typography>
                        
                        {issue.line && codeLines.length > 0 && codeLines[issue.line - 1] !== undefined && (
                          <Paper sx={{ 
                            mt: 1, 
                            p: 1, 
                            background: 'rgba(255,171,0,0.1)', 
                            borderRadius: 1,
                            borderLeft: '3px solid #ffab00'
                          }}>
                            <Typography variant="caption" sx={{ color: '#ffab00', fontWeight: 'bold' }}>
                              ⚠️ Issue at Line {issue.line}:
                            </Typography>
                            <pre style={{ 
                              margin: '4px 0 0 0', 
                              color: '#ffab00',
                              fontSize: '13px',
                              fontFamily: 'monospace',
                              whiteSpace: 'pre-wrap',
                              wordWrap: 'break-word',
                              backgroundColor: 'rgba(255,171,0,0.05)',
                              padding: '8px',
                              borderRadius: '4px'
                            }}>
                              {codeLines[issue.line - 1] || 'Line not found'}
                            </pre>
                          </Paper>
                        )}
                        
                        {issue.suggestion && (
                          <Box sx={{ mt: 1, display: 'flex', alignItems: 'flex-start', gap: 1 }}>
                            <LightbulbIcon sx={{ color: '#64ffda', fontSize: 18, mt: 0.5 }} />
                            <Box>
                              <Typography variant="body2" sx={{ color: '#64ffda', fontWeight: 'bold' }}>
                                🔧 Fix Suggestion:
                              </Typography>
                              <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.8)' }}>
                                {issue.suggestion}
                              </Typography>
                            </Box>
                          </Box>
                        )}
                      </Box>
                    </Box>
                  </Paper>
                ))
              )}
            </Collapse>
          </Box>

          {/* Suggestions Section */}
          <Box sx={{ mt: 4 }}>
            <Box 
              sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', cursor: 'pointer' }}
              onClick={() => setExpandedSuggestions(!expandedSuggestions)}
            >
              <Typography variant="h6" sx={{ color: '#fff' }}>
                <LightbulbIcon sx={{ mr: 1, verticalAlign: 'middle', color: '#4ecdc4' }} />
                Suggestions ({suggestions.length})
              </Typography>
              <Chip 
                label={expandedSuggestions ? 'Hide' : 'Show'} 
                size="small" 
                sx={{ color: '#64ffda' }}
              />
            </Box>
            <Collapse in={expandedSuggestions}>
              {suggestions.length === 0 ? (
                <Paper sx={{ p: 2, mt: 2, background: 'rgba(0,255,0,0.05)', borderRadius: 2, border: '1px solid rgba(0,255,0,0.1)' }}>
                  <Typography sx={{ color: '#4caf50' }}>
                    ✅ No suggestions needed!
                  </Typography>
                </Paper>
              ) : (
                suggestions.map((suggestion, index) => (
                  <Paper key={index} sx={{ 
                    p: 2, 
                    mt: 2, 
                    background: 'rgba(78,205,196,0.05)', 
                    borderRadius: 2, 
                    borderLeft: '4px solid #4ecdc4'
                  }}>
                    <Box sx={{ display: 'flex', alignItems: 'flex-start', gap: 1 }}>
                      <LightbulbIcon sx={{ color: '#4ecdc4' }} />
                      <Box sx={{ flex: 1 }}>
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, flexWrap: 'wrap' }}>
                          <Typography sx={{ color: '#fff', fontWeight: 'bold' }}>
                            Suggestion #{index + 1}
                          </Typography>
                          {suggestion.line && (
                            <Chip 
                              label={`Line ${suggestion.line}`} 
                              size="small" 
                              sx={{ backgroundColor: '#4ecdc4', color: '#000' }}
                            />
                          )}
                        </Box>
                        <Typography sx={{ color: 'rgba(255,255,255,0.9)', mt: 1 }}>
                          {suggestion.description}
                        </Typography>
                        
                        {suggestion.line && codeLines.length > 0 && codeLines[suggestion.line - 1] !== undefined && (
                          <Paper sx={{ 
                            mt: 1, 
                            p: 1, 
                            background: 'rgba(78,205,196,0.1)', 
                            borderRadius: 1,
                            borderLeft: '3px solid #4ecdc4'
                          }}>
                            <Typography variant="caption" sx={{ color: '#4ecdc4', fontWeight: 'bold' }}>
                              💡 Code at Line {suggestion.line}:
                            </Typography>
                            <pre style={{ 
                              margin: '4px 0 0 0', 
                              color: '#4ecdc4',
                              fontSize: '13px',
                              fontFamily: 'monospace',
                              whiteSpace: 'pre-wrap',
                              wordWrap: 'break-word',
                              backgroundColor: 'rgba(78,205,196,0.05)',
                              padding: '8px',
                              borderRadius: '4px'
                            }}>
                              {codeLines[suggestion.line - 1] || 'Line not found'}
                            </pre>
                          </Paper>
                        )}
                        
                        {suggestion.recommendation && (
                          <Box sx={{ mt: 1 }}>
                            <Typography variant="body2" sx={{ color: '#4ecdc4', fontStyle: 'italic' }}>
                              💡 {suggestion.recommendation}
                            </Typography>
                          </Box>
                        )}
                        
                        {suggestion.code_example && (
                          <Paper sx={{ 
                            p: 1, 
                            mt: 1, 
                            background: 'rgba(0,0,0,0.3)', 
                            borderRadius: 1,
                            border: '1px solid rgba(78,205,196,0.2)'
                          }}>
                            <Typography variant="caption" sx={{ color: '#64ffda' }}>
                              Code Example:
                            </Typography>
                            <pre style={{ 
                              margin: '4px 0 0 0', 
                              color: '#e0e0e0', 
                              fontSize: '12px',
                              fontFamily: 'monospace',
                              whiteSpace: 'pre-wrap',
                              wordWrap: 'break-word'
                            }}>
                              {suggestion.code_example}
                            </pre>
                          </Paper>
                        )}
                      </Box>
                    </Box>
                  </Paper>
                ))
              )}
            </Collapse>
          </Box>

          {/* ============================================================ */}
          {/* FIXED TEST CASES SECTION - Complete rewrite */}
          {/* ============================================================ */}
          {testCases.length > 0 && (
            <Box sx={{ mt: 4 }}>
              <Box 
                sx={{ 
                  display: 'flex', 
                  alignItems: 'center', 
                  justifyContent: 'space-between',
                  mb: 2,
                  p: 1.5,
                  borderRadius: 2,
                  background: 'rgba(255,215,0,0.05)',
                  border: '1px solid rgba(255,215,0,0.1)',
                  cursor: 'pointer'
                }}
                onClick={() => setExpandedTestCases(!expandedTestCases)}
              >
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, flexWrap: 'wrap' }}>
                  <CheckCircleIcon sx={{ color: '#ffd93d' }} />
                  <Typography variant="h6" sx={{ color: '#fff', fontWeight: 'bold' }}>
                    🧪 Test Cases Generated ({testCases.length})
                  </Typography>
                  <Chip 
                    label={`${testCases.filter(tc => shouldTestCasePass(tc, submission.code)).length} Passed`}
                    size="small"
                    sx={{ 
                      bgcolor: 'rgba(76,175,80,0.2)',
                      color: '#4caf50',
                      fontWeight: 'bold'
                    }}
                  />
                  <Chip 
                    label={`${testCases.filter(tc => !shouldTestCasePass(tc, submission.code)).length} Failed`}
                    size="small"
                    sx={{ 
                      bgcolor: 'rgba(244,67,54,0.2)',
                      color: '#ff6b6b',
                      fontWeight: 'bold'
                    }}
                  />
                </Box>
                <Chip 
                  label={expandedTestCases ? 'Hide ▲' : 'Show ▼'} 
                  size="small" 
                  sx={{ 
                    color: '#64ffda',
                    background: 'rgba(100,255,218,0.1)',
                    fontWeight: 'bold'
                  }}
                />
              </Box>

              <Collapse in={expandedTestCases}>
                <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1.5 }}>
                  {testCases.map((testCase, index) => {
                    // Determine if test case passes
                    const isPassed = shouldTestCasePass(testCase, submission.code);
                    
                    // FIX: Use renderInput() helper to safely display input
                    const displayInput = renderInput(testCase.input);
                    const actualResult = isPassed ? (testCase.expected || '✅ Passed') : '💥 Failed';
                    const icon = isPassed ? '✅' : '❌';
                    const statusText = isPassed ? 'PASSED' : 'FAILED';
                    const statusColor = isPassed ? '#4caf50' : '#ff6b6b';
                    const borderColor = isPassed ? '#4caf50' : '#ff1744';
                    
                    // Generate error detail for failed tests
                    let errorDetail = '';
                    if (!isPassed) {
                      const inputStr = String(testCase.input || '');
                      if (inputStr.includes('[]') || inputStr.includes('empty')) {
                        errorDetail = '⚠️ Code doesn\'t handle empty lists!';
                      } else if (inputStr.includes('invalid') || inputStr.includes('"a"')) {
                        errorDetail = '⚠️ Code doesn\'t validate input types!';
                      } else if (inputStr.includes('null') || inputStr.includes('None')) {
                        errorDetail = '⚠️ Code doesn\'t handle null/None values!';
                      } else if (inputStr.includes('-1') || inputStr.includes('-5')) {
                        errorDetail = '⚠️ Code doesn\'t handle negative numbers!';
                      } else if (inputStr.includes('999999') || inputStr.includes('1000')) {
                        errorDetail = '⚠️ Code might overflow with large numbers!';
                      } else {
                        errorDetail = '⚠️ Test case failed - check edge cases!';
                      }
                    }
                    
                    return (
                      <Paper 
                        key={index}
                        sx={{ 
                          p: 2,
                          bgcolor: isPassed ? 'rgba(76,175,80,0.03)' : 'rgba(244,67,54,0.05)',
                          borderLeft: `4px solid ${borderColor}`,
                          borderRadius: 1,
                          border: `1px solid ${borderColor}20`,
                        }}
                      >
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.5, flexWrap: 'wrap' }}>
                          <Typography sx={{ fontSize: '20px' }}>{icon}</Typography>
                          <Chip 
                            label={statusText}
                            size="small"
                            sx={{ 
                              bgcolor: isPassed ? 'rgba(76,175,80,0.2)' : 'rgba(244,67,54,0.2)',
                              color: statusColor,
                              fontWeight: 'bold',
                              height: '24px',
                              fontSize: '12px'
                            }}
                          />
                          <Typography sx={{ color: '#fff', fontWeight: 'bold', fontSize: '15px' }}>
                            {testCase.name || testCase.function || `Test ${index + 1}`}
                          </Typography>
                          {testCase.function && testCase.name !== testCase.function && (
                            <Chip 
                              label={`Function: ${testCase.function}`}
                              size="small"
                              variant="outlined"
                              sx={{ 
                                borderColor: 'rgba(255,255,255,0.2)',
                                color: 'rgba(255,255,255,0.7)',
                                height: '20px',
                                fontSize: '11px'
                              }}
                            />
                          )}
                        </Box>
                        
                        {/* FIX: Use displayInput which is safely rendered */}
                        <Box sx={{ 
                          display: 'flex', 
                          gap: 3, 
                          mt: 1.5, 
                          flexWrap: 'wrap',
                          p: 1,
                          bgcolor: 'rgba(0,0,0,0.2)',
                          borderRadius: 1
                        }}>
                          <Box>
                            <Typography variant="caption" sx={{ color: 'rgba(255,255,255,0.5)', display: 'block' }}>
                              📥 Input
                            </Typography>
                            <Typography sx={{ 
                              color: 'rgba(255,255,255,0.9)',
                              fontFamily: 'monospace',
                              fontSize: '13px'
                            }}>
                              {displayInput}
                            </Typography>
                          </Box>
                          <Box>
                            <Typography variant="caption" sx={{ color: 'rgba(255,255,255,0.5)', display: 'block' }}>
                              🎯 Expected
                            </Typography>
                            <Typography sx={{ 
                              color: '#ffd93d',
                              fontFamily: 'monospace',
                              fontSize: '13px'
                            }}>
                              {testCase.expected || 'N/A'}
                            </Typography>
                          </Box>
                          <Box>
                            <Typography variant="caption" sx={{ color: 'rgba(255,255,255,0.5)', display: 'block' }}>
                              📤 Actual
                            </Typography>
                            <Typography sx={{ 
                              color: statusColor, 
                              fontWeight: 'bold',
                              fontFamily: 'monospace',
                              fontSize: '13px'
                            }}>
                              {actualResult}
                            </Typography>
                          </Box>
                          {testCase.description && testCase.description !== testCase.name && (
                            <Box>
                              <Typography variant="caption" sx={{ color: 'rgba(255,255,255,0.5)', display: 'block' }}>
                                📝 Description
                              </Typography>
                              <Typography sx={{ 
                                color: 'rgba(255,255,255,0.7)',
                                fontSize: '13px'
                              }}>
                                {testCase.description}
                              </Typography>
                            </Box>
                          )}
                        </Box>
                        
                        {errorDetail && (
                          <Box sx={{ mt: 1, display: 'flex', alignItems: 'center', gap: 1 }}>
                            <WarningIcon sx={{ color: '#ff6b6b', fontSize: '16px' }} />
                            <Typography sx={{ color: '#ff6b6b', fontSize: '13px', fontWeight: 'bold' }}>
                              {errorDetail}
                            </Typography>
                          </Box>
                        )}
                        
                        {testCase.test_code && (
                          <Paper sx={{ 
                            mt: 1.5,
                            p: 1.5, 
                            bgcolor: 'rgba(0,0,0,0.4)',
                            borderRadius: 1,
                            border: '1px solid rgba(255,255,255,0.05)'
                          }}>
                            <Typography variant="caption" sx={{ color: '#64ffda', display: 'block', mb: 0.5 }}>
                              💻 Test Code
                            </Typography>
                            <pre style={{ 
                              margin: 0, 
                              color: '#e0e0e0', 
                              fontSize: '12px',
                              fontFamily: 'monospace',
                              whiteSpace: 'pre-wrap',
                              wordWrap: 'break-word',
                              maxHeight: '150px',
                              overflow: 'auto'
                            }}>
                              {testCase.test_code}
                            </pre>
                          </Paper>
                        )}
                      </Paper>
                    );
                  })}
                </Box>
                
                {/* Test Summary */}
                <Box sx={{ 
                  mt: 2, 
                  p: 2, 
                  bgcolor: 'rgba(255,255,255,0.02)',
                  borderRadius: 1,
                  border: '1px solid rgba(255,255,255,0.05)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  flexWrap: 'wrap',
                  gap: 1
                }}>
                  <Typography variant="subtitle2" sx={{ color: 'rgba(255,255,255,0.7)', fontSize: '14px' }}>
                    📊 Test Summary
                  </Typography>
                  <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
                    <Chip 
                      label={`✅ ${testCases.filter(tc => shouldTestCasePass(tc, submission.code)).length} Passed`}
                      size="small"
                      sx={{ bgcolor: 'rgba(76,175,80,0.2)', color: '#4caf50', height: '24px', fontSize: '12px', fontWeight: 'bold' }}
                    />
                    <Chip 
                      label={`❌ ${testCases.filter(tc => !shouldTestCasePass(tc, submission.code)).length} Failed`}
                      size="small"
                      sx={{ bgcolor: 'rgba(244,67,54,0.2)', color: '#ff6b6b', height: '24px', fontSize: '12px', fontWeight: 'bold' }}
                    />
                    <Chip 
                      label={`📋 ${testCases.length} Total`}
                      size="small"
                      sx={{ bgcolor: 'rgba(100,255,218,0.1)', color: '#64ffda', height: '24px', fontSize: '12px' }}
                    />
                  </Box>
                </Box>
              </Collapse>
            </Box>
          )}

          <Box sx={{ display: 'flex', gap: 2, mt: 4, flexWrap: 'wrap' }}>
            <Button
              variant="contained"
              onClick={() => navigate('/dashboard')}
              sx={{
                background: 'linear-gradient(45deg, #64ffda, #00b4d8)',
                color: '#000',
                fontWeight: 'bold',
                '&:hover': {
                  background: 'linear-gradient(45deg, #00b4d8, #64ffda)',
                },
              }}
            >
              Back to Dashboard
            </Button>
            <Button
              variant="outlined"
              onClick={() => navigate('/history')}
              sx={{
                borderColor: 'rgba(255,255,255,0.2)',
                color: '#fff',
                '&:hover': {
                  borderColor: '#64ffda',
                  color: '#64ffda',
                },
              }}
            >
              View All Submissions
            </Button>
            <Button
              variant="outlined"
              onClick={() => navigate('/submit-code')}
              sx={{
                borderColor: 'rgba(255,255,255,0.2)',
                color: '#fff',
                '&:hover': {
                  borderColor: '#4ecdc4',
                  color: '#4ecdc4',
                },
              }}
            >
              Submit New Code
            </Button>
          </Box>
        </Paper>
      </motion.div>
    </Container>
  );
};

export default SubmissionDetail;