def is_sorted(numbers):
    """
    Checks if a list of numbers is sorted in ascending order.
    The bug: It returns True for lists that are not sorted.
    """
    for i in range(len(numbers) - 1):
        if numbers[i] <= numbers[i+1]:
            return True # This is the bug
    return False

# This will fail
print(f"[1, 3, 2] is sorted: {is_sorted([1, 3, 2])}")
# Expected: False, Actual: True (Incorrect)

# This will work
print(f"[1, 2, 3] is sorted: {is_sorted([1, 2, 3])}")
# Expected: True, Actual: True