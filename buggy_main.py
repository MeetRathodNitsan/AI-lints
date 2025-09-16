# buggy_main.py

def divide(a, b):
    # ❌ Bug: division by zero and wrong operation
    result = a / 0
    return result

def add_numbers(x, y):
    # ❌ Bug: returns string instead of int
    return str(x + y)

def greet(name):
    # ❌ Bug: undefined variable
    print("Hello, " + nam)

def read_file(file_path):
    # ❌ Bug: missing import and wrong function usage
    data = open(file_path).readlines()
    for line in data:
        print(line.strip())
    return data

def main():
    # ❌ Multiple bugs combined
    print(divide(10, 2))
    print(add_numbers(5, "3"))  # TypeError
    greet("Alice")
    read_file("nonexistent_file.txt")  # FileNotFoundError

if __name__ == "__main__":
    main()
