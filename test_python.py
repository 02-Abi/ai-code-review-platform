"""
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
