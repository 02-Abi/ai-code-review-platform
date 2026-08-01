"""
Views for Code Review App - Complete
With AUTO LANGUAGE DETECTION & DYNAMIC CODE ANALYSIS!
Enhanced with ChatGPT-like intelligent test case generation and execution!
SYNTAX ERROR DETECTION FOR ALL LANGUAGES - FIXED!
"""
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.db.models import Q, Avg, Count, Sum
from .models import (
    ProgrammingLanguage, CodeSubmission, ReviewHistory,
    CodeReviewComment, CodeSnippet
)
from .serializers import (
    ProgrammingLanguageSerializer, CodeSubmissionSerializer,
    CodeSubmissionCreateSerializer, ReviewHistorySerializer,
    CodeReviewCommentSerializer, CodeSnippetSerializer
)
from django.utils import timezone
import logging
import re
import ast
import json
import sys
import io
import contextlib
import traceback
import subprocess
import tempfile
import os
import signal
import time
from typing import Dict, List, Any, Optional, Tuple

logger = logging.getLogger(__name__)


# ============================================================
# SYNTAX ERROR DETECTOR - For ALL Languages - FIXED!
# ============================================================

class SyntaxErrorDetector:
    """
    Detects syntax errors in multiple programming languages
    """
    
    @staticmethod
    def detect_syntax_errors(code: str, language: str) -> List[Dict]:
        """
        Detect syntax errors based on language
        """
        errors = []
        
        if language.lower() in ['python']:
            errors = SyntaxErrorDetector._check_python_syntax(code)
        elif language.lower() in ['javascript', 'js']:
            errors = SyntaxErrorDetector._check_javascript_syntax(code)
        elif language.lower() in ['java']:
            errors = SyntaxErrorDetector._check_java_syntax(code)
        elif language.lower() in ['cpp', 'c++']:
            errors = SyntaxErrorDetector._check_cpp_syntax(code)
        elif language.lower() in ['c']:
            errors = SyntaxErrorDetector._check_c_syntax(code)
        elif language.lower() in ['go']:
            errors = SyntaxErrorDetector._check_go_syntax(code)
        elif language.lower() in ['rust']:
            errors = SyntaxErrorDetector._check_rust_syntax(code)
        elif language.lower() in ['ruby']:
            errors = SyntaxErrorDetector._check_ruby_syntax(code)
        elif language.lower() in ['php']:
            errors = SyntaxErrorDetector._check_php_syntax(code)
        elif language.lower() in ['sql']:
            errors = SyntaxErrorDetector._check_sql_syntax(code)
        elif language.lower() in ['shell', 'bash']:
            errors = SyntaxErrorDetector._check_shell_syntax(code)
        elif language.lower() in ['typescript', 'ts']:
            errors = SyntaxErrorDetector._check_typescript_syntax(code)
        elif language.lower() in ['swift']:
            errors = SyntaxErrorDetector._check_swift_syntax(code)
        elif language.lower() in ['kotlin']:
            errors = SyntaxErrorDetector._check_kotlin_syntax(code)
        else:
            errors = SyntaxErrorDetector._check_generic_syntax(code)
        
        return errors
    
    @staticmethod
    def _check_python_syntax(code: str) -> List[Dict]:
        """Check Python syntax errors with accurate line numbers"""
        errors = []
        lines = code.split('\n')
        
        try:
            ast.parse(code)
        except SyntaxError as e:
            line_num = e.lineno if e.lineno else 1
            error_msg = str(e)
            
            # Get the actual line
            actual_line = lines[line_num - 1] if line_num <= len(lines) else ''
            
            # Provide specific suggestion
            suggestion = SyntaxErrorDetector._get_python_suggestion(error_msg, actual_line)
            
            errors.append({
                'line': line_num,
                'message': f'Syntax Error: {error_msg}',
                'suggestion': suggestion,
                'code_line': actual_line
            })
        except Exception as e:
            errors.append({
                'line': 1,
                'message': f'Error: {str(e)}',
                'suggestion': 'Fix the syntax error in your Python code'
            })
        
        return errors
    
    @staticmethod
    def _get_python_suggestion(error_msg: str, code_line: str = '') -> str:
        """Generate suggestion for Python syntax error"""
        error_lower = error_msg.lower()
        
        if 'invalid syntax' in error_lower:
            if 'def' in code_line and ',' not in code_line and '(' in code_line and ')' in code_line:
                return 'Missing comma between function parameters. Example: def func(a, b):'
            if ':' not in code_line and 'def' in code_line:
                return 'Missing colon (:) after function definition. Example: def func():'
            return 'Check for missing parentheses, brackets, quotes, or invalid syntax'
        elif 'unexpected indent' in error_lower:
            return 'Fix indentation - ensure consistent use of spaces/tabs (4 spaces recommended)'
        elif 'expected an indented block' in error_lower:
            return 'Add indented block after colon (:) for function/class/loop/conditional'
        elif 'unterminated string' in error_lower:
            return 'Close string with matching quote (", \', or """)'
        elif 'unmatched' in error_lower:
            return 'Check for matching parentheses (), brackets [], or curly braces {}'
        elif 'missing' in error_lower and 'comma' in error_lower:
            return 'Add missing comma between function parameters or list elements'
        elif 'positional argument' in error_lower:
            return 'Check function call: ensure correct number and order of arguments'
        elif 'EOL' in error_msg or 'end of line' in error_lower:
            return 'Check for incomplete statement - missing closing quote or parenthesis'
        elif 'name' in error_lower and 'defined' in error_lower:
            return 'Variable or function used before definition - check spelling and order'
        else:
            return 'Fix the syntax error in your Python code'
    
    @staticmethod
    def _check_javascript_syntax(code: str) -> List[Dict]:
        """Check JavaScript syntax errors"""
        errors = []
        lines = code.split('\n')
        paren_stack = []
        brace_stack = []
        bracket_stack = []
        
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            
            # Skip comments
            if stripped.startswith('//') or stripped.startswith('/*'):
                continue
            
            # Check for unterminated strings (basic check)
            quote_count = stripped.count("'") + stripped.count('"')
            if quote_count % 2 != 0:
                errors.append({
                    'line': i,
                    'message': 'Syntax Error: Unterminated string literal',
                    'suggestion': 'Close string with matching quote (single or double)',
                    'code_line': line
                })
                break
            
            # Check for missing semicolon (basic check)
            if not stripped.endswith((';', '{', '}', '(', '/', '//', '/*', '*/')):
                if 'function' not in stripped and 'if' not in stripped and 'else' not in stripped:
                    if 'class' not in stripped and 'try' not in stripped:
                        errors.append({
                            'line': i,
                            'message': 'Syntax Error: Missing semicolon',
                            'suggestion': 'Add semicolon (;) at the end of the statement',
                            'code_line': line
                        })
                        break
            
            # Check for unmatched parentheses
            for char in line:
                if char == '(':
                    paren_stack.append(i)
                elif char == ')':
                    if paren_stack:
                        paren_stack.pop()
                    else:
                        errors.append({
                            'line': i,
                            'message': 'Syntax Error: Unmatched closing parenthesis )',
                            'suggestion': 'Remove extra closing parenthesis or add matching opening parenthesis',
                            'code_line': line
                        })
                        break
            
            # Check for unmatched braces
            for char in line:
                if char == '{':
                    brace_stack.append(i)
                elif char == '}':
                    if brace_stack:
                        brace_stack.pop()
                    else:
                        errors.append({
                            'line': i,
                            'message': 'Syntax Error: Unmatched closing brace }',
                            'suggestion': 'Remove extra closing brace or add matching opening brace',
                            'code_line': line
                        })
                        break
            
            # Check for unmatched brackets
            for char in line:
                if char == '[':
                    bracket_stack.append(i)
                elif char == ']':
                    if bracket_stack:
                        bracket_stack.pop()
                    else:
                        errors.append({
                            'line': i,
                            'message': 'Syntax Error: Unmatched closing bracket ]',
                            'suggestion': 'Remove extra closing bracket or add matching opening bracket',
                            'code_line': line
                        })
                        break
        
        # Check if any unmatched items remain
        if paren_stack:
            errors.append({
                'line': paren_stack[0],
                'message': 'Syntax Error: Unmatched opening parenthesis (',
                'suggestion': 'Add closing parenthesis )',
                'code_line': lines[paren_stack[0] - 1]
            })
        
        if brace_stack:
            errors.append({
                'line': brace_stack[0],
                'message': 'Syntax Error: Unmatched opening brace {',
                'suggestion': 'Add closing brace }',
                'code_line': lines[brace_stack[0] - 1]
            })
        
        if bracket_stack:
            errors.append({
                'line': bracket_stack[0],
                'message': 'Syntax Error: Unmatched opening bracket [',
                'suggestion': 'Add closing bracket ]',
                'code_line': lines[bracket_stack[0] - 1]
            })
        
        return errors
    
    @staticmethod
    def _check_java_syntax(code: str) -> List[Dict]:
        """Check Java syntax errors"""
        errors = []
        lines = code.split('\n')
        brace_stack = []
        
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            
            if stripped.startswith('//') or stripped.startswith('/*'):
                continue
            
            # Check for missing semicolon
            if ';' not in line and not stripped.endswith(('{', '}', '//', '/*')):
                if 'class' not in stripped and 'public' not in stripped and 'private' not in stripped:
                    if 'import' not in stripped and 'package' not in stripped:
                        errors.append({
                            'line': i,
                            'message': 'Syntax Error: Missing semicolon',
                            'suggestion': 'Add semicolon (;) at the end of the statement',
                            'code_line': line
                        })
                        break
            
            # Check for unmatched braces
            for char in line:
                if char == '{':
                    brace_stack.append(i)
                elif char == '}':
                    if brace_stack:
                        brace_stack.pop()
                    else:
                        errors.append({
                            'line': i,
                            'message': 'Syntax Error: Unmatched closing brace }',
                            'suggestion': 'Remove extra closing brace or add matching opening brace',
                            'code_line': line
                        })
                        break
            
            # Check for unterminated strings
            if stripped.count('"') % 2 != 0 and not stripped.startswith('//'):
                errors.append({
                    'line': i,
                    'message': 'Syntax Error: Unterminated string literal',
                    'suggestion': 'Close string with matching double quote "',
                    'code_line': line
                })
                break
        
        if brace_stack:
            errors.append({
                'line': brace_stack[0],
                'message': 'Syntax Error: Unmatched opening brace {',
                'suggestion': 'Add closing brace }',
                'code_line': lines[brace_stack[0] - 1]
            })
        
        return errors
    
    @staticmethod
    def _check_cpp_syntax(code: str) -> List[Dict]:
        """Check C++ syntax errors"""
        errors = []
        lines = code.split('\n')
        brace_stack = []
        
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            
            if stripped.startswith('//') or stripped.startswith('/*'):
                continue
            
            # Check for missing semicolon
            if ';' not in line and not stripped.endswith(('{', '}', '//', '/*')):
                if '#include' not in stripped and 'using' not in stripped:
                    if 'class' not in stripped and 'template' not in stripped:
                        errors.append({
                            'line': i,
                            'message': 'Syntax Error: Missing semicolon',
                            'suggestion': 'Add semicolon (;) at the end of the statement',
                            'code_line': line
                        })
                        break
            
            # Check for unmatched braces
            for char in line:
                if char == '{':
                    brace_stack.append(i)
                elif char == '}':
                    if brace_stack:
                        brace_stack.pop()
                    else:
                        errors.append({
                            'line': i,
                            'message': 'Syntax Error: Unmatched closing brace }',
                            'suggestion': 'Remove extra closing brace or add matching opening brace',
                            'code_line': line
                        })
                        break
            
            # Check for unterminated strings
            if stripped.count('"') % 2 != 0:
                errors.append({
                    'line': i,
                    'message': 'Syntax Error: Unterminated string literal',
                    'suggestion': 'Close string with matching double quote "',
                    'code_line': line
                })
                break
        
        if brace_stack:
            errors.append({
                'line': brace_stack[0],
                'message': 'Syntax Error: Unmatched opening brace {',
                'suggestion': 'Add closing brace }',
                'code_line': lines[brace_stack[0] - 1]
            })
        
        return errors
    
    @staticmethod
    def _check_c_syntax(code: str) -> List[Dict]:
        """Check C syntax errors"""
        return SyntaxErrorDetector._check_cpp_syntax(code)
    
    @staticmethod
    def _check_go_syntax(code: str) -> List[Dict]:
        """Check Go syntax errors"""
        errors = []
        lines = code.split('\n')
        brace_stack = []
        
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            
            if stripped.startswith('//'):
                continue
            
            # Check for missing imports
            if 'fmt.Println' in line or 'fmt.Printf' in line:
                has_import = False
                for j in range(max(0, i-10), min(i+10, len(lines))):
                    if 'import' in lines[j]:
                        has_import = True
                        break
                if not has_import:
                    errors.append({
                        'line': i,
                        'message': 'Syntax Error: Missing import for fmt package',
                        'suggestion': 'Add `import "fmt"` at the top of the file',
                        'code_line': line
                    })
                    break
            
            # Check for unmatched braces
            for char in line:
                if char == '{':
                    brace_stack.append(i)
                elif char == '}':
                    if brace_stack:
                        brace_stack.pop()
                    else:
                        errors.append({
                            'line': i,
                            'message': 'Syntax Error: Unmatched closing brace }',
                            'suggestion': 'Remove extra closing brace or add matching opening brace',
                            'code_line': line
                        })
                        break
        
        if brace_stack:
            errors.append({
                'line': brace_stack[0],
                'message': 'Syntax Error: Unmatched opening brace {',
                'suggestion': 'Add closing brace }',
                'code_line': lines[brace_stack[0] - 1]
            })
        
        return errors
    
    @staticmethod
    def _check_rust_syntax(code: str) -> List[Dict]:
        """Check Rust syntax errors"""
        errors = []
        lines = code.split('\n')
        brace_stack = []
        
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            
            if stripped.startswith('//'):
                continue
            
            # Check for missing semicolon
            if ';' not in line and not stripped.endswith(('{', '}', '//')):
                if 'fn' not in stripped and 'let' not in stripped and 'use' not in stripped:
                    if 'struct' not in stripped and 'impl' not in stripped:
                        errors.append({
                            'line': i,
                            'message': 'Syntax Error: Missing semicolon',
                            'suggestion': 'Add semicolon (;) at the end of the statement',
                            'code_line': line
                        })
                        break
            
            # Check for unmatched braces
            for char in line:
                if char == '{':
                    brace_stack.append(i)
                elif char == '}':
                    if brace_stack:
                        brace_stack.pop()
                    else:
                        errors.append({
                            'line': i,
                            'message': 'Syntax Error: Unmatched closing brace }',
                            'suggestion': 'Remove extra closing brace or add matching opening brace',
                            'code_line': line
                        })
                        break
            
            # Check for unterminated strings
            if stripped.count('"') % 2 != 0:
                errors.append({
                    'line': i,
                    'message': 'Syntax Error: Unterminated string literal',
                    'suggestion': 'Close string with matching double quote "',
                    'code_line': line
                })
                break
        
        if brace_stack:
            errors.append({
                'line': brace_stack[0],
                'message': 'Syntax Error: Unmatched opening brace {',
                'suggestion': 'Add closing brace }',
                'code_line': lines[brace_stack[0] - 1]
            })
        
        return errors
    
    @staticmethod
    def _check_ruby_syntax(code: str) -> List[Dict]:
        """Check Ruby syntax errors"""
        errors = []
        lines = code.split('\n')
        
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            
            if stripped.startswith('#'):
                continue
            
            # Check for missing end
            if 'def ' in stripped or 'class ' in stripped or 'module ' in stripped:
                has_end = False
                end_count = 0
                for j in range(i, min(i + 50, len(lines))):
                    if 'end' in lines[j]:
                        end_count += 1
                        if end_count >= stripped.count('def') + stripped.count('class') + stripped.count('module'):
                            has_end = True
                            break
                if not has_end:
                    errors.append({
                        'line': i,
                        'message': 'Syntax Error: Missing `end` for block',
                        'suggestion': 'Add `end` to close the block (function/class/module)',
                        'code_line': line
                    })
                    break
            
            # Check for unterminated strings
            if stripped.count('"') % 2 != 0 or stripped.count("'") % 2 != 0:
                errors.append({
                    'line': i,
                    'message': 'Syntax Error: Unterminated string literal',
                    'suggestion': 'Close string with matching quote (" or \')',
                    'code_line': line
                })
                break
        
        return errors
    
    @staticmethod
    def _check_php_syntax(code: str) -> List[Dict]:
        """Check PHP syntax errors"""
        errors = []
        lines = code.split('\n')
        
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            
            if stripped.startswith('//') or stripped.startswith('#'):
                continue
            
            # Check for missing semicolon
            if ';' not in line and not stripped.endswith(('{', '}', '//', '/*', '?')):
                if 'echo' in stripped or 'print' in stripped or 'return' in stripped:
                    errors.append({
                        'line': i,
                        'message': 'Syntax Error: Missing semicolon',
                        'suggestion': 'Add semicolon (;) at the end of the statement',
                        'code_line': line
                    })
                    break
            
            # Check for unterminated strings
            if stripped.count('"') % 2 != 0 or stripped.count("'") % 2 != 0:
                errors.append({
                    'line': i,
                    'message': 'Syntax Error: Unterminated string literal',
                    'suggestion': 'Close string with matching quote (" or \')',
                    'code_line': line
                })
                break
            
            # Check for missing opening PHP tag
            if i == 1 and not stripped.startswith('<?php') and not stripped.startswith('<?='):
                errors.append({
                    'line': i,
                    'message': 'Syntax Error: Missing opening PHP tag',
                    'suggestion': 'Add `<?php` at the beginning of the file',
                    'code_line': line
                })
                break
        
        return errors
    
    @staticmethod
    def _check_sql_syntax(code: str) -> List[Dict]:
        """Check SQL syntax errors"""
        errors = []
        lines = code.split('\n')
        
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            upper_line = line.upper()
            
            if not stripped or stripped.startswith('--'):
                continue
            
            # Check for missing WHERE in DELETE/UPDATE
            if ('DELETE' in upper_line or 'UPDATE' in upper_line) and 'WHERE' not in upper_line:
                if ';' not in stripped:
                    errors.append({
                        'line': i,
                        'message': 'Syntax Error: DELETE/UPDATE without WHERE clause',
                        'suggestion': 'Add WHERE clause to restrict the operation or use LIMIT',
                        'code_line': line
                    })
                    break
            
            # Check for missing semicolon
            if ';' not in line and not stripped.startswith('--'):
                if 'SELECT' in upper_line or 'INSERT' in upper_line or 'UPDATE' in upper_line:
                    errors.append({
                        'line': i,
                        'message': 'Syntax Error: Missing semicolon',
                        'suggestion': 'Add semicolon (;) at the end of the statement',
                        'code_line': line
                    })
                    break
        
        return errors
    
    @staticmethod
    def _check_shell_syntax(code: str) -> List[Dict]:
        """Check Shell script syntax errors"""
        errors = []
        lines = code.split('\n')
        
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            
            if stripped.startswith('#'):
                continue
            
            # Check for missing shebang
            if i == 1 and not stripped.startswith('#!'):
                errors.append({
                    'line': i,
                    'message': 'Syntax Error: Missing shebang (#!) line',
                    'suggestion': 'Add shebang: `#!/bin/bash` or `#!/bin/sh`',
                    'code_line': line
                })
                break
            
            # Check for unquoted variables
            if '$' in stripped and '=' in stripped:
                if '"$' not in stripped and "'$" not in stripped:
                    errors.append({
                        'line': i,
                        'message': 'Syntax Error: Unquoted variable',
                        'suggestion': 'Quote variables: `"$VAR"` to prevent word splitting',
                        'code_line': line
                    })
                    break
        
        return errors
    
    @staticmethod
    def _check_typescript_syntax(code: str) -> List[Dict]:
        """Check TypeScript syntax errors"""
        # Use JavaScript checker as base since TypeScript is a superset
        errors = SyntaxErrorDetector._check_javascript_syntax(code)
        
        # Additional TypeScript-specific checks
        lines = code.split('\n')
        
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            
            if stripped.startswith('//') or stripped.startswith('/*'):
                continue
            
            # Check for missing type annotations
            if 'function' in stripped and '(' in stripped and ':' not in stripped:
                if ':' not in stripped:
                    errors.append({
                        'line': i,
                        'message': 'TypeScript: Missing type annotation',
                        'suggestion': 'Add type annotation: `function func(param: type): returnType`',
                        'code_line': line
                    })
                    break
        
        return errors
    
    @staticmethod
    def _check_swift_syntax(code: str) -> List[Dict]:
        """Check Swift syntax errors"""
        errors = []
        lines = code.split('\n')
        
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            
            if stripped.startswith('//'):
                continue
            
            # Check for missing closing braces
            if 'class' in stripped or 'struct' in stripped or 'func' in stripped:
                if '{' in stripped and '}' not in stripped:
                    has_close = False
                    for j in range(i, min(i + 50, len(lines))):
                        if '}' in lines[j]:
                            has_close = True
                            break
                    if not has_close:
                        errors.append({
                            'line': i,
                            'message': 'Syntax Error: Missing closing brace }',
                            'suggestion': 'Add closing brace } to close the block',
                            'code_line': line
                        })
                        break
            
            # Check for unterminated strings
            if stripped.count('"') % 2 != 0:
                errors.append({
                    'line': i,
                    'message': 'Syntax Error: Unterminated string literal',
                    'suggestion': 'Close string with matching double quote "',
                    'code_line': line
                })
                break
        
        return errors
    
    @staticmethod
    def _check_kotlin_syntax(code: str) -> List[Dict]:
        """Check Kotlin syntax errors"""
        errors = []
        lines = code.split('\n')
        
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            
            if stripped.startswith('//'):
                continue
            
            # Check for missing closing braces
            if 'fun' in stripped or 'class' in stripped:
                if '{' in stripped and '}' not in stripped:
                    has_close = False
                    for j in range(i, min(i + 50, len(lines))):
                        if '}' in lines[j]:
                            has_close = True
                            break
                    if not has_close:
                        errors.append({
                            'line': i,
                            'message': 'Syntax Error: Missing closing brace }',
                            'suggestion': 'Add closing brace } to close the block',
                            'code_line': line
                        })
                        break
            
            # Check for missing return type
            if 'fun' in stripped and ':' not in stripped:
                if 'Unit' not in stripped and '=' not in stripped:
                    errors.append({
                        'line': i,
                        'message': 'Syntax Error: Missing return type',
                        'suggestion': 'Add return type: `fun func(): ReturnType { ... }`',
                        'code_line': line
                    })
                    break
            
            # Check for unterminated strings
            if stripped.count('"') % 2 != 0 or stripped.count("'") % 2 != 0:
                errors.append({
                    'line': i,
                    'message': 'Syntax Error: Unterminated string literal',
                    'suggestion': 'Close string with matching quote (" or \')',
                    'code_line': line
                })
                break
        
        return errors
    
    @staticmethod
    def _check_generic_syntax(code: str) -> List[Dict]:
        """Generic syntax checking for unknown languages"""
        errors = []
        lines = code.split('\n')
        paren_stack = []
        brace_stack = []
        
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            
            if stripped.startswith(('//', '#', '/*', '--')):
                continue
            
            # Check for unmatched parentheses
            for char in line:
                if char == '(':
                    paren_stack.append(i)
                elif char == ')':
                    if paren_stack:
                        paren_stack.pop()
                    else:
                        errors.append({
                            'line': i,
                            'message': 'Syntax Error: Unmatched closing parenthesis )',
                            'suggestion': 'Check for matching parentheses',
                            'code_line': line
                        })
                        break
            
            # Check for unmatched braces
            for char in line:
                if char == '{':
                    brace_stack.append(i)
                elif char == '}':
                    if brace_stack:
                        brace_stack.pop()
                    else:
                        errors.append({
                            'line': i,
                            'message': 'Syntax Error: Unmatched closing brace }',
                            'suggestion': 'Check for matching braces',
                            'code_line': line
                        })
                        break
        
        if paren_stack:
            errors.append({
                'line': paren_stack[0],
                'message': 'Syntax Error: Unmatched opening parenthesis (',
                'suggestion': 'Add closing parenthesis )',
                'code_line': lines[paren_stack[0] - 1]
            })
        
        if brace_stack:
            errors.append({
                'line': brace_stack[0],
                'message': 'Syntax Error: Unmatched opening brace {',
                'suggestion': 'Add closing brace }',
                'code_line': lines[brace_stack[0] - 1]
            })
        
        return errors


# ============================================================
# INTELLIGENT TEST GENERATOR - Like ChatGPT
# ============================================================

class IntelligentTestGenerator:
    """
    AI-powered test case generator like ChatGPT
    Intelligently analyzes code and generates comprehensive test cases
    """
    
    @staticmethod
    def analyze_code_intelligently(code: str, language: str) -> Dict:
        """
        Deep analysis of code to understand its behavior
        Like ChatGPT's code understanding capability
        """
        analysis = {
            'functions': [],
            'classes': [],
            'imports': [],
            'complexity': 'simple',
            'has_input_validation': False,
            'has_error_handling': False,
            'has_print': False,
            'data_types': [],
            'edge_cases': [],
            'dependencies': [],
            'syntax_error': None
        }
        
        if language.lower() == 'python':
            try:
                tree = ast.parse(code)
                
                for node in ast.walk(tree):
                    # Detect functions
                    if isinstance(node, ast.FunctionDef):
                        func_info = {
                            'name': node.name,
                            'params': [arg.arg for arg in node.args.args if arg.arg != 'self'],
                            'has_return': False,
                            'has_try': False,
                            'has_validation': False,
                            'has_recursion': False,
                            'has_loop': False,
                            'complexity': 'low',
                            'infinite_loop_risk': False,
                            'line_numbers': []
                        }
                        
                        # Get line numbers
                        func_info['line_numbers'] = list(range(node.lineno, node.end_lineno + 1))
                        
                        # Analyze function body
                        for child in ast.walk(node):
                            if isinstance(child, ast.Return):
                                func_info['has_return'] = True
                            if isinstance(child, ast.Try):
                                func_info['has_try'] = True
                            if isinstance(child, ast.If):
                                if isinstance(child.test, ast.Compare):
                                    func_info['has_validation'] = True
                            if isinstance(child, ast.Call):
                                if isinstance(child.func, ast.Name):
                                    if child.func.id == 'print':
                                        analysis['has_print'] = True
                        
                        # Detect recursion
                        for child in ast.walk(node):
                            if isinstance(child, ast.Call):
                                if isinstance(child.func, ast.Name) and child.func.id == node.name:
                                    func_info['has_recursion'] = True
                        
                        # Detect loops and infinite loop risk
                        for child in ast.walk(node):
                            if isinstance(child, (ast.For, ast.While)):
                                func_info['has_loop'] = True
                                if isinstance(child, ast.While):
                                    has_increment = False
                                    for inner in ast.walk(child):
                                        if isinstance(inner, ast.AugAssign):
                                            has_increment = True
                                        elif isinstance(inner, ast.Assign):
                                            if isinstance(inner.targets[0], ast.Name):
                                                has_increment = True
                                    if not has_increment:
                                        func_info['infinite_loop_risk'] = True
                        
                        analysis['functions'].append(func_info)
                    
                    # Detect classes
                    elif isinstance(node, ast.ClassDef):
                        class_info = {
                            'name': node.name,
                            'methods': [],
                            'has_init': False,
                            'line_numbers': list(range(node.lineno, node.end_lineno + 1))
                        }
                        for method in node.body:
                            if isinstance(method, ast.FunctionDef):
                                class_info['methods'].append(method.name)
                                if method.name == '__init__':
                                    class_info['has_init'] = True
                        analysis['classes'].append(class_info)
                    
                    # Detect imports
                    elif isinstance(node, ast.Import):
                        for alias in node.names:
                            analysis['imports'].append(alias.name)
                    elif isinstance(node, ast.ImportFrom):
                        analysis['imports'].append(f"{node.module}.{node.names[0].name if node.names else ''}")
                
                # Determine complexity
                total_functions = len(analysis['functions'])
                if total_functions > 5:
                    analysis['complexity'] = 'high'
                elif total_functions > 2:
                    analysis['complexity'] = 'medium'
                
                # Check for error handling
                analysis['has_error_handling'] = any('try' in str(node) for node in ast.walk(tree))
                analysis['has_input_validation'] = any(
                    isinstance(node, ast.If) and isinstance(node.test, ast.Compare) 
                    for node in ast.walk(tree)
                )
                
            except SyntaxError as e:
                analysis['syntax_error'] = str(e)
        
        return analysis
    
    @staticmethod
    def generate_intelligent_test_cases(code: str, language: str, analysis: Dict) -> List[Dict]:
        """
        Generate test cases like ChatGPT would - intelligent and comprehensive
        """
        test_cases = []
        
        if language.lower() != 'python':
            return test_cases
        
        try:
            # Parse the code
            tree = ast.parse(code)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    func_tests = IntelligentTestGenerator._generate_function_tests(
                        node, code, analysis
                    )
                    test_cases.extend(func_tests)
                
                elif isinstance(node, ast.ClassDef):
                    for method in node.body:
                        if isinstance(method, ast.FunctionDef):
                            func_tests = IntelligentTestGenerator._generate_function_tests(
                                method, code, analysis, class_name=node.name
                            )
                            test_cases.extend(func_tests)
        
        except SyntaxError:
            # If code has syntax errors, generate basic tests
            test_cases = IntelligentTestGenerator._generate_basic_tests(code, language)
        
        return test_cases
    
    @staticmethod
    def _generate_function_tests(func_node: ast.FunctionDef, code: str, analysis: Dict, 
                                 class_name: Optional[str] = None) -> List[Dict]:
        """
        Generate intelligent test cases for a single function
        """
        tests = []
        func_name = func_node.name
        params = [arg.arg for arg in func_node.args.args if arg.arg not in ['self', 'cls']]
        
        # Skip private methods and built-ins
        if func_name.startswith('_') and func_name != '__init__':
            return tests
        
        # 1. Normal case test
        normal_input = IntelligentTestGenerator._generate_normal_inputs(params, code)
        tests.append({
            'name': f'test_{func_name}_normal',
            'function': func_name,
            'class': class_name,
            'input': normal_input,
            'expected': IntelligentTestGenerator._predict_output(
                func_name, normal_input, code, analysis
            ),
            'description': f'Test {func_name} with normal inputs',
            'test_code': IntelligentTestGenerator._generate_test_code(
                func_name, normal_input, class_name, 'normal'
            ),
            'category': 'normal'
        })
        
        # 2. Edge cases based on parameter types
        for param in params:
            # Test with None/null
            none_input = normal_input.copy()
            none_input[param] = 'None'
            tests.append({
                'name': f'test_{func_name}_null_{param}',
                'function': func_name,
                'class': class_name,
                'input': none_input,
                'expected': IntelligentTestGenerator._predict_output(
                    func_name, none_input, code, analysis
                ),
                'description': f'Test {func_name} with null {param}',
                'test_code': IntelligentTestGenerator._generate_test_code(
                    func_name, none_input, class_name, 'null'
                ),
                'category': 'edge_case'
            })
            
            # Test with empty values for string/list params
            if any(keyword in param.lower() for keyword in ['str', 'list', 'array', 'items', 'data']):
                empty_input = normal_input.copy()
                if 'list' in param.lower() or 'array' in param.lower() or 'items' in param.lower():
                    empty_input[param] = '[]'
                else:
                    empty_input[param] = "''"
                tests.append({
                    'name': f'test_{func_name}_empty_{param}',
                    'function': func_name,
                    'class': class_name,
                    'input': empty_input,
                    'expected': IntelligentTestGenerator._predict_output(
                        func_name, empty_input, code, analysis
                    ),
                    'description': f'Test {func_name} with empty {param}',
                    'test_code': IntelligentTestGenerator._generate_test_code(
                        func_name, empty_input, class_name, 'empty'
                    ),
                    'category': 'edge_case'
                })
            
            # Test with boundary values for numeric params
            if any(keyword in param.lower() for keyword in ['num', 'count', 'id', 'int', 'float', 'price']):
                # Test with 0
                zero_input = normal_input.copy()
                zero_input[param] = '0'
                tests.append({
                    'name': f'test_{func_name}_zero_{param}',
                    'function': func_name,
                    'class': class_name,
                    'input': zero_input,
                    'expected': IntelligentTestGenerator._predict_output(
                        func_name, zero_input, code, analysis
                    ),
                    'description': f'Test {func_name} with zero {param}',
                    'test_code': IntelligentTestGenerator._generate_test_code(
                        func_name, zero_input, class_name, 'boundary'
                    ),
                    'category': 'boundary'
                })
                
                # Test with negative
                neg_input = normal_input.copy()
                neg_input[param] = '-1'
                tests.append({
                    'name': f'test_{func_name}_negative_{param}',
                    'function': func_name,
                    'class': class_name,
                    'input': neg_input,
                    'expected': IntelligentTestGenerator._predict_output(
                        func_name, neg_input, code, analysis
                    ),
                    'description': f'Test {func_name} with negative {param}',
                    'test_code': IntelligentTestGenerator._generate_test_code(
                        func_name, neg_input, class_name, 'boundary'
                    ),
                    'category': 'boundary'
                })
                
                # Test with large number
                large_input = normal_input.copy()
                large_input[param] = '999999'
                tests.append({
                    'name': f'test_{func_name}_large_{param}',
                    'function': func_name,
                    'class': class_name,
                    'input': large_input,
                    'expected': IntelligentTestGenerator._predict_output(
                        func_name, large_input, code, analysis
                    ),
                    'description': f'Test {func_name} with large {param}',
                    'test_code': IntelligentTestGenerator._generate_test_code(
                        func_name, large_input, class_name, 'boundary'
                    ),
                    'category': 'boundary'
                })
        
        # 3. Special cases based on function analysis
        if func_node.name == '__init__':
            tests.append({
                'name': f'test_{func_name}_object_creation',
                'function': func_name,
                'class': class_name,
                'input': normal_input,
                'expected': f'{class_name} object created successfully',
                'description': f'Test {class_name} object creation',
                'test_code': IntelligentTestGenerator._generate_test_code(
                    func_name, normal_input, class_name, 'object_creation'
                ),
                'category': 'special'
            })
        
        # 4. Recursion test
        if any(isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == func_name 
               for node in ast.walk(func_node)):
            # Test with base case
            base_input = normal_input.copy()
            tests.append({
                'name': f'test_{func_name}_recursion_base',
                'function': func_name,
                'class': class_name,
                'input': base_input,
                'expected': 'Base case handled',
                'description': f'Test {func_name} recursion base case',
                'test_code': IntelligentTestGenerator._generate_test_code(
                    func_name, base_input, class_name, 'recursion'
                ),
                'category': 'special'
            })
        
        # 5. Loop test
        if any(isinstance(node, (ast.For, ast.While)) for node in ast.walk(func_node)):
            loop_input = normal_input.copy()
            tests.append({
                'name': f'test_{func_name}_loop',
                'function': func_name,
                'class': class_name,
                'input': loop_input,
                'expected': 'Loop processed successfully',
                'description': f'Test {func_name} loop functionality',
                'test_code': IntelligentTestGenerator._generate_test_code(
                    func_name, loop_input, class_name, 'loop'
                ),
                'category': 'special'
            })
        
        return tests
    
    @staticmethod
    def _generate_normal_inputs(params: List[str], code: str) -> Dict:
        """
        Generate intelligent normal inputs based on parameter names and context
        """
        inputs = {}
        
        # Context-aware input generation
        for param in params:
            param_lower = param.lower()
            
            # Check if code has type hints or context
            if 'name' in param_lower or 'username' in param_lower or 'filename' in param_lower:
                inputs[param] = "'test_value'"
            elif 'id' in param_lower or 'num' in param_lower or 'count' in param_lower:
                inputs[param] = '42'
            elif 'price' in param_lower or 'amount' in param_lower or 'total' in param_lower:
                inputs[param] = '100.50'
            elif 'email' in param_lower:
                inputs[param] = "'test@example.com'"
            elif 'url' in param_lower:
                inputs[param] = "'https://example.com/api'"
            elif 'data' in param_lower or 'dict' in param_lower or 'config' in param_lower:
                inputs[param] = "{'key': 'value'}"
            elif 'list' in param_lower or 'items' in param_lower or 'array' in param_lower:
                inputs[param] = '[1, 2, 3]'
            elif 'bool' in param_lower or 'flag' in param_lower or 'is_' in param_lower:
                inputs[param] = 'True'
            else:
                inputs[param] = '42'
        
        return inputs
    
    @staticmethod
    def _predict_output(func_name: str, inputs: Dict, code: str, analysis: Dict) -> str:
        """
        Intelligently predict expected output based on code analysis
        Like ChatGPT's prediction capability
        """
        # Try to find function implementation
        try:
            # Parse code to find function
            tree = ast.parse(code)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and node.name == func_name:
                    # Analyze return statements
                    returns = []
                    for child in ast.walk(node):
                        if isinstance(child, ast.Return):
                            if child.value:
                                if isinstance(child.value, ast.Constant):
                                    returns.append(str(child.value.value))
                                elif isinstance(child.value, ast.Name):
                                    returns.append(f"value of {child.value.id}")
                                elif isinstance(child.value, ast.BinOp):
                                    returns.append("calculated result")
                    
                    if returns:
                        return returns[0]
                    
                    # Check if it's a void function (no return)
                    has_return = any(isinstance(node, ast.Return) for node in ast.walk(node))
                    if not has_return:
                        return "None (void function)"
                    
                    # Check if it returns based on logic
                    has_if = any(isinstance(node, ast.If) for node in ast.walk(node))
                    if has_if:
                        return "Conditional output"
            
        except:
            pass
        
        # Default predictions based on function name
        func_lower = func_name.lower()
        if 'get' in func_lower or 'fetch' in func_lower or 'find' in func_lower:
            return "Data retrieved successfully"
        elif 'calculate' in func_lower or 'compute' in func_lower:
            return "Calculation result"
        elif 'process' in func_lower or 'handle' in func_lower:
            return "Data processed"
        elif 'create' in func_lower or 'add' in func_lower:
            return "Item added"
        elif 'delete' in func_lower or 'remove' in func_lower:
            return "Item removed"
        elif 'update' in func_lower or 'set' in func_lower:
            return "Item updated"
        else:
            return "Function executed successfully"
    
    @staticmethod
    def _generate_test_code(func_name: str, inputs: Dict, class_name: Optional[str], 
                           test_type: str) -> str:
        """
        Generate executable test code
        """
        if class_name:
            # Instance method test
            call_args = ', '.join([f"{k}={v}" for k, v in inputs.items() if k != 'self'])
            return f"""
def test_{func_name}_{test_type}():
    # Test {func_name} with inputs: {inputs}
    obj = {class_name}()
    result = obj.{func_name}({call_args})
    print(f"Result: {{result}}")
    # Assert expected behavior
    # assert result is not None

if __name__ == "__main__":
    test_{func_name}_{test_type}()
"""
        else:
            # Function test
            call_args = ', '.join([f"{k}={v}" for k, v in inputs.items()])
            return f"""
def test_{func_name}_{test_type}():
    # Test {func_name} with inputs: {inputs}
    result = {func_name}({call_args})
    print(f"Result: {{result}}")
    # Assert expected behavior
    # assert result is not None

if __name__ == "__main__":
    test_{func_name}_{test_type}()
"""
    
    @staticmethod
    def _generate_basic_tests(code: str, language: str) -> List[Dict]:
        """
        Generate basic tests if intelligent analysis fails
        """
        test_cases = []
        
        # Extract function names using regex
        func_matches = re.findall(r'def\s+(\w+)\s*\(', code)
        
        for func_name in func_matches:
            test_cases.append({
                'name': f'test_{func_name}_basic',
                'function': func_name,
                'class': None,
                'input': {'arg': 'test_value'},
                'expected': 'Function executed',
                'description': f'Basic test for {func_name}',
                'test_code': f"""
def test_{func_name}_basic():
    # Basic test for {func_name}
    result = {func_name}(test_value)
    print(f"Result: {{result}}")
    
if __name__ == "__main__":
    test_{func_name}_basic()
""",
                'category': 'basic'
            })
        
        return test_cases


# ============================================================
# TEST EXECUTOR - Actually runs the tests
# ============================================================

class TestExecutor:
    """
    Executes test cases in a sandboxed environment
    Like ChatGPT's test execution capability
    """
    
    @staticmethod
    def execute_test_cases(code: str, test_cases: List[Dict]) -> List[Dict]:
        """
        Execute test cases and return results
        """
        results = []
        logger.info(f"🔬 Executing {len(test_cases)} test cases...")
        
        for test_case in test_cases:
            result = TestExecutor._execute_single_test(code, test_case)
            results.append(result)
        
        return results
    
    @staticmethod
    def _execute_single_test(code: str, test_case: Dict) -> Dict:
        """
        Execute a single test case in a sandbox
        """
        test_code = test_case.get('test_code', '')
        func_name = test_case.get('function', '')
        
        # Create execution environment
        exec_globals = {}
        exec_locals = {}
        
        # Prepare test script
        test_script = code + "\n\n" + test_code
        
        # Execute in sandbox
        start_time = time.time()
        passed = False
        output = ""
        error = None
        execution_time = 0
        
        try:
            # Use subprocess for isolation
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(test_script)
                f.flush()
                temp_file = f.name
            
            # Run with timeout
            result = subprocess.run(
                ['python', temp_file],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            execution_time = time.time() - start_time
            output = result.stdout
            
            if result.returncode == 0:
                passed = True
            else:
                error = result.stderr
            
            # Cleanup
            os.unlink(temp_file)
            
        except subprocess.TimeoutExpired:
            error = "Test execution timed out (10 seconds)"
            execution_time = 10
        except Exception as e:
            error = str(e)
            execution_time = time.time() - start_time
        
        # Determine if test case should pass based on actual execution
        # and heuristic checks
        should_pass = TestExecutor._should_pass(test_case, output, error)
        
        return {
            'name': test_case.get('name', 'test'),
            'function': func_name,
            'input': test_case.get('input', {}),
            'expected': test_case.get('expected', 'N/A'),
            'actual': output if not error else error,
            'passed': passed and should_pass,
            'execution_time': round(execution_time, 3),
            'output': output[:500] if output else '',
            'error': error,
            'test_code': test_code,
            'category': test_case.get('category', 'general')
        }
    
    @staticmethod
    def _should_pass(test_case: Dict, output: str, error: str) -> bool:
        """
        Determine if test case should pass
        """
        # If there's an error, it fails
        if error:
            return False
        
        # Check if output contains expected result
        expected = test_case.get('expected', '')
        if expected and expected not in output and expected != 'N/A':
            # Special cases
            if 'None' in expected and 'None' in output:
                return True
            if 'Function executed' in expected:
                return True
            if 'successfully' in expected and ('success' in output.lower() or 'true' in output.lower()):
                return True
            return False
        
        # Check for specific outputs based on function type
        func_name = test_case.get('function', '').lower()
        category = test_case.get('category', '')
        
        if 'get' in func_name or 'fetch' in func_name:
            return 'data' in output.lower() or 'result' in output.lower() or 'none' not in output.lower()
        elif 'calculate' in func_name:
            return any(char.isdigit() for char in output) and 'none' not in output.lower()
        elif 'process' in func_name or 'handle' in func_name:
            return 'processed' in output.lower() or 'handled' in output.lower() or 'true' in output.lower()
        elif 'add' in func_name or 'create' in func_name:
            return 'added' in output.lower() or 'created' in output.lower()
        elif 'delete' in func_name or 'remove' in func_name:
            return 'removed' in output.lower() or 'deleted' in output.lower()
        elif 'update' in func_name:
            return 'updated' in output.lower()
        elif 'validate' in func_name:
            return 'valid' in output.lower() or 'invalid' in output.lower()
        
        return True


# ============================================================
# LANGUAGE DETECTION
# ============================================================

def detect_programming_language(code):
    """Auto-detect programming language from code content - 25+ languages!"""
    if not code or not code.strip():
        return 'python'
    
    code_lower = code.lower()
    code_upper = code.upper()
    first_line = code.split('\n')[0] if code else ''
    
    # 1. Shebang detection
    if first_line.startswith('#!'):
        if 'python' in first_line:
            return 'python'
        if 'node' in first_line:
            return 'javascript'
        if 'ruby' in first_line:
            return 'ruby'
        if 'perl' in first_line:
            return 'perl'
        if 'bash' in first_line or 'sh' in first_line:
            return 'shell'
        if 'php' in first_line:
            return 'php'
    
    # 2. RUST
    rust_score = 0
    if 'fn ' in code and '->' in code:
        rust_score += 30
    if 'println!' in code:
        rust_score += 25
    if 'use std::' in code:
        rust_score += 30
    if 'let mut' in code:
        rust_score += 20
    if 'unwrap()' in code:
        rust_score += 15
    if 'match ' in code and '=>' in code:
        rust_score += 20
    if 'unsafe {' in code:
        rust_score += 15
    if 'loop {' in code:
        rust_score += 15
    if 'Option<' in code or 'Result<' in code:
        rust_score += 20
    if '&str' in code:
        rust_score += 15
    if 'Vec<' in code:
        rust_score += 10
    if '::' in code and 'std::' not in code:
        rust_score += 5
    if ';' in code and 'println!' in code:
        rust_score += 5
    
    if rust_score >= 20:
        return 'rust'
    
    # 3. C#
    csharp_score = 0
    if 'using System' in code:
        csharp_score += 30
    if 'namespace ' in code and '{' in code:
        csharp_score += 25
    if 'Console.WriteLine' in code or 'Console.Write' in code:
        csharp_score += 25
    if 'class ' in code and ':' in code:
        csharp_score += 15
    if 'private const string' in code:
        csharp_score += 15
    if 'using System.Collections.Generic' in code:
        csharp_score += 20
    if 'List<' in code:
        csharp_score += 10
    if 'GC.Collect' in code:
        csharp_score += 10
    if 'SqlCommand' in code:
        csharp_score += 15
    
    if csharp_score >= 20:
        return 'csharp'
    
    # 4. JAVA
    java_score = 0
    if 'public class' in code and '{' in code:
        java_score += 25
    if 'public static void main' in code:
        java_score += 30
    if 'System.out.println' in code or 'System.out.print' in code:
        java_score += 25
    if 'import java.' in code:
        java_score += 30
    if 'extends ' in code or 'implements ' in code:
        java_score += 15
    if '@Override' in code or '@Test' in code:
        java_score += 15
    if 'private ' in code and 'public ' in code and 'protected ' in code:
        java_score += 10
    if 'String[]' in code and 'String args' in code:
        java_score += 15
    if 'throws ' in code:
        java_score += 10
    if 'synchronized ' in code:
        java_score += 10
    if 'final ' in code and 'static ' in code:
        java_score += 10
    if 'catch (Exception' in code:
        java_score += 10
    
    if java_score >= 20:
        return 'java'
    
    # 5. TYPESCRIPT
    ts_score = 0
    if 'interface ' in code and 'export' not in code:
        if 'public interface' not in code:
            ts_score += 25
    if 'type ' in code and '=' in code and '|' in code:
        ts_score += 25
    if ': string' in code or ': number' in code or ': boolean' in code:
        ts_score += 20
    if 'as ' in code and 'as any' not in code:
        ts_score += 15
    if '<T>' in code or '<T extends' in code:
        ts_score += 20
    if 'export interface' in code or 'export type' in code:
        ts_score += 25
    if 'readonly ' in code:
        ts_score += 10
    if '?.' in code:
        ts_score += 5
    if '??' in code:
        ts_score += 5
    
    if ts_score >= 20 and 'System.out' not in code and 'public class' not in code and 'using System' not in code and 'fn ' not in code:
        return 'typescript'
    
    # 6. JAVASCRIPT
    js_count = 0
    if 'import React' in code:
        return 'javascript'
    if 'export default' in code:
        js_count += 10
    if 'useState' in code or 'useEffect' in code:
        return 'javascript'
    if '<div' in code and '</div>' in code:
        return 'javascript'
    if 'props.' in code or 'state.' in code:
        return 'javascript'
    if 'function ' in code and '(' in code:
        js_count += 1
    if 'const ' in code or 'let ' in code or 'var ' in code:
        js_count += 1
    if 'console.log' in code:
        js_count += 1
    if '=>' in code:
        js_count += 1
    if 'document.' in code or 'window.' in code:
        js_count += 1
    if 'JSON.parse' in code or 'JSON.stringify' in code:
        js_count += 1
    if 'setInterval' in code or 'setTimeout' in code:
        js_count += 1
    if '.innerHTML' in code:
        js_count += 1
    if 'document.write' in code:
        js_count += 1
    
    if js_count >= 2:
        return 'javascript'
    
    # 7. GO
    go_score = 0
    if 'package ' in code and 'func ' in code:
        go_score += 30
    if 'fmt.Println' in code or 'fmt.Printf' in code:
        go_score += 25
    if 'import (' in code:
        go_score += 15
    if ':= ' in code:
        go_score += 10
    if 'defer' in code:
        go_score += 10
    if 'go ' in code and 'func' in code:
        go_score += 10
    if 'chan ' in code or 'make(chan' in code:
        go_score += 10
    if 'error' in code and 'err' in code:
        go_score += 10
    
    if go_score >= 20:
        return 'go'
    
    # 8. C++
    cpp_score = 0
    if 'std::' in code:
        cpp_score += 25
    if 'cout' in code or 'cin' in code:
        cpp_score += 20
    if 'using namespace std;' in code:
        cpp_score += 20
    if '#include <iostream>' in code:
        cpp_score += 25
    if 'class ' in code and 'public:' in code:
        cpp_score += 15
    if 'template' in code:
        cpp_score += 15
    if 'virtual ' in code:
        cpp_score += 15
    if 'override' in code:
        cpp_score += 15
    if 'nullptr' in code:
        cpp_score += 15
    if 'public:' in code or 'private:' in code:
        cpp_score += 10
    
    if cpp_score >= 10:
        return 'cpp'
    
    # 9. C
    c_score = 0
    if '#include' in code and ('printf' in code or 'scanf' in code):
        c_score += 15
    if '#include <stdio.h>' in code:
        c_score += 15
    if 'malloc(' in code or 'free(' in code:
        c_score += 10
    if 'int main(' in code:
        c_score += 10
    if 'struct ' in code and ';' in code:
        c_score += 5
    
    if c_score >= 10:
        return 'c'
    
    # 10. PYTHON
    python_score = 0
    if 'def ' in code and ':' in code:
        python_score += 10
    if 'class ' in code and ':' in code:
        python_score += 10
    if 'if __name__' in code:
        python_score += 25
    if 'print(' in code:
        python_score += 10
    if 'import ' in code and 'from ' not in code:
        python_score += 5
    if 'from ' in code and 'import ' in code:
        python_score += 5
    if 'self.' in code:
        python_score += 10
    if '__init__' in code or '__str__' in code:
        python_score += 10
    if 'django' in code:
        python_score += 15
    if 'except ' in code:
        python_score += 10
    if 'with ' in code and 'as ' in code:
        python_score += 5
    if 'elif ' in code:
        python_score += 5
    
    if python_score >= 8 and 'cout' not in code and 'System.out' not in code and 'public class' not in code and 'using System' not in code and 'fn ' not in code:
        return 'python'
    
    # 11. RUBY
    ruby_score = 0
    if 'def ' in code and 'end' in code:
        ruby_score += 10
    if 'attr_accessor' in code:
        ruby_score += 20
    if 'puts ' in code:
        ruby_score += 10
    if 'require ' in code:
        ruby_score += 5
    if 'class ' in code and 'end' in code:
        ruby_score += 5
    if 'module ' in code and 'end' in code:
        ruby_score += 10
    if '.each' in code:
        ruby_score += 5
    
    if ruby_score >= 10:
        return 'ruby'
    
    # 12. PHP
    if '<?php' in code:
        return 'php'
    if '$' in code and 'echo' in code:
        return 'php'
    
    # 13. SWIFT
    if 'import UIKit' in code or 'import Foundation' in code:
        return 'swift'
    if 'func ' in code and '->' in code:
        return 'swift'
    
    # 14. KOTLIN
    if 'fun ' in code and 'var ' in code:
        return 'kotlin'
    if 'val ' in code:
        return 'kotlin'
    
    # 15. HASKELL
    if 'module ' in code and '::' in code:
        return 'haskell'
    if '->' in code and '::' in code:
        return 'haskell'
    
    # 16. JULIA
    if 'function ' in code and 'end' in code:
        return 'julia'
    if 'println(' in code and 'end' in code:
        return 'julia'
    
    # 17. SQL
    if 'SELECT ' in code_upper or 'INSERT ' in code_upper:
        return 'sql'
    if 'FROM ' in code_upper or 'WHERE ' in code_upper:
        return 'sql'
    
    # 18. HTML
    if '<!DOCTYPE html>' in code or '<html>' in code:
        return 'html'
    if '<body>' in code or '<head>' in code:
        return 'html'
    
    # 19. CSS
    if 'color:' in code or 'margin:' in code:
        return 'css'
    if 'padding:' in code or 'display:' in code:
        return 'css'
    
    # 20. SHELL
    if '#!/bin/bash' in code or '#!/bin/sh' in code:
        return 'shell'
    if 'echo ' in code and '$' in code:
        return 'shell'
    
    return 'python'


# ============================================================
# LANGUAGE MAPPING
# ============================================================

LANGUAGE_MAPPING = {
    'python': 'Python',
    'javascript': 'JavaScript',
    'js': 'JavaScript',
    'typescript': 'TypeScript',
    'ts': 'TypeScript',
    'java': 'Java',
    'c': 'C',
    'cpp': 'C++',
    'c++': 'C++',
    'csharp': 'C#',
    'c#': 'C#',
    'go': 'Go',
    'golang': 'Go',
    'rust': 'Rust',
    'ruby': 'Ruby',
    'php': 'PHP',
    'html': 'HTML',
    'css': 'CSS',
    'sql': 'SQL',
    'swift': 'Swift',
    'kotlin': 'Kotlin',
    'haskell': 'Haskell',
    'hs': 'Haskell',
    'julia': 'Julia',
    'shell': 'Shell',
    'bash': 'Shell',
    'perl': 'Perl',
    'r': 'R',
    'scala': 'Scala',
    'dart': 'Dart',
    'elixir': 'Elixir',
    'lua': 'Lua',
}


# ============================================================
# VIEWS
# ============================================================

class ProgrammingLanguageListView(generics.ListAPIView):
    queryset = ProgrammingLanguage.objects.filter(is_active=True)
    serializer_class = ProgrammingLanguageSerializer
    permission_classes = [permissions.AllowAny]


class CodeSubmissionListView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CodeSubmissionCreateSerializer
        return CodeSubmissionSerializer
    
    def get_queryset(self):
        user = self.request.user
        if getattr(user, 'user_type', None) == 'admin':
            return CodeSubmission.objects.all().order_by('-created_at')
        return CodeSubmission.objects.filter(user=user).order_by('-created_at')
    
    def create(self, request, *args, **kwargs):
        logger.info("=== CREATE SUBMISSION ===")
        
        code = request.data.get('code', '')
        detected_lang = detect_programming_language(code)
        detected_lang_name = LANGUAGE_MAPPING.get(detected_lang, 'Python')
        logger.info(f"Auto-detected language: {detected_lang_name}")

        lang_obj = ProgrammingLanguage.objects.filter(name__iexact=detected_lang_name).first()
        if not lang_obj:
            lang_obj = ProgrammingLanguage.objects.create(
                name=detected_lang_name,
                is_active=True
            )
        
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            logger.info("Serializer valid")
            submission = serializer.save(language=lang_obj)
            logger.info(f"Submission created with ID: {submission.id}")
            
            response_data = CodeSubmissionSerializer(submission).data
            headers = self.get_success_headers(serializer.data)
            return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            logger.error(f"Serializer errors: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CodeSubmissionDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CodeSubmissionSerializer
    
    def get_queryset(self):
        user = self.request.user
        if getattr(user, 'user_type', None) == 'admin':
            return CodeSubmission.objects.all()
        return CodeSubmission.objects.filter(user=user)


class CodeSubmissionStatusView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def patch(self, request, pk):
        submission = get_object_or_404(CodeSubmission, pk=pk)
        
        if getattr(request.user, 'user_type', None) != 'admin' and submission.user != request.user:
            return Response({
                'status': 'error',
                'message': 'You do not have permission to update this submission'
            }, status=status.HTTP_403_FORBIDDEN)
        
        status_value = request.data.get('status')
        if status_value not in ['pending', 'processing', 'completed', 'failed']:
            return Response({
                'status': 'error',
                'message': 'Invalid status'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        submission.status = status_value
        if status_value == 'completed':
            submission.reviewed_at = timezone.now()
        submission.save()
        
        return Response({
            'status': 'success',
            'message': 'Status updated successfully',
            'data': CodeSubmissionSerializer(submission).data
        }, status=status.HTTP_200_OK)


class ReviewHistoryListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ReviewHistorySerializer
    
    def get_queryset(self):
        user = self.request.user
        if getattr(user, 'user_type', None) == 'admin':
            return ReviewHistory.objects.all()
        return ReviewHistory.objects.filter(user=user)


class ReviewHistoryDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ReviewHistorySerializer
    
    def get_queryset(self):
        user = self.request.user
        if getattr(user, 'user_type', None) == 'admin':
            return ReviewHistory.objects.all()
        return ReviewHistory.objects.filter(user=user)


class CodeReviewCommentView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CodeReviewCommentSerializer
    
    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        return CodeReviewComment.objects.filter(review_id=review_id)
    
    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(ReviewHistory, pk=review_id)
        serializer.save(user=self.request.user, review=review)


class CodeSnippetView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CodeSnippetSerializer
    
    def get_queryset(self):
        user = self.request.user
        return CodeSnippet.objects.filter(
            Q(user=user) | Q(is_public=True)
        ).distinct()
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CodeSnippetDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CodeSnippetSerializer
    
    def get_queryset(self):
        user = self.request.user
        return CodeSnippet.objects.filter(user=user)


# ============================================================
# CODE REVIEW STATS VIEW
# ============================================================

class CodeReviewStatsView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        user = request.user
        logger.info(f"=== GETTING STATS FOR USER: {user.username} ===")
        
        try:
            submissions = CodeSubmission.objects.filter(user=user)
            
            total = submissions.count()
            completed = submissions.filter(status='completed').count()
            pending = submissions.filter(status='pending').count()
            
            avg_result = submissions.filter(status='completed').aggregate(avg=Avg('quality_score'))
            avg_score = avg_result['avg'] or 0
            
            total_bugs = submissions.aggregate(Sum('bug_count'))['bug_count__sum'] or 0
            total_issues = submissions.aggregate(Sum('issue_count'))['issue_count__sum'] or 0
            total_suggestions = submissions.aggregate(Sum('suggestion_count'))['suggestion_count__sum'] or 0
            
            language_stats = {}
            for lang in ProgrammingLanguage.objects.all():
                count = submissions.filter(language=lang).count()
                if count > 0:
                    language_stats[lang.name] = count
            
            recent = submissions.order_by('-created_at')[:5]
            recent_data = []
            for sub in recent:
                recent_data.append({
                    'id': str(sub.id),
                    'title': sub.title or 'Untitled',
                    'status': sub.status,
                    'created_at': sub.created_at.isoformat(),
                    'language': sub.language.name if sub.language else 'Unknown',
                    'quality_score': sub.quality_score or 0,
                    'bug_count': sub.bug_count or 0,
                    'issue_count': sub.issue_count or 0,
                    'suggestion_count': sub.suggestion_count or 0
                })
            
            stats = {
                'total_submissions': total,
                'completed_reviews': completed,
                'pending_reviews': pending,
                'average_quality_score': round(avg_score, 1),
                'total_bugs_found': total_bugs,
                'total_issues_found': total_issues,
                'total_suggestions': total_suggestions,
                'language_breakdown': language_stats,
                'recent_activity': recent_data
            }
            
            logger.info(f"✅ Stats: total={total}, completed={completed}, bugs={total_bugs}, score={avg_score}")
            
            return Response({
                'status': 'success',
                'data': stats
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"❌ Error in stats: {str(e)}")
            return Response({
                'status': 'error',
                'message': str(e),
                'data': {
                    'total_submissions': 0,
                    'completed_reviews': 0,
                    'pending_reviews': 0,
                    'average_quality_score': 0,
                    'total_bugs_found': 0,
                    'total_issues_found': 0,
                    'total_suggestions': 0,
                    'language_breakdown': {},
                    'recent_activity': []
                }
            }, status=status.HTTP_200_OK)


# ============================================================
# ENHANCED AI REVIEW VIEW WITH TEST GENERATION & EXECUTION
# ============================================================

class InitiateCodeReviewView(APIView):
    """
    Initiate AI code review - DYNAMIC CODE ANALYSIS ENGINE!
    With ChatGPT-like intelligent test case generation and execution!
    SYNTAX ERROR DETECTION FOR ALL LANGUAGES!
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        submission_id = request.data.get('submission_id')
        logger.info(f"Initiate review for submission: {submission_id}")
        
        if not submission_id:
            return Response({
                'status': 'error',
                'message': 'submission_id is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            submission = CodeSubmission.objects.get(
                id=submission_id, 
                user=request.user
            )
            logger.info(f"Found submission: {submission.id} - {submission.title}")
            
            detected_lang = detect_programming_language(submission.code)
            detected_lang_name = LANGUAGE_MAPPING.get(detected_lang, 'Python')
            
            lang_obj, created = ProgrammingLanguage.objects.get_or_create(
                name=detected_lang_name,
                defaults={'is_active': True}
            )
            submission.language = lang_obj
            submission.save()
            
            logger.info(f"Executing review for language: {submission.language.name}")
        except CodeSubmission.DoesNotExist:
            logger.error(f"Submission {submission_id} not found")
            return Response({
                'status': 'error',
                'message': 'Submission not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error: {str(e)}")
            return Response({
                'status': 'error',
                'message': f'Error: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        submission.status = 'processing'
        submission.save()
        
        try:
            # Step 1: Check for syntax errors FIRST
            logger.info("🔍 Checking for syntax errors...")
            syntax_errors = SyntaxErrorDetector.detect_syntax_errors(
                submission.code, 
                submission.language.name
            )
            
            if syntax_errors:
                logger.warning(f"⚠️ Found {len(syntax_errors)} syntax errors")
                for error in syntax_errors:
                    logger.error(f"Syntax error at line {error.get('line', 1)}: {error.get('message', 'Unknown error')}")
            
            # Step 2: Analyze code
            analysis_result = self._analyze_code(
                code=submission.code, 
                language=submission.language.name,
                syntax_errors=syntax_errors
            )
            logger.info(f"Analysis result: score={analysis_result['quality_score']}, bugs={len(analysis_result['bugs'])}")
            
            # Step 3: Generate intelligent test cases
            logger.info("🧠 Generating intelligent test cases...")
            test_cases = self._generate_intelligent_tests(
                code=submission.code,
                language=submission.language.name,
                analysis=analysis_result
            )
            logger.info(f"✅ Generated {len(test_cases)} intelligent test cases")
            
            # Step 4: Execute test cases (skip if syntax errors)
            if syntax_errors:
                logger.warning("⚠️ Skipping test execution due to syntax errors")
                test_results = []
                for tc in test_cases:
                    test_results.append({
                        'name': tc.get('name', 'test'),
                        'function': tc.get('function', ''),
                        'input': tc.get('input', {}),
                        'expected': tc.get('expected', 'N/A'),
                        'actual': 'Syntax Error - Cannot execute',
                        'passed': False,
                        'execution_time': 0,
                        'output': '',
                        'error': 'Code contains syntax errors',
                        'test_code': tc.get('test_code', ''),
                        'category': tc.get('category', 'general')
                    })
            else:
                logger.info("🔬 Executing test cases...")
                test_results = self._execute_tests(
                    code=submission.code,
                    test_cases=test_cases
                )
                logger.info(f"✅ Test execution complete: {len([t for t in test_results if t['passed']])} passed, {len([t for t in test_results if not t['passed']])} failed")
            
        except Exception as e:
            logger.error(f"❌ Analysis failed: {str(e)}")
            logger.error(traceback.format_exc())
            submission.status = 'failed'
            submission.save()
            return Response({
                'status': 'error',
                'message': f'Analysis failed: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Create review with all data
        review = ReviewHistory.objects.create(
            submission=submission,
            user=request.user,
            quality_score=analysis_result['quality_score'],
            bugs=analysis_result['bugs'],
            issues=analysis_result['issues'],
            suggestions=analysis_result['suggestions'],
            explanation=analysis_result['explanation'],
            test_cases=test_results,
            ai_provider='intelligent_analysis',
            ai_model='chatgpt-like',
            ai_response={
                'status': 'success',
                'analysis': analysis_result,
                'test_cases': test_results,
                'syntax_errors': syntax_errors
            }
        )
        
        submission.status = 'completed'
        submission.quality_score = analysis_result['quality_score']
        submission.bug_count = len(analysis_result['bugs'])
        submission.issue_count = len(analysis_result['issues'])
        submission.suggestion_count = len(analysis_result['suggestions'])
        submission.reviewed_at = timezone.now()
        submission.analysis_result = {
            'bugs': analysis_result['bugs'],
            'issues': analysis_result['issues'],
            'suggestions': analysis_result['suggestions'],
            'explanation': analysis_result['explanation'],
            'test_cases': test_results,
            'quality_score': analysis_result['quality_score'],
            'syntax_errors': syntax_errors,
            'test_summary': {
                'total': len(test_results),
                'passed': len([t for t in test_results if t['passed']]),
                'failed': len([t for t in test_results if not t['passed']]),
                'execution_time': sum(t.get('execution_time', 0) for t in test_results)
            }
        }
        submission.save()
        
        return Response({
            'status': 'success',
            'message': 'Code review completed successfully with intelligent test cases!',
            'submission_id': str(submission.id),
            'review_id': str(review.id),
            'quality_score': analysis_result['quality_score'],
            'analysis': analysis_result,
            'language_detected': submission.language.name,
            'syntax_errors': syntax_errors,
            'has_syntax_errors': len(syntax_errors) > 0,
            'test_summary': {
                'total': len(test_results),
                'passed': len([t for t in test_results if t['passed']]),
                'failed': len([t for t in test_results if not t['passed']]),
            },
            'test_results': test_results[:20]
        }, status=status.HTTP_200_OK)
    
    def _generate_intelligent_tests(self, code: str, language: str, analysis: Dict) -> List[Dict]:
        """
        Generate intelligent test cases like ChatGPT
        """
        code_analysis = IntelligentTestGenerator.analyze_code_intelligently(code, language)
        test_cases = IntelligentTestGenerator.generate_intelligent_test_cases(
            code, language, code_analysis
        )
        return test_cases
    
    def _execute_tests(self, code: str, test_cases: List[Dict]) -> List[Dict]:
        """
        Execute test cases and return results
        """
        return TestExecutor.execute_test_cases(code, test_cases)
    
    # ============================================================
    # MAIN ANALYSIS - Enhanced with intelligent detection
    # ============================================================
    
    def _analyze_code(self, code, language, syntax_errors=None):
        """Dynamic analysis - works for ANY language!"""
        bugs = []
        issues = []
        suggestions = []
        
        lang = language.lower().strip()
        display_lang = LANGUAGE_MAPPING.get(lang, language)
        logger.info(f"🔍 Analyzing {display_lang} code...")
        
        code_lines = code.split('\n')
        
        # Add syntax errors as bugs
        if syntax_errors:
            for error in syntax_errors:
                bugs.append({
                    'line': error.get('line', 1),
                    'description': error.get('message', 'Unknown syntax error'),
                    'severity': 'critical',
                    'suggestion': error.get('suggestion', 'Fix the syntax error in your code')
                })
        
        if not code or len(code.strip()) == 0:
            return {
                'quality_score': 0,
                'bugs': bugs if bugs else [],
                'issues': [],
                'suggestions': [{
                    'line': 1,
                    'title': '📝 No Code Provided',
                    'description': 'Your submission is empty.'
                }],
                'explanation': 'No code to analyze.',
                'test_cases': []
            }
        
        # Use the enhanced analyzers with deduplication
        if lang in ['python']:
            b, i, s = self._analyze_python(code_lines)
        elif lang in ['rust']:
            b, i, s = self._analyze_rust(code_lines)
        elif lang in ['cpp', 'c++']:
            b, i, s = self._analyze_cpp(code_lines)
        elif lang in ['c']:
            b, i, s = self._analyze_c(code_lines)
        elif lang in ['javascript', 'js']:
            b, i, s = self._analyze_javascript(code_lines)
        elif lang in ['typescript', 'ts']:
            b, i, s = self._analyze_typescript(code_lines)
        elif lang in ['java']:
            b, i, s = self._analyze_java(code_lines)
        elif lang in ['csharp', 'c#']:
            b, i, s = self._analyze_csharp(code_lines)
        elif lang in ['go']:
            b, i, s = self._analyze_go(code_lines)
        elif lang in ['ruby']:
            b, i, s = self._analyze_ruby(code_lines)
        elif lang in ['php']:
            b, i, s = self._analyze_php(code_lines)
        elif lang in ['sql']:
            b, i, s = self._analyze_sql(code_lines)
        elif lang in ['haskell']:
            b, i, s = self._analyze_haskell(code_lines)
        elif lang in ['swift']:
            b, i, s = self._analyze_swift(code_lines)
        elif lang in ['kotlin']:
            b, i, s = self._analyze_kotlin(code_lines)
        elif lang in ['julia']:
            b, i, s = self._analyze_julia(code_lines)
        elif lang in ['html', 'css']:
            b, i, s = self._analyze_html_css(code_lines)
        elif lang in ['shell']:
            b, i, s = self._analyze_shell(code_lines)
        else:
            b, i, s = self._analyze_universal(code_lines)
        
        # Merge with syntax errors (avoid duplicates)
        bugs.extend(b)
        
        # Calculate quality score - syntax errors penalize heavily
        penalty = 0
        for bug in bugs:
            sev = bug.get('severity', 'critical')
            penalty += 15 if sev == 'critical' else 10 if sev == 'high' else 5
        for issue in issues:
            sev = issue.get('severity', 'medium')
            penalty += 6 if sev == 'high' else 4 if sev == 'medium' else 2
        
        quality_score = max(20, min(100, 100 - penalty))

        explanation = (
            f"Static Analysis & Debugger Report for {display_lang}:\n\n"
            f"📊 Quality Score: {quality_score}%\n"
            f"🐛 Bugs Found: {len(bugs)}\n"
            f"⚠️ Issues Identified: {len(issues)}\n"
            f"💡 Suggestions Generated: {len(suggestions)}"
        )

        return {
            'quality_score': quality_score,
            'bugs': bugs,
            'issues': issues,
            'suggestions': suggestions,
            'explanation': explanation,
            'test_cases': []
        }

    # ============================================================
    # PYTHON ANALYZER
    # ============================================================
    
    def _analyze_python(self, code_lines):
        bugs = []
        issues = []
        suggestions = []
        found_bugs = set()
        found_issues = set()
        found_suggestions = set()
        
        for i, line in enumerate(code_lines, 1):
            stripped = line.strip()
            if not stripped or stripped.startswith('#'):
                continue
            
            # Hardcoded credentials
            hardcoded_patterns = [
                (r'API_KEY\s*=\s*["\']([^"\']+)["\']', 'API Key'),
                (r'API_SECRET\s*=\s*["\']([^"\']+)["\']', 'API Secret'),
                (r'PASSWORD\s*=\s*["\']([^"\']+)["\']', 'Password'),
                (r'SECRET_KEY\s*=\s*["\']([^"\']+)["\']', 'Secret Key'),
                (r'SECRET_TOKEN\s*=\s*["\']([^"\']+)["\']', 'Secret Token'),
                (r'AWS_ACCESS_KEY\s*=\s*["\']([^"\']+)["\']', 'AWS Access Key'),
                (r'AWS_SECRET_KEY\s*=\s*["\']([^"\']+)["\']', 'AWS Secret Key'),
                (r'DATABASE_PASSWORD\s*=\s*["\']([^"\']+)["\']', 'Database Password'),
            ]
            
            for pattern, desc in hardcoded_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    var_match = re.search(r'([a-zA-Z_][a-zA-Z0-9_]*)\s*=', line)
                    var_name = var_match.group(1) if var_match else 'variable'
                    bug_key = f"hardcoded_{var_name}_{i}"
                    if bug_key not in found_bugs:
                        bugs.append({
                            'line': i,
                            'description': f'Hardcoded {desc} in `{var_name}`',
                            'severity': 'critical',
                            'suggestion': f'Use environment variables: `os.getenv("{var_name}")`'
                        })
                        found_bugs.add(bug_key)
                    break
            
            # Division by zero
            if '/' in line and not '//' in line:
                if '/0' in line or '/ 0' in line:
                    bug_key = f"div_zero_{i}"
                    if bug_key not in found_bugs:
                        bugs.append({
                            'line': i,
                            'description': 'Division by zero detected',
                            'severity': 'critical',
                            'suggestion': 'Add validation: `if denominator != 0:` before division'
                        })
                        found_bugs.add(bug_key)
                
                if 'len(' in line and '/' in line:
                    bug_key = f"div_len_{i}"
                    if bug_key not in found_bugs:
                        bugs.append({
                            'line': i,
                            'description': 'Division by len() without checking if list is empty',
                            'severity': 'critical',
                            'suggestion': 'Check if list is not empty before division'
                        })
                        found_bugs.add(bug_key)
            
            # eval()
            if 'eval(' in line and not 'ast.literal_eval' in line:
                bug_key = f"eval_{i}"
                if bug_key not in found_bugs:
                    bugs.append({
                        'line': i,
                        'description': 'Dangerous eval() detected - can execute arbitrary code',
                        'severity': 'critical',
                        'suggestion': 'Use `ast.literal_eval()` for safe evaluation'
                    })
                    found_bugs.add(bug_key)
            
            # SQL Injection
            if 'SELECT' in line.upper() or 'INSERT' in line.upper() or 'UPDATE' in line.upper():
                if '+' in line and ('"' in line or "'" in line):
                    bug_key = f"sql_injection_{i}"
                    if bug_key not in found_bugs:
                        bugs.append({
                            'line': i,
                            'description': 'SQL Injection vulnerability - string concatenation in query',
                            'severity': 'critical',
                            'suggestion': 'Use parameterized queries or ORM'
                        })
                        found_bugs.add(bug_key)
            
            # Resource leaks
            if 'open(' in line and 'with' not in line:
                has_close = False
                for j in range(i, min(i + 20, len(code_lines))):
                    if 'close()' in code_lines[j]:
                        has_close = True
                        break
                if not has_close:
                    bug_key = f"resource_leak_{i}"
                    if bug_key not in found_bugs:
                        bugs.append({
                            'line': i,
                            'description': 'Resource leak - file opened but not closed',
                            'severity': 'critical',
                            'suggestion': 'Use context manager: `with open(filename, "r") as f:`'
                        })
                        found_bugs.add(bug_key)
            
            # Bare except
            if stripped.startswith('except:') or stripped == 'except:':
                bug_key = f"bare_except_{i}"
                if bug_key not in found_bugs:
                    bugs.append({
                        'line': i,
                        'description': 'Bare except clause catches all exceptions',
                        'severity': 'critical',
                        'suggestion': 'Catch specific exceptions: `except (ValueError, TypeError) as e:`'
                    })
                    found_bugs.add(bug_key)
            
            # Print statements
            if 'print(' in line and not stripped.startswith('#'):
                issue_key = f"print_{i}"
                if issue_key not in found_issues:
                    issues.append({
                        'line': i,
                        'description': 'Print statement in production code',
                        'severity': 'low',
                        'suggestion': 'Use logging module: `logging.info()`'
                    })
                    found_issues.add(issue_key)
        
        return bugs, issues, suggestions

    # ============================================================
    # JAVASCRIPT ANALYZER
    # ============================================================
    
    def _analyze_javascript(self, code_lines):
        bugs = []
        issues = []
        suggestions = []
        found_bugs = set()
        found_issues = set()
        found_suggestions = set()
        
        for i, line in enumerate(code_lines, 1):
            stripped = line.strip()
            if not stripped or stripped.startswith(('//', '/*')):
                continue
            
            # Hardcoded credentials
            hardcoded_patterns = [
                (r'API_KEY\s*=\s*["\']([^"\']+)["\']', 'API Key'),
                (r'API_SECRET\s*=\s*["\']([^"\']+)["\']', 'API Secret'),
                (r'PASSWORD\s*=\s*["\']([^"\']+)["\']', 'Password'),
                (r'SECRET_KEY\s*=\s*["\']([^"\']+)["\']', 'Secret Key'),
                (r'SECRET_TOKEN\s*=\s*["\']([^"\']+)["\']', 'Secret Token'),
                (r'AWS_ACCESS_KEY\s*=\s*["\']([^"\']+)["\']', 'AWS Access Key'),
                (r'AWS_SECRET_KEY\s*=\s*["\']([^"\']+)["\']', 'AWS Secret Key'),
                (r'DATABASE_PASSWORD\s*=\s*["\']([^"\']+)["\']', 'Database Password'),
            ]
            
            for pattern, desc in hardcoded_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    var_match = re.search(r'(const|let|var)?\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*=', line)
                    var_name = var_match.group(2) if var_match else 'variable'
                    bug_key = f"hardcoded_{var_name}_{i}"
                    if bug_key not in found_bugs:
                        bugs.append({
                            'line': i,
                            'description': f'Hardcoded {desc} in `{var_name}`',
                            'severity': 'critical',
                            'suggestion': f'Use environment variables: `process.env.{var_name}`'
                        })
                        found_bugs.add(bug_key)
                    break
            
            # Division by zero
            if '/' in line and not '//' in line:
                if '/0' in line or '/ 0' in line:
                    bug_key = f"div_zero_{i}"
                    if bug_key not in found_bugs:
                        bugs.append({
                            'line': i,
                            'description': 'Division by zero detected',
                            'severity': 'critical',
                            'suggestion': 'Check denominator before division'
                        })
                        found_bugs.add(bug_key)
                
                if '.length' in line and '/' in line:
                    bug_key = f"div_len_{i}"
                    if bug_key not in found_bugs:
                        bugs.append({
                            'line': i,
                            'description': 'Division by array.length without checking if array is empty',
                            'severity': 'critical',
                            'suggestion': 'Check if array has elements: `if (numbers.length > 0)`'
                        })
                        found_bugs.add(bug_key)
            
            # eval()
            if 'eval(' in line:
                bug_key = f"eval_{i}"
                if bug_key not in found_bugs:
                    bugs.append({
                        'line': i,
                        'description': 'Dangerous eval() detected - can execute arbitrary code',
                        'severity': 'critical',
                        'suggestion': 'Avoid eval() - use safe alternatives'
                    })
                    found_bugs.add(bug_key)
            
            # SQL Injection
            if 'SELECT' in line.upper() or 'INSERT' in line.upper() or 'UPDATE' in line.upper():
                if '+' in line and ('"' in line or "'" in line):
                    bug_key = f"sql_injection_{i}"
                    if bug_key not in found_bugs:
                        bugs.append({
                            'line': i,
                            'description': 'SQL Injection vulnerability - string concatenation in query',
                            'severity': 'critical',
                            'suggestion': 'Use parameterized queries or ORM'
                        })
                        found_bugs.add(bug_key)
                
                if '${' in line and '`' in line:
                    bug_key = f"sql_injection_template_{i}"
                    if bug_key not in found_bugs:
                        bugs.append({
                            'line': i,
                            'description': 'SQL Injection vulnerability - template literal in query',
                            'severity': 'critical',
                            'suggestion': 'Use parameterized queries or ORM'
                        })
                        found_bugs.add(bug_key)
            
            # XSS
            if '.innerHTML' in line and '=' in line:
                bug_key = f"xss_{i}"
                if bug_key not in found_bugs:
                    bugs.append({
                        'line': i,
                        'description': 'XSS vulnerability - innerHTML without sanitization',
                        'severity': 'critical',
                        'suggestion': 'Use textContent for plain text or sanitize HTML content'
                    })
                    found_bugs.add(bug_key)
            
            # console.log
            if 'console.log' in line or 'console.error' in line:
                issue_key = f"console_{i}"
                if issue_key not in found_issues:
                    issues.append({
                        'line': i,
                        'description': 'console.log in production',
                        'severity': 'low',
                        'suggestion': 'Remove console.log before production'
                    })
                    found_issues.add(issue_key)
        
        return bugs, issues, suggestions

    # ============================================================
    # OTHER ANALYZERS (Rust, C, C++, Go, Java, C#, Ruby, PHP, SQL, Swift, Kotlin, etc.)
    # ============================================================
    
    def _analyze_rust(self, code_lines):
        bugs = []
        issues = []
        suggestions = []
        found_bugs = set()
        found_issues = set()
        
        for i, line in enumerate(code_lines, 1):
            stripped = line.strip()
            if not stripped or stripped.startswith(('//', '/*')):
                continue
            
            # Hardcoded credentials
            if any(k in line.lower() for k in ['password', 'secret', 'apikey', 'token']):
                if '="' in line or '= "' in line:
                    var_match = re.search(r'const\s+(\w+):\s*&str\s*=', line)
                    if var_match:
                        var_name = var_match.group(1)
                        bug_key = f"hardcoded_{var_name}_{i}"
                        if bug_key not in found_bugs:
                            bugs.append({
                                'line': i,
                                'description': f'Hardcoded credential in `{var_name}`',
                                'severity': 'critical',
                                'suggestion': f'Use environment variables: `std::env::var("{var_name}")`'
                            })
                            found_bugs.add(bug_key)
            
            # Division by zero
            if '/' in line and ('/0' in line or '/ 0' in line):
                bug_key = f"div_zero_{i}"
                if bug_key not in found_bugs:
                    bugs.append({
                        'line': i,
                        'description': 'Division by zero detected',
                        'severity': 'critical',
                        'suggestion': 'Check denominator before division'
                    })
                    found_bugs.add(bug_key)
            
            # .unwrap()
            if '.unwrap()' in line:
                bug_key = f"unwrap_{i}"
                if bug_key not in found_bugs:
                    bugs.append({
                        'line': i,
                        'description': '.unwrap() may panic - potential crash',
                        'severity': 'high',
                        'suggestion': 'Use `match`, `?` operator, or `.expect()`'
                    })
                    found_bugs.add(bug_key)
            
            # println!
            if 'println!' in line or 'eprintln!' in line:
                issue_key = f"print_{i}"
                if issue_key not in found_issues:
                    issues.append({
                        'line': i,
                        'description': 'Print statement in production',
                        'severity': 'low',
                        'suggestion': 'Use proper logging framework'
                    })
                    found_issues.add(issue_key)
        
        return bugs, issues, suggestions

    def _analyze_c(self, code_lines):
        bugs = []
        issues = []
        suggestions = []
        found_bugs = set()
        
        for i, line in enumerate(code_lines, 1):
            stripped = line.strip()
            if not stripped or stripped.startswith(('//', '/*', '#')):
                continue
            
            # Memory leaks
            if 'malloc(' in line or 'calloc(' in line:
                has_free = False
                for j in range(i, min(i + 20, len(code_lines))):
                    if 'free(' in code_lines[j]:
                        has_free = True
                        break
                if not has_free:
                    bug_key = f"memory_leak_{i}"
                    if bug_key not in found_bugs:
                        bugs.append({
                            'line': i,
                            'description': 'Memory leak: malloc without free',
                            'severity': 'critical',
                            'suggestion': 'Add free() to release allocated memory'
                        })
                        found_bugs.add(bug_key)
            
            # Buffer overflow
            if 'strcpy(' in line or 'strcat(' in line or 'sprintf(' in line or 'gets(' in line:
                bug_key = f"buffer_overflow_{i}"
                if bug_key not in found_bugs:
                    bugs.append({
                        'line': i,
                        'description': 'Buffer overflow risk - unsafe function',
                        'severity': 'critical',
                        'suggestion': 'Use safe alternatives: strncpy, strncat, snprintf, fgets'
                    })
                    found_bugs.add(bug_key)
        
        return bugs, issues, suggestions

    def _analyze_cpp(self, code_lines):
        bugs = []
        issues = []
        suggestions = []
        found_bugs = set()
        
        for i, line in enumerate(code_lines, 1):
            stripped = line.strip()
            if not stripped or stripped.startswith(('//', '/*', '#')):
                continue
            
            # Memory leaks
            if 'new ' in line and 'delete' not in line:
                has_delete = False
                for j in range(i, min(i + 15, len(code_lines))):
                    if 'delete' in code_lines[j]:
                        has_delete = True
                        break
                if not has_delete:
                    bug_key = f"memory_leak_{i}"
                    if bug_key not in found_bugs:
                        bugs.append({
                            'line': i,
                            'description': 'Memory leak - new without delete',
                            'severity': 'critical',
                            'suggestion': 'Add delete or use smart pointers'
                        })
                        found_bugs.add(bug_key)
        
        return bugs, issues, suggestions

    def _analyze_go(self, code_lines):
        bugs = []
        issues = []
        suggestions = []
        found_bugs = set()
        found_issues = set()
        
        for i, line in enumerate(code_lines, 1):
            stripped = line.strip()
            if not stripped or stripped.startswith('//'):
                continue
            
            # Error handling
            if ':=' in line and 'err' in line:
                has_check = False
                for j in range(i, min(i + 10, len(code_lines))):
                    if 'if err' in code_lines[j] or 'err != nil' in code_lines[j]:
                        has_check = True
                        break
                if not has_check:
                    bug_key = f"error_handling_{i}"
                    if bug_key not in found_bugs:
                        bugs.append({
                            'line': i,
                            'description': 'Error returned but not handled',
                            'severity': 'critical',
                            'suggestion': 'Always handle errors: `if err != nil { return err }`'
                        })
                        found_bugs.add(bug_key)
            
            # Print statements
            if 'fmt.Println' in line or 'fmt.Printf' in line:
                issue_key = f"print_{i}"
                if issue_key not in found_issues:
                    issues.append({
                        'line': i,
                        'description': 'Print statement in production',
                        'severity': 'low',
                        'suggestion': 'Use proper logging package'
                    })
                    found_issues.add(issue_key)
        
        return bugs, issues, suggestions

    def _analyze_java(self, code_lines):
        bugs = []
        issues = []
        suggestions = []
        found_bugs = set()
        found_issues = set()
        
        for i, line in enumerate(code_lines, 1):
            stripped = line.strip()
            if not stripped or stripped.startswith(('//', '/*')):
                continue
            
            # Hardcoded credentials
            if any(k in line.lower() for k in ['password', 'secret', 'apikey', 'token']):
                if '="' in line or '= "' in line:
                    var_match = re.search(r'(private\s+static\s+final\s+String\s+)?([a-zA-Z_][a-zA-Z0-9_]*)\s*=', line)
                    if var_match:
                        var_name = var_match.group(2) if var_match.group(2) else 'variable'
                        bug_key = f"hardcoded_{var_name}_{i}"
                        if bug_key not in found_bugs:
                            bugs.append({
                                'line': i,
                                'description': f'Hardcoded credential in `{var_name}`',
                                'severity': 'critical',
                                'suggestion': f'Use environment variables: `System.getenv("{var_name}")`'
                            })
                            found_bugs.add(bug_key)
            
            # Print statements
            if 'System.out.println' in line or 'System.out.print' in line:
                issue_key = f"print_{i}"
                if issue_key not in found_issues:
                    issues.append({
                        'line': i,
                        'description': 'Print statement in production',
                        'severity': 'low',
                        'suggestion': 'Use logging framework (SLF4J, Log4j)'
                    })
                    found_issues.add(issue_key)
        
        return bugs, issues, suggestions

    def _analyze_csharp(self, code_lines):
        bugs = []
        issues = []
        suggestions = []
        found_bugs = set()
        found_issues = set()
        
        for i, line in enumerate(code_lines, 1):
            stripped = line.strip()
            if not stripped or stripped.startswith(('//', '/*')):
                continue
            
            # Hardcoded credentials
            if any(k in line.lower() for k in ['password', 'secret', 'apikey', 'token']):
                if '="' in line or '= "' in line:
                    var_match = re.search(r'(private\s+const\s+string\s+)?([a-zA-Z_][a-zA-Z0-9_]*)\s*=', line)
                    if var_match:
                        var_name = var_match.group(2) if var_match.group(2) else 'variable'
                        bug_key = f"hardcoded_{var_name}_{i}"
                        if bug_key not in found_bugs:
                            bugs.append({
                                'line': i,
                                'description': f'Hardcoded credential in `{var_name}`',
                                'severity': 'critical',
                                'suggestion': f'Use environment variables'
                            })
                            found_bugs.add(bug_key)
            
            # Print statements
            if 'Console.WriteLine' in line or 'Console.Write' in line:
                issue_key = f"print_{i}"
                if issue_key not in found_issues:
                    issues.append({
                        'line': i,
                        'description': 'Print statement in production',
                        'severity': 'low',
                        'suggestion': 'Use proper logging framework'
                    })
                    found_issues.add(issue_key)
        
        return bugs, issues, suggestions

    def _analyze_ruby(self, code_lines):
        bugs = []
        issues = []
        suggestions = []
        found_bugs = set()
        
        for i, line in enumerate(code_lines, 1):
            stripped = line.strip()
            if not stripped or stripped.startswith('#'):
                continue
            
            if 'rescue Exception' in line:
                bug_key = f"rescue_exception_{i}"
                if bug_key not in found_bugs:
                    bugs.append({
                        'line': i,
                        'description': 'Rescuing generic Exception',
                        'severity': 'critical',
                        'suggestion': 'Rescue StandardError or specific exceptions'
                    })
                    found_bugs.add(bug_key)

        return bugs, issues, suggestions

    def _analyze_php(self, code_lines):
        bugs = []
        issues = []
        suggestions = []
        found_bugs = set()
        
        for i, line in enumerate(code_lines, 1):
            stripped = line.strip()
            if not stripped or stripped.startswith(('//', '#')):
                continue
            
            if 'eval(' in line:
                bug_key = f"eval_{i}"
                if bug_key not in found_bugs:
                    bugs.append({
                        'line': i,
                        'description': 'Dangerous eval() detected',
                        'severity': 'critical',
                        'suggestion': 'Refactor to remove dynamic string execution'
                    })
                    found_bugs.add(bug_key)

        return bugs, issues, suggestions

    def _analyze_sql(self, code_lines):
        bugs = []
        issues = []
        suggestions = []
        found_bugs = set()
        found_issues = set()
        
        for i, line in enumerate(code_lines, 1):
            stripped = line.strip()
            upper_line = line.upper()
            
            if not stripped or stripped.startswith('--'):
                continue
            
            if 'SELECT *' in upper_line:
                issue_key = f"select_star_{i}"
                if issue_key not in found_issues:
                    issues.append({
                        'line': i,
                        'description': 'SELECT * used - performance issue',
                        'severity': 'medium',
                        'suggestion': 'Specify required column names'
                    })
                    found_issues.add(issue_key)
            
            if ('DELETE FROM' in upper_line or 'DELETE ' in upper_line) and 'WHERE' not in upper_line:
                bug_key = f"delete_without_where_{i}"
                if bug_key not in found_bugs:
                    bugs.append({
                        'line': i,
                        'description': 'DELETE without WHERE - risk of data loss',
                        'severity': 'critical',
                        'suggestion': 'Add WHERE clause to restrict deletions'
                    })
                    found_bugs.add(bug_key)

            if 'UPDATE ' in upper_line and 'WHERE' not in upper_line:
                bug_key = f"update_without_where_{i}"
                if bug_key not in found_bugs:
                    bugs.append({
                        'line': i,
                        'description': 'UPDATE without WHERE - risk of data corruption',
                        'severity': 'critical',
                        'suggestion': 'Add WHERE clause to restrict updates'
                    })
                    found_bugs.add(bug_key)

        return bugs, issues, suggestions

    def _analyze_swift(self, code_lines):
        bugs = []
        issues = []
        suggestions = []
        found_issues = set()
        
        for i, line in enumerate(code_lines, 1):
            stripped = line.strip()
            if not stripped or stripped.startswith('//'):
                continue
            
            if '!' in line and 'if let' not in line and 'guard let' not in line and '!=' in line:
                issue_key = f"force_unwrap_{i}"
                if issue_key not in found_issues:
                    issues.append({
                        'line': i,
                        'description': 'Force unwrapping (!) may crash',
                        'severity': 'high',
                        'suggestion': 'Use if let, guard let, or ?? for safe unwrapping'
                    })
                    found_issues.add(issue_key)

        return bugs, issues, suggestions

    def _analyze_kotlin(self, code_lines):
        bugs = []
        issues = []
        suggestions = []
        found_bugs = set()
        
        for i, line in enumerate(code_lines, 1):
            stripped = line.strip()
            if not stripped or stripped.startswith('//'):
                continue
            
            if '!!' in line:
                bug_key = f"not_null_assertion_{i}"
                if bug_key not in found_bugs:
                    bugs.append({
                        'line': i,
                        'description': '!! operator may cause NPE',
                        'severity': 'high',
                        'suggestion': 'Use safe call (?.) or Elvis (?:) operator'
                    })
                    found_bugs.add(bug_key)

        return bugs, issues, suggestions

    def _analyze_haskell(self, code_lines):
        bugs = []
        issues = []
        suggestions = []
        found_issues = set()
        
        for i, line in enumerate(code_lines, 1):
            stripped = line.strip()
            if not stripped or stripped.startswith('--'):
                continue
            
            if 'head ' in line or 'tail ' in line:
                issue_key = f"partial_function_{i}"
                if issue_key not in found_issues:
                    issues.append({
                        'line': i,
                        'description': 'Partial function fails on empty list',
                        'severity': 'medium',
                        'suggestion': 'Use pattern matching or safe list functions'
                    })
                    found_issues.add(issue_key)

        return bugs, issues, suggestions

    def _analyze_julia(self, code_lines):
        bugs = []
        issues = []
        suggestions = []
        found_issues = set()
        
        for i, line in enumerate(code_lines, 1):
            stripped = line.strip()
            if not stripped or stripped.startswith('#'):
                continue
            
            if 'global ' in line:
                issue_key = f"global_var_{i}"
                if issue_key not in found_issues:
                    issues.append({
                        'line': i,
                        'description': 'Global variable used',
                        'severity': 'medium',
                        'suggestion': 'Avoid global variables for better performance'
                    })
                    found_issues.add(issue_key)

        return bugs, issues, suggestions

    def _analyze_html_css(self, code_lines):
        bugs = []
        issues = []
        suggestions = []
        found_suggestions = set()
        found_issues = set()
        
        for i, line in enumerate(code_lines, 1):
            stripped = line.strip()
            if not stripped:
                continue
            
            if '<img' in line and 'alt=' not in line:
                suggestion_key = f"missing_alt_{i}"
                if suggestion_key not in found_suggestions:
                    suggestions.append({
                        'line': i,
                        'description': 'Image missing alt attribute',
                        'severity': 'low',
                        'suggestion': 'Add descriptive alt attribute for accessibility'
                    })
                    found_suggestions.add(suggestion_key)
            
            if '!important' in line:
                issue_key = f"important_{i}"
                if issue_key not in found_issues:
                    issues.append({
                        'line': i,
                        'description': 'Use of !important',
                        'severity': 'low',
                        'suggestion': 'Refactor selector specificity instead'
                    })
                    found_issues.add(issue_key)

        return bugs, issues, suggestions

    def _analyze_shell(self, code_lines):
        bugs = []
        issues = []
        suggestions = []
        found_bugs = set()
        
        for i, line in enumerate(code_lines, 1):
            stripped = line.strip()
            if not stripped or stripped.startswith('#'):
                continue
            
            if 'rm -rf $' in line and '"$' not in line:
                bug_key = f"unquoted_variable_{i}"
                if bug_key not in found_bugs:
                    bugs.append({
                        'line': i,
                        'description': 'Unquoted variable in rm -rf',
                        'severity': 'critical',
                        'suggestion': 'Quote variable: rm -rf "$VAR"'
                    })
                    found_bugs.add(bug_key)

        return bugs, issues, suggestions

    def _analyze_typescript(self, code_lines):
        bugs, issues, suggestions = self._analyze_javascript(code_lines)
        
        found_issues = set()
        
        for i, line in enumerate(code_lines, 1):
            stripped = line.strip()
            if not stripped or stripped.startswith('//'):
                continue
            
            if ': any' in line or 'as any' in line:
                target = line.split(':')[0].strip() if ':' in line else 'expression'
                issue_key = f"any_type_{i}"
                if issue_key not in found_issues:
                    issues.append({
                        'line': i,
                        'description': f'"any" type used for `{target}`',
                        'severity': 'medium',
                        'suggestion': 'Define explicit type instead of "any"'
                    })
                    found_issues.add(issue_key)

        return bugs, issues, suggestions

    def _analyze_universal(self, code_lines):
        bugs = []
        issues = []
        suggestions = []
        found_bugs = set()
        found_issues = set()
        
        for i, line in enumerate(code_lines, 1):
            stripped = line.strip()
            if not stripped or stripped.startswith(('//', '#', '--', '/*')):
                continue
            
            if '/' in line and ('/0' in line or '/ 0' in line):
                bug_key = f"div_zero_{i}"
                if bug_key not in found_bugs:
                    bugs.append({
                        'line': i,
                        'description': f'Division by zero on line {i}',
                        'severity': 'critical',
                        'suggestion': 'Validate denominator before division'
                    })
                    found_bugs.add(bug_key)
            
            if any(k in line.lower() for k in ['password', 'secret', 'api_key']):
                if '=' in line and ('"' in line or "'" in line):
                    var_name = line.split('=')[0].strip()
                    bug_key = f"hardcoded_{var_name}_{i}"
                    if bug_key not in found_bugs:
                        bugs.append({
                            'line': i,
                            'description': f'Hardcoded credential in variable "{var_name}"',
                            'severity': 'critical',
                            'suggestion': 'Use environment variables'
                        })
                        found_bugs.add(bug_key)
            
            print_keywords = ['console.log', 'printf', 'puts', 'echo', 'println', 'print_r', 'var_dump']
            for pk in print_keywords:
                if pk in line:
                    issue_key = f"print_{i}"
                    if issue_key not in found_issues:
                        issues.append({
                            'line': i,
                            'description': f'Debug print statement: `{stripped[:35]}`',
                            'severity': 'low',
                            'suggestion': 'Remove debug statements'
                        })
                        found_issues.add(issue_key)
                    break

        return bugs, issues, suggestions

        