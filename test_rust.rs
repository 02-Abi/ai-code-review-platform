/**
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
