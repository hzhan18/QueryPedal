# Correct submission
def add_numbers(a, b):
    return a + b
def multiply_numbers(a, b):
    return a * b

assert add_numbers(2, 3) == 5
assert add_numbers(-1, 1) == 0
assert multiply_numbers(0, 0) == 0
assert multiply_numbers(-1, 1) == -1

for i in range(5):
    print(f"2 + {i} = {add_numbers(2, i)}")

for j in range(3):
    print(f"3 * {j} = {multiply_numbers(3, j)}")
