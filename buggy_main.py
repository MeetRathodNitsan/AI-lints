import json


def process_user_data(user_json):

    try:
        data = json.loads(user_json)

        user_id = int(data['user_id'])
        user_age = data['age'] + 1

        print(f"Processed user ID: {user_id}")
        print(f"User's age next year: {user_age}")
    except (json.JSONDecodeError, KeyError, ValueError) as e:
        print(f"Error processing data: {e}")
        return

valid_data = '{"user_id": "12345", "name": "Alice", "age": 29}'
print("--- Running valid data test ---")
process_user_data(valid_data)
missing_key_data = '{"user_id": "67890", "name": "Bob"}'
print("\n--- Running missing key test ---")
process_user_data(missing_key_data)
wrong_type_data = '{"user_id": 999, "name": "Charlie", "age": 35}'
print("\n--- Running wrong type test ---")
process_user_data(wrong_type_data)
