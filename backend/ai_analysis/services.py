"""
AI Analysis Service for Code Review
"""
import os
import json
import logging
import ast
import subprocess
import tempfile
from typing import Dict, List, Any
import openai
import google.generativeai as genai
from django.conf import settings

logger = logging.getLogger(__name__)


class AIAnalysisService:
    """
    Service for AI-powered code analysis
    """

    def __init__(self, provider='openai'):
        self.provider = provider
        self._initialize_client()

    def _initialize_client(self):
        """Initialize the AI client based on provider"""
        if self.provider == 'openai':
            openai.api_key = settings.OPENAI_API_KEY
            self.model = settings.AI_MODEL
        elif self.provider == 'gemini':
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.model = genai.GenerativeModel('gemini-pro')
        else:
            raise ValueError(f"Unsupported AI provider: {self.provider}")

    def analyze_code(self, code: str, language: str, review_type: str = 'full') -> Dict[str, Any]:
        """
        Analyze code and return review results
        """
        try:
            if self.provider == 'openai':
                return self._analyze_with_openai(code, language, review_type)
            elif self.provider == 'gemini':
                return self._analyze_with_gemini(code, language, review_type)
            else:
                return self._get_error_response(f"Unsupported provider: {self.provider}")
        except Exception as e:
            logger.error(f"AI Analysis failed: {str(e)}")
            return self._get_error_response(str(e))

    def _analyze_with_openai(self, code: str, language: str, review_type: str) -> Dict[str, Any]:
        """Analyze code using OpenAI"""
        prompt = self._build_prompt(code, language, review_type)

        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert code reviewer and software engineer. Analyze code and provide detailed feedback."
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=settings.AI_TEMPERATURE,
                max_tokens=settings.AI_MAX_TOKENS
            )

            result = json.loads(response.choices[0].message.content)
            return result
        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            return self._get_error_response(str(e))

    def _analyze_with_gemini(self, code: str, language: str, review_type: str) -> Dict[str, Any]:
        """Analyze code using Gemini"""
        prompt = self._build_prompt(code, language, review_type)

        try:
            response = self.model.generate_content(prompt)
            result = json.loads(response.text)
            return result
        except Exception as e:
            logger.error(f"Gemini API error: {str(e)}")
            return self._get_error_response(str(e))

    def _build_prompt(self, code: str, language: str, review_type: str) -> str:
        """Build the prompt for AI analysis"""
        
        if review_type == 'full':
            prompt = f"""Analyze the following {language} code and provide a comprehensive review.

Code:
Please provide your analysis in the following JSON format:
{
    "quality_score": 0,
    "bugs": [
        {{
            "line": 0,
            "description": "description",
            "severity": "low|medium|high|critical",
            "suggestion": "how to fix"
        }}
    ],
    "issues": [
        {{
            "line": 0,
            "description": "description",
            "type": "syntax|style|performance|security",
            "suggestion": "how to fix"
        }}
    ],
    "suggestions": [
        {{
            "line": 0,
            "description": "description",
            "recommendation": "recommended approach",
            "code_example": "example code"
        }}
    ],
    "explanation": "brief explanation of what the code does",
    "test_cases": [
        {{
            "name": "test case name",
            "input": "test input",
            "expected": "expected output",
            "description": "what this test verifies"
        }}
    ]
}

Be specific and detailed. Include line numbers where applicable.
Return ONLY valid JSON. Do not include any other text."""

        elif review_type == 'bugs':
            prompt = f"""Analyze the following {language} code and identify all bugs and errors.

Code:
Focus on:
1. Syntax errors
2. Logical errors
3. Runtime errors
4. Edge cases
5. Security vulnerabilities

Provide your analysis in JSON format:
{{
    "bugs": [
        {{
            "line": 0,
            "description": "bug description",
            "severity": "low|medium|high|critical",
            "suggestion": "how to fix"
        }}
    ],
    "quality_score": 0
}}
Return ONLY valid JSON."""

        elif review_type == 'security':
            prompt = f"""Perform a security analysis of the following {language} code.

Code:
Identify:
1. Security vulnerabilities
2. Injection risks
3. Authentication issues
4. Data exposure
5. Best practices violations

Provide your analysis in JSON format:
{{
    "issues": [
        {{
            "line": 0,
            "description": "security issue description",
            "type": "security",
            "suggestion": "how to fix"
        }}
    ],
    "quality_score": 0
}}
Return ONLY valid JSON."""

        elif review_type == 'optimization':
            prompt = f"""Analyze the following {language} code for optimization opportunities.

Code:
Identify:
1. Performance issues
2. Code efficiency
3. Memory usage
4. Time complexity improvements
5. Best practices

Provide your analysis in JSON format:
{{
    "suggestions": [
        {{
            "line": 0,
            "description": "optimization description",
            "recommendation": "recommended approach",
            "code_example": "optimized code example"
        }}
    ],
    "quality_score": 0
}}
Return ONLY valid JSON."""

        elif review_type == 'explanation':
            prompt = f"""Provide a detailed explanation of the following {language} code.

Code:
Explain:
1. What the code does
2. How it works step by step
3. Key concepts used
4. Potential improvements

Provide your analysis in JSON format:
{{
    "explanation": "detailed explanation of the code",
    "quality_score": 0
}}
Return ONLY valid JSON."""

        else:
            prompt = f"""Analyze the following {language} code.

Code:
Provide your analysis in JSON format:
{{
    "quality_score": 0,
    "explanation": "code explanation"
}}
Return ONLY valid JSON."""

        return prompt

    def _get_error_response(self, error_message: str) -> Dict[str, Any]:
        """Return error response when AI analysis fails"""
        return {
            "quality_score": 0,
            "bugs": [
                {
                    "line": 0,
                    "description": f"AI Analysis failed: {error_message}",
                    "severity": "critical",
                    "suggestion": "Please try again or check your code"
                }
            ],
            "issues": [],
            "suggestions": [],
            "explanation": "Analysis failed due to an error.",
            "test_cases": []
        }

    def generate_test_cases(self, code: str, language: str) -> List[Dict[str, Any]]:
        """Generate test cases for the given code"""
        prompt = f"""Generate comprehensive test cases for the following {language} code.

Code:
Include:
1. Unit tests for each function
2. Edge cases
3. Negative test cases
4. Integration test scenarios

Provide test cases in JSON format:
{{
    "test_cases": [
        {{
            "name": "test name",
            "input": "test input",
            "expected": "expected output",
            "description": "what this test verifies"
        }}
    ]
}}
Return ONLY valid JSON."""

        try:
            if self.provider == 'openai':
                response = openai.ChatCompletion.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are a testing expert."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3,
                    max_tokens=1500
                )
                result = json.loads(response.choices[0].message.content)
                return result.get('test_cases', [])
            else:
                response = self.model.generate_content(prompt)
                result = json.loads(response.text)
                return result.get('test_cases', [])
        except Exception as e:
            logger.error(f"Test case generation failed: {str(e)}")
            return []

    def explain_code(self, code: str, language: str) -> str:
       
        prompt = f"""Explain the following {language} code in simple, understandable language."""
        


        try:
            if self.provider == 'openai':
                response = openai.ChatCompletion.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are a coding tutor."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.5,
                    max_tokens=1000
                )
                return response.choices[0].message.content
            else:
                response = self.model.generate_content(prompt)
                return response.text
        except Exception as e:
            logger.error(f"Code explanation failed: {str(e)}")
            return "Unable to explain the code at this time."


class StaticCodeAnalyzer:
   

    @staticmethod
    def analyze_python(code: str) -> Dict[str, Any]:
        
        results = {
            'syntax_errors': [],
            'style_issues': [],
            'complexity': 0,
            'functions': [],
            'classes': [],
            'imports': []
        }

        # AST Analysis
        try:
            tree = ast.parse(code)

            # Extract functions, classes, imports
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    results['functions'].append({
                        'name': node.name,
                        'line': node.lineno,
                        'args': [arg.arg for arg in node.args.args]
                    })
                elif isinstance(node, ast.ClassDef):
                    results['classes'].append({
                        'name': node.name,
                        'line': node.lineno
                    })
                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        results['imports'].append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    for alias in node.names:
                        results['imports'].append(f"{node.module}.{alias.name}")

            # Calculate cyclomatic complexity (simplified)
            decision_count = 0
            for node in ast.walk(tree):
                if isinstance(node, (ast.If, ast.For, ast.While, ast.Try, ast.ExceptHandler, ast.And, ast.Or)):
                    decision_count += 1
            results['complexity'] = decision_count + 1

        except SyntaxError as e:
            results['syntax_errors'].append({
                'line': e.lineno,
                'message': str(e),
                'type': 'syntax_error'
            })
        except Exception as e:
            results['syntax_errors'].append({
                'line': 0,
                'message': f"AST parsing error: {str(e)}",
                'type': 'parse_error'
            })

        # Pylint analysis (if available)
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(code)
                f.flush()
                temp_file = f.name

            try:
                result = subprocess.run(
                    ['pylint', temp_file, '--output-format=json'],
                    capture_output=True,
                    text=True,
                    timeout=10
                )

                if result.stdout:
                    issues = json.loads(result.stdout)
                    for issue in issues:
                        results['style_issues'].append({
                            'line': issue.get('line', 0),
                            'message': issue.get('message', ''),
                            'type': issue.get('symbol', 'style'),
                            'severity': 'medium'
                        })
            finally:
                if os.path.exists(temp_file):
                    os.unlink(temp_file)
        except FileNotFoundError:
            logger.warning("Pylint not found. Skipping style analysis.")
        except subprocess.TimeoutExpired:
            logger.warning("Pylint analysis timed out.")
        except Exception as e:
            logger.warning(f"Pylint analysis skipped: {str(e)}")

        return results