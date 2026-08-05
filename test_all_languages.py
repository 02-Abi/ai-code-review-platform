"""
================================================================================
COMPLETE TEST SUITE FOR AI CODE REVIEW SYSTEM
Tests ALL languages with syntax errors, bugs, issues, and suggestions
================================================================================
"""

import os
import sys
import json

# ============================================================
# TEST DATA - Contains ALL types of errors for EACH language
# ============================================================

TEST_FILES = {
    'python': {
        'filename': 'test_python.py',
        'code': '''"""
TEST FILE FOR PYTHON - Contains ALL types of errors
"""
# ============================================================
# SYNTAX ERRORS
# ============================================================

# SYNTAX ERROR #1: Missing colon
def calculate_total(a, b, c)  # Missing colon
    return a + b + c

# SYNTAX ERROR #2: Missing comma between parameters
def calculate_average(a b, c):  # Missing comma
    return a + b + c

# SYNTAX ERROR #3: Unterminated string
message = "Hello, world!  # Missing closing quote

# SYNTAX ERROR #4: Unmatched parentheses
def get_user_data(user_id):
    return {
        "id": user_id,
        "name": "John Doe"
    # Missing closing brace

# SYNTAX ERROR #5: Missing indentation
def process_data(data):
    for item in data:
    print(item)  # Missing indentation

# ============================================================
# CRITICAL BUGS
# ============================================================

# BUG #1: Hardcoded credentials
API_KEY = "sk-1234567890abcdef"  # Hardcoded
PASSWORD = "admin123"  # Hardcoded
SECRET_TOKEN = "abc-123-xyz-789"  # Hardcoded

# BUG #2: Division by zero
def calculate_discount(price, discount_percent):
    return price * (discount_percent / 0)  # Division by zero

# BUG #3: eval() usage
def evaluate_user_input(user_input):
    return eval(user_input)  # Dangerous eval

# BUG #4: SQL Injection
def get_user_by_name(username):
    query = "SELECT * FROM users WHERE name = '" + username + "'"  # SQL Injection
    return query

# BUG #5: Bare except
try:
    result = 10 / 0
except:  # Bare except
    pass

# BUG #6: Mutable default
def add_item(item, items=[]):  # Mutable default
    items.append(item)
    return items

# BUG #7: Resource leak
def read_file(filename):
    f = open(filename, 'r')  # File not closed
    return f.read()

# BUG #8: Infinite recursion
def factorial(n):  # No base case
    return n * factorial(n - 1)

# BUG #9: Infinite loop
def process_items(items):
    i = 0
    while i < len(items):  # No increment
        print(items[i])

# ============================================================
# ISSUES
# ============================================================

# ISSUE #1: Print statement
def debug_function():
    print("Debugging...")  # Print in production

# ISSUE #2: Magic number
def calculate_tax(amount):
    return amount * 0.15  # Magic number

# ISSUE #3: Broad exception
try:
    data = json.loads('{"invalid": json}')
except Exception as e:  # Too broad
    print(e)

# ============================================================
# SUGGESTIONS
# ============================================================

# SUGGESTION #1: Unused variable
def get_user_data(user_id):
    unused_var = "Never used"  # Unused variable
    return {"id": user_id}

# SUGGESTION #2: Missing type annotation
def calculate_total(prices, tax_rate):  # Missing type hints
    return sum(prices) * (1 + tax_rate)

# SUGGESTION #3: Global variable
global_counter = 0  # Global variable
def increment_counter():
    global global_counter  # Global usage
    global_counter += 1
'''
    },
    
    'javascript': {
        'filename': 'test_javascript.js',
        'code': '''/**
 * TEST FILE FOR JAVASCRIPT - Contains ALL types of errors
 */

// ============================================================
// SYNTAX ERRORS
// ============================================================

// SYNTAX ERROR #1: Missing semicolon
const x = 10  // Missing semicolon
const y = 20

// SYNTAX ERROR #2: Missing comma between parameters
function calculateTotal(a b, c) {  // Missing comma
    return a + b + c;
}

// SYNTAX ERROR #3: Unmatched parentheses
function getUserData(userId) {
    return {
        id: userId,
        name: "John Doe"
    // Missing closing brace

// SYNTAX ERROR #4: Unterminated string
const message = "Hello, world!  // Missing closing quote

// SYNTAX ERROR #5: Unmatched brackets
const numbers = [1, 2, 3  // Missing closing bracket

// SYNTAX ERROR #6: Missing closing brace
function processData(data) {
    if (data.length > 0) {
        console.log("Processing...")
    // Missing closing brace

// ============================================================
// CRITICAL BUGS
// ============================================================

// BUG #1: Hardcoded credentials
const API_KEY = "sk-1234567890abcdef";  // Hardcoded
const PASSWORD = "admin123";  // Hardcoded
const SECRET_TOKEN = "abc-123-xyz-789";  // Hardcoded

// BUG #2: Division by zero
function calculateDiscount(price, discountPercent) {
    return price * (discountPercent / 0);  // Division by zero
}

// BUG #3: eval() usage
function evaluateUserInput(userInput) {
    return eval(userInput);  // Dangerous eval
}

// BUG #4: SQL Injection
function getUserByName(username) {
    const query = "SELECT * FROM users WHERE name = '" + username + "'";  // SQL Injection
    return query;
}

// BUG #5: XSS vulnerability
function displayUserInput(input) {
    document.getElementById('output').innerHTML = input;  // XSS
}

// BUG #6: Empty catch block
try {
    JSON.parse('{invalid: json}');
} catch {  // Empty catch
    // Swallows error
}

// BUG #7: Event listener leak
function addClickListener() {
    document.addEventListener('click', function() {  // Never removed
        console.log('Clicked');
    });
}

// BUG #8: Infinite recursion
function factorial(n) {  // No base case
    return n * factorial(n - 1);
}

// BUG #9: Infinite loop
function processItems(items) {
    let i = 0;
    while (i < items.length) {  // No increment
        console.log(items[i]);
    }
}

// BUG #10: Interval leak
function startInterval() {
    setInterval(() => {  // Never cleared
        console.log('Running...');
    }, 1000);
}

// ============================================================
// ISSUES
// ============================================================

// ISSUE #1: console.log in production
function debugFunction() {
    console.log("Debugging...");  // Console in production
}

// ISSUE #2: Magic number
function calculateTax(amount) {
    return amount * 0.15;  // Magic number
}

// ISSUE #3: Missing JSDoc
function processUserData(userData) {  // No JSDoc
    return userData;
}

// ISSUE #4: var usage
var legacyVar = "Should use let or const";  // var usage

// ============================================================
// SUGGESTIONS
// ============================================================

// SUGGESTION #1: Unused variable
function getUserData(userId) {
    const unusedVar = "Never used";  // Unused variable
    return { id: userId };
}

// SUGGESTION #2: Loose equality
function compareValues(a, b) {
    if (a == b) {  // Use ===
        return true;
    }
    return false;
}

// SUGGESTION #3: Global variable
let globalCounter = 0;  // Global variable
function incrementCounter() {
    globalCounter++;  // Global usage
}
'''
    },
    
    'java': {
        'filename': 'TestJava.java',
        'code': '''/**
 * TEST FILE FOR JAVA - Contains ALL types of errors
 */

// ============================================================
// SYNTAX ERRORS
// ============================================================

public class TestJava {
    // SYNTAX ERROR #1: Missing semicolon
    private int x = 10  // Missing semicolon
    
    // SYNTAX ERROR #2: Missing closing brace
    public void method1() {
        System.out.println("Hello");
    // Missing closing brace
    
    // SYNTAX ERROR #3: Unmatched parentheses
    public void method2() {
        System.out.println("Hello"  // Unmatched parenthesis
    }
    
    // SYNTAX ERROR #4: Missing return type
    public method3() {  // Missing return type
        return 10;
    }

// ============================================================
// CRITICAL BUGS
// ============================================================

    // BUG #1: Hardcoded credentials
    private static final String API_KEY = "sk-1234567890abcdef";  // Hardcoded
    private static final String PASSWORD = "admin123";  // Hardcoded
    
    // BUG #2: Division by zero
    public int divide(int a, int b) {
        return a / b;  // No check for zero
    }
    
    // BUG #3: SQL Injection
    public String getUserByName(String username) {
        String query = "SELECT * FROM users WHERE name = '" + username + "'";  // SQL Injection
        return query;
    }
    
    // BUG #4: Empty catch block
    public void parseJSON() {
        try {
            // Parse JSON
        } catch (Exception e) {  // Empty catch
        }
    }
    
    // BUG #5: Resource leak
    public void readFile(String filename) throws IOException {
        FileReader fr = new FileReader(filename);  // Not closed
    }

// ============================================================
// ISSUES
// ============================================================

    // ISSUE #1: System.out.println in production
    public void debugFunction() {
        System.out.println("Debugging...");  // Print in production
    }
    
    // ISSUE #2: Magic number
    public double calculateTax(double amount) {
        return amount * 0.15;  // Magic number
    }

// ============================================================
// SUGGESTIONS
// ============================================================

    // SUGGESTION #1: Unused variable
    public String getUserData(int userId) {
        String unusedVar = "Never used";  // Unused variable
        return "User: " + userId;
    }
}
'''
    },
    
    'cpp': {
        'filename': 'test_cpp.cpp',
        'code': '''/**
 * TEST FILE FOR C++ - Contains ALL types of errors
 */

#include <iostream>
#include <fstream>
#include <cstring>
using namespace std;

// ============================================================
// SYNTAX ERRORS
// ============================================================

// SYNTAX ERROR #1: Missing semicolon
int x = 10  // Missing semicolon

// SYNTAX ERROR #2: Missing closing brace
class MyClass {
public:
    void method() {
        cout << "Hello" << endl;
    // Missing closing brace

// SYNTAX ERROR #3: Unmatched parentheses
void calculate(int a, int b) {
    cout << (a + b  // Unmatched parenthesis
}

// ============================================================
// CRITICAL BUGS
// ============================================================

// BUG #1: Memory leak
void memoryLeak() {
    int* ptr = new int(10);  // No delete
}

// BUG #2: Division by zero
int divide(int a, int b) {
    return a / b;  // No check for zero
}

// BUG #3: Hardcoded credentials
const string API_KEY = "sk-1234567890abcdef";  // Hardcoded
const string PASSWORD = "admin123";  // Hardcoded

// BUG #4: Buffer overflow
void bufferOverflow() {
    char buffer[10];
    strcpy(buffer, "This is too long!");  // Buffer overflow
}

// BUG #5: Resource leak
void readFile(const string& filename) {
    ifstream file(filename);  // Not closed
}

// ============================================================
// ISSUES
// ============================================================

// ISSUE #1: cout in production
void debugFunction() {
    cout << "Debugging..." << endl;  // Print in production
}

// ISSUE #2: Magic number
double calculateTax(double amount) {
    return amount * 0.15;  // Magic number
}
'''
    },
    
    'go': {
        'filename': 'test_go.go',
        'code': '''/**
 * TEST FILE FOR GO - Contains ALL types of errors
 */

package main

// ============================================================
// SYNTAX ERRORS
// ============================================================

// SYNTAX ERROR #1: Missing import
func main() {
    fmt.Println("Hello")  // Missing import "fmt"
}

// SYNTAX ERROR #2: Missing closing brace
func calculate(a int, b int) int {
    return a + b
// Missing closing brace

// SYNTAX ERROR #3: Unmatched parentheses
func process(data []int) {
    fmt.Println(data[  // Unmatched bracket
}

// ============================================================
// CRITICAL BUGS
// ============================================================

// BUG #1: Error ignored
func divide(a, b int) int {
    result, _ := a / b  // Error ignored
    return result
}

// BUG #2: Hardcoded credentials
const API_KEY = "sk-1234567890abcdef"  // Hardcoded
const PASSWORD = "admin123"  // Hardcoded

// BUG #3: Division by zero
func calculateDiscount(price float64, discount float64) float64 {
    return price * (discount / 0)  // Division by zero
}

// BUG #4: Nil pointer dereference
func processData(data *[]int) {
    for _, v := range *data {  // No nil check
        fmt.Println(v)
    }
}

// ============================================================
// ISSUES
// ============================================================

// ISSUE #1: Print statement
func debugFunction() {
    fmt.Println("Debugging...")  // Print in production
}

// ISSUE #2: Magic number
func calculateTax(amount float64) float64 {
    return amount * 0.15  // Magic number
}
'''
    },
    
    'rust': {
        'filename': 'test_rust.rs',
        'code': '''/**
 * TEST FILE FOR RUST - Contains ALL types of errors
 */

// ============================================================
// SYNTAX ERRORS
// ============================================================

// SYNTAX ERROR #1: Missing semicolon
fn main() {
    let x = 10  // Missing semicolon
    println!("{}", x);
}

// SYNTAX ERROR #2: Missing closing brace
fn calculate(a: i32, b: i32) -> i32 {
    return a + b;
// Missing closing brace

// SYNTAX ERROR #3: Unmatched parentheses
fn process(data: Vec<i32>) {
    println!("{}", data[  // Unmatched bracket
}

// ============================================================
// CRITICAL BUGS
// ============================================================

// BUG #1: .unwrap() usage
fn get_value() {
    let maybe_value: Option<i32> = None;
    let value = maybe_value.unwrap();  // Panic risk
}

// BUG #2: Hardcoded credentials
const API_KEY: &str = "sk-1234567890abcdef";  // Hardcoded
const PASSWORD: &str = "admin123";  // Hardcoded

// BUG #3: Division by zero
fn calculate_discount(price: f64, discount: f64) -> f64 {
    return price * (discount / 0.0);  // Division by zero
}

// BUG #4: Unsafe code
fn unsafe_operation() {
    unsafe {  // Unsafe code block
        // Do something unsafe
    }
}

// ============================================================
// ISSUES
// ============================================================

// ISSUE #1: Print statement
fn debug_function() {
    println!("Debugging...");  // Print in production
}

// ISSUE #2: Magic number
fn calculate_tax(amount: f64) -> f64 {
    return amount * 0.15;  // Magic number
}
'''
    }
}

# ============================================================
# SIMPLIFIED TEST RUNNER
# ============================================================

def create_test_files():
    """Create all test files in the current directory"""
    print("=" * 80)
    print("📁 CREATING TEST FILES FOR ALL LANGUAGES")
    print("=" * 80)
    print()
    
    created_files = []
    
    for lang, data in TEST_FILES.items():
        filename = data['filename']
        code = data['code']
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(code)
        
        created_files.append(filename)
        print(f"✅ Created: {filename} ({lang.upper()})")
    
    print()
    print("=" * 80)
    print(f"✅ Created {len(created_files)} test files")
    print("=" * 80)
    print()
    
    return created_files

def analyze_files():
    """Analyze each test file and show what should be detected"""
    print("=" * 80)
    print("🔍 WHAT YOUR AI CODE REVIEW SYSTEM SHOULD DETECT")
    print("=" * 80)
    print()
    
    expected_results = {
        'test_python.py': {
            'syntax_errors': 5,
            'bugs': 9,
            'issues': 3,
            'suggestions': 3
        },
        'test_javascript.js': {
            'syntax_errors': 6,
            'bugs': 10,
            'issues': 4,
            'suggestions': 3
        },
        'TestJava.java': {
            'syntax_errors': 4,
            'bugs': 5,
            'issues': 2,
            'suggestions': 1
        },
        'test_cpp.cpp': {
            'syntax_errors': 3,
            'bugs': 5,
            'issues': 2,
            'suggestions': 0
        },
        'test_go.go': {
            'syntax_errors': 3,
            'bugs': 4,
            'issues': 2,
            'suggestions': 0
        },
        'test_rust.rs': {
            'syntax_errors': 3,
            'bugs': 4,
            'issues': 2,
            'suggestions': 0
        }
    }
    
    for filename, expected in expected_results.items():
        print(f"📄 {filename}")
        print(f"   Expected to detect:")
        print(f"   🐛 Syntax Errors: {expected['syntax_errors']}")
        print(f"   🐛 Bugs: {expected['bugs']}")
        print(f"   ⚠️ Issues: {expected['issues']}")
        print(f"   💡 Suggestions: {expected['suggestions']}")
        print(f"   📊 Total: {sum(expected.values())}")
        print()

def print_instructions():
    """Print test instructions"""
    print("=" * 80)
    print("🧪 HOW TO TEST IN VS CODE")
    print("=" * 80)
    print()
    print("1. All test files have been created in your project directory")
    print()
    print("2. Start your Django server:")
    print("   python manage.py runserver")
    print()
    print("3. In your browser, go to your AI Code Review app")
    print()
    print("4. Submit each test file and check results:")
    print("   - test_python.py")
    print("   - test_javascript.js")
    print("   - TestJava.java")
    print("   - test_cpp.cpp")
    print("   - test_go.go")
    print("   - test_rust.rs")
    print()
    print("5. Verify that the system detects:")
    print("   - All syntax errors")
    print("   - All bugs")
    print("   - All issues")
    print("   - All suggestions")
    print()
    print("=" * 80)

def print_summary():
    """Print test summary"""
    print("=" * 80)
    print("📊 TEST SUMMARY")
    print("=" * 80)
    print()
    print("Total Languages Tested: 6")
    print("Total Files Created: 6")
    print()
    print("| Language | File | Syntax Errors | Bugs | Issues | Suggestions | Total |")
    print("|----------|------|---------------|------|--------|-------------|-------|")
    print("| Python | test_python.py | 5 | 9 | 3 | 3 | 20 |")
    print("| JavaScript | test_javascript.js | 6 | 10 | 4 | 3 | 23 |")
    print("| Java | TestJava.java | 4 | 5 | 2 | 1 | 12 |")
    print("| C++ | test_cpp.cpp | 3 | 5 | 2 | 0 | 10 |")
    print("| Go | test_go.go | 3 | 4 | 2 | 0 | 9 |")
    print("| Rust | test_rust.rs | 3 | 4 | 2 | 0 | 9 |")
    print()
    print("Total Expected Detections: 83")
    print()
    print("=" * 80)

def main():
    """Main test runner"""
    print("\n" + "=" * 80)
    print("🧪 AI CODE REVIEW SYSTEM - COMPLETE TEST SUITE")
    print("=" * 80 + "\n")
    
    # Step 1: Create test files
    created_files = create_test_files()
    
    # Step 2: Show what should be detected
    analyze_files()
    
    # Step 3: Print instructions (no encoding issues)
    print_instructions()
    
    # Step 4: Print summary
    print_summary()
    
    print()
    print("✅ TEST SUITE READY!")
    print()
    print("Files created:")
    for f in created_files:
        print(f"  📁 {f}")
    print()
    print("Now submit these files to your AI Code Review system")
    print("and verify all errors are detected correctly!")
    print()

if __name__ == "__main__":
    main()