/**
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
