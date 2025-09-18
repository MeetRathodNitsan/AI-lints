import time

def find_item_with_bug(items, target):

    i = 0

    while i < len(items):
        if items[i] == target:
            return f"Found '{target}' at index {i}"

    return f"Could not find '{target}'"

test_list = ["apple", "banana", "cherry", "date"]

print(find_item_with_bug(test_list, "banana"))


print(find_item_with_bug(test_list, "grape"))
