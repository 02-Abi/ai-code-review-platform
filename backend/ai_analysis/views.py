"""
Views for AI Code Review App
Complete implementation with all required views
"""
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
import logging
import re
import json

logger = logging.getLogger(__name__)


# ============================================================
# LANGUAGE DETECTION HELPER
# ============================================================

def detect_programming_language(code):
    """Enhanced language detection"""
    if not code or not code.strip():
        return 'python'
    
    code_lower = code.lower()
    code_upper = code.upper()
    first_line = code.split('\n')[0] if code else ''
    
    # Check shebang
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
    
    # HASKELL - Check first to avoid false positives
    if 'module ' in code and 'where' in code:
        if '::' in code and '->' in code:
            return 'haskell'
        if 'import Data.' in code or 'import Control.' in code:
            return 'haskell'
        if 'data ' in code and '=' in code and 'deriving' in code:
            return 'haskell'
        if 'class ' in code and 'where' in code and 'instance' in code:
            return 'haskell'
        if 'do' in code and '<-' in code and 'return' in code:
            return 'haskell'
    
    # GO
    if 'package ' in code and 'func ' in code:
        if 'fmt.Println' in code or 'fmt.Printf' in code:
            return 'go'
        if 'import (' in code or 'import "' in code:
            return 'go'
        if 'go ' in code or 'chan ' in code:
            return 'go'
        if 'func main()' in code:
            return 'go'
    
    # RUST
    if 'fn ' in code and 'let mut' in code:
        if 'println!' in code or 'print!' in code:
            return 'rust'
        if 'match ' in code or 'impl ' in code:
            return 'rust'
        if 'pub fn' in code or 'mod ' in code:
            return 'rust'
        if 'fn main()' in code:
            return 'rust'
    
    # PYTHON
    if 'def ' in code or 'import ' in code or 'from ' in code:
        if 'if __name__' in code or 'print(' in code:
            return 'python'
        if 'class ' in code and ':' in code:
            return 'python'
        if '@' in code and 'def ' in code:
            return 'python'
        if 'self' in code and 'def ' in code:
            return 'python'
    
    # JULIA
    if 'function ' in code and 'end' in code:
        if '::' in code and 'println(' in code:
            return 'julia'
        if 'using ' in code or 'import ' in code:
            return 'julia'
        if 'Dict{' in code or 'Array{' in code:
            return 'julia'
        if 'Vector{' in code or 'Matrix{' in code:
            return 'julia'
    
    # JAVASCRIPT / TYPESCRIPT
    if 'function ' in code or 'const ' in code or 'let ' in code or 'var ' in code:
        if 'console.log' in code or '=>' in code:
            return 'javascript'
        if 'export ' in code or 'import ' in code:
            if 'from ' in code:
                return 'javascript'
        if 'async ' in code or 'await ' in code:
            return 'javascript'
        if 'document.' in code or 'window.' in code:
            return 'javascript'
        if 'interface ' in code or 'type ' in code:
            if ': string' in code or ': number' in code:
                return 'typescript'
        if '<T>' in code or 'extends ' in code:
            return 'typescript'
    
    # JAVA
    if 'public class' in code or 'private ' in code or 'protected ' in code:
        if 'System.out.println' in code:
            return 'java'
        if 'public static void main' in code:
            return 'java'
        if 'import java.' in code:
            return 'java'
        if '@Override' in code:
            return 'java'
    
    # C
    if '#include' in code and 'int main(' in code:
        if 'printf(' in code or 'scanf(' in code:
            return 'c'
        if 'malloc(' in code or 'free(' in code:
            return 'c'
        if 'char*' in code or 'int*' in code:
            return 'c'
    
    # C++
    if '#include' in code and 'std::' in code:
        if 'cout' in code or 'cin' in code:
            return 'cpp'
        if 'class ' in code and 'public:' in code:
            return 'cpp'
        if 'namespace ' in code:
            return 'cpp'
        if 'template' in code:
            return 'cpp'
    
    # C#
    if 'using System' in code and 'namespace ' in code:
        if 'Console.WriteLine' in code:
            return 'csharp'
        if 'class ' in code and 'private ' in code:
            return 'csharp'
        if 'get; set;' in code:
            return 'csharp'
        if 'static void Main' in code:
            return 'csharp'
    
    # RUBY
    if 'def ' in code and 'end' in code:
        if 'attr_accessor' in code or 'puts ' in code:
            return 'ruby'
        if 'class ' in code and '< ' in code:
            return 'ruby'
        if 'require ' in code:
            return 'ruby'
        if '# encoding:' in code or '# frozen_string_literal:' in code:
            return 'ruby'
    
    # PHP
    if '<?php' in code:
        return 'php'
    if 'echo ' in code and '$' in code:
        return 'php'
    if 'function ' in code and '$' in code:
        return 'php'
    if '$_GET' in code or '$_POST' in code:
        return 'php'
    
    # SWIFT
    if 'import UIKit' in code or 'import Foundation' in code:
        if 'func ' in code and 'var ' in code:
            return 'swift'
        if 'class ' in code and 'override' in code:
            return 'swift'
        if 'let ' in code and 'var ' in code:
            return 'swift'
    
    # KOTLIN
    if 'fun ' in code and 'var ' in code:
        if 'class ' in code and 'val ' in code:
            return 'kotlin'
        if 'suspend' in code or 'coroutine' in code:
            return 'kotlin'
        if 'data class' in code:
            return 'kotlin'
        if 'companion object' in code:
            return 'kotlin'
    
    # SQL
    if 'SELECT ' in code_upper or 'INSERT ' in code_upper:
        if 'FROM ' in code_upper or 'WHERE ' in code_upper:
            return 'sql'
        if 'CREATE ' in code_upper or 'ALTER ' in code_upper:
            return 'sql'
        if 'JOIN ' in code_upper or 'GROUP BY ' in code_upper:
            return 'sql'
        if 'UPDATE ' in code_upper or 'DELETE ' in code_upper:
            return 'sql'
    
    # HTML
    if '<!DOCTYPE html>' in code or '<html>' in code:
        return 'html'
    if '<body>' in code or '<div>' in code:
        return 'html'
    if '<head>' in code or '<title>' in code:
        return 'html'
    
    # CSS
    if 'color:' in code or 'margin:' in code or 'padding:' in code:
        if '{' in code and '}' in code:
            return 'css'
        if '@media' in code or '@keyframes' in code:
            return 'css'
        if '@import' in code:
            return 'css'
    
    # Default to Python
    return 'python'


# ============================================================
# LANGUAGE INFO
# ============================================================

def get_language_info(lang):
    """Get language information"""
    languages = {
        'python': {'name': 'Python', 'icon': '🐍', 'color': '#3776AB', 'extension': '.py'},
        'javascript': {'name': 'JavaScript', 'icon': '🟡', 'color': '#F7DF1E', 'extension': '.js'},
        'typescript': {'name': 'TypeScript', 'icon': '🔵', 'color': '#3178C6', 'extension': '.ts'},
        'java': {'name': 'Java', 'icon': '☕', 'color': '#007396', 'extension': '.java'},
        'c': {'name': 'C', 'icon': '⚙️', 'color': '#00599C', 'extension': '.c'},
        'cpp': {'name': 'C++', 'icon': '⚙️', 'color': '#00599C', 'extension': '.cpp'},
        'csharp': {'name': 'C#', 'icon': '🟣', 'color': '#239120', 'extension': '.cs'},
        'go': {'name': 'Go', 'icon': '🐹', 'color': '#00ADD8', 'extension': '.go'},
        'rust': {'name': 'Rust', 'icon': '🦀', 'color': '#DEA584', 'extension': '.rs'},
        'ruby': {'name': 'Ruby', 'icon': '💎', 'color': '#CC342D', 'extension': '.rb'},
        'php': {'name': 'PHP', 'icon': '🐘', 'color': '#777BB4', 'extension': '.php'},
        'haskell': {'name': 'Haskell', 'icon': 'λ', 'color': '#5E5086', 'extension': '.hs'},
        'sql': {'name': 'SQL', 'icon': '🗄️', 'color': '#4479A1', 'extension': '.sql'},
        'html': {'name': 'HTML', 'icon': '🌐', 'color': '#E34F26', 'extension': '.html'},
        'css': {'name': 'CSS', 'icon': '🎨', 'color': '#1572B6', 'extension': '.css'},
        'shell': {'name': 'Shell', 'icon': '💻', 'color': '#4EAA25', 'extension': '.sh'},
        'swift': {'name': 'Swift', 'icon': '🐦', 'color': '#FA7343', 'extension': '.swift'},
        'kotlin': {'name': 'Kotlin', 'icon': '📱', 'color': '#7F52FF', 'extension': '.kt'},
        'julia': {'name': 'Julia', 'icon': '🔢', 'color': '#9558B2', 'extension': '.jl'},
        'scala': {'name': 'Scala', 'icon': '🔄', 'color': '#DC322F', 'extension': '.scala'},
        'perl': {'name': 'Perl', 'icon': '🐪', 'color': '#39457E', 'extension': '.pl'},
        'r': {'name': 'R', 'icon': '📊', 'color': '#276DC3', 'extension': '.r'},
        'dart': {'name': 'Dart', 'icon': '🎯', 'color': '#00B4AB', 'extension': '.dart'},
        'elixir': {'name': 'Elixir', 'icon': '🧪', 'color': '#4E2A8E', 'extension': '.ex'},
        'lua': {'name': 'Lua', 'icon': '🌙', 'color': '#000080', 'extension': '.lua'},
    }
    return languages.get(lang, {'name': lang.capitalize(), 'icon': '📄', 'color': '#6c757d', 'extension': ''})


# ============================================================
# HEALTH CHECK VIEW
# ============================================================

class HealthCheckView(APIView):
    """Health check endpoint"""
    permission_classes = [AllowAny]
    
    def get(self, request):
        return Response({
            'status': 'healthy',
            'message': 'AI Code Review API is running',
            'version': '1.0.0'
        }, status=status.HTTP_200_OK)


# ============================================================
# CODE ANALYSIS VIEW
# ============================================================

class CodeAnalysisView(APIView):
    """
    Main code analysis view
    Analyzes code and returns bugs, issues, and suggestions
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        code = request.data.get('code', '')
        language = request.data.get('language', 'auto')
        filename = request.data.get('filename', '')
        
        if not code:
            return Response({
                'status': 'error',
                'message': 'Code is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Detect language if auto
        if language == 'auto':
            language = detect_programming_language(code)
        
        # Get language info
        lang_info = get_language_info(language)
        
        # Analyze code
        bugs, issues, suggestions = self._analyze_code(code, language)
        
        # Calculate quality score
        quality_score = max(50, 100 - len(bugs) * 10 - len(issues) * 5 - len(suggestions) * 2)
        
        # Generate test cases
        test_cases = self._generate_test_cases(code, language)
        
        return Response({
            'status': 'success',
            'data': {
                'language': language,
                'language_name': lang_info['name'],
                'icon': lang_info['icon'],
                'color': lang_info['color'],
                'quality_score': quality_score,
                'bugs': bugs,
                'issues': issues,
                'suggestions': suggestions,
                'test_cases': test_cases,
                'explanation': self._generate_explanation(code, language, quality_score, bugs, issues, suggestions)
            }
        }, status=status.HTTP_200_OK)
    
    def _analyze_code(self, code, language):
        """Analyze code for bugs"""
        bugs = []
        issues = []
        suggestions = []
        code_lines = code.split('\n')
        
        # Common bug patterns
        for i, line in enumerate(code_lines, 1):
            stripped = line.strip()
            
            if not stripped:
                continue
            
            # Skip comments
            if stripped.startswith('//') or stripped.startswith('#') or stripped.startswith('--'):
                continue
            if stripped.startswith('/*') or stripped.startswith('{-'):
                continue
            
            # BUG: Division by zero
            if '/' in line and not stripped.startswith('//'):
                if '/ 0' in line or '/0' in line:
                    bugs.append({
                        'line': i,
                        'description': 'Division by zero detected',
                        'severity': 'critical',
                        'suggestion': 'Check for division by zero before performing division'
                    })
            
            # BUG: Hardcoded credentials
            line_lower = line.lower()
            if 'password' in line_lower or 'secret' in line_lower or 'api_key' in line_lower:
                if '=' in line and ('"' in line or "'" in line):
                    bugs.append({
                        'line': i,
                        'description': 'Hardcoded credentials detected',
                        'severity': 'critical',
                        'suggestion': 'Use environment variables or .env file for sensitive data'
                    })
            
            # ISSUE: Print/debug statements
            print_keywords = ['print', 'console.log', 'printf', 'puts', 'echo', 'println']
            for pk in print_keywords:
                if pk in line and not stripped.startswith('#') and not stripped.startswith('//'):
                    if pk in line:
                        issues.append({
                            'line': i,
                            'description': 'Print/debug statement found',
                            'type': 'debug',
                            'suggestion': 'Use proper logging framework or remove in production'
                        })
                        break
        
        return bugs, issues, suggestions
    
    def _generate_test_cases(self, code, language):
        """Generate test cases for the code"""
        test_cases = []
        
        # Detect functions
        functions = []
        code_lines = code.split('\n')
        
        if language == 'python':
            for line in code_lines:
                stripped = line.strip()
                if stripped.startswith('def ') and ':' in line:
                    func_name = stripped.split('def ')[1].split('(')[0].strip()
                    if func_name and not func_name.startswith('_'):
                        functions.append(func_name)
        
        # Generate test cases for each function
        for func in functions[:3]:
            test_cases.append({
                'name': 'Test {} with valid input'.format(func),
                'input': 'Valid input data',
                'expected': 'Expected output',
                'description': 'Test {} basic functionality'.format(func)
            })
        
        if not test_cases:
            test_cases.append({
                'name': 'Test Basic Functionality',
                'input': 'Default input',
                'expected': 'Expected output',
                'description': 'Basic test case for the code'
            })
        
        return test_cases[:5]
    
    def _generate_explanation(self, code, language, quality_score, bugs, issues, suggestions):
        """Generate explanation for the analysis"""
        lang_name = get_language_info(language)['name']
        total_lines = len(code.split('\n'))
        total_chars = len(code)
        
        explanation_lines = []
        explanation_lines.append("Code Analysis Report")
        explanation_lines.append("=" * 40)
        explanation_lines.append("")
        explanation_lines.append("Language: {}".format(lang_name))
        explanation_lines.append("Quality Score: {}%".format(quality_score))
        explanation_lines.append("")
        explanation_lines.append("Code Statistics:")
        explanation_lines.append("- Lines of Code: {}".format(total_lines))
        explanation_lines.append("- Characters: {}".format(total_chars))
        explanation_lines.append("")
        explanation_lines.append("Issues Found:")
        explanation_lines.append("- Bugs: {}".format(len(bugs)))
        explanation_lines.append("- Issues: {}".format(len(issues)))
        explanation_lines.append("- Suggestions: {}".format(len(suggestions)))
        explanation_lines.append("")
        
        if len(bugs) == 0:
            explanation_lines.append("No bugs found! Great job!")
        else:
            explanation_lines.append("Please review the bugs found above.")
        
        explanation_lines.append("")
        explanation_lines.append("=" * 40)
        
        return "\n".join(explanation_lines)


# ============================================================
# GENERATE TEST CASES VIEW
# ============================================================

class GenerateTestCasesView(APIView):
    """Generate test cases for code"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        code = request.data.get('code', '')
        language = request.data.get('language', 'auto')
        
        if not code:
            return Response({
                'status': 'error',
                'message': 'Code is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if language == 'auto':
            language = detect_programming_language(code)
        
        test_cases = self._generate_test_cases(code, language)
        
        return Response({
            'status': 'success',
            'data': {
                'language': language,
                'language_name': get_language_info(language)['name'],
                'test_cases': test_cases,
                'total': len(test_cases)
            }
        }, status=status.HTTP_200_OK)
    
    def _generate_test_cases(self, code, language):
        """Generate test cases"""
        test_cases = []
        code_lines = code.split('\n')
        functions = []
        
        if language == 'python':
            for line in code_lines:
                stripped = line.strip()
                if stripped.startswith('def ') and ':' in line:
                    func_name = stripped.split('def ')[1].split('(')[0].strip()
                    if func_name and not func_name.startswith('_'):
                        functions.append(func_name)
        
        for func in functions[:3]:
            test_cases.append({
                'name': 'Test {} - Valid Input'.format(func),
                'input': 'Valid input data',
                'expected': 'Expected output',
                'description': 'Test {} with valid input'.format(func)
            })
            test_cases.append({
                'name': 'Test {} - Invalid Input'.format(func),
                'input': 'Invalid input data',
                'expected': 'Error handling',
                'description': 'Test {} with invalid input'.format(func)
            })
        
        if not test_cases:
            test_cases = [
                {
                    'name': 'Test Basic Functionality',
                    'input': 'Default input',
                    'expected': 'Expected output',
                    'description': 'Basic test case'
                }
            ]
        
        return test_cases[:10]


# ============================================================
# EXPLAIN CODE VIEW
# ============================================================

class ExplainCodeView(APIView):
    """Explain what the code does"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        code = request.data.get('code', '')
        language = request.data.get('language', 'auto')
        
        if not code:
            return Response({
                'status': 'error',
                'message': 'Code is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if language == 'auto':
            language = detect_programming_language(code)
        
        explanation = self._explain_code(code, language)
        
        return Response({
            'status': 'success',
            'data': {
                'language': language,
                'language_name': get_language_info(language)['name'],
                'explanation': explanation
            }
        }, status=status.HTTP_200_OK)
    
    def _explain_code(self, code, language):
        """Explain what the code does"""
        code_lines = code.split('\n')
        
        function_count = 0
        class_count = 0
        
        for line in code_lines:
            stripped = line.strip()
            if stripped.startswith('def ') or stripped.startswith('function ') or stripped.startswith('func '):
                function_count += 1
            if stripped.startswith('class ') or stripped.startswith('class '):
                class_count += 1
        
        lang_name = get_language_info(language)['name']
        
        explanation_lines = []
        explanation_lines.append("Code Explanation")
        explanation_lines.append("=" * 40)
        explanation_lines.append("")
        explanation_lines.append("Overview:")
        explanation_lines.append("This is a {} program with {} lines of code.".format(lang_name, len(code_lines)))
        explanation_lines.append("")
        explanation_lines.append("Structure:")
        explanation_lines.append("- Functions: {}".format(function_count))
        explanation_lines.append("- Classes: {}".format(class_count))
        explanation_lines.append("")
        explanation_lines.append("=" * 40)
        
        return "\n".join(explanation_lines)


# ============================================================
# STATIC ANALYSIS VIEW
# ============================================================

class StaticAnalysisView(APIView):
    """Perform static analysis on code"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        code = request.data.get('code', '')
        language = request.data.get('language', 'auto')
        
        if not code:
            return Response({
                'status': 'error',
                'message': 'Code is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if language == 'auto':
            language = detect_programming_language(code)
        
        analysis = self._static_analysis(code, language)
        
        return Response({
            'status': 'success',
            'data': analysis
        }, status=status.HTTP_200_OK)
    
    def _static_analysis(self, code, language):
        """Perform static analysis"""
        code_lines = code.split('\n')
        
        total_lines = len(code_lines)
        blank_lines = sum(1 for line in code_lines if not line.strip())
        code_lines_count = total_lines - blank_lines
        
        function_count = 0
        class_count = 0
        
        for line in code_lines:
            stripped = line.strip()
            if stripped.startswith('def ') or stripped.startswith('function ') or stripped.startswith('func '):
                function_count += 1
            if stripped.startswith('class ') or stripped.startswith('class '):
                class_count += 1
        
        quality_score = min(100, 60 + function_count * 5 + class_count * 5)
        
        return {
            'language': language,
            'language_name': get_language_info(language)['name'],
            'metrics': {
                'total_lines': total_lines,
                'code_lines': code_lines_count,
                'blank_lines': blank_lines,
                'function_count': function_count,
                'class_count': class_count
            },
            'scores': {
                'quality_score': quality_score
            }
        }