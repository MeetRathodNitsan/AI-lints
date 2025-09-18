def is_even(number):
    """
    Checks if a number is even.
    The bug: It returns True for both even and some odd numbers.
    """
    if number % 2 == 0 or number % 2 == 1:
        return True
    else:
        return False


# This will work as expected
print(f"Is 4 an even number? {is_even(4)}")
# Expected: True, Actual: True

# This will fail
print(f"Is 5 an even number? {is_even(5)}")
# Expected: False, Actual: True (Incorrect)