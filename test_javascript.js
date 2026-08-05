/**
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
