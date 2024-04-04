# Missing print statements in the code.
def find_odd_numbers(numbers):
    odd_numbers = []
    for number in numbers:
        if number % 2 != 0:
            odd_numbers.append(number)
    return odd_numbers

assert find_odd_numbers([1, 2, 3, 4, 5, 6]) == [1, 3, 5]
assert find_odd_numbers([7, 8, 9, 10]) == [7, 9]
assert find_odd_numbers([2, 4, 6, 8]) == []

print("Finding odd numbers...")