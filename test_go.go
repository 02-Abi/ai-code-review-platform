/**
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
