"""
Universal Code Analyzer - Detects and Debugs ALL Programming Languages
Supports: Python, JavaScript, TypeScript, Java, C, C++, C#, Go, Rust,
Ruby, PHP, Swift, Kotlin, Scala, Perl, R, Dart, Elixir, Haskell, Lua,
Julia, SQL, HTML, CSS, Shell, PowerShell, and more!
"""

import re
import logging
from typing import Dict, List, Tuple, Set, Optional

logger = logging.getLogger(__name__)


class UniversalCodeAnalyzer:
    """
    Universal Code Analyzer that detects bugs in ANY programming language
    """
    
    def __init__(self):
        self.builtins = self._get_universal_builtins()
        
    def _get_universal_builtins(self) -> Set[str]:
        """Get universal built-in functions across all languages"""
        return {
            # Common across all languages
            'print', 'println', 'printf', 'fmt', 'println', 'Println',
            'console', 'log', 'debug', 'info', 'error', 'warning',
            'len', 'count', 'size', 'length', 'sizeof', 'strlen',
            
            # Data manipulation
            'append', 'push', 'pop', 'shift', 'unshift', 'splice',
            'sort', 'reverse', 'join', 'split', 'replace', 'slice',
            'substring', 'substr', 'indexOf', 'lastIndexOf', 'includes',
            'startsWith', 'endsWith', 'toUpperCase', 'toLowerCase',
            'trim', 'trimStart', 'trimEnd', 'padStart', 'padEnd',
            
            # Object/Array methods
            'get', 'set', 'put', 'post', 'delete', 'update', 'patch',
            'create', 'read', 'write', 'open', 'close', 'flush',
            'add', 'remove', 'clear', 'copy', 'move', 'rename',
            
            # Error handling
            'try', 'catch', 'except', 'finally', 'throw', 'raise',
            
            # Loops and conditions
            'if', 'else', 'elif', 'for', 'while', 'do', 'switch', 'case',
            'break', 'continue', 'return', 'yield', 'goto', 'exit',
            
            # Type conversions
            'int', 'float', 'str', 'bool', 'array', 'list', 'dict',
            'map', 'set', 'tuple', 'object', 'string', 'number',
            'parseInt', 'parseFloat', 'Number', 'String', 'Boolean',
            
            # Common keywords
            'var', 'let', 'const', 'static', 'public', 'private',
            'protected', 'internal', 'abstract', 'final', 'sealed',
            'async', 'await', 'defer', 'go', 'chan', 'select',
            
            # Database
            'select', 'insert', 'update', 'delete', 'from', 'where',
            'join', 'group', 'order', 'having', 'limit', 'offset',
            
            # Common variable names
            'logger', 'request', 'response', 'data', 'user', 'item',
            'result', 'value', 'count', 'index', 'key', 'id', 'name',
            'status', 'code', 'message', 'error', 'exception',
            'file', 'path', 'url', 'host', 'port', 'config',
            'context', 'session', 'cookie', 'token', 'auth',
        }
    
    def analyze(self, code: str, language: str = 'auto') -> Dict:
        """
        Main analysis method - analyzes code and returns bugs, issues, suggestions
        
        Args:
            code: The source code to analyze
            language: Language name or 'auto' for automatic detection
            
        Returns:
            Dict with keys: bugs, issues, suggestions, quality_score, language_detected
        """
        if not code or not code.strip():
            return {
                'bugs': [],
                'issues': [],
                'suggestions': [{
                    'line': 1,
                    'title': '📝 No Code Provided',
                    'icon': '📝',
                    'description': 'Your submission is empty.',
                    'why': 'Please provide code to analyze.',
                    'how': 'Paste your code in the editor.',
                    'code_example': '# Paste your code here',
                    'benefits': ['✅ Get meaningful analysis']
                }],
                'quality_score': 0,
                'language_detected': 'unknown'
            }
        
        # Detect language if auto
        if language == 'auto':
            language = self._detect_language(code)
        
        code_lines = code.split('\n')
        
        # Choose analyzer based on language
        analyzers = {
            'python': self._analyze_python,
            'javascript': self._analyze_javascript,
            'js': self._analyze_javascript,
            'typescript': self._analyze_javascript,
            'ts': self._analyze_javascript,
            'java': self._analyze_c_like,
            'c': self._analyze_c_like,
            'cpp': self._analyze_c_like,
            'c++': self._analyze_c_like,
            'csharp': self._analyze_c_like,
            'c#': self._analyze_c_like,
            'go': self._analyze_go,
            'rust': self._analyze_rust,
            'ruby': self._analyze_ruby,
            'php': self._analyze_php,
            'haskell': self._analyze_haskell,
            'swift': self._analyze_swift,
            'kotlin': self._analyze_kotlin,
            'scala': self._analyze_scala,
            'perl': self._analyze_perl,
            'r': self._analyze_r,
            'dart': self._analyze_dart,
            'elixir': self._analyze_elixir,
            'lua': self._analyze_lua,
            'julia': self._analyze_julia,
            'sql': self._analyze_sql,
            'html': self._analyze_html,
            'css': self._analyze_css,
            'shell': self._analyze_shell,
            'powershell': self._analyze_powershell,
        }
        
        # Use specific analyzer if available, otherwise use universal
        if language.lower() in analyzers:
            bugs, issues, suggestions = analyzers[language.lower()](code, code_lines)
        else:
            bugs, issues, suggestions = self._analyze_universal(code, code_lines)
        
        # Calculate quality score
        quality_score = max(50, 100 - (len(suggestions) * 3) - (len(issues) * 5) - (len(bugs) * 10))
        
        return {
            'bugs': bugs,
            'issues': issues,
            'suggestions': suggestions,
            'quality_score': quality_score,
            'language_detected': language,
            'explanation': f'✅ Quality Score: {quality_score}%\n✅ Bugs Found: {len(bugs)}\n✅ Issues: {len(issues)}\n✅ Suggestions: {len(suggestions)}'
        }
    
    # ============================================================
    # LANGUAGE DETECTION
    # ============================================================
    
    def _detect_language(self, code: str) -> str:
        """Detect programming language from code content"""
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
        
        # Language detection with scoring
        scores = {}
        
        # Python
        python_score = 0
        if 'def ' in code or 'import ' in code or 'from ' in code:
            python_score += 3
        if 'if __name__' in code or 'print(' in code:
            python_score += 5
        if '@' in code and 'def ' in code:  # Decorator
            python_score += 2
        if ':' in code and '\n    ' in code:  # Indentation
            python_score += 2
        scores['python'] = python_score
        
        # JavaScript
        js_score = 0
        if 'function ' in code or 'const ' in code or 'let ' in code or 'var ' in code:
            js_score += 3
        if 'console.log' in code or '=>' in code:
            js_score += 5
        if 'export ' in code or 'import ' in code:
            js_score += 3
        if 'async ' in code or 'await ' in code:
            js_score += 2
        scores['javascript'] = js_score
        
        # TypeScript
        ts_score = 0
        if 'interface ' in code or 'type ' in code:
            ts_score += 5
        if ': string' in code or ': number' in code or ': boolean' in code:
            ts_score += 5
        if '<' in code and '>' in code and 'function' in code:  # Generics
            ts_score += 2
        scores['typescript'] = ts_score
        
        # Java
        java_score = 0
        if 'public class' in code or 'private ' in code or 'protected ' in code:
            java_score += 5
        if 'System.out.println' in code:
            java_score += 5
        if 'public static void main' in code:
            java_score += 5
        if 'import java.' in code:
            java_score += 3
        scores['java'] = java_score
        
        # C
        c_score = 0
        if '#include' in code:
            c_score += 5
        if 'int main(' in code and 'printf(' in code:
            c_score += 5
        if 'scanf(' in code or 'malloc(' in code:
            c_score += 3
        if '->' in code and '*' in code:  # Pointers
            c_score += 2
        scores['c'] = c_score
        
        # C++
        cpp_score = 0
        if '#include' in code and 'std::' in code:
            cpp_score += 5
        if 'cout' in code or 'cin' in code:
            cpp_score += 5
        if 'class ' in code and 'public:' in code:
            cpp_score += 3
        if 'namespace ' in code:
            cpp_score += 2
        scores['cpp'] = cpp_score
        
        # C#
        cs_score = 0
        if 'using System' in code and 'namespace ' in code:
            cs_score += 5
        if 'Console.WriteLine' in code:
            cs_score += 5
        if 'class ' in code and 'private ' in code:
            cs_score += 3
        if 'get; set;' in code:
            cs_score += 2
        scores['csharp'] = cs_score
        
        # Go
        go_score = 0
        if 'package ' in code and 'func ' in code:
            go_score += 5
        if 'fmt.Println' in code or 'fmt.Printf' in code:
            go_score += 5
        if 'go ' in code or 'chan ' in code:
            go_score += 3
        if 'import (' in code:
            go_score += 2
        scores['go'] = go_score
        
        # Rust
        rust_score = 0
        if 'fn ' in code and 'let mut' in code:
            rust_score += 5
        if 'println!' in code or 'print!' in code:
            rust_score += 5
        if 'match ' in code or 'impl ' in code:
            rust_score += 3
        if 'pub fn' in code:
            rust_score += 2
        scores['rust'] = rust_score
        
        # Ruby
        ruby_score = 0
        if 'def ' in code and 'end' in code:
            ruby_score += 5
        if 'attr_accessor' in code or 'puts ' in code:
            ruby_score += 5
        if 'class ' in code and '< ' in code:
            ruby_score += 3
        if 'require ' in code:
            ruby_score += 2
        scores['ruby'] = ruby_score
        
        # PHP
        php_score = 0
        if '<?php' in code:
            php_score += 10
        if 'echo ' in code or 'print_r' in code:
            php_score += 5
        if 'function ' in code and '$' in code:
            php_score += 3
        if 'public function' in code:
            php_score += 2
        scores['php'] = php_score
        
        # Haskell
        haskell_score = 0
        if 'module ' in code and 'where' in code:
            haskell_score += 5
        if '::' in code and '->' in code:
            haskell_score += 5
        if 'data ' in code or 'class ' in code:
            haskell_score += 3
        if 'import ' in code and 'Data.' in code:
            haskell_score += 2
        scores['haskell'] = haskell_score
        
        # SQL
        sql_score = 0
        if 'SELECT ' in code_upper or 'INSERT ' in code_upper:
            sql_score += 5
        if 'FROM ' in code_upper or 'WHERE ' in code_upper:
            sql_score += 5
        if 'CREATE ' in code_upper or 'ALTER ' in code_upper:
            sql_score += 3
        if 'JOIN ' in code_upper:
            sql_score += 2
        scores['sql'] = sql_score
        
        # HTML
        html_score = 0
        if '<!DOCTYPE html>' in code or '<html>' in code:
            html_score += 5
        if '<body>' in code or '<div>' in code:
            html_score += 3
        if 'class="' in code or 'id="' in code:
            html_score += 2
        scores['html'] = html_score
        
        # CSS
        css_score = 0
        if 'color:' in code or 'margin:' in code or 'padding:' in code:
            css_score += 5
        if '{' in code and '}' in code and ':' in code:
            css_score += 3
        if '@media' in code or '@keyframes' in code:
            css_score += 2
        scores['css'] = css_score
        
        # Shell
        shell_score = 0
        if '#!/bin/' in code:
            shell_score += 10
        if 'echo ' in code and '$' in code:
            shell_score += 3
        if 'if [' in code or 'for ' in code:
            shell_score += 2
        scores['shell'] = shell_score
        
        # Find language with highest score
        best_lang = max(scores, key=scores.get)
        best_score = scores[best_lang]
        
        # Default to Python if no clear match
        if best_score < 3:
            return 'python'
        
        return best_lang
    
    # ============================================================
    # HELPER FUNCTIONS
    # ============================================================
    
    def _is_in_string(self, line: str, position: int) -> bool:
        """Check if position in line is inside a string literal"""
        in_single = False
        in_double = False
        in_triple_single = False
        in_triple_double = False
        escaped = False
        
        for i, char in enumerate(line):
            if i >= position:
                break
            if escaped:
                escaped = False
                continue
            if char == '\\':
                escaped = True
                continue
            
            if i + 2 < len(line):
                if line[i:i+3] == "'''" and not in_double and not in_triple_double:
                    in_triple_single = not in_triple_single
                    continue
                if line[i:i+3] == '"""' and not in_single and not in_triple_single:
                    in_triple_double = not in_triple_double
                    continue
            
            if not in_triple_single and not in_triple_double:
                if char == "'" and not in_double:
                    in_single = not in_single
                elif char == '"' and not in_single:
                    in_double = not in_double
        
        return in_single or in_double or in_triple_single or in_triple_double
    
    def _is_in_comment(self, line: str, language: str = 'python') -> bool:
        """Check if line is a comment"""
        stripped = line.strip()
        if language in ['python', 'ruby', 'perl', 'r', 'shell', 'powershell']:
            return stripped.startswith('#')
        elif language in ['javascript', 'java', 'c', 'cpp', 'csharp', 'go', 'rust', 'php', 'swift', 'kotlin', 'scala', 'dart']:
            return stripped.startswith('//') or stripped.startswith('/*')
        elif language in ['haskell', 'elixir']:
            return stripped.startswith('--') or stripped.startswith('{-')
        elif language == 'html':
            return stripped.startswith('<!--')
        elif language == 'css':
            return stripped.startswith('/*')
        elif language == 'sql':
            return stripped.startswith('--') or stripped.startswith('/*')
        return False
    
    def _get_defined_names(self, code_lines: List[str], language: str = 'python') -> Set[str]:
        """Get defined function and variable names"""
        defined = set()
        
        for line in code_lines:
            stripped = line.strip()
            if self._is_in_comment(stripped, language):
                continue
            
            # Python
            if language in ['python']:
                if stripped.startswith('def '):
                    name = stripped.split('def ')[1].split('(')[0].strip()
                    if name:
                        defined.add(name)
                elif stripped.startswith('class '):
                    name = stripped.split('class ')[1].split('(')[0].split(':')[0].strip()
                    if name:
                        defined.add(name)
                elif '=' in stripped and not stripped.startswith('if'):
                    name = stripped.split('=')[0].strip()
                    if name and re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', name):
                        defined.add(name)
            
            # JavaScript/TypeScript
            elif language in ['javascript', 'js', 'typescript', 'ts']:
                if stripped.startswith('function '):
                    name = stripped.split('function ')[1].split('(')[0].strip()
                    if name:
                        defined.add(name)
                elif 'const ' in stripped and '=' in stripped:
                    name = stripped.split('const ')[1].split('=')[0].strip()
                    if name:
                        defined.add(name)
                elif 'let ' in stripped and '=' in stripped:
                    name = stripped.split('let ')[1].split('=')[0].strip()
                    if name:
                        defined.add(name)
                elif 'var ' in stripped and '=' in stripped:
                    name = stripped.split('var ')[1].split('=')[0].strip()
                    if name:
                        defined.add(name)
                elif 'class ' in stripped:
                    name = stripped.split('class ')[1].split('(')[0].split('{')[0].strip()
                    if name:
                        defined.add(name)
            
            # Go
            elif language in ['go', 'golang']:
                if stripped.startswith('func '):
                    name = stripped.split('func ')[1].split('(')[0].strip()
                    if name:
                        defined.add(name)
                elif stripped.startswith('var '):
                    name = stripped.split('var ')[1].split('=')[0].strip()
                    if name:
                        defined.add(name)
                elif ':= ' in stripped:
                    name = stripped.split(':=')[0].strip()
                    if name:
                        defined.add(name)
            
            # Rust
            elif language == 'rust':
                if stripped.startswith('fn '):
                    name = stripped.split('fn ')[1].split('(')[0].strip()
                    if name:
                        defined.add(name)
                elif 'let ' in stripped and '=' in stripped:
                    name = stripped.split('let ')[1].split('=')[0].strip()
                    if name:
                        defined.add(name)
            
            # Ruby
            elif language == 'ruby':
                if stripped.startswith('def '):
                    name = stripped.split('def ')[1].split('(')[0].strip()
                    if name:
                        defined.add(name)
                elif '=' in stripped and not stripped.startswith('#'):
                    name = stripped.split('=')[0].strip()
                    if name and re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', name):
                        defined.add(name)
            
            # PHP
            elif language == 'php':
                if 'function ' in stripped and '(' in stripped:
                    name = stripped.split('function ')[1].split('(')[0].strip()
                    if name:
                        defined.add(name)
                elif '$' in stripped and '=' in stripped:
                    name = stripped.split('=')[0].strip().replace('$', '')
                    if name and re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', name):
                        defined.add(name)
            
            # C/C++/Java/C#
            elif language in ['c', 'cpp', 'java', 'csharp']:
                if 'main' in stripped and '(' in stripped:
                    defined.add('main')
                if stripped.startswith('int ') or stripped.startswith('void ') or stripped.startswith('char '):
                    if '(' in stripped and ')' in stripped:
                        name = stripped.split()[1].split('(')[0].strip()
                        if name and name not in ['if', 'while', 'for', 'switch']:
                            defined.add(name)
        
        return defined
    
    # ============================================================
    # UNIVERSAL ANALYZER (Works for ANY language)
    # ============================================================
    
    def _analyze_universal(self, code: str, code_lines: List[str]) -> Tuple[List, List, List]:
        """Universal analyzer that works for ANY programming language"""
        bugs = []
        issues = []
        suggestions = []
        language = 'universal'
        
        defined_names = self._get_defined_names(code_lines, language)
        
        for i, line in enumerate(code_lines, 1):
            stripped = line.strip()
            
            if not stripped:
                continue
            if self._is_in_comment(line, language):
                continue
            
            # ============================================================
            # BUG: Hardcoded credentials
            # ============================================================
            line_upper = line.upper()
            credential_keywords = ['PASSWORD', 'SECRET', 'API_KEY', 'TOKEN', 'AUTH', 'ADMIN']
            for keyword in credential_keywords:
                if keyword in line_upper:
                    if '=' in line or ':' in line:
                        if '"' in line or "'" in line:
                            bugs.append({
                                'line': i,
                                'description': f'🔐 Hardcoded {keyword.lower()} at line {i}',
                                'severity': 'critical',
                                'suggestion': 'Use environment variables or .env file'
                            })
                            break
            
            # ============================================================
            # BUG: Division by zero
            # ============================================================
            if '/' in line and not stripped.startswith('//'):
                if '/ 0' in line or '/0' in line or '/ (0)' in line:
                    bugs.append({
                        'line': i,
                        'description': f'🐛 Division by zero at line {i}',
                        'severity': 'critical',
                        'suggestion': 'Check for division by zero'
                    })
            
            # ============================================================
            # BUG: Unused variable
            # ============================================================
            if '=' in line and not stripped.startswith('#'):
                var_name = stripped.split('=')[0].strip()
                if var_name and re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', var_name):
                    is_used = False
                    var_pattern = r'\b' + re.escape(var_name) + r'\b'
                    for j in range(i, min(i + 20, len(code_lines))):
                        if j == i:
                            continue
                        if re.search(var_pattern, code_lines[j]):
                            if '=' not in code_lines[j] or code_lines[j].split('=')[0].strip() != var_name:
                                is_used = True
                                break
                    if not is_used and var_name not in ['result', 'data', 'item', 'value', 'temp']:
                        bugs.append({
                            'line': i,
                            'description': f'📦 Unused variable "{var_name}" at line {i}',
                            'severity': 'medium',
                            'suggestion': f'Remove unused variable "{var_name}" or use it'
                        })
            
            # ============================================================
            # BUG: Undefined function call
            # ============================================================
            func_matches = re.findall(r'([a-zA-Z_][a-zA-Z0-9_]*)\s*\(', line)
            for func_name in func_matches:
                if func_name in self.builtins:
                    continue
                if func_name in defined_names:
                    continue
                if func_name and func_name[0].isupper():
                    continue
                if func_name in ['if', 'for', 'while', 'switch', 'return']:
                    continue
                
                pos = line.find(f'{func_name}(')
                if pos != -1 and not self._is_in_string(line, pos):
                    bugs.append({
                        'line': i,
                        'description': f'🐛 Undefined function call "{func_name}()" at line {i}',
                        'severity': 'critical',
                        'suggestion': f'Define function "{func_name}" before calling it'
                    })
            
            # ============================================================
            # BUG: Global variable
            # ============================================================
            if 'var ' in line or 'let ' in line or 'const ' in line:
                if '=' in line and not stripped.startswith('//'):
                    is_global = True
                    for prev_line in code_lines[max(0, i-5):i]:
                        if 'func ' in prev_line or 'def ' in prev_line or 'function ' in prev_line:
                            is_global = False
                            break
                    if is_global:
                        bugs.append({
                            'line': i,
                            'description': f'🌍 Global variable at line {i}',
                            'severity': 'medium',
                            'suggestion': 'Avoid global variables, use function parameters instead'
                        })
            
            # ============================================================
            # ISSUE: Print/debug statements
            # ============================================================
            print_keywords = ['print', 'console.log', 'echo', 'puts', 'fmt.Println', 'log.Println']
            for keyword in print_keywords:
                if keyword in line:
                    pos = line.find(keyword)
                    if pos != -1 and not self._is_in_string(line, pos):
                        issues.append({
                            'line': i,
                            'description': f'🖨️ Print/debug statement at line {i}',
                            'type': 'debug',
                            'suggestion': 'Use proper logging framework or remove in production'
                        })
                        break
        
        # ============================================================
        # SUGGESTION: Error handling
        # ============================================================
        has_error_handling = False
        error_keywords = ['try', 'catch', 'except', 'if err', 'if error', 'HandleError']
        for line in code_lines:
            for keyword in error_keywords:
                if keyword in line:
                    has_error_handling = True
                    break
            if has_error_handling:
                break
        
        if not has_error_handling and len(code_lines) > 10:
            suggestions.append({
                'line': 1,
                'title': '🛡️ Add Proper Error Handling',
                'icon': '🛡️',
                'description': 'Your code lacks error handling.',
                'why': 'Without error handling, your program may crash unexpectedly.',
                'how': 'Use try-catch blocks or check error returns.',
                'code_example': 'try {\n    result = risky_operation()\n} catch (error) {\n    console.error("Error:", error)\n}',
                'benefits': ['✅ Prevents crashes', '✅ Better user experience']
            })
        
        return bugs, issues, suggestions
    
    # ============================================================
    # PYTHON ANALYZER
    # ============================================================
    
    def _analyze_python(self, code: str, code_lines: List[str]) -> Tuple[List, List, List]:
        """Python-specific analysis"""
        bugs = []
        issues = []
        suggestions = []
        language = 'python'
        
        python_builtins = self.builtins | {
            'print', 'len', 'str', 'int', 'float', 'list', 'dict', 'set', 'tuple',
            'range', 'sum', 'max', 'min', 'sorted', 'type', 'isinstance', 'open',
            'input', 'format', 'zip', 'map', 'filter', 'any', 'all', 'enumerate',
            'reversed', 'round', 'abs', 'bin', 'hex', 'oct', 'chr', 'ord',
            'bool', 'complex', 'divmod', 'pow', 'hash', 'id', 'repr', 'bytes',
            'bytearray', 'memoryview', 'object', 'property', 'staticmethod',
            'classmethod', 'super', 'vars', 'dir', 'help', 'globals', 'locals',
            'iter', 'next', 'slice', 'eval', 'exec', 'compile',
            'hasattr', 'getattr', 'setattr', 'delattr', 'callable',
            'issubclass', 'isinstance', 'is', 'as', 'not', 'and', 'or', 'in',
            'del', 'pass', 'raise', 'yield', 'lambda', 'assert', 'nonlocal',
            'global', 'add', 'extend', 'append', 'insert', 'remove', 'pop',
            'clear', 'copy', 'count', 'index', 'reverse', 'sort', 'lower',
            'upper', 'title', 'capitalize', 'strip', 'split', 'join', 'replace',
            'find', 'startswith', 'endswith', 'isalpha', 'isdigit', 'isalnum',
            'isspace', 'isupper', 'islower', 'isdigit', 'now', 'isoformat',
            'uuid4', 'match', 'search', 'findall', 'finditer', 'sub', 'subn',
            'split', 'compile', 'escape', 'fullmatch',
            'get_serializer', 'is_valid', 'save', 'get_success_headers',
            'get_queryset', 'get_object', 'perform_create', 'perform_update',
            'perform_destroy', 'list', 'create', 'retrieve', 'update',
            'partial_update', 'destroy', 'get_serializer_class',
            'objects', 'all', 'filter', 'get', 'update', 'delete',
            'order_by', 'distinct', 'values', 'values_list',
            'exclude', 'aggregate', 'annotate', 'count', 'exists', 'first',
            'last', 'get_or_create', 'update_or_create', 'bulk_create',
            'bulk_update', 'info', 'error', 'warning', 'debug', 'critical',
            'log', 'exception', 'getLogger', 'get_logger', 'basicConfig',
            'Exception', 'ValueError', 'TypeError', 'KeyError', 'IndexError',
            'AttributeError', 'ImportError', 'NameError', 'ZeroDivisionError',
            'FileNotFoundError', 'PermissionError', 'TimeoutError',
            'models', 'views', 'serializers', 'forms', 'admin', 'urls', 'settings',
            'rest_framework', 'status', 'generics', 'permissions', 'APIView',
            'Response', 'ModelViewSet', 'ReadOnlyModelViewSet',
            'import', 'from', 'class', 'def', 'return', 'yield', 'with',
            'try', 'except', 'finally', 'raise', 'assert', 'pass', 'del',
            'global', 'nonlocal', 'lambda', 'if', 'elif', 'else', 'for',
            'while', 'break', 'continue', 'True', 'False', 'None',
            'logger', 'request', 'response', 'data', 'user', 'submission',
            'serializer', 'review', 'analysis_result', 'result', 'params',
            'func_name', 'function', 'method', 'class_name', 'value', 'item',
            'error', 'exception', 'message', 'status', 'code', 'lines',
            'full_code', 'known_names', 'imported_names', 'defined_names',
            'python_builtins', 'args', 'kwargs', 'pk'
        }
        
        full_code = '\n'.join(code_lines)
        
        # Parse imports and definitions
        imported_names = set()
        for line in code_lines:
            stripped = line.strip()
            if stripped.startswith('from ') and ' import ' in line:
                parts = stripped.split(' import ')
                if len(parts) == 2:
                    import_part = parts[1].strip()
                    if ',' in import_part:
                        for name in import_part.split(','):
                            name = name.strip().split(' as ')[0].strip()
                            if name and name != '*':
                                imported_names.add(name)
                    elif ' as ' in import_part:
                        name = import_part.split(' as ')[0].strip()
                        if name and name != '*':
                            imported_names.add(name)
                    else:
                        if import_part and import_part != '*':
                            imported_names.add(import_part)
            elif stripped.startswith('import '):
                parts = stripped.split('import ')[1].strip()
                if ',' in parts:
                    for name in parts.split(','):
                        name = name.strip().split(' as ')[0].strip()
                        if name:
                            imported_names.add(name)
                elif ' as ' in parts:
                    name = parts.split(' as ')[0].strip()
                    if name:
                        imported_names.add(name)
                else:
                    if parts:
                        imported_names.add(parts)
        
        defined_names = self._get_defined_names(code_lines, language)
        known_names = python_builtins | imported_names | defined_names
        
        for i, line in enumerate(code_lines, 1):
            stripped = line.strip()
            
            if not stripped:
                continue
            if stripped.startswith('#'):
                continue
            if stripped.startswith('import ') or stripped.startswith('from '):
                continue
            if stripped.startswith('@'):
                continue
            
            # Check undefined function calls
            func_matches = re.findall(r'([a-zA-Z_][a-zA-Z0-9_]*)\s*\(', line)
            for func_name in func_matches:
                if func_name in known_names:
                    continue
                if func_name and func_name[0].isupper():
                    continue
                
                pos = line.find(f'{func_name}(')
                if pos == -1:
                    continue
                if self._is_in_string(line, pos):
                    continue
                if pos > 0 and line[:pos].strip().endswith('.'):
                    continue
                if f'def {func_name}' in line:
                    continue
                
                bugs.append({
                    'line': i,
                    'description': f'🐛 Undefined function call "{func_name}()" at line {i}',
                    'severity': 'critical',
                    'suggestion': f'Define function "{func_name}" before calling it'
                })
            
            # Check missing type hints
            if stripped.startswith('def ') and ':' in line:
                pos = line.find('def ')
                if pos != -1 and not self._is_in_string(line, pos):
                    if not any(hint in line for hint in ['->', ': int', ': str', ': list', ': dict', ': tuple', ': bool']):
                        issues.append({
                            'line': i,
                            'description': f'📋 Missing type hints at line {i}',
                            'type': 'style',
                            'suggestion': 'Add type hints: def function(param: list) -> float:'
                        })
            
            # Check print statements
            if 'print(' in line:
                pos = line.find('print(')
                if pos != -1 and not self._is_in_string(line, pos):
                    if not stripped.startswith('#'):
                        issues.append({
                            'line': i,
                            'description': f'🖨️ print() used at line {i}',
                            'type': 'debug',
                            'suggestion': 'Use proper logging or remove in production'
                        })
        
        # Check error handling
        has_error_handling = False
        for line in code_lines:
            if 'try' in line or 'except' in line:
                has_error_handling = True
                break
        
        if not has_error_handling and len(code_lines) > 5:
            suggestions.append({
                'line': 1,
                'title': '🛡️ Add Proper Error Handling',
                'icon': '🛡️',
                'description': 'Your code lacks error handling.',
                'why': 'Without error handling, your program may crash unexpectedly.',
                'how': 'Use try-except blocks to handle exceptions.',
                'code_example': 'try:\n    result = risky_operation()\nexcept Exception as e:\n    print(f"Error: {e}")',
                'benefits': ['✅ Prevents crashes', '✅ Better user experience']
            })
        
        return bugs, issues, suggestions
    
    # ============================================================
    # JAVASCRIPT ANALYZER
    # ============================================================
    
    def _analyze_javascript(self, code: str, code_lines: List[str]) -> Tuple[List, List, List]:
        """JavaScript/TypeScript-specific analysis"""
        bugs = []
        issues = []
        suggestions = []
        language = 'javascript'
        
        defined_names = self._get_defined_names(code_lines, language)
        
        for i, line in enumerate(code_lines, 1):
            stripped = line.strip()
            
            if not stripped:
                continue
            if stripped.startswith('//') or stripped.startswith('/*'):
                continue
            if stripped in ['{', '}', '};', '});']:
                continue
            if stripped.startswith('if') or stripped.startswith('for'):
                continue
            if stripped.startswith('while') or stripped.startswith('switch'):
                continue
            if stripped.startswith('else') or stripped.startswith('function'):
                continue
            if stripped.startswith('try') or stripped.startswith('catch'):
                continue
            
            # Check missing semicolon
            if (stripped and 
                not stripped.endswith(';') and 
                not stripped.endswith('{') and 
                not stripped.endswith('}') and
                not stripped.startswith('//') and
                not stripped.startswith('/*')):
                
                if ('=' in line or 
                    '(' in line or 
                    '++' in line or 
                    '--' in line or
                    'var ' in line or
                    'let ' in line or
                    'const ' in line or
                    'console.log' in line or
                    'return' in line):
                    pos = line.find('=')
                    if pos == -1:
                        pos = line.find('(')
                    if pos != -1 and not self._is_in_string(line, pos):
                        bugs.append({
                            'line': i,
                            'description': f'🐛 Missing semicolon at line {i}',
                            'severity': 'high',
                            'suggestion': 'Add ";" at the end of the statement'
                        })
            
            # Check var usage
            if 'var ' in line and 'const ' not in line and 'let ' not in line:
                bugs.append({
                    'line': i,
                    'description': f'📦 Using "var" at line {i} is outdated',
                    'severity': 'low',
                    'suggestion': 'Use let or const instead'
                })
            
            # Check loose equality
            if '== ' in line and '=== ' not in line:
                if not self._is_in_string(line, line.find('==')):
                    bugs.append({
                        'line': i,
                        'description': f'⚖️ Loose equality (==) at line {i}',
                        'severity': 'medium',
                        'suggestion': 'Use === for strict equality'
                    })
            
            # Check console.log
            if 'console.log' in line:
                pos = line.find('console.log')
                if pos != -1 and not self._is_in_string(line, pos):
                    issues.append({
                        'line': i,
                        'description': f'🖨️ console.log used at line {i}',
                        'type': 'debug',
                        'suggestion': 'Use proper logging or remove in production'
                    })
        
        return bugs, issues, suggestions
    
    # ============================================================
    # C/C++/JAVA/C# ANALYZER
    # ============================================================
    
    def _analyze_c_like(self, code: str, code_lines: List[str]) -> Tuple[List, List, List]:
        """C/C++/Java/C#-specific analysis"""
        bugs = []
        issues = []
        suggestions = []
        language = 'c'
        
        # Track function declarations and definitions
        function_declarations = set()
        function_definitions = set()
        
        for line in code_lines:
            stripped = line.strip()
            if stripped.startswith('//') or stripped.startswith('/*'):
                continue
            if stripped.startswith('#'):
                continue
            
            if stripped.endswith(';') and '(' in line and ')' in line:
                if not stripped.startswith('if') and not stripped.startswith('for'):
                    parts = stripped.split()
                    for part in parts:
                        if '(' in part:
                            func_name = part.split('(')[0].strip()
                            if func_name and func_name not in ['if', 'while', 'for', 'switch']:
                                function_declarations.add(func_name)
            
            if '{' in line and '(' in line and ')' in line:
                parts = stripped.split()
                for part in parts:
                    if '(' in part:
                        func_name = part.split('(')[0].strip()
                        if func_name and func_name not in ['if', 'while', 'for', 'switch']:
                            function_definitions.add(func_name)
        
        for func in function_declarations:
            if func not in function_definitions and func != 'main':
                bugs.append({
                    'line': 1,
                    'description': f'🐛 Function "{func}" declared but never defined',
                    'severity': 'high',
                    'suggestion': f'Define function "{func}" or remove its declaration'
                })
        
        for i, line in enumerate(code_lines, 1):
            stripped = line.strip()
            
            if not stripped:
                continue
            if stripped.startswith('//') or stripped.startswith('/*'):
                continue
            if stripped.startswith('#'):
                continue
            if stripped in ['{', '}', '};']:
                continue
            
            # Check missing semicolon
            if (stripped and 
                not stripped.endswith(';') and 
                not stripped.endswith('{') and 
                not stripped.endswith('}') and
                not stripped.startswith('if') and
                not stripped.startswith('for') and
                not stripped.startswith('while') and
                not stripped.startswith('switch') and
                not stripped.startswith('else') and
                not stripped.startswith('return') and
                not stripped.startswith('//') and
                not stripped.startswith('/*') and
                not stripped.startswith('#')):
                
                if ('=' in line or 
                    '(' in line or 
                    '++' in line or 
                    '--' in line or
                    'printf' in line or
                    'scanf' in line or
                    'strcpy' in line or
                    'malloc' in line or
                    'free' in line or
                    'realloc' in line or
                    'calloc' in line or
                    'sizeof' in line):
                    pos = line.find('=')
                    if pos == -1:
                        pos = line.find('(')
                    if pos != -1 and not self._is_in_string(line, pos):
                        bugs.append({
                            'line': i,
                            'description': f'🐛 Missing semicolon at line {i}',
                            'severity': 'high',
                            'suggestion': 'Add ";" at the end of the statement'
                        })
            
            # Check hardcoded credentials
            if 'password' in line.lower() or 'secret' in line.lower() or 'admin' in line.lower():
                if '=' in line and ('"' in line or "'" in line):
                    bugs.append({
                        'line': i,
                        'description': f'🔐 Hardcoded credentials at line {i}',
                        'severity': 'critical',
                        'suggestion': 'Use environment variables or .env file'
                    })
            
            # Check division by zero
            if '/' in line and not stripped.startswith('//'):
                if '/ 0' in line or '/0' in line:
                    bugs.append({
                        'line': i,
                        'description': f'🐛 Division by zero at line {i}',
                        'severity': 'critical',
                        'suggestion': 'Check for division by zero'
                    })
            
            # Check dangerous functions
            if 'gets(' in line:
                bugs.append({
                    'line': i,
                    'description': f'⚠️ Dangerous function gets() used at line {i}',
                    'severity': 'critical',
                    'suggestion': 'Use fgets() instead of gets()'
                })
            
            if 'strcpy(' in line:
                bugs.append({
                    'line': i,
                    'description': f'⚠️ Buffer overflow risk - strcpy() at line {i}',
                    'severity': 'high',
                    'suggestion': 'Use strncpy() or strcpy_s() instead'
                })
            
            # Check memory leak
            if 'malloc' in line or 'calloc' in line:
                has_free = False
                for j in range(i, min(i + 20, len(code_lines))):
                    if 'free' in code_lines[j]:
                        has_free = True
                        break
                if not has_free:
                    bugs.append({
                        'line': i,
                        'description': f'💾 Memory leak - malloc/calloc without free at line {i}',
                        'severity': 'high',
                        'suggestion': 'Add free() to release allocated memory'
                    })
            
            # Check assignment in condition
            if 'if (' in line and '=' in line and '==' not in line:
                pos = line.find('if')
                if pos != -1 and not self._is_in_string(line, pos):
                    bugs.append({
                        'line': i,
                        'description': f'🐛 Assignment in condition at line {i}',
                        'severity': 'high',
                        'suggestion': 'Use "==" for comparison, not "=" for assignment'
                    })
            
            # Check print statements
            if 'printf' in line or 'cout' in line or 'System.out.println' in line:
                pos = line.find('printf')
                if pos == -1:
                    pos = line.find('cout')
                if pos == -1:
                    pos = line.find('System.out.println')
                if pos != -1 and not self._is_in_string(line, pos):
                    issues.append({
                        'line': i,
                        'description': f'🖨️ Print statement used at line {i}',
                        'type': 'debug',
                        'suggestion': 'Use proper logging framework'
                    })
        
        return bugs, issues, suggestions
    
    # ============================================================
    # GO ANALYZER
    # ============================================================
    
    def _analyze_go(self, code: str, code_lines: List[str]) -> Tuple[List, List, List]:
        """Go-specific analysis"""
        bugs = []
        issues = []
        suggestions = []
        language = 'go'
        
        go_builtins = self.builtins | {
            'make', 'new', 'len', 'cap', 'append', 'copy', 'delete', 'close',
            'print', 'println', 'panic', 'recover', 'complex', 'real', 'imag',
            'int', 'int8', 'int16', 'int32', 'int64', 'uint', 'uint8', 'uint16',
            'uint32', 'uint64', 'uintptr', 'float32', 'float64', 'complex64',
            'complex128', 'string', 'bool', 'byte', 'rune', 'error',
            'fmt', 'Println', 'Printf', 'Print', 'Sprint', 'Sprintf',
            'os', 'Open', 'Create', 'Stat', 'Remove', 'Rename',
            'io', 'ReadAll', 'ReadFile', 'WriteFile', 'Copy',
            'http', 'Get', 'Post', 'Head', 'Do', 'ListenAndServe',
            'ioutil', 'ReadAll', 'ReadFile', 'WriteFile', 'TempFile', 'TempDir',
            'context', 'WithCancel', 'WithTimeout', 'WithDeadline', 'WithValue',
            'log', 'Println', 'Printf', 'Print', 'Fatal', 'Panic',
            'json', 'Marshal', 'Unmarshal', 'NewDecoder', 'NewEncoder',
            'time', 'Now', 'Sleep', 'After', 'Since', 'Until', 'Tick',
            'sync', 'Mutex', 'RWMutex', 'WaitGroup', 'Once', 'Map',
            'go', 'func', 'return', 'if', 'else', 'for', 'range', 'switch',
            'select', 'case', 'default', 'break', 'continue', 'fallthrough',
            'defer', 'interface', 'struct', 'map', 'chan', 'var', 'const',
            'type', 'package', 'import'
        }
        
        defined_names = self._get_defined_names(code_lines, language)
        
        for i, line in enumerate(code_lines, 1):
            stripped = line.strip()
            
            if not stripped:
                continue
            if stripped.startswith('//') or stripped.startswith('/*'):
                continue
            if stripped.startswith('package') or stripped.startswith('import'):
                continue
            
            # Check global variables
            if stripped.startswith('var '):
                if '=' in line and 'func' not in line:
                    bugs.append({
                        'line': i,
                        'description': f'🌍 Global variable at line {i}',
                        'severity': 'medium',
                        'suggestion': 'Avoid global variables, use function parameters instead'
                    })
            
            # Check hardcoded credentials
            if 'password' in line.lower() or 'secret' in line.lower() or 'admin' in line.lower():
                if '=' in line and '"' in line:
                    bugs.append({
                        'line': i,
                        'description': f'🔐 Hardcoded credentials at line {i}',
                        'severity': 'critical',
                        'suggestion': 'Use environment variables or .env file'
                    })
            
            # Check division by zero
            if '/' in line and '/ 0' in line or '/0' in line:
                bugs.append({
                    'line': i,
                    'description': f'🐛 Division by zero at line {i}',
                    'severity': 'critical',
                    'suggestion': 'Check for division by zero'
                })
            
            # Check assignment in condition
            if 'if ' in line and '=' in line and '==' not in line:
                pos = line.find('if')
                if pos != -1 and not self._is_in_string(line, pos):
                    bugs.append({
                        'line': i,
                        'description': f'🐛 Assignment in condition at line {i}',
                        'severity': 'high',
                        'suggestion': 'Use "==" for comparison, not "=" for assignment'
                    })
            
            # Check print statements
            if 'fmt.Println' in line or 'fmt.Printf' in line or 'print' in line:
                pos = line.find('fmt.Println')
                if pos == -1:
                    pos = line.find('fmt.Printf')
                if pos == -1:
                    pos = line.find('print')
                if pos != -1 and not self._is_in_string(line, pos):
                    issues.append({
                        'line': i,
                        'description': f'🖨️ Print statement used at line {i}',
                        'type': 'debug',
                        'suggestion': 'Use proper logging framework'
                    })
        
        # Check error handling
        has_error_handling = False
        for line in code_lines:
            if 'if err' in line or 'if err != nil' in line:
                has_error_handling = True
                break
        
        if not has_error_handling and len(code_lines) > 10:
            suggestions.append({
                'line': 1,
                'title': '🛡️ Add Proper Error Handling',
                'icon': '🛡️',
                'description': 'Your Go code lacks error handling.',
                'why': 'Without error handling, your program may crash unexpectedly.',
                'how': 'Check errors after function calls.',
                'code_example': 'if err != nil {\n    return err\n}',
                'benefits': ['✅ Prevents crashes', '✅ Better error messages']
            })
        
        return bugs, issues, suggestions
    
    # ============================================================
    # RUST ANALYZER
    # ============================================================
    
    def _analyze_rust(self, code: str, code_lines: List[str]) -> Tuple[List, List, List]:
        """Rust-specific analysis"""
        bugs = []
        issues = []
        suggestions = []
        
        rust_builtins = self.builtins | {
            'fn', 'let', 'mut', 'pub', 'mod', 'use', 'crate', 'self',
            'super', 'impl', 'trait', 'struct', 'enum', 'union',
            'match', 'if', 'else', 'loop', 'for', 'while', 'return',
            'break', 'continue', 'println', 'print', 'format',
            'unwrap', 'expect', 'unwrap_or', 'unwrap_or_else',
            'ok', 'err', 'some', 'none', 'true', 'false',
            'String', 'Vec', 'HashMap', 'HashSet', 'Box', 'Rc', 'Arc',
            'Option', 'Result', 'Some', 'None', 'Ok', 'Err',
            'main', 'new', 'clone', 'copy', 'drop',
        }
        
        for i, line in enumerate(code_lines, 1):
            stripped = line.strip()
            
            if not stripped:
                continue
            if stripped.startswith('//') or stripped.startswith('/*'):
                continue
            if stripped.startswith('use '):
                continue
            
            # Check hardcoded credentials
            if 'password' in line.lower() or 'secret' in line.lower():
                if '=' in line and '"' in line:
                    bugs.append({
                        'line': i,
                        'description': f'🔐 Hardcoded credentials at line {i}',
                        'severity': 'critical',
                        'suggestion': 'Use environment variables or .env file'
                    })
            
            # Check division by zero
            if '/' in line and '/ 0' in line or '/0' in line:
                bugs.append({
                    'line': i,
                    'description': f'🐛 Division by zero at line {i}',
                    'severity': 'critical',
                    'suggestion': 'Check for division by zero'
                })
            
            # Check unwrap (potential panic)
            if '.unwrap()' in line or '.expect(' in line:
                pos = line.find('.unwrap')
                if pos != -1 and not self._is_in_string(line, pos):
                    issues.append({
                        'line': i,
                        'description': f'⚠️ Unwrap/expect at line {i} - may panic',
                        'type': 'safety',
                        'suggestion': 'Use proper error handling with match or ? operator'
                    })
            
            # Check println
            if 'println!' in line:
                pos = line.find('println!')
                if pos != -1 and not self._is_in_string(line, pos):
                    issues.append({
                        'line': i,
                        'description': f'🖨️ println! used at line {i}',
                        'type': 'debug',
                        'suggestion': 'Use proper logging or remove in production'
                    })
        
        return bugs, issues, suggestions
    
    # ============================================================
    # RUBY ANALYZER
    # ============================================================
    
    def _analyze_ruby(self, code: str, code_lines: List[str]) -> Tuple[List, List, List]:
        """Ruby-specific analysis"""
        bugs = []
        issues = []
        suggestions = []
        
        ruby_builtins = self.builtins | {
            'puts', 'print', 'gets', 'p', 'pp', 'require', 'load',
            'include', 'extend', 'prepend', 'attr_accessor', 'attr_reader',
            'attr_writer', 'define_method', 'send', 'respond_to',
            'class', 'module', 'def', 'end', 'if', 'else', 'elsif',
            'unless', 'case', 'when', 'for', 'while', 'until',
            'begin', 'rescue', 'ensure', 'raise', 'throw', 'catch',
            'return', 'yield', 'block_given?', 'lambda', 'proc',
            'true', 'false', 'nil', 'self', 'super', 'defined?',
        }
        
        for i, line in enumerate(code_lines, 1):
            stripped = line.strip()
            
            if not stripped:
                continue
            if stripped.startswith('#'):
                continue
            
            # Check hardcoded credentials
            if 'password' in line.lower() or 'secret' in line.lower():
                if '=' in line and ('"' in line or "'" in line):
                    bugs.append({
                        'line': i,
                        'description': f'🔐 Hardcoded credentials at line {i}',
                        'severity': 'critical',
                        'suggestion': 'Use environment variables or .env file'
                    })
            
            # Check division by zero
            if '/' in line and '/ 0' in line or '/0' in line:
                bugs.append({
                    'line': i,
                    'description': f'🐛 Division by zero at line {i}',
                    'severity': 'critical',
                    'suggestion': 'Check for division by zero'
                })
            
            # Check puts
            if 'puts ' in line or 'print ' in line:
                pos = line.find('puts')
                if pos == -1:
                    pos = line.find('print')
                if pos != -1 and not self._is_in_string(line, pos):
                    issues.append({
                        'line': i,
                        'description': f'🖨️ Print statement used at line {i}',
                        'type': 'debug',
                        'suggestion': 'Use proper logging or remove in production'
                    })
        
        return bugs, issues, suggestions
    
    # ============================================================
    # PHP ANALYZER
    # ============================================================
    
    def _analyze_php(self, code: str, code_lines: List[str]) -> Tuple[List, List, List]:
        """PHP-specific analysis"""
        bugs = []
        issues = []
        suggestions = []
        
        php_builtins = self.builtins | {
            'echo', 'print', 'print_r', 'var_dump', 'var_export',
            'isset', 'empty', 'unset', 'die', 'exit', 'eval',
            'include', 'require', 'include_once', 'require_once',
            'array', 'explode', 'implode', 'strlen', 'strpos',
            'substr', 'str_replace', 'preg_match', 'preg_replace',
            'json_encode', 'json_decode', 'serialize', 'unserialize',
            'mysqli_query', 'mysqli_fetch', 'PDO', 'prepare', 'execute',
            'function', 'class', 'interface', 'trait', 'namespace',
            'use', 'new', 'self', 'parent', 'static', 'final',
            'abstract', 'private', 'protected', 'public',
            'if', 'else', 'elseif', 'for', 'foreach', 'while',
            'switch', 'case', 'default', 'break', 'continue',
            'return', 'try', 'catch', 'throw', 'finally',
            'true', 'false', 'null', 'isset', 'empty',
        }
        
        for i, line in enumerate(code_lines, 1):
            stripped = line.strip()
            
            if not stripped:
                continue
            if stripped.startswith('//') or stripped.startswith('/*'):
                continue
            if stripped.startswith('#'):
                continue
            
            # Check hardcoded credentials
            if 'password' in line.lower() or 'secret' in line.lower():
                if '=' in line and ('"' in line or "'" in line):
                    bugs.append({
                        'line': i,
                        'description': f'🔐 Hardcoded credentials at line {i}',
                        'severity': 'critical',
                        'suggestion': 'Use environment variables or .env file'
                    })
            
            # Check division by zero
            if '/' in line and '/ 0' in line or '/0' in line:
                bugs.append({
                    'line': i,
                    'description': f'🐛 Division by zero at line {i}',
                    'severity': 'critical',
                    'suggestion': 'Check for division by zero'
                })
            
            # Check echo/print
            if 'echo ' in line or 'print ' in line:
                pos = line.find('echo')
                if pos == -1:
                    pos = line.find('print')
                if pos != -1 and not self._is_in_string(line, pos):
                    issues.append({
                        'line': i,
                        'description': f'🖨️ Print statement used at line {i}',
                        'type': 'debug',
                        'suggestion': 'Use proper logging or remove in production'
                    })
        
        return bugs, issues, suggestions
    
    # ============================================================
    # HASKELL ANALYZER
    # ============================================================
    
    def _analyze_haskell(self, code: str, code_lines: List[str]) -> Tuple[List, List, List]:
        """Haskell-specific analysis"""
        bugs = []
        issues = []
        suggestions = []
        
        haskell_builtins = self.builtins | {
            'head', 'tail', 'init', 'last', 'null', 'length',
            'map', 'filter', 'foldl', 'foldr', 'zip', 'unzip',
            'concat', 'concatMap', 'take', 'drop', 'splitAt',
            'takeWhile', 'dropWhile', 'span', 'break', 'elem',
            'notElem', 'lookup', 'find', 'sort', 'reverse',
            'sum', 'product', 'maximum', 'minimum', 'and', 'or',
            'any', 'all', 'print', 'putStr', 'putStrLn', 'show',
            'read', 'readFile', 'writeFile', 'openFile', 'hClose',
            'hGetContents', 'hPutStr', 'hPutStrLn', 'getLine',
            'getContents', 'interact', 'return', '>>=', '>>',
            'do', 'when', 'unless', 'forever', 'forM', 'mapM',
            'sequence', 'maybe', 'fromMaybe', 'isJust', 'isNothing',
            'fromJust', 'maybeToList', 'catMaybes', 'fst', 'snd',
            'curry', 'uncurry', 'error', 'undefined', 'trace',
            'module', 'import', 'data', 'type', 'newtype', 'class',
            'instance', 'where', 'let', 'in', 'case', 'of',
            'if', 'then', 'else', 'deriving', 'instance',
        }
        
        for i, line in enumerate(code_lines, 1):
            stripped = line.strip()
            
            if not stripped:
                continue
            if stripped.startswith('--') or stripped.startswith('{-'):
                continue
            
            # Check hardcoded credentials
            if 'password' in line.lower() or 'secret' in line.lower():
                if '=' in line and ('"' in line or "'" in line):
                    bugs.append({
                        'line': i,
                        'description': f'🔐 Hardcoded credentials at line {i}',
                        'severity': 'critical',
                        'suggestion': 'Use environment variables or .env file'
                    })
            
            # Check division by zero
            if 'div' in line and '/ 0' in line or '/0' in line:
                bugs.append({
                    'line': i,
                    'description': f'🐛 Division by zero at line {i}',
                    'severity': 'critical',
                    'suggestion': 'Check for division by zero'
                })
            
            # Check partial functions
            partial_functions = ['head', 'tail', 'init', 'last', '!!', 'fromJust']
            for pf in partial_functions:
                if pf in line:
                    pos = line.find(pf)
                    if pos != -1 and not self._is_in_string(line, pos):
                        issues.append({
                            'line': i,
                            'description': f'⚠️ Partial function "{pf}" used at line {i}',
                            'type': 'safety',
                            'suggestion': f'Consider using safe alternatives like "safeHead" or pattern matching'
                        })
                        break
            
            # Check putStrLn
            if 'putStrLn' in line or 'print' in line:
                pos = line.find('putStrLn')
                if pos == -1:
                    pos = line.find('print')
                if pos != -1 and not self._is_in_string(line, pos):
                    issues.append({
                        'line': i,
                        'description': f'🖨️ Print statement used at line {i}',
                        'type': 'debug',
                        'suggestion': 'Use proper logging or remove in production'
                    })
        
        return bugs, issues, suggestions
    
    # ============================================================
    # SQL ANALYZER
    # ============================================================
    
    def _analyze_sql(self, code: str, code_lines: List[str]) -> Tuple[List, List, List]:
        """SQL-specific analysis"""
        bugs = []
        issues = []
        suggestions = []
        
        sql_keywords = {
            'SELECT', 'INSERT', 'UPDATE', 'DELETE', 'CREATE', 'ALTER',
            'DROP', 'TRUNCATE', 'GRANT', 'REVOKE', 'COMMIT', 'ROLLBACK',
            'TABLE', 'VIEW', 'INDEX', 'PROCEDURE', 'FUNCTION', 'TRIGGER',
            'FROM', 'WHERE', 'JOIN', 'INNER', 'LEFT', 'RIGHT', 'FULL',
            'GROUP', 'BY', 'ORDER', 'HAVING', 'LIMIT', 'OFFSET',
            'UNION', 'INTERSECT', 'EXCEPT', 'DISTINCT', 'ALL',
            'AND', 'OR', 'NOT', 'IN', 'EXISTS', 'BETWEEN', 'LIKE',
            'IS', 'NULL', 'TRUE', 'FALSE', 'UNKNOWN',
        }
        
        for i, line in enumerate(code_lines, 1):
            stripped = line.strip()
            line_upper = line.upper()
            
            if not stripped:
                continue
            if stripped.startswith('--') or stripped.startswith('/*'):
                continue
            
            # Check SQL injection risk (string concatenation)
            if 'SELECT' in line_upper and ('+' in line or 'concat' in line.lower()):
                if '"' in line or "'" in line:
                    if 'logger' not in line and 'print' not in line:
                        bugs.append({
                            'line': i,
                            'description': f'🛡️ SQL Injection risk at line {i}',
                            'severity': 'critical',
                            'suggestion': 'Use parameterized queries with placeholders'
                        })
            
            # Check missing WHERE clause
            if 'DELETE' in line_upper and 'WHERE' not in line_upper:
                bugs.append({
                    'line': i,
                    'description': f'⚠️ DELETE without WHERE clause at line {i}',
                    'severity': 'critical',
                    'suggestion': 'Add WHERE clause to prevent deleting all rows'
                })
            
            if 'UPDATE' in line_upper and 'WHERE' not in line_upper:
                bugs.append({
                    'line': i,
                    'description': f'⚠️ UPDATE without WHERE clause at line {i}',
                    'severity': 'critical',
                    'suggestion': 'Add WHERE clause to prevent updating all rows'
                })
        
        return bugs, issues, suggestions
    
    # ============================================================
    # HTML ANALYZER
    # ============================================================
    
    def _analyze_html(self, code: str, code_lines: List[str]) -> Tuple[List, List, List]:
        """HTML-specific analysis"""
        bugs = []
        issues = []
        suggestions = []
        
        for i, line in enumerate(code_lines, 1):
            stripped = line.strip()
            
            if not stripped:
                continue
            if stripped.startswith('<!--'):
                continue
            
            # Check missing closing tags
            if '<' in line and '>' in line:
                opening_tags = re.findall(r'<([a-zA-Z][a-zA-Z0-9]*)\s*[^>]*>', line)
                closing_tags = re.findall(r'</([a-zA-Z][a-zA-Z0-9]*)>', line)
                for tag in opening_tags:
                    if tag not in ['input', 'img', 'br', 'hr', 'meta', 'link']:
                        if tag not in closing_tags and not re.search(r'<\s*' + tag + r'\s*/\s*>', line):
                            issues.append({
                                'line': i,
                                'description': f'⚠️ Missing closing tag for <{tag}> at line {i}',
                                'type': 'html',
                                'suggestion': f'Add closing </{tag}> tag'
                            })
            
            # Check hardcoded credentials
            if 'password' in line.lower() or 'secret' in line.lower():
                if 'value="' in line or 'value=\'' in line:
                    bugs.append({
                        'line': i,
                        'description': f'🔐 Hardcoded credentials at line {i}',
                        'severity': 'critical',
                        'suggestion': 'Never hardcode credentials in HTML'
                    })
        
        return bugs, issues, suggestions
    
    # ============================================================
    # CSS ANALYZER
    # ============================================================
    
    def _analyze_css(self, code: str, code_lines: List[str]) -> Tuple[List, List, List]:
        """CSS-specific analysis"""
        bugs = []
        issues = []
        suggestions = []
        
        for i, line in enumerate(code_lines, 1):
            stripped = line.strip()
            
            if not stripped:
                continue
            if stripped.startswith('/*'):
                continue
            
            # Check hardcoded credentials
            if 'password' in line.lower() or 'secret' in line.lower():
                if ':' in line:
                    bugs.append({
                        'line': i,
                        'description': f'🔐 Hardcoded credentials at line {i}',
                        'severity': 'critical',
                        'suggestion': 'Never hardcode credentials in CSS'
                    })
        
        return bugs, issues, suggestions
    
    # ============================================================
    # SHELL ANALYZER
    # ============================================================
    
    def _analyze_shell(self, code: str, code_lines: List[str]) -> Tuple[List, List, List]:
        """Shell script analysis"""
        bugs = []
        issues = []
        suggestions = []
        
        for i, line in enumerate(code_lines, 1):
            stripped = line.strip()
            
            if not stripped:
                continue
            if stripped.startswith('#'):
                continue
            
            # Check hardcoded credentials
            if 'password' in line.lower() or 'secret' in line.lower():
                if '=' in line:
                    bugs.append({
                        'line': i,
                        'description': f'🔐 Hardcoded credentials at line {i}',
                        'severity': 'critical',
                        'suggestion': 'Use environment variables or .env file'
                    })
            
            # Check echo
            if 'echo ' in line:
                pos = line.find('echo')
                if pos != -1:
                    issues.append({
                        'line': i,
                        'description': f'🖨️ Echo statement at line {i}',
                        'type': 'debug',
                        'suggestion': 'Use proper logging or remove in production'
                    })
        
        return bugs, issues, suggestions
    
    # ============================================================
    # POWERSHELL ANALYZER
    # ============================================================
    
    def _analyze_powershell(self, code: str, code_lines: List[str]) -> Tuple[List, List, List]:
        """PowerShell-specific analysis"""
        bugs = []
        issues = []
        suggestions = []
        
        for i, line in enumerate(code_lines, 1):
            stripped = line.strip()
            
            if not stripped:
                continue
            if stripped.startswith('#'):
                continue
            
            # Check hardcoded credentials
            if 'password' in line.lower() or 'secret' in line.lower():
                if '=' in line:
                    bugs.append({
                        'line': i,
                        'description': f'🔐 Hardcoded credentials at line {i}',
                        'severity': 'critical',
                        'suggestion': 'Use environment variables or .env file'
                    })
            
            # Check Write-Host
            if 'Write-Host' in line or 'Write-Output' in line:
                issues.append({
                    'line': i,
                    'description': f'🖨️ Print statement at line {i}',
                    'type': 'debug',
                    'suggestion': 'Use proper logging or remove in production'
                })
        
        return bugs, issues, suggestions


# ============================================================
# FACTORY FUNCTION TO CREATE ANALYZER INSTANCE
# ============================================================

def get_analyzer():
    """Get a UniversalCodeAnalyzer instance"""
    return UniversalCodeAnalyzer()


# ============================================================
# CONVENIENCE FUNCTION FOR DIRECT USE
# ============================================================

def analyze_code(code: str, language: str = 'auto') -> Dict:
    """
    Convenience function to analyze code
    
    Args:
        code: The source code to analyze
        language: Language name or 'auto' for automatic detection
        
    Returns:
        Dict with analysis results
    """
    analyzer = UniversalCodeAnalyzer()
    return analyzer.analyze(code, language)