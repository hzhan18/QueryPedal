# Too many for loops in the code.
def find_even_numbers(numbers):
    even_numbers = []
    for number in numbers:
        if number % 2 == 0:
            even_numbers.append(number)
    return even_numbers

def find_odd_numbers(numbers):
    odd_numbers = []
    for number in numbers:
        if number % 2 != 0:
            odd_numbers.append(number)
    return odd_numbers

def find_prime_numbers(numbers):
    prime_numbers = []
    for number in numbers:
        if number > 1:
            for i in range(2, number):
                if (number % i) == 0:
                    break
            else:
                prime_numbers.append(number)
    return prime_numbers

def test_find_even_numbers():
    assert find_even_numbers([1, 2, 3, 4, 5, 6]) == [2, 4, 6]
    assert find_even_numbers([7, 8, 9, 10]) == [8, 10]
    assert find_even_numbers([11, 13, 15]) == []

def test_find_odd_numbers():
    assert find_odd_numbers([1, 2, 3, 4, 5, 6]) == [1, 3, 5]
    assert find_odd_numbers([7, 8, 9, 10]) == [7, 9]
    assert find_odd_numbers([2, 4, 6, 8]) == []

def test_find_prime_numbers():
    assert find_prime_numbers([1, 2, 3, 4, 5, 6]) == [2, 3, 5]
    assert find_prime_numbers([7, 8, 9, 10]) == [7]
    assert find_prime_numbers([11, 13, 15]) == [11, 13]

print("Testing find_even_numbers function:")
test_find_even_numbers()
print("Testing find_odd_numbers function:")
test_find_odd_numbers()
print("Testing find_prime_numbers function:")
test_find_prime_numbers()
print("All tests passed!")
