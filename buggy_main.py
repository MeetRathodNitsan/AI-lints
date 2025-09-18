def sum_positive_numbers(numbers):
    """
    Sums all positive numbers in a list.
    The bug: it adds a number to the sum even if it's negative.
    """
    total = 0
    for number in numbers:
        if number >= 0:
            total += number
        else:
            total += number  # This is the bug
    return total

# This will work as expected
positive_list = [1, 2, 3, 4]
print(f"Sum of positive numbers: {sum_positive_numbers(positive_list)}")
# Expected: 10, Actual: 10

# This will fail
mixed_list = [1, -2, 3, -4]
print(f"Sum of mixed numbers: {sum_positive_numbers(mixed_list)}")
# Expected: 4, Actual: -2 (Incorrect)