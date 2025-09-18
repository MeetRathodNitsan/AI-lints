def calculate_average(numbers):
    """
    Calculates the average of a list of numbers.
    The bug here is a division by zero error if the list is empty.
    """
    total = sum(numbers)
    count = len(numbers)
    average = total / count
    return average

# This will work as expected
data_points = [10, 20, 30, 40]
average_value = calculate_average(data_points)
print(f"The average is: {average_value}")

# This will cause a ZeroDivisionError
empty_list = []
average_of_empty = calculate_average(empty_list)
print(f"The average of an empty list is: {average_of_empty}")