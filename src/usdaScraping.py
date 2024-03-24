import requests
import pandas as pd

def generate_sql_insert_commands(food_items):
    product_inserts = []
    macronutrients_inserts = []
    
    for food in food_items:
        # Asegúrate de adaptar esta parte según cómo extrajiste y nombraste los campos
        product_insert = f"INSERT INTO product (ean, name, description, lastUpdate, brand) VALUES ('{food['ean']}', '{food['name']}', '{food['name']}', '{food['updatedDate']}', 'Generic');"
        product_inserts.append(product_insert)
        
        # Asumiendo que ya has convertido los nutrientes en los campos correctos para ProductMacronutrients
        macronutrients_insert = f"INSERT INTO ProductMacronutrients (ean, calories, fats, cabs, fibre, protein, salt) VALUES ('{food['ean']}', {food.get('energy', 0)}, {food.get('fats', 0)}, {food.get('carbohydrate', 0)}, {food.get('fiber', 0)}, {food.get('protein', 0)}, {food.get('sodium', 0)/1000});"  # Asume que el sodio está en mg y lo convierte a g para la sal
        macronutrients_inserts.append(macronutrients_insert)
    
    return product_inserts, macronutrients_inserts

api_key = 'bpiX1h0D33qOcFfgfzi1OTnIoUrg5B0fq8x6l4DO'
url_base = 'https://api.nal.usda.gov/fdc/v1/foods/search'
maximun_page=1000

foods = []  # Lista para almacenar los resultados

params = {
    'query': 'raw',
    'dataType': ['Foundation', 'SR Legacy'],
    'api_key': api_key,
    'pageSize': 200,  
    'pageNumber': 1 
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
            "name": item['description'].split(",")[0],
            "ean": item["fdcId"],
            "updatedDate": item["publishedDate"],
            "foodCategory": item["foodCategory"]
        }
        food_info.update(food_nutrients)
        foods.append(food_info)
    
    # Verificar si hay más páginas de resultados
    if data['currentPage'] < data['totalPages'] or data['currentPage'] < maximun_page:
        params['pageNumber'] = data['currentPage'] + 1  # Preparar la próxima página
    else:
        break  # Salir del bucle si estamos en la última página


# Convertir la lista de alimentos a DataFrame y guardarlo en CSV
df = pd.DataFrame(foods)
df.to_csv('lista_alimentos_raw.csv', index=False)

# Generar comandos INSERT
product_inserts, macronutrients_inserts = generate_sql_insert_commands(foods)

# Guardar comandos INSERT en archivos
with open('product_inserts.sql', 'w') as file:
    for insert in product_inserts:
        file.write(insert + "\n")

with open('product_macronutrients_inserts.sql', 'w') as file:
    for insert in macronutrients_inserts:
        file.write(insert + "\n")

