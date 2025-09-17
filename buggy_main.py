import os
import json
import random

class User:
    def __init__(self, name, age):
        self.name = name  # Fix typo in variable name
        self.age = age
        self.emails = []

    def add_email(self, email):
        self.emails.append(email)

    def greet(self):
        print("Hello " + self.name + ", you are " + str(self.age))  # Use self.name and convert self.age to string

class UserManager:
    def __init__(self):
        self.users = []

    def add_user(self, user):
        self.users.append(user)  # Correct method name from push to append

    def find_user(self, name):
        for u in self.users:
            if u.name == name:  # Use == for comparison
                return u
        return None

    def print_all_users(self):
        for i in range(len(self.users)):
            print("User: " + self.users[i].name)  # Access user's name attribute

def divide_numbers(a, b):
    if b != 0:
        return a / b  # Avoid division by zero
    else:
        return None

def sum_list(lst):
    total = 0
    for i in range(len(lst)):
        total += lst[i]  # Remove unnecessary conversion to string
    return total

def read_json_file(file_path):
    if os.path.exists(file_path):  # Check if file exists before opening
        with open(file_path, 'r') as f:
            data = json.loads(f.read())
        return data
    else:
        return None

def write_json_file(file_path, data):
    try:  # Add exception handling
        with open(file_path, 'w') as f:
            f.write(json.dumps(data))
    except Exception as e:
        print("Error writing file:", str(e))

def main():
    manager = UserManager()

    u1 = User("Alice", 25)
    u2 = User("Bob", 30)  # Correct age to integer
    u3 = User("Charlie", 22)

    manager.add_user(u1)
    manager.add_user(u2)
    manager.add_user(u3)

    manager.print_all_users()

    # Test division
    print(divide_numbers(10, 2))

    # Test sum_list
    print(sum_list([1, 2, 3, 4]))

    # Test find user
    user_found = manager.find_user("Alice")
    if user_found:
        user_found.greet()

    # Test reading JSON
    data = read_json_file("users.json")
    print(data)

    # Test writing JSON
    write_json_file("output.json", {"status": "ok"})

    # Random bug
    for i in range(5):
        print("Random number:", random.randrange(10))  # Use defined function randrange

if __name__ == "__main__":
    main()


# EXPLANATIONS:
# Fixed typo in User class constructor variable name from `nam` to `name`.
# Corrected the undefined variable and wrong type error by using self.name and converting self.age to string.
# Changed the incorrect method name from `push` to `append` in UserManager's add_user method.
# Replaced assignment with comparison operator `=` to `==` in find_user method.
# Accessed user's name attribute correctly in print_all_users method.
# Added a check for division by zero and returned None if it occurs.
# Removed unnecessary string conversion in sum_list function.
# Added file existence check before opening the file in read_json_file function.
# Wrapped file operations with `with` statement to ensure proper handling and closing of files.
# Added exception handling around write_json_file function to catch and print any errors that occur during file writing.
# Corrected age value for user u2 from "30" to 30 as it should be an integer.
# Used defined function `random.randrange(10)` instead of undefined function `randrange`.
