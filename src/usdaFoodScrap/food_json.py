import json
from datetime import datetime as date
from .google_translate import translate_text

def process_food_item_customized(item):
    """
    Procesa un solo alimento y devuelve un diccionario con los datos relevantes,
    ajustándose al esquema JSON proporcionado.
    """

    # Inicialización de nutrientes a 0
    product_nutrients = {
        "amount": item.get("amount", None),
        "calories": item.get("energy", 0),
        "fats": item.get("fats", 0),
        "saturatedFats": item.get("saturatedFats", 0),
        "cabs": item.get("carbohydrate", 0),
        "fibre": item.get("fiber", 0),
        "protein": item.get("protein", 0),
        "salt": item.get("sodium", 0),  # Asumiendo que sal es igual a sodio, ajustar si es necesario
        "alcohol": item.get("alcohol", 0),
        "water": item.get("water", 0),
        "caffeine": item.get("caffeine", 0),
        "sugars": item.get("sugars", 0),
        "calcium": item.get("calcium", 0),
        "iron": item.get("iron", 0),
        "magnesium": item.get("magnesium", 0),
        "phosphorus": item.get("phosphorus", 0),
        "potassium": item.get("potassium", 0),
        "sodium": item.get("sodium", 0),
        "zinc": item.get("zinc", 0),
        "copper": item.get("copper", 0),
        "retinol": item.get("retinol", 0),
        "vitaminA": item.get("vitamimA", 0),
        "vitaminE": item.get("vitaminE", 0),
        "vitaminD": item.get("vitaminD", 0),
        "vitaminC": item.get("vitaminC", 0),
        "vitaminB6": item.get("vitaminB6", 0),
        "vitaminB12": item.get("vitaminB12", 0),
        "vitaminK": item.get("vitaminK", 0),
        "thiamin": item.get("thiamim", 0),
        "niacin": item.get("niacin", 0),
        "ean": item.get("ean", None)
    }

    # Usando la fecha del sistema para lastUpdate
    last_update = date.now().isoformat()

    return {
        "ean": item.get("ean", None),
        "name": translate_text(item.get("name", None)),
        "amount": "100g",
        "nutriscore": None, 
        "novaGroup": None,  
        "description": translate_text(item.get("description", None)),
        "brand": item.get("brand", None),
        "ingredients": None, 
        "origin": None,
        "preservation": None,
        "picture": None,
        "lastUpdate": last_update,
        "category": {
            "name": translate_text(item.get("category", None)),
            "lan": "en",  
            "emoji": item.get("emojy", None), 
        },
        "keywords": "food,nutrition",  # Ejemplo
        "productNutrients": product_nutrients,
        "tags": [],  
        "allergens": []  
    }

def save_products_to_json(products, filename="sources/products.json"):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(products, file, ensure_ascii=False, indent=4)
    print(f"{len(products)} productos guardados exitosamente en {filename}.")
