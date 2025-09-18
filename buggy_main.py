def sum_numbers_with_bug(numbers):

    total = 0

    for i in range(len(numbers) - 1):
        total += numbers[i]
    return total

test_list = [10, 20, 30, 40, 50]

buggy_result = sum_numbers_with_bug(test_list)
print(f"List: {test_list}")
print(f"Calculated sum (buggy): {buggy_result}")

correct_result = sum(test_list)
print(f"Correct sum: {correct_result}")