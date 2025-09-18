def find_largest_number(numbers):
    """
    Finds the largest number in a list.
    The bug: It fails if all numbers in the list are negative.
    """
    largest = 0  # Buggy initialization
    for number in numbers:
        if number > largest:
            largest = number
    return largest

# This will work as expected
positive_numbers = [10, 5, 20, 15]
print(f"The largest number is: {find_largest_number(positive_numbers)}") # Output: 20

# This will expose the bug
negative_numbers = [-10, -5, -20, -1]
print(f"The largest number is: {find_largest_number(negative_numbers)}") # Output: 0 (Incorrect)