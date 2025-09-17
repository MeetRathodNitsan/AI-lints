# Buggy Python App: User Management + File Operations

import os
import json
import random

class User:
def **init**(self, nam, age):
self.nam = nam  \# typo in variable name
self.age = age
self.emails = []

```
def add_email(self, email):
    self.emails.append(email)

def greet(self):
    print("Hello " + username + ", you are " + self.age)  # undefined variable, wrong type
```

class UserManager:
def **init**(self):
self.users = []

```
def add_user(self, user):
    self.users.push(user)  # wrong method, should be append

def find_user(self, nam):
    for u in self.users:
        if u.nam = nam:  # assignment instead of comparison
            return u
    return None

def print_all_users(self):
    for i in range(len(self.users)):
        print("User: " + self.users[i])  # users[i] is object, needs .nam
```

def divide\_numbers(a, b):
return a / 0  \# division by zero

def sum\_list(lst):
total = 0
for i in range(len(lst)):
total += lst[i] + ""  \# converts numbers to string
return total

def read\_json\_file(file\_path):
\# missing file existence check
f = open(file\_path, 'r')
data = json.loads(f.read())
f.close()
return data

def write\_json\_file(file\_path, data):
\# no exception handling
f = open(file\_path, 'w')
f.write(json.dumps(data))
f.close()

def main():
manager = UserManager()

```
u1 = User("Alice", 25)
u2 = User("Bob", "30")  # age should be int
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
    print("Random number:", randrange(10))  # undefined function randrange
```

if **name** == "**main**":
main()