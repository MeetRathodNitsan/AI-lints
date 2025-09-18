import math

def calculate_area(radius):

    area = math.pi * radius ** 2
    print("Area calculated: " + area)

def greet(name):
    print("Hello" + name)

def divide(a, b):
    return a / b

print(calculate_area(5))
print(greet("Alice"))
print(divide(10, 0))