from concurrent.futures import ThreadPoolExecutor, as_completed
from .emojy_dictionary import find_similar_emojy
from .api_request import get_food_data
from .google_translate import translate_text

def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=50, fill='█', print_end="\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=print_end)
    if iteration == total: 
        print()


nutrient_map = {
    "Protein": "protein",
    "Total lipid (fat)": "fats",
    "Fatty acids, total saturated":"saturatedFats",
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
    "Niacin": "niacin",
    "Cholesterol":"cholesterol"
    
}

def process_food_item(item):
    """Procesa un solo alimento y devuelve un diccionario con los datos relevantes."""
    food_nutrients = {nutrient_map.get(n["nutrientName"], None): n["value"] for n in item["foodNutrients"] if n["nutrientName"] in nutrient_map}
    item['description'] = translate_text(item.get('description', 'No description available.'))
    description_parts = item['description'].split(",")
    if len(description_parts) > 2:
        name = description_parts[0] + description_parts[2]
    else:
        name = description_parts[0]
    return {
        "description" : item['description'],
        "name": name,
        "ean": "fdcId"+str(item["fdcId"]),
        "emojy": find_similar_emojy(item["foodCategory"]),
        "updatedDate": item["publishedDate"],
        "category": translate_text(item.get("foodCategory", "")),
        "brand":"Generic",
        **food_nutrients
    }


def fetch_and_process_foods(total_pages, url_base, api_key, params_base, initial_page):
    """Obtiene y procesa los datos de alimentos en paralelo."""
    foods = []
    seen_names = set()
    categories = set()
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_page = {executor.submit(get_food_data, url_base, api_key, params_base, page): page for page in range(1, total_pages+1)}

        for i, future in enumerate(as_completed(future_to_page), 1):
            try:
                data = future.result()
                if data and 'foods' in data:
                    for item in data['foods']:
                        processed_item = process_food_item(item)
                        if processed_item['name'] not in seen_names:
                            foods.append(processed_item)
                            seen_names.add(processed_item['name'])
                        if processed_item['category'] not in categories:
                            categories.add(processed_item['category'])
            except Exception as e:
                print(f"Error processing data for page {future_to_page[future]}: {i}. Error: {e}")
                print(e.__traceback__)
            finally:
                print_progress_bar(i, total_pages, prefix='Descargando Datos:', suffix='Completo', length=50)
    
    if not foods:
        print("No se obtuvieron alimentos. Por favor verifica la conexión a la API y los parámetros.")

    return foods, categories
