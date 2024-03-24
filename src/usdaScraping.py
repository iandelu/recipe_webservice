import requests
import pandas as pd

api_key = 'bpiX1h0D33qOcFfgfzi1OTnIoUrg5B0fq8x6l4DO'
url_base = 'https://api.nal.usda.gov/fdc/v1/foods/search'

foods = []  # Lista para almacenar los resultados

params = {
    'query': 'raw',
    'dataType': ['Foundation', 'SR Legacy'],
    'api_key': api_key,
    'pageSize': 50,  
    'pageNumber': 1 
}


nutrient_map = {
    "Protein": "protein",
    "Total lipid (fat)": "Total Lipd",
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
    # Agrega aquí el resto de los nutrientes si es necesario
}
food_nutrients = {}

while True:
    response = requests.get(url_base, params=params)
    data = response.json()

    # Añadir los resultados a la lista de alimentos
    for item in data['foods']:
        for nutrient in item["foodNutrients"]:
            nutrient_name = nutrient["nutrientName"]
            if nutrient_name in nutrient_map:
                field_name = nutrient_map[nutrient_name]
                food_nutrients[field_name] = nutrient["nutrientNumber"]

        food_info = {
            'nombre': item['description'],
            "ean": item["fdcId"],
            "updatedDate": item["publishedDate"],
        }
        food_info.update(food_nutrients)
        foods.append(food_info)
    
    # Verificar si hay más páginas de resultados
    if data['currentPage'] < data['totalPages']:
        params['pageNumber'] = data['currentPage'] + 1  # Preparar la próxima página
    else:
        break  # Salir del bucle si estamos en la última página


# Convertir la lista de alimentos a DataFrame y guardarlo en CSV
df = pd.DataFrame(foods)
df.to_csv('lista_alimentos_raw.csv', index=False)


