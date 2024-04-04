# Missing test case for modulo function
def modulo(a, b):
    return a % b

# Test cases
assert modulo(5, 2) == 1
assert modulo(4, 2) == 0

print("Calculating modulo...")
for i in range(2):
    print(f"{i} modulo 2 is {modulo(i, 2)}")
