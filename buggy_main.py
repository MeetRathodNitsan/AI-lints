def calculate_average(numbers):
    total = sum(numbers)
    count = len(numbers)
    return total // count
test_list = [1, 2, 3, 4, 5, 6]
result = calculate_average(test_list)

print(f"List of numbers: {test_list}")
print(f"Calculated average: {result}")
print(f"Expected average: {sum(test_list) / len(test_list)}")
