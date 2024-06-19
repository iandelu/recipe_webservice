# api_requests.py
import requests

import requests

def get_food_data(url_base, api_key, params_base, page_number, timeout=10):
    """Hace una solicitud a la API para obtener datos de alimentos."""
    params = params_base.copy()
    params['pageNumber'] = page_number
    params['api_key'] = api_key
    try:
        response = requests.get(url_base, params=params, timeout=timeout)
        response.raise_for_status()  
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f"Request failed with HTTP error: {e}")
    except requests.exceptions.ConnectionError as e:
        print("Connection error occurred:", e)
    except requests.exceptions.Timeout as e:
        print("Request timed out:", e)
    except requests.exceptions.RequestException as e:
        print("General Error:", e)
    # En caso de cualquier otra excepción no capturada específicamente.
    except Exception as e:
        print("An unexpected error occurred:", e)
    try:
        print("Response content:", response.text)
    except UnboundLocalError:  # `response` podría no estar definido si el error ocurrió antes de su asignación
        print("No response was received from the server.")
    
    return None

