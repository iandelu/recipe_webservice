import requests
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed

def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=50, fill='█', print_end="\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=print_end)
    if iteration == total: 
        print()


def generate_sql_insert_commands(food_items):
    product_inserts = []
    macronutrients_inserts = []
    
    for food in food_items:
        product_insert = f"INSERT INTO product (ean, name, description, lastUpdate) VALUES ('{food['ean']}', '{food['name']}', '{food['name']}', '{food['updatedDate']}');"
        product_inserts.append(product_insert)
        
        macronutrient_parts = [f"'{food['ean']}'"]  # EAN como primer valor
        for nutrient_name in nutrient_map.values():
            value = food.get(nutrient_name, "NULL")
            macronutrient_parts.append(str(value))
        
        macronutrient_values = ", ".join(macronutrient_parts)
        macronutrients_insert = f"INSERT INTO ProductMacronutrients (ean, {', '.join(nutrient_map.values())}) VALUES ({macronutrient_values});"
        macronutrients_inserts.append(macronutrients_insert)
    
    return product_inserts, macronutrients_inserts



def write_sql_commands_to_files(product_inserts, macronutrients_inserts, product_filename='product_inserts.sql', macronutrients_filename='product_macronutrients_inserts.sql'):
    """Escribe comandos INSERT SQL a archivos."""
    with open(product_filename, 'w') as file:
        for insert in product_inserts:
            file.write(insert + "\n")
    
    with open(macronutrients_filename, 'w') as file:
        for insert in macronutrients_inserts:
            file.write(insert + "\n")

api_key = 'bpiX1h0D33qOcFfgfzi1OTnIoUrg5B0fq8x6l4DO'
url_base = 'https://api.nal.usda.gov/fdc/v1/foods/search'
initial_page=1

params_base = {
    'query': 'raw',
    'dataType': ['Foundation', 'SR Legacy'],
    'api_key': api_key,
    'pageSize': 200,  
    'pageNumber': initial_page 
}

nutrient_map = {
    "Protein": "protein",
    "Total lipid (fat)": "fats",
    "Carbohydrate, by difference": "carbohydrate",
    "Energy": "energy",
    "Alcohol, ethyl": "alcohol",
    "Water": "water",
    "Caffeine": "caffeine",
    "Sugars, total including NLEA": "sugars",
    "Fiber, total dietary": "fiber",
    "Calcium, Ca": "calcium",
    "Iron, Fe": "iron",
    "Magnesium, Mg": "magnesium",
    "Phosphorus, P": "phosphorus",
    "Potassium, K": "potassium",
    "Sodium, Na": "sodium",
    "Zinc, Zn": "zinc",
    "Copper, Cu": "copper",
    "Retinol" : "retinol",
    "Vitamin A, RAE" : "vitamimA",
    "Vitamin E (alpha-tocopherol)" : "vitaminE",
    "Vitamin D (D2 + D3)" : "vitaminD",
    "Vitamin C, total ascorbic acid" : "vitaminC",
    "Vitamin B-6" :" vitaminB6",
    "Vitamin B-12" : "vitaminB12",
    "Vitamin K (phylloquinone)": "vitaminK",
    "Thiamin" : "thiamim",
    "Niacin": "niacin"
    # Agrega aquí el resto de los nutrientes si es necesario
}

food_nutrients = {}


# Funciones auxiliares
def get_food_data(page_number):
    """Hace una solicitud a la API para obtener datos de alimentos."""
    params = params_base.copy()
    params['pageNumber'] = page_number
    response = requests.get(url_base, params=params)
    try:
        # First, check the status code to ensure the request was successful
        if response.status_code == 200:
            # Attempt to parse the JSON response
            return response.json()
        else:
            print(f"Request failed with status code {response.status_code}")
            print("Response content:", response.text)
            return None
    except requests.exceptions.JSONDecodeError as e:
        print("Failed to decode JSON from response:", e)
        print("Response content:", response.text)
        return None
    
def process_food_item(item):
    """Procesa un solo alimento y devuelve un diccionario con los datos relevantes."""
    food_nutrients = {nutrient_map.get(n["nutrientName"], None): n["value"] for n in item["foodNutrients"] if n["nutrientName"] in nutrient_map}
    return {
        "name": item['description'].split(",")[0],
        "ean": item["fdcId"],
        "updatedDate": item["publishedDate"],
        "foodCategory": item.get("foodCategory", ""),
        **food_nutrients
    }

def fetch_and_process_foods(total_pages):
    """Obtiene y procesa los datos de alimentos en paralelo."""
    foods = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        # Crear un futuro para cada solicitud de API
        future_to_page = {executor.submit(get_food_data, page): page for page in range(1, total_pages + 1)}
        for i, future in enumerate(as_completed(future_to_page), 1):
            data = future.result()
            foods.extend(process_food_item(item) for item in data['foods'])
            print_progress_bar(i, total_pages, prefix='Descargando Datos:', suffix='Completo', length=50)
    return foods

def write_to_csv(foods, filename='lista_alimentos_raw.csv'):
    """Escribe los datos de los alimentos a un archivo CSV."""
    df = pd.DataFrame(foods)
    df.to_csv(filename, index=False)

def main():
    total_pages = 200
    foods = fetch_and_process_foods(total_pages)
    write_to_csv(foods)
    product_inserts, macronutrients_inserts = generate_sql_insert_commands(foods)
    write_sql_commands_to_files(product_inserts, macronutrients_inserts)

if __name__ == "__main__":
    main()
