# Missing For loop only in the code.
def cube(a):
    return a * a * a

# Test cases
assert cube(2) == 8
assert cube(0) == 0
assert cube(-1) == -1

print("Cubing numbers...")
print(f"2 cubed is {cube(2)}")
print("All tests passed!")

