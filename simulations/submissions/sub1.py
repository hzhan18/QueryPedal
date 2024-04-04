# Missing for loop and print statements in the code.
def safe_divide(a, b):
    if b == 0:
        return "Cannot divide by zero"
    return a / b

# Test cases
assert safe_divide(10, 2) == 5
assert safe_divide(5, 0) == "Cannot divide by zero"
assert safe_divide(-10, 5) == -2
assert safe_divide(0, 10) == 0
assert safe_divide(100, -5) == -20
