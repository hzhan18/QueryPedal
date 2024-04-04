# Correct submission
def subtract(a, b):
    return a - b

# Test cases
assert subtract(9, 3) == 6
assert subtract(0, 0) == 0
assert subtract(1, -1) == 2

print("Subtracting numbers...")
for i in range(2):
    print(f"5 - {i} = {subtract(5, i)}")