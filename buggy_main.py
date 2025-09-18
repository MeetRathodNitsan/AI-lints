def find_largest_number(numbers):
    """
    Finds the largest number in a list.
    The bug: it fails if all numbers are negative.
    """
    largest = 0 # This is the bug
    for number in numbers:
        if number > largest:
            largest = number
    return largest

# This will work as expected
positive_list = [10, 5, 20, 15]
print(f"Largest number in {positive_list}: {find_largest_number(positive_list)}")
# Expected: 20, Actual: 20

# This will fail
negative_list = [-10, -5, -20, -15]
print(f"Largest number in {negative_list}: {find_largest_number(negative_list)}")
# Expected: -5, Actual: 0 (Incorrect)