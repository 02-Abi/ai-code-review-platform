/**
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
