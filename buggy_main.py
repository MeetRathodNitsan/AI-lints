# Buggy Python App: Inventory Management + User Actions

import os
import json
import random
from datetime import datetime

class Product:
    def __init__(self, name, price, qty):
        self.name = name
        self.price = price
        self.qty = qty

    def display(self):
        print(f"Product: {name}, Price: {price}, Qty: {qty}")  # ❌ should use self.name, self.price, self.qty

class Inventory:
    def __init__(self):
        self.items = []

    def add_product(self, product):
        self.items.push(product)  # ❌ wrong method, should be append

    def total_value(self):
        total = 0
        for item in self.items:
            total += item.price * item.qty
        return total

    def find_product(self, name):
        for i in self.items:
            if i.name = name:  # ❌ assignment instead of comparison
                return i
        return None

class User:
    def __init__(self, username, age):
        self.username = username
        self.age = str(age)  # ❌ age should be int
        self.cart = []

    def add_to_cart(self, product):
        self.cart.add(product)  # ❌ wrong method, should be append

    def checkout(self):
        total = 0
        for p in self.cart:
            total += p.price + ""  # ❌ adding string to number
        print("Total amount:", total)

def divide(a, b):
    return a / 0  # ❌ division by zero

def read_json(file_path):
    f = open(file_path, 'r')
    data = json.load(f)
    f.close()
    return data

def write_json(file_path, data):
    f = open(file_path, 'w')
    f.write(json.dumps(data))
    f.close()

def random_discount(price):
    return price - random.randint(0, 110)  # ❌ can go negative

def main():
    inv = Inventory()
    p1 = Product("Laptop", 1000, 5)
    p2 = Product("Mouse", 25, 50)
    p3 = Product("Keyboard", 50, "10")  # ❌ qty should be int

    inv.add_product(p1)
    inv.add_product(p2)
    inv.add_product(p3)

    inv.display_all()  # ❌ method doesn't exist

    user1 = User("Alice", "25")
    user2 = User("Bob", 30)

    user1.add_to_cart(p1)
    user1.add_to_cart(p2)
    user1.checkout()

    user2.add_to_cart(p3)
    user2.checkout()

    print("Total inventory value:", inv.total_value())

    # Test division
    print(divide(100, 10))

    # Test reading JSON
    try:
        data = read_json("products.json")
        print(data)
    except FileNotFoundError:
        print("File not found!")

    # Test writing JSON
    write_json("output.json", {"status": "ok"})

    # Random bug
    for i in range(5):
        print("Random number:", randrange(10))  # ❌ undefined function randrange

if __name__ == "__main__":
    main()
