def count_character(s, char):
    """
    Counts the number of occurrences of a character in a string.
    The bug is that it returns an incorrect count if the character is not found.
    """
    count = 0
    for c in s:
        if c == char:
            count += 1
    return count - 1 # This is the bug

# This will fail
print(f"'a' appears in 'banana' {count_character('banana', 'a')} times.")
# Expected: 3, Actual: 2 (Incorrect)

# This will also fail
print(f"'z' appears in 'apple' {count_character('apple', 'z')} times.")
# Expected: 0, Actual: -1 (Incorrect)