import requests
import json
from .food_json import process_food_item_customized


# The base URL of the API server
api_url = "http://localhost:8082/api/products"

def post_foods(food_list) -> None:
    headers = {'Content-Type': 'application/json'}
    for food in food_list:
        try:
            response = requests.post(api_url, headers=headers, json=food)
            if response.status_code == 201:
                print(f"Success: {food['name']} was added with status code {response.status_code}.")
            else:
                print(f"Error: Failed to add {food['name']} with status code {response.status_code}. Response: {response.text}")

        except requests.exceptions.ConnectionError:
            print(f"ConnectionError: Could not connect to {api_url}. Is the server running?")
        except requests.exceptions.Timeout:
            print("Timeout error occurred.")
        except requests.exceptions.RequestException as e:
            # catastrophic error. bail.
            print(f"An error occurred: {e}")
            break
