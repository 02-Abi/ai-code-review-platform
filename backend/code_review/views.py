# code_review/views.py - COMPLETE ANALYSIS & DEBUGGING LIKE CHATGPT

import logging
import re
import ast
import json
import traceback
import subprocess
import tempfile
import os
import time
from typing import Dict, List, Any, Optional
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.db.models import Q, Avg, Count, Sum
from django.conf import settings
from django.utils import timezone
from .models import (
    ProgrammingLanguage, CodeSubmission, ReviewHistory,
    CodeReviewComment, CodeSnippet
)
from .serializers import (
    ProgrammingLanguageSerializer, CodeSubmissionSerializer,
    CodeSubmissionCreateSerializer, ReviewHistorySerializer,
    CodeReviewCommentSerializer, CodeSnippetSerializer
)

logger = logging.getLogger(__name__)


# ============================================================
# LLM ANALYZER - LIKE CHATGPT ANALYSIS
# ============================================================

class LLMAnalyzer:
    """LLM-based code analysis using Gemini - Like ChatGPT"""

    @staticmethod
    def analyze_like_chatgpt(code: str, language: str) -> Dict:
        """
        Complete code analysis like ChatGPT with Gemini
        """
        try:
            from google import genai

            api_key = getattr(settings, "GEMINI_API_KEY", None)
            if not api_key:
                logger.warning("Gemini API key not configured")
                return LLMAnalyzer._fallback_analysis(code, language)

            client = genai.Client(api_key=api_key)

            if len(code) > 4000:
                code = code[:4000] + "\n... [truncated] ..."

            # ===== COMPLETE PROMPT LIKE CHATGPT =====
            prompt = f"""
Analyze this {language} code COMPLETELY like an expert code reviewer.

CODE TO REVIEW:
```{language}
{code}
```

Provide a COMPLETE analysis including:
1. Bugs - Every bug that exists, why it's a problem, and exactly how to fix it
2. Security Issues - All security vulnerabilities
3. Logic Errors - Code that doesn't work as intended
4. Performance Issues - Slow or inefficient code
5. Best Practice Violations - Things that should be done differently
6. Test Cases - Comprehensive test cases covering edge cases

Return ONLY valid JSON with this EXACT structure:

{{
  "bugs": [
    {{
      "line": 1,
      "description": "Detailed bug description",
      "severity": "critical/high/medium/low",
      "suggestion": "Exact fix with code example",
      "category": "security/logic/performance/error_handling"
    }}
  ],
  "issues": [
    {{
      "line": 1,
      "description": "Detailed issue description",
      "severity": "medium/low",
      "suggestion": "How to improve"
    }}
  ],
  "suggestions": [
    {{
      "line": 1,
      "description": "Improvement suggestion",
      "severity": "low",
      "suggestion": "Implementation advice"
    }}
  ],
  "test_cases": [
    {{
      "name": "test_name",
      "description": "What this test validates",
      "input": {{"param": "value"}},
      "expected": "Expected behavior",
      "test_code": "Complete runnable test code"
    }}
  ],
  "quality_score": 75,
  "summary": "Overall code quality assessment in 2-3 sentences",
  "detailed_analysis": "Detailed breakdown of the code in 5-6 sentences"
}}

BE THOROUGH. Find EVERY real issue.
"""

            print(f"[DEBUG] Analyzing {language} code like ChatGPT...")

            response = client.models.generate_content(
                model="gemini-3.1-flash-lite",
                contents=prompt
            )

            content = response.text.strip()

            # Extract JSON
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                content = json_match.group(0)

            result = json.loads(content)

            # Ensure required keys exist
            required_keys = ['bugs', 'issues', 'suggestions', 'test_cases', 'quality_score', 'summary', 'detailed_analysis']
            for key in required_keys:
                if key not in result:
                    if key == 'quality_score':
                        result[key] = 50
                    elif key == 'summary':
                        result[key] = 'Analysis completed'
                    elif key == 'detailed_analysis':
                        result[key] = 'Detailed analysis not available'
                    else:
                        result[key] = []
                elif key != 'quality_score' and key != 'summary' and key != 'detailed_analysis' and not isinstance(result[key], list):
                    result[key] = []

            # Mark source as Gemini
            for bug in result.get('bugs', []):
                bug['source'] = 'gemini'
            for issue in result.get('issues', []):
                issue['source'] = 'gemini'
            for suggestion in result.get('suggestions', []):
                suggestion['source'] = 'gemini'

            print(f"[DEBUG] Found: {len(result.get('bugs', []))} bugs, "
                  f"{len(result.get('issues', []))} issues, "
                  f"{len(result.get('suggestions', []))} suggestions, "
                  f"{len(result.get('test_cases', []))} test cases")

            return result

        except ImportError:
            logger.warning("Google GenAI package not installed")
            return LLMAnalyzer._fallback_analysis(code, language)
        except Exception as e:
            logger.error(f"Gemini analysis failed: {e}")
            return LLMAnalyzer._fallback_analysis(code, language)

    @staticmethod
    def detect_language_with_gemini(code: str) -> Dict:
        """
        Detect programming language using Google Gemini.
        """
        try:
            from google import genai

            api_key = getattr(settings, "GEMINI_API_KEY", None)
            if not api_key:
                return {
                    "language": None,
                    "confidence": 0,
                    "extensions": [],
                    "method": "no_key",
                }

            client = genai.Client(api_key=api_key)

            if len(code) > 3000:
                code = code[:3000] + "\n... [truncated] ..."

            prompt = f"""
Detect the programming language of this code.

CODE:
{code}

Return ONLY a valid JSON object in this format:

{{
  "language": "language_name",
  "confidence": 95,
  "extensions": [".ext1", ".ext2"]
}}

Examples of supported languages:
Python, JavaScript, TypeScript, Java, C#, C++, C,
Rust, Go, Ruby, PHP, Swift, Kotlin, Scala,
Perl, Lua, R, Dart, Elixir, Haskell, Julia,
Shell, SQL, HTML, CSS, JSON, YAML, XML, Markdown.
"""

            response = client.models.generate_content(
                model="gemini-3.1-flash-lite",
                contents=prompt
            )

            content = response.text.strip()
            json_match = re.search(r"\{.*\}", content, re.DOTALL)
            if json_match:
                content = json_match.group(0)

            result = json.loads(content)

            language = result.get("language", "").strip()
            confidence = result.get("confidence", 70)
            extensions = result.get("extensions", [])

            language_map = {
                "python": "Python",
                "javascript": "JavaScript",
                "js": "JavaScript",
                "typescript": "TypeScript",
                "ts": "TypeScript",
                "java": "Java",
                "c#": "C#",
                "csharp": "C#",
                "c++": "C++",
                "cpp": "C++",
                "c": "C",
                "rust": "Rust",
                "go": "Go",
                "ruby": "Ruby",
                "php": "PHP",
                "swift": "Swift",
                "kotlin": "Kotlin",
                "scala": "Scala",
                "perl": "Perl",
                "lua": "Lua",
                "r": "R",
                "dart": "Dart",
                "elixir": "Elixir",
                "haskell": "Haskell",
                "julia": "Julia",
                "shell": "Shell",
                "sql": "SQL",
                "html": "HTML",
                "css": "CSS",
                "json": "JSON",
                "yaml": "YAML",
                "xml": "XML",
                "markdown": "Markdown",
            }

            normalized = language_map.get(language.lower(), language)

            return {
                "language": normalized,
                "confidence": confidence,
                "extensions": extensions,
                "method": "gemini",
            }

        except ImportError:
            logger.error("Google GenAI package not installed")
            return {
                "language": None,
                "confidence": 0,
                "extensions": [],
                "method": "no_package",
            }

        except json.JSONDecodeError:
            logger.error("Failed to parse Gemini JSON response")
            return {
                "language": None,
                "confidence": 0,
                "extensions": [],
                "method": "invalid_json",
            }

        except Exception as e:
            logger.error(f"Gemini detection failed: {e}")
            return {
                "language": None,
                "confidence": 0,
                "extensions": [],
                "method": "error",
            }

    @staticmethod
    def _fallback_analysis(code: str, language: str) -> Dict:
        """Fallback when Gemini fails"""
        return {
            'bugs': [],
            'issues': [],
            'suggestions': [],
            'test_cases': [],
            'quality_score': 50,
            'summary': 'Gemini analysis failed. Please check your API key and try again.',
            'detailed_analysis': 'Unable to perform detailed analysis.'
        }


# ============================================================
# LANGUAGE SUPPORT - STATIC DETECTION (FALLBACK)
# ============================================================

class LanguageSupport:
    """Static language detection (fallback when LLM fails)"""

    SUPPORTED_LANGUAGES = {
        'python': {'name': 'Python', 'extensions': ['.py', '.pyw'], 'full_support': True},
        'javascript': {'name': 'JavaScript', 'extensions': ['.js', '.mjs'], 'full_support': True},
        'typescript': {'name': 'TypeScript', 'extensions': ['.ts', '.tsx'], 'full_support': True},
        'java': {'name': 'Java', 'extensions': ['.java'], 'full_support': True},
        'csharp': {'name': 'C#', 'extensions': ['.cs'], 'full_support': True},
        'cpp': {'name': 'C++', 'extensions': ['.cpp', '.cc', '.hpp'], 'full_support': True},
        'c': {'name': 'C', 'extensions': ['.c', '.h'], 'full_support': True},
        'rust': {'name': 'Rust', 'extensions': ['.rs'], 'full_support': True},
        'go': {'name': 'Go', 'extensions': ['.go'], 'full_support': True},
        'ruby': {'name': 'Ruby', 'extensions': ['.rb'], 'full_support': True},
        'php': {'name': 'PHP', 'extensions': ['.php'], 'full_support': True},
        'swift': {'name': 'Swift', 'extensions': ['.swift'], 'full_support': True},
        'kotlin': {'name': 'Kotlin', 'extensions': ['.kt'], 'full_support': True},
        'scala': {'name': 'Scala', 'extensions': ['.scala'], 'full_support': True},
        'perl': {'name': 'Perl', 'extensions': ['.pl', '.pm'], 'full_support': True},
        'lua': {'name': 'Lua', 'extensions': ['.lua'], 'full_support': True},
        'r': {'name': 'R', 'extensions': ['.r', '.R'], 'full_support': True},
        'dart': {'name': 'Dart', 'extensions': ['.dart'], 'full_support': True},
        'elixir': {'name': 'Elixir', 'extensions': ['.ex', '.exs'], 'full_support': True},
        'haskell': {'name': 'Haskell', 'extensions': ['.hs', '.lhs'], 'full_support': True},
        'julia': {'name': 'Julia', 'extensions': ['.jl'], 'full_support': True},
        'shell': {'name': 'Shell/Bash', 'extensions': ['.sh', '.bash'], 'full_support': True},
        'sql': {'name': 'SQL', 'extensions': ['.sql'], 'full_support': True},
        'html': {'name': 'HTML', 'extensions': ['.html', '.htm'], 'full_support': True},
        'css': {'name': 'CSS', 'extensions': ['.css', '.scss'], 'full_support': True},
        'json': {'name': 'JSON', 'extensions': ['.json'], 'full_support': True},
        'yaml': {'name': 'YAML', 'extensions': ['.yaml', '.yml'], 'full_support': True},
        'xml': {'name': 'XML', 'extensions': ['.xml'], 'full_support': True},
        'markdown': {'name': 'Markdown', 'extensions': ['.md'], 'full_support': True},
    }

    @staticmethod
    def detect_language(code: str) -> Dict[str, Any]:
        """Static language detection (fallback)"""
        if not code or not str(code).strip():
            return LanguageSupport.get_language_info('python')

        code = str(code)
        code_lower = code.lower()

        # ===== PYTHON =====
        if 'def ' in code_lower and ':' in code_lower:
            if 'import ' in code_lower or 'from ' in code_lower:
                return LanguageSupport.get_language_info('python')
            if 'print(' in code_lower or 'if __name__' in code_lower:
                return LanguageSupport.get_language_info('python')
            if 'class ' in code_lower and 'self' in code_lower:
                return LanguageSupport.get_language_info('python')
            if 'except' in code_lower or 'try' in code_lower:
                return LanguageSupport.get_language_info('python')

        # ===== TYPESCRIPT =====
        ts_patterns = ['interface ', 'type ', 'enum ', ': string', ': number', ': boolean', ': any', ': void']
        for pattern in ts_patterns:
            if pattern in code_lower:
                return LanguageSupport.get_language_info('typescript')

        # ===== JAVASCRIPT =====
        if 'function ' in code_lower or 'const ' in code_lower or 'let ' in code_lower:
            if '=>' in code_lower or 'console.log' in code_lower:
                return LanguageSupport.get_language_info('javascript')

        # ===== JAVA =====
        if 'public class' in code_lower and 'void' in code_lower and 'static' in code_lower:
            if 'public static void main' in code_lower:
                return LanguageSupport.get_language_info('java')

        # ===== C# =====
        if 'using system' in code_lower or 'namespace ' in code_lower:
            if 'class ' in code_lower and 'static void main' in code_lower:
                return LanguageSupport.get_language_info('csharp')

        # ===== C/C++ =====
        if '#include' in code_lower:
            if 'printf' in code_lower or 'scanf' in code_lower:
                return LanguageSupport.get_language_info('c')
            if 'cout' in code_lower or 'cin' in code_lower:
                return LanguageSupport.get_language_info('cpp')
            return LanguageSupport.get_language_info('cpp')

        # ===== GO =====
        if 'package main' in code_lower or ('func ' in code_lower and 'import ' in code_lower):
            if 'fmt.println' in code_lower or 'fmt.printf' in code_lower:
                return LanguageSupport.get_language_info('go')

        # ===== RUST =====
        if 'fn ' in code_lower and 'let ' in code_lower and 'mut ' in code_lower:
            if 'println!' in code_lower:
                return LanguageSupport.get_language_info('rust')

        # ===== RUBY =====
        if 'class ' in code_lower and 'module ' in code_lower:
            if 'def ' in code_lower and 'end' in code_lower:
                return LanguageSupport.get_language_info('ruby')

        # ===== PHP =====
        if '<?php' in code_lower or '<?=' in code_lower:
            return LanguageSupport.get_language_info('php')

        # ===== SWIFT =====
        if 'func ' in code_lower and 'struct ' in code_lower and 'protocol ' in code_lower:
            return LanguageSupport.get_language_info('swift')

        # ===== KOTLIN =====
        if 'fun ' in code_lower and 'data class' in code_lower:
            if 'val ' in code_lower or 'var ' in code_lower:
                return LanguageSupport.get_language_info('kotlin')

        # ===== SCALA =====
        if 'object ' in code_lower and 'trait ' in code_lower:
            return LanguageSupport.get_language_info('scala')

        # ===== PERL =====
        if 'sub ' in code_lower and 'my ' in code_lower:
            return LanguageSupport.get_language_info('perl')

        # ===== LUA =====
        if 'function ' in code_lower and 'local ' in code_lower and 'table ' in code_lower:
            return LanguageSupport.get_language_info('lua')

        # ===== R =====
        if 'function(' in code_lower and '<-' in code_lower:
            return LanguageSupport.get_language_info('r')

        # ===== DART =====
        if 'void main()' in code_lower or 'void main(' in code_lower:
            return LanguageSupport.get_language_info('dart')

        # ===== ELIXIR =====
        if 'defmodule ' in code_lower:
            return LanguageSupport.get_language_info('elixir')

        # ===== HASKELL =====
        if 'module ' in code_lower and 'data ' in code_lower:
            return LanguageSupport.get_language_info('haskell')

        # ===== JULIA =====
        if 'function ' in code_lower and 'struct ' in code_lower and 'module ' in code_lower:
            return LanguageSupport.get_language_info('julia')

        # ===== SHELL =====
        if '#!/bin/bash' in code_lower or '#!/usr/bin/env bash' in code_lower:
            return LanguageSupport.get_language_info('shell')

        # ===== SQL =====
        sql_keywords = ['select ', 'insert ', 'update ', 'delete ', 'create table', 'alter table']
        for keyword in sql_keywords:
            if keyword in code_lower:
                if not any(p in code_lower for p in ['def ', 'import ', 'from ', 'print(']):
                    return LanguageSupport.get_language_info('sql')

        # ===== HTML =====
        if '<!doctype html' in code_lower or '<html' in code_lower:
            return LanguageSupport.get_language_info('html')

        # ===== CSS =====
        if '{' in code and ':' in code and ';' in code:
            css_props = ['color:', 'background:', 'font-size:', 'margin:', 'padding:']
            for prop in css_props:
                if prop in code_lower:
                    return LanguageSupport.get_language_info('css')

        # ===== JSON =====
        if '{' in code and ':' in code and '"' in code and '}' in code:
            try:
                json.loads(code)
                return LanguageSupport.get_language_info('json')
            except Exception:
                pass

        # ===== YAML =====
        if '---' in code and ':' in code:
            if '- ' in code or 'true' in code_lower or 'false' in code_lower:
                return LanguageSupport.get_language_info('yaml')

        # ===== XML =====
        if '<?xml' in code_lower or ('<' in code and '</' in code):
            return LanguageSupport.get_language_info('xml')

        # ===== MARKDOWN =====
        if '#' in code and '```' in code:
            if '**' in code or '_' in code:
                return LanguageSupport.get_language_info('markdown')

        return LanguageSupport.get_language_info('python')

    @staticmethod
    def get_language_info(lang_key: str) -> Dict[str, Any]:
        """Get language information by key"""
        lang_key = lang_key.lower()
        lang_info = LanguageSupport.SUPPORTED_LANGUAGES.get(lang_key, {})
        if not lang_info:
            lang_info = dict(LanguageSupport.SUPPORTED_LANGUAGES['python'])
        else:
            lang_info = dict(lang_info)
        lang_info['key'] = lang_key
        return lang_info

    @staticmethod
    def get_all_languages() -> List[Dict[str, Any]]:
        """Get all supported languages"""
        languages = []
        for key, info in LanguageSupport.SUPPORTED_LANGUAGES.items():
            languages.append({
                'key': key,
                'name': info['name'],
                'extensions': info.get('extensions', []),
                'full_support': info.get('full_support', True)
            })
        return languages


# ============================================================
# DETECT LANGUAGE VIEW
# ============================================================

class DetectLanguageView(APIView):
    """Use Gemini to detect programming language"""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        code = request.data.get('code', '')

        if isinstance(code, dict):
            code = code.get('code', '')
        code = str(code)

        if not code or not code.strip():
            return Response({
                'status': 'error',
                'message': 'No code provided'
            }, status=status.HTTP_400_BAD_REQUEST)

        print("[DEBUG] DetectLanguageView called")
        print(f"[DEBUG] Code length: {len(code)}")

        # Try Gemini detection first
        try:
            print("[DEBUG] Trying Gemini detection...")
            gemini_result = LLMAnalyzer.detect_language_with_gemini(code)
            print(f"[DEBUG] Gemini result: {gemini_result}")

            if gemini_result and gemini_result.get('language') and gemini_result.get('method') == 'gemini':
                return Response({
                    'status': 'success',
                    'language': gemini_result['language'],
                    'confidence': gemini_result.get('confidence', 85),
                    'method': 'gemini',
                    'extensions': gemini_result.get('extensions', [])
                }, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"[DEBUG] Gemini detection failed: {e}")
            logger.error(f"Gemini detection failed: {e}")

        # Fallback to static
        print("[DEBUG] Falling back to static detection...")
        fallback = LanguageSupport.detect_language(code)
        return Response({
            'status': 'success',
            'language': fallback.get('name', 'Python'),
            'confidence': 60,
            'method': 'static_fallback',
            'key': fallback.get('key', 'python')
        }, status=status.HTTP_200_OK)


# ============================================================
# SYNTAX ERROR DETECTOR
# ============================================================

class SyntaxErrorDetector:
    """Detect syntax errors in multiple languages"""

    @staticmethod
    def detect_syntax_errors(code: str, language: str) -> List[Dict]:
        errors = []
        lang = language.lower().strip()

        if lang in ['python', 'py']:
            try:
                ast.parse(code)
            except SyntaxError as e:
                errors.append({
                    'line': e.lineno or 1,
                    'message': 'Syntax Error: ' + str(e),
                    'suggestion': 'Fix the syntax error'
                })
            except Exception:
                pass

        elif lang in ['javascript', 'js', 'typescript', 'ts']:
            lines = code.split('\n')
            for i, line in enumerate(lines, 1):
                stripped = line.strip()
                if not stripped or stripped.startswith(('//', '/*')):
                    continue
                if stripped.count("'") % 2 != 0 or stripped.count('"') % 2 != 0:
                    errors.append({
                        'line': i,
                        'message': 'Syntax Error: Unterminated string literal',
                        'suggestion': 'Close string with matching quote'
                    })
                    break
                if stripped.count('(') != stripped.count(')'):
                    errors.append({
                        'line': i,
                        'message': 'Syntax Error: Unmatched parentheses',
                        'suggestion': 'Check for matching parentheses'
                    })
                    break
                if stripped.count('{') != stripped.count('}'):
                    errors.append({
                        'line': i,
                        'message': 'Syntax Error: Unmatched braces',
                        'suggestion': 'Check for matching braces'
                    })
                    break

        elif lang in ['c', 'java', 'cpp', 'c++', 'csharp', 'cs', 'go', 'rust', 'scala', 'kotlin', 'dart']:
            lines = code.split('\n')
            brace_count = 0
            for i, line in enumerate(lines, 1):
                stripped = line.strip()
                if stripped.startswith(('//', '/*')):
                    continue
                brace_count += stripped.count('{')
                brace_count -= stripped.count('}')
            if brace_count > 0:
                errors.append({
                    'line': len(lines),
                    'message': 'Syntax Error: Unclosed braces',
                    'suggestion': 'Check for missing closing braces'
                })
            if brace_count < 0:
                errors.append({
                    'line': 1,
                    'message': 'Syntax Error: Extra closing braces',
                    'suggestion': 'Check for extra closing braces'
                })

        elif lang in ['ruby']:
            lines = code.split('\n')
            for i, line in enumerate(lines, 1):
                stripped = line.strip()
                if stripped.startswith('#'):
                    continue
                if 'def ' in stripped and 'end' not in stripped:
                    if not any('end' in l for l in lines[i:min(i + 10, len(lines))]):
                        errors.append({
                            'line': i,
                            'message': 'Syntax Error: Missing end keyword',
                            'suggestion': 'Add end after method body'
                        })
                        break

        elif lang in ['php']:
            lines = code.split('\n')
            for i, line in enumerate(lines, 1):
                stripped = line.strip()
                if '<?php' in stripped and '?>' not in stripped:
                    if not any('?>' in l for l in lines[i:min(i + 5, len(lines))]):
                        errors.append({
                            'line': i,
                            'message': 'PHP code block not closed',
                            'suggestion': 'Close with ?>'
                        })
                        break

        elif lang in ['sql']:
            lines = code.split('\n')
            for i, line in enumerate(lines, 1):
                stripped = line.strip().upper()
                if 'SELECT' in stripped and 'FROM' not in stripped:
                    if ';' not in line:
                        errors.append({
                            'line': i,
                            'message': 'Possible incomplete SQL statement',
                            'suggestion': 'Check SQL syntax'
                        })
                        break

        elif lang in ['html']:
            lines = code.split('\n')
            if '<html>' in code.lower() and '</html>' not in code.lower():
                errors.append({
                    'line': len(lines),
                    'message': 'HTML tag not closed',
                    'suggestion': 'Close all HTML tags'
                })

        elif lang in ['json']:
            try:
                json.loads(code)
            except json.JSONDecodeError as e:
                errors.append({
                    'line': e.lineno or 1,
                    'message': f'JSON Syntax Error: {e.msg}',
                    'suggestion': 'Fix JSON structure'
                })

        return errors


# ============================================================
# TEST EXECUTOR
# ============================================================

class TestExecutor:
    """Execute test cases for multiple languages"""

    @staticmethod
    def execute_test_cases(code: str, test_cases: List[Dict], language: str = 'python') -> List[Dict]:
        results = []
        for test_case in test_cases:
            result = TestExecutor._execute_single_test(code, test_case, language)
            results.append(result)
        return results

    @staticmethod
    def _execute_single_test(code: str, test_case: Dict, language: str) -> Dict:
        test_code = test_case.get('test_code', '')
        func_name = test_case.get('function', '')
        passed = False
        output = ""
        error = None

        lang = language.lower().strip()

        try:
            if lang in ['python', 'py']:
                full_code = code + "\n\n" + test_code
                with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                    f.write(full_code)
                    f.flush()
                    temp_file = f.name

                try:
                    result = subprocess.run(
                        ['python', temp_file],
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                    passed = result.returncode == 0
                    output = result.stdout
                    error = result.stderr if not passed else None
                finally:
                    try:
                        os.unlink(temp_file)
                    except Exception:
                        pass

            elif lang in ['javascript', 'js', 'typescript', 'ts']:
                full_code = code + "\n\n" + test_code
                with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
                    f.write(full_code)
                    f.flush()
                    temp_file = f.name

                try:
                    result = subprocess.run(
                        ['node', temp_file],
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                    passed = result.returncode == 0
                    output = result.stdout
                    error = result.stderr if not passed else None
                except FileNotFoundError:
                    error = "Node.js not found"
                finally:
                    try:
                        os.unlink(temp_file)
                    except Exception:
                        pass

            elif lang in ['java']:
                full_code = code + "\n\n" + test_code
                class_match = re.search(r'public\s+class\s+(\w+)', full_code)
                if class_match:
                    class_name = class_match.group(1)
                    with tempfile.NamedTemporaryFile(mode='w', suffix='.java', delete=False) as f:
                        f.write(full_code)
                        f.flush()
                        temp_file = f.name

                    try:
                        compile_result = subprocess.run(
                            ['javac', temp_file],
                            capture_output=True,
                            text=True,
                            timeout=5
                        )

                        if compile_result.returncode == 0:
                            run_result = subprocess.run(
                                ['java', '-cp', os.path.dirname(temp_file), class_name],
                                capture_output=True,
                                text=True,
                                timeout=5
                            )
                            passed = run_result.returncode == 0
                            output = run_result.stdout
                            error = run_result.stderr if not passed else None
                        else:
                            error = compile_result.stderr
                    except FileNotFoundError:
                        error = "Java not found"
                    finally:
                        try:
                            os.unlink(temp_file)
                            class_file = temp_file.replace('.java', '.class')
                            if os.path.exists(class_file):
                                os.unlink(class_file)
                        except Exception:
                            pass

            elif lang in ['cpp', 'c++', 'c']:
                full_code = code + "\n\n" + test_code
                with tempfile.NamedTemporaryFile(mode='w', suffix='.cpp', delete=False) as f:
                    f.write(full_code)
                    f.flush()
                    temp_file = f.name

                try:
                    compile_result = subprocess.run(
                        ['g++', temp_file, '-o', temp_file + '.out'],
                        capture_output=True,
                        text=True,
                        timeout=5
                    )

                    if compile_result.returncode == 0:
                        run_result = subprocess.run(
                            [temp_file + '.out'],
                            capture_output=True,
                            text=True,
                            timeout=5
                        )
                        passed = run_result.returncode == 0
                        output = run_result.stdout
                        error = run_result.stderr if not passed else None
                    else:
                        error = compile_result.stderr
                except FileNotFoundError:
                    error = "G++ not found"
                finally:
                    try:
                        os.unlink(temp_file)
                        if os.path.exists(temp_file + '.out'):
                            os.unlink(temp_file + '.out')
                    except Exception:
                        pass

            elif lang in ['rust']:
                full_code = code + "\n\n" + test_code
                with tempfile.NamedTemporaryFile(mode='w', suffix='.rs', delete=False) as f:
                    f.write(full_code)
                    f.flush()
                    temp_file = f.name

                try:
                    compile_result = subprocess.run(
                        ['rustc', temp_file, '-o', temp_file + '.out'],
                        capture_output=True,
                        text=True,
                        timeout=5
                    )

                    if compile_result.returncode == 0:
                        run_result = subprocess.run(
                            [temp_file + '.out'],
                            capture_output=True,
                            text=True,
                            timeout=5
                        )
                        passed = run_result.returncode == 0
                        output = run_result.stdout
                        error = run_result.stderr if not passed else None
                    else:
                        error = compile_result.stderr
                except FileNotFoundError:
                    error = "Rustc not found"
                finally:
                    try:
                        os.unlink(temp_file)
                        if os.path.exists(temp_file + '.out'):
                            os.unlink(temp_file + '.out')
                    except Exception:
                        pass

            elif lang in ['go']:
                full_code = code + "\n\n" + test_code
                with tempfile.TemporaryDirectory() as temp_dir:
                    main_path = os.path.join(temp_dir, 'main.go')
                    with open(main_path, 'w') as f:
                        f.write(full_code)

                    try:
                        result = subprocess.run(
                            ['go', 'run', main_path],
                            capture_output=True,
                            text=True,
                            timeout=5
                        )
                        passed = result.returncode == 0
                        output = result.stdout
                        error = result.stderr if not passed else None
                    except FileNotFoundError:
                        error = "Go not found"

            elif lang in ['ruby']:
                full_code = code + "\n\n" + test_code
                with tempfile.NamedTemporaryFile(mode='w', suffix='.rb', delete=False) as f:
                    f.write(full_code)
                    f.flush()
                    temp_file = f.name

                try:
                    result = subprocess.run(
                        ['ruby', temp_file],
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                    passed = result.returncode == 0
                    output = result.stdout
                    error = result.stderr if not passed else None
                except FileNotFoundError:
                    error = "Ruby not found"
                finally:
                    try:
                        os.unlink(temp_file)
                    except Exception:
                        pass

            elif lang in ['php']:
                full_code = code + "\n\n" + test_code
                with tempfile.NamedTemporaryFile(mode='w', suffix='.php', delete=False) as f:
                    f.write(full_code)
                    f.flush()
                    temp_file = f.name

                try:
                    result = subprocess.run(
                        ['php', temp_file],
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                    passed = result.returncode == 0
                    output = result.stdout
                    error = result.stderr if not passed else None
                except FileNotFoundError:
                    error = "PHP not found"
                finally:
                    try:
                        os.unlink(temp_file)
                    except Exception:
                        pass

            elif lang in ['swift']:
                full_code = code + "\n\n" + test_code
                with tempfile.NamedTemporaryFile(mode='w', suffix='.swift', delete=False) as f:
                    f.write(full_code)
                    f.flush()
                    temp_file = f.name

                try:
                    result = subprocess.run(
                        ['swift', temp_file],
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                    passed = result.returncode == 0
                    output = result.stdout
                    error = result.stderr if not passed else None
                except FileNotFoundError:
                    error = "Swift not found"
                finally:
                    try:
                        os.unlink(temp_file)
                    except Exception:
                        pass

            elif lang in ['kotlin']:
                full_code = code + "\n\n" + test_code
                with tempfile.NamedTemporaryFile(mode='w', suffix='.kt', delete=False) as f:
                    f.write(full_code)
                    f.flush()
                    temp_file = f.name

                try:
                    compile_result = subprocess.run(
                        ['kotlinc', temp_file, '-include-runtime', '-d', temp_file + '.jar'],
                        capture_output=True,
                        text=True,
                        timeout=5
                    )

                    if compile_result.returncode == 0:
                        run_result = subprocess.run(
                            ['java', '-jar', temp_file + '.jar'],
                            capture_output=True,
                            text=True,
                            timeout=5
                        )
                        passed = run_result.returncode == 0
                        output = run_result.stdout
                        error = run_result.stderr if not passed else None
                    else:
                        error = compile_result.stderr
                except FileNotFoundError:
                    error = "Kotlin not found"
                finally:
                    try:
                        os.unlink(temp_file)
                        if os.path.exists(temp_file + '.jar'):
                            os.unlink(temp_file + '.jar')
                    except Exception:
                        pass

            else:
                return {
                    'name': test_case.get('name', 'test'),
                    'function': func_name,
                    'input': test_case.get('input', {}),
                    'expected': test_case.get('expected', 'N/A'),
                    'actual': 'Not executed',
                    'passed': True,
                    'error': None,
                    'test_code': test_code
                }

        except Exception as e:
            error = str(e)

        return {
            'name': test_case.get('name', 'test'),
            'function': func_name,
            'input': test_case.get('input', {}),
            'expected': test_case.get('expected', 'N/A'),
            'actual': output if not error else error,
            'passed': passed,
            'error': error,
            'test_code': test_code
        }


# ============================================================
# VIEWS - ALL VIEWS
# ============================================================

class ProgrammingLanguageListView(generics.ListAPIView):
    """List all programming languages"""
    queryset = ProgrammingLanguage.objects.filter(is_active=True)
    serializer_class = ProgrammingLanguageSerializer
    permission_classes = [permissions.AllowAny]


class CodeSubmissionListView(generics.ListCreateAPIView):
    """List and create code submissions"""
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
        code = request.data.get('code', '')

        # ===== USE GEMINI FOR LANGUAGE DETECTION =====
        lang_name = 'Python'
        detection_method = 'default'

        try:
            gemini_result = LLMAnalyzer.detect_language_with_gemini(code)
            if gemini_result and gemini_result.get('language'):
                lang_name = gemini_result['language']
                detection_method = 'gemini'
                print(f"[DEBUG] Gemini detected language: {lang_name}")
            else:
                static_lang = LanguageSupport.detect_language(code)
                lang_name = static_lang.get('name', 'Python')
                detection_method = 'static'
                print(f"[DEBUG] Static detected language: {lang_name}")
        except Exception as e:
            print(f"[DEBUG] Language detection failed: {e}")
            static_lang = LanguageSupport.detect_language(code)
            lang_name = static_lang.get('name', 'Python')
            detection_method = 'fallback'

        lang_obj = ProgrammingLanguage.objects.filter(name__iexact=lang_name).first()
        if not lang_obj:
            lang_obj = ProgrammingLanguage.objects.create(
                name=lang_name,
                is_active=True
            )

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            submission = serializer.save(language=lang_obj)
            response_data = CodeSubmissionSerializer(submission).data
            response_data['detected_language'] = {
                'name': lang_name,
                'method': detection_method
            }
            headers = self.get_success_headers(serializer.data)
            return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CodeSubmissionDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Get, update, or delete a code submission"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CodeSubmissionSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        user = self.request.user
        if getattr(user, 'user_type', None) == 'admin':
            return CodeSubmission.objects.all()
        return CodeSubmission.objects.filter(user=user)


class CodeSubmissionStatusView(APIView):
    """Update submission status"""
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk):
        submission = get_object_or_404(CodeSubmission, pk=pk)

        if getattr(request.user, 'user_type', None) != 'admin' and submission.user != request.user:
            return Response({
                'status': 'error',
                'message': 'Permission denied'
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
    """List review history"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ReviewHistorySerializer

    def get_queryset(self):
        user = self.request.user
        if getattr(user, 'user_type', None) == 'admin':
            return ReviewHistory.objects.all()
        return ReviewHistory.objects.filter(user=user)


class ReviewHistoryDetailView(generics.RetrieveAPIView):
    """Get review history details"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ReviewHistorySerializer

    def get_queryset(self):
        user = self.request.user
        if getattr(user, 'user_type', None) == 'admin':
            return ReviewHistory.objects.all()
        return ReviewHistory.objects.filter(user=user)


class CodeReviewCommentView(generics.ListCreateAPIView):
    """List and create review comments"""
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
    """List and create code snippets"""
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
    """Get, update, or delete a code snippet"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CodeSnippetSerializer

    def get_queryset(self):
        user = self.request.user
        return CodeSnippet.objects.filter(user=user)


class CodeReviewStatsView(APIView):
    """Get code review statistics"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user

        try:
            submissions = CodeSubmission.objects.filter(user=user)

            stats = {
                'total_submissions': submissions.count(),
                'completed_reviews': submissions.filter(status='completed').count(),
                'pending_reviews': submissions.filter(status='pending').count(),
                'processing_reviews': submissions.filter(status='processing').count(),
                'failed_reviews': submissions.filter(status='failed').count(),
                'average_quality_score': round(
                    submissions.filter(status='completed').aggregate(avg=Avg('quality_score'))['avg'] or 0, 1
                ),
                'total_bugs_found': submissions.aggregate(Sum('bug_count'))['bug_count__sum'] or 0,
                'total_issues_found': submissions.aggregate(Sum('issue_count'))['issue_count__sum'] or 0,
                'total_suggestions': submissions.aggregate(Sum('suggestion_count'))['suggestion_count__sum'] or 0,
                'supported_languages': LanguageSupport.get_all_languages()
            }

            return Response({
                'status': 'success',
                'data': stats
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class LanguageSupportView(APIView):
    """Get all supported languages"""
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        languages = LanguageSupport.get_all_languages()

        return Response({
            'status': 'success',
            'total_languages': len(languages),
            'languages': languages,
            'summary': {
                'fully_supported': len([l for l in languages if l['full_support']]),
            }
        }, status=status.HTTP_200_OK)


class LLMStatusView(APIView):
    """Check LLM configuration and status"""
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        config = {
            'llm_configured': bool(getattr(settings, 'GEMINI_API_KEY', None)),
            'llm_model': 'gemini-3.1-flash-lite',
            'gemini_available': self._check_gemini_available(),
            'total_languages_supported': len(LanguageSupport.SUPPORTED_LANGUAGES),
            'active_provider': 'gemini' if self._check_gemini_available() else 'static'
        }

        return Response({
            'status': 'success',
            'data': config
        }, status=status.HTTP_200_OK)

    def _check_gemini_available(self):
        try:
            from google import genai
            return True
        except ImportError:
            return False


# ============================================================
# MAIN CODE REVIEW VIEW - LIKE CHATGPT ANALYSIS
# ============================================================

class InitiateCodeReviewView(APIView):
    """Initiate code review with Gemini - Like ChatGPT analysis"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        submission_id = request.data.get('submission_id')
        use_llm = request.data.get('use_llm', True)
        full_analysis = request.data.get('full_analysis', True)

        if not submission_id:
            return Response({
                'status': 'error',
                'message': 'submission_id is required'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            submission = CodeSubmission.objects.get(id=submission_id, user=request.user)
        except CodeSubmission.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Submission not found'
            }, status=status.HTTP_404_NOT_FOUND)

        submission.status = 'processing'
        submission.save()

        gemini_available = bool(getattr(settings, 'GEMINI_API_KEY', None))

        if use_llm and not gemini_available:
            logger.warning("Gemini requested but not available, using static analysis")
            use_llm = False

        try:
            # Detect language
            lang_info = None
            llm_detected = False

            if use_llm and gemini_available:
                try:
                    gemini_lang = LLMAnalyzer.detect_language_with_gemini(submission.code)
                    if gemini_lang and gemini_lang.get('language'):
                        lang_info = {
                            'name': gemini_lang['language'],
                            'key': gemini_lang['language'].lower(),
                            'confidence': gemini_lang.get('confidence', 85),
                            'method': 'gemini'
                        }
                        llm_detected = True
                        logger.info(f"Gemini detected language: {lang_info['name']}")
                except Exception as e:
                    logger.error(f"Gemini language detection failed: {e}")

            if not lang_info:
                static_lang = LanguageSupport.detect_language(submission.code)
                lang_info = {
                    'name': static_lang.get('name', 'Python'),
                    'key': static_lang.get('key', 'python'),
                    'confidence': 60,
                    'method': 'static'
                }

            language_name = lang_info['name']

            # Detect syntax errors
            syntax_errors = SyntaxErrorDetector.detect_syntax_errors(
                submission.code,
                language_name
            )

            # ===== GEMINI ANALYSIS - LIKE CHATGPT =====
            bugs = []
            issues = []
            suggestions = []
            test_cases = []
            quality_score = 50
            summary = ""
            detailed_analysis = ""

            if use_llm and gemini_available:
                try:
                    logger.info(f"Starting ChatGPT-like analysis for submission {submission.id}")

                    # Use Gemini for complete analysis
                    gemini_result = LLMAnalyzer.analyze_like_chatgpt(
                        submission.code,
                        language_name
                    )

                    bugs = gemini_result.get('bugs', [])
                    issues = gemini_result.get('issues', [])
                    suggestions = gemini_result.get('suggestions', [])
                    test_cases = gemini_result.get('test_cases', [])
                    quality_score = gemini_result.get('quality_score', 50)
                    summary = gemini_result.get('summary', '')
                    detailed_analysis = gemini_result.get('detailed_analysis', '')

                    logger.info(f"Gemini found: {len(bugs)} bugs, {len(issues)} issues, "
                                f"{len(suggestions)} suggestions, {len(test_cases)} test cases")

                except Exception as e:
                    logger.error(f"Gemini analysis failed: {e}")

                    # Fallback to static
                    static_bugs, static_issues, static_suggestions = self._static_analysis(
                        submission.code,
                        language_name
                    )
                    bugs = static_bugs
                    issues = static_issues
                    suggestions = static_suggestions
                    quality_score = self._calculate_static_score(bugs)
                    summary = "Static analysis completed (Gemini failed)"
            else:
                # Static analysis fallback
                static_bugs, static_issues, static_suggestions = self._static_analysis(
                    submission.code,
                    language_name
                )
                bugs = static_bugs
                issues = static_issues
                suggestions = static_suggestions
                quality_score = self._calculate_static_score(bugs)
                summary = "Static analysis completed"

            # ===== EXECUTE TESTS =====
            test_results = []
            if test_cases:
                test_results = TestExecutor.execute_test_cases(
                    submission.code,
                    test_cases,
                    language_name
                )
            elif full_analysis and not syntax_errors:
                # Generate basic tests if Gemini didn't provide any
                basic_tests = self._generate_basic_tests(submission.code, language_name)
                if basic_tests:
                    test_results = TestExecutor.execute_test_cases(
                        submission.code,
                        basic_tests,
                        language_name
                    )

            # ===== CREATE REVIEW =====
            review = ReviewHistory.objects.create(
                submission=submission,
                user=request.user,
                quality_score=quality_score,
                bugs=bugs,
                issues=issues,
                suggestions=suggestions,
                explanation=self._generate_chatgpt_style_explanation(
                    bugs, issues, suggestions,
                    quality_score, use_llm, language_name,
                    syntax_errors, test_results, summary,
                    detailed_analysis, llm_detected, lang_info
                ),
                test_cases=test_results,
                ai_provider='gemini' if use_llm else 'static_analysis',
                ai_model='gemini-3.1-flash-lite' if use_llm else 'built-in'
            )

            # ===== UPDATE SUBMISSION =====
            submission.status = 'completed'
            submission.quality_score = quality_score
            submission.bug_count = len(bugs)
            submission.issue_count = len(issues)
            submission.suggestion_count = len(suggestions)
            submission.reviewed_at = timezone.now()
            submission.analysis_result = {
                'bugs': bugs,
                'issues': issues,
                'suggestions': suggestions,
                'test_cases': test_results,
                'syntax_errors': syntax_errors,
                'quality_score': quality_score,
                'use_llm': use_llm,
                'llm_enabled': gemini_available,
                'llm_model': 'gemini-3.1-flash-lite' if use_llm else None,
                'language': language_name,
                'language_info': lang_info,
                'language_detection_method': lang_info.get('method', 'static'),
                'llm_detected': llm_detected,
                'analysis_time': timezone.now().isoformat(),
                'summary': summary,
                'detailed_analysis': detailed_analysis,
            }
            submission.save()

            # ===== RETURN RESPONSE =====
            return Response({
                'status': 'success',
                'message': 'Code review completed successfully!',
                'submission_id': str(submission.id),
                'review_id': str(review.id),
                'quality_score': quality_score,
                'bugs_found': len(bugs),
                'issues_found': len(issues),
                'suggestions': len(suggestions),
                'syntax_errors': syntax_errors,
                'has_syntax_errors': len(syntax_errors) > 0,
                'use_llm': use_llm,
                'llm_enabled': gemini_available,
                'language': language_name,
                'language_detection': {
                    'method': lang_info.get('method', 'static'),
                    'confidence': lang_info.get('confidence', 0),
                    'llm_detected': llm_detected
                },
                'language_support': lang_info,
                'test_summary': {
                    'total': len(test_results),
                    'passed': len([t for t in test_results if t.get('passed')]),
                    'failed': len([t for t in test_results if not t.get('passed')])
                },
                'test_cases': test_results,
                'bugs': bugs,
                'issues': issues,
                'suggestions': suggestions,
                'explanation': review.explanation,
                'summary': summary,
                'detailed_analysis': detailed_analysis,
                'analysis_metadata': {
                    'llm_used': use_llm and gemini_available,
                    'static_analysis_used': not use_llm or not gemini_available,
                    'total_issues_found': len(bugs) + len(issues) + len(suggestions),
                    'test_cases_generated': len(test_cases) if use_llm else 0,
                }
            }, status=status.HTTP_200_OK)

        except Exception as e:
            submission.status = 'failed'
            submission.save()
            logger.error(f"Analysis failed: {traceback.format_exc()}")
            return Response({
                'status': 'error',
                'message': 'Analysis failed: ' + str(e),
                'traceback': traceback.format_exc() if settings.DEBUG else None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def _static_analysis(self, code: str, language: str) -> tuple:
        """Static code analysis - used only when Gemini is not available"""
        bugs = []
        issues = []
        suggestions = []
        lines = code.split('\n')
        found_bugs = set()

        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if not stripped or stripped.startswith(('#', '//', '/*', '--')):
                continue

            # Hardcoded credentials
            cred_patterns = ['API_KEY', 'PASSWORD', 'SECRET', 'AWS_', 'TOKEN', 'KEY', 'SECRET_KEY']
            for pattern in cred_patterns:
                if pattern in line.upper() and '=' in line and ('"' in line or "'" in line):
                    key = 'cred_' + str(i)
                    if key not in found_bugs:
                        bugs.append({
                            'line': i,
                            'description': f'Hardcoded credential detected: {pattern}',
                            'severity': 'critical',
                            'suggestion': 'Use environment variables or secrets manager',
                            'source': 'static'
                        })
                        found_bugs.add(key)
                    break

            # Division by zero
            if '/' in line and ('/0' in line or '/ 0' in line):
                key = 'div_zero_' + str(i)
                if key not in found_bugs:
                    bugs.append({
                        'line': i,
                        'description': 'Division by zero detected',
                        'severity': 'critical',
                        'suggestion': 'Check denominator before division',
                        'source': 'static'
                    })
                    found_bugs.add(key)

            # Dangerous functions
            dangerous_funcs = ['eval(', 'exec(', 'system(', 'shell_exec(', 'popen(', 'subprocess.call']
            for func in dangerous_funcs:
                if func in line:
                    key = 'dangerous_' + str(i)
                    if key not in found_bugs:
                        bugs.append({
                            'line': i,
                            'description': f'Dangerous function {func} detected',
                            'severity': 'critical',
                            'suggestion': 'Avoid using dangerous functions',
                            'source': 'static'
                        })
                        found_bugs.add(key)
                    break

            # SQL Injection
            sql_patterns = ['SELECT', 'INSERT', 'UPDATE', 'DELETE']
            for pattern in sql_patterns:
                if pattern in line.upper() and ('+' in line or '%' in line):
                    key = 'sql_' + str(i)
                    if key not in found_bugs:
                        bugs.append({
                            'line': i,
                            'description': f'Potential SQL Injection vulnerability with {pattern}',
                            'severity': 'critical',
                            'suggestion': 'Use parameterized queries or ORM',
                            'source': 'static'
                        })
                        found_bugs.add(key)
                    break

        return bugs, issues, suggestions

    def _calculate_static_score(self, bugs: List) -> int:
        """Calculate quality score from bugs"""
        score = 100
        for bug in bugs:
            severity = bug.get('severity', 'medium')
            if severity == 'critical':
                score -= 15
            elif severity == 'high':
                score -= 10
            elif severity == 'medium':
                score -= 5
            else:
                score -= 2
        return max(20, min(100, score))

    def _generate_basic_tests(self, code: str, language: str) -> List[Dict]:
        """Generate basic test cases statically"""
        test_cases = []
        lang = language.lower().strip()

        if lang in ['python', 'py']:
            func_matches = re.findall(r'def\s+(\w+)\s*\(([^)]*)\)', code)
            for func_name, params in func_matches:
                if func_name.startswith('_') or func_name == 'main':
                    continue
                param_list = [p.split(':')[0].strip() for p in params.split(',') if p.strip()]
                test_inputs = {p: 'test_value' for p in param_list}
                args_str = ', '.join([f'{k}="{v}"' for k, v in test_inputs.items()])
                test_code = (
                    f"def test_{func_name}():\n"
                    f"    try:\n"
                    f"        result = {func_name}({args_str})\n"
                    f"        print('PASS: {func_name} passed')\n"
                    f"        return True\n"
                    f"    except Exception as e:\n"
                    f"        print('FAIL: {func_name} failed:', e)\n"
                    f"        return False\n\n"
                    f"if __name__ == '__main__':\n"
                    f"    test_{func_name}()\n"
                )
                test_cases.append({
                    'name': f'test_{func_name}',
                    'function': func_name,
                    'input': test_inputs,
                    'expected': 'Function executes without errors',
                    'test_code': test_code,
                    'passed': None
                })

        return test_cases

    def _generate_chatgpt_style_explanation(self, bugs, issues, suggestions, score, use_llm,
                                             language, syntax_errors, test_results, summary,
                                             detailed_analysis, llm_detected, lang_info) -> str:
        """Generate ChatGPT-style explanation"""

        detection_method = "Gemini (AI)" if llm_detected else "Static"
        confidence = lang_info.get('confidence', 0)

        explanation = f"""
╔══════════════════════════════════════════════════════════════╗
║ CODE REVIEW REPORT - {language.upper()}
║ (AI-POWERED ANALYSIS)
╚══════════════════════════════════════════════════════════════╝

📊 QUALITY SCORE: {score}/100

🔍 ANALYSIS SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Language Detected: {language}
Detection Method: {detection_method} (Confidence: {confidence}%)
Analysis Method: {'🤖 Gemini AI' if use_llm else '📊 Static Analysis'}
Bugs Found: {len(bugs)}
Issues Found: {len(issues)}
Suggestions Made: {len(suggestions)}
Syntax Errors: {len(syntax_errors)}
Test Cases Generated: {len(test_results)}
Tests Passed: {len([t for t in test_results if t.get('passed')])}
Tests Failed: {len([t for t in test_results if not t.get('passed')])}

{'✅ NO SYNTAX ERRORS DETECTED' if not syntax_errors else '❌ SYNTAX ERRORS FOUND'}

"""

        if use_llm:
            explanation += f"""
📝 DETAILED ANALYSIS (AI-GENERATED)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{detailed_analysis if detailed_analysis else summary}

"""

        if bugs:
            explanation += f"""
🐛 CRITICAL BUGS FOUND ({len(bugs)})
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
            for idx, bug in enumerate(bugs, 1):
                line = bug.get('line', '?')
                severity = bug.get('severity', 'unknown').upper()
                desc = bug.get('description', '')
                suggestion = bug.get('suggestion', '')
                category = bug.get('category', 'general')
                source = bug.get('source', 'gemini')
                source_label = '🤖 Gemini' if source == 'gemini' else '🔧 Static'
                explanation += f"""
Bug #{idx} - Line {line} [{severity}] {source_label}
└─ Category: {category}
   Issue: {desc}
   💡 Fix: {suggestion}
"""
        else:
            explanation += """
✅ NO BUGS FOUND! Code looks clean.

"""

        if issues:
            explanation += f"""
⚠️ ISSUES FOUND ({len(issues)})
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
            for idx, issue in enumerate(issues, 1):
                line = issue.get('line', '?')
                severity = issue.get('severity', 'unknown').upper()
                desc = issue.get('description', '')
                suggestion = issue.get('suggestion', '')
                source = issue.get('source', 'gemini')
                source_label = '🤖 Gemini' if source == 'gemini' else '🔧 Static'
                explanation += f"""
Issue #{idx} - Line {line} [{severity}] {source_label}
└─ {desc}
   💡 {suggestion}
"""
        else:
            explanation += """
✅ NO ISSUES FOUND!

"""

        if suggestions:
            explanation += f"""
💡 SUGGESTIONS ({len(suggestions)})
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
            for idx, suggestion in enumerate(suggestions[:5], 1):
                line = suggestion.get('line', '?')
                desc = suggestion.get('description', '')
                impl = suggestion.get('suggestion', '')
                explanation += f"""
Suggestion #{idx} - Line {line}
└─ {desc}
   💡 {impl}
"""
            if len(suggestions) > 5:
                explanation += f"""
... and {len(suggestions) - 5} more suggestions

"""
        else:
            explanation += """
✅ NO SUGGESTIONS NEEDED!

"""

        if test_results:
            explanation += f"""
🧪 TEST EXECUTION RESULTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
            passed_tests = [t for t in test_results if t.get('passed')]
            failed_tests = [t for t in test_results if not t.get('passed')]

            for test in passed_tests[:5]:
                name = test.get('name', 'unknown')
                explanation += f"  ✅ PASS: {name}\n"

            for test in failed_tests:
                name = test.get('name', 'unknown')
                error = test.get('error', '')
                explanation += f"""  ❌ FAIL: {name}
     Error: {error}
"""

            if len(passed_tests) > 5:
                explanation += f"  ... and {len(passed_tests) - 5} more passed\n"

            explanation += f"""
Summary: {len(passed_tests)} passed, {len(failed_tests)} failed

"""

        explanation += """
📋 RECOMMENDATIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        recommendations = []
        if len(bugs) > 0:
            recommendations.append("🔴 Fix all critical bugs immediately")
        if len(issues) > 0:
            recommendations.append("🟡 Address all issues before deployment")
        if len(suggestions) > 0:
            recommendations.append("🟢 Consider implementing suggested improvements")
        if len(syntax_errors) > 0:
            recommendations.append("🔴 Fix syntax errors first")
        if len(test_results) > len([t for t in test_results if t.get('passed')]):
            recommendations.append("🔴 Fix failing test cases")
        if len(bugs) == 0 and len(issues) == 0:
            recommendations.append("✅ Code looks good! Ready for review.")

        for i, rec in enumerate(recommendations, 1):
            explanation += f"  {i}. {rec}\n"

        if score >= 80:
            quality = "🌟🌟🌟 EXCELLENT"
            message = "High quality code. Minor improvements suggested."
        elif score >= 60:
            quality = "🌟🌟 GOOD"
            message = "Good quality code with some issues to address."
        elif score >= 40:
            quality = "🌟 NEEDS IMPROVEMENT"
            message = "Significant issues need attention."
        else:
            quality = "⚠️ POOR"
            message = "Major issues require immediate action."

        explanation += f"""
┌─────────────────────────────────────────────────────────────────────┐
│ OVERALL QUALITY: {quality}
│ {message}
└─────────────────────────────────────────────────────────────────────┘

Review completed: {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}
Total issues found: {len(bugs) + len(issues) + len(suggestions)}
Detection method: {detection_method}
{'✅ Gemini AI Analysis Enabled' if use_llm else 'ℹ️ Static Analysis Only'}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

        return explanation
        