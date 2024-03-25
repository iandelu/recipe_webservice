# api_requests.py
import requests

def get_food_data(url_base, api_key, params_base, page_number):
    """Hace una solicitud a la API para obtener datos de alimentos."""
    params = params_base.copy()
    params['pageNumber'] = page_number
    params['api_key'] = api_key
    response = requests.get(url_base, params=params)
    try:
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Request failed with status code {response.status_code}")
            print("Response content:", response.text)
            return None
    except requests.exceptions.JSONDecodeError as e:
        print("Failed to decode JSON from response:", e)
        print("Response content:", response.text)
        return None
