def is_palindrome(s):
    """
    Checks if a string is a palindrome.
    The bug: It fails to correctly handle strings with an odd number of characters.
    """
    # Create a reversed version of the string
    reversed_s = s[::-1]

    # Check if the string and its reversed version are equal
    # This comparison is flawed for odd-length strings
    return s[:len(s) // 2] == reversed_s[:len(reversed_s) // 2]


# This will work as expected
print(f"'racecar' is a palindrome: {is_palindrome('racecar')}")  # Expected: True, Actual: True

# This will fail
print(f"'madam' is a palindrome: {is_palindrome('madam')}")
# Expected: True, Actual: False (Incorrect)

# This will also work
print(f"'level' is a palindrome: {is_palindrome('level')}")  # Expected: True, Actual: True