# No tests written for the factorial function
def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)

for i in range(4):
    print(f"{i} factorial is {factorial(i)}")
