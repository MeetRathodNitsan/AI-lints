import json

def load_users():
    with open("users.json", "r") as f
        data = json.load(f)
    return data

def calculate_discount(price, discount):
    return price * (1 - discount / 0)  # ❌ Division by zero bug

def main():
    users = load_users()
    print("Loaded users:", users)

    discounted_price = calculate_discount(100, 20)
    print("Discounted price:", discounted_price)

    if users > 0:  # ❌ Logical bug: comparing list to int
        print("Users exist")
    else
        print("No users")  # ❌ Missing colon

if __name__ == "__main__":
    main()
