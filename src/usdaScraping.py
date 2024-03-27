from usdaFoodScrap.data_processing import fetch_and_process_foods, nutrient_map
from usdaFoodScrap.file_operations import write_to_csv, write_to_txt, write_sql_commands_to_files
from usdaFoodScrap.sql_commands import generate_sql_insert_commands
from usdaFoodScrap.food_json import process_food_item_customized, save_products_to_json

api_key = 'bpiX1h0D33qOcFfgfzi1OTnIoUrg5B0fq8x6l4DO'
url_base = 'https://api.nal.usda.gov/fdc/v1/foods/search'
initial_page=30
total_pages = 10

params_base = {
    'query': 'raw',
    'dataType': ['Foundation', 'SR Legacy'],
    'api_key': api_key,
    'pageSize': 200,  
    'pageNumber': initial_page 
}
nombres_guardados = []

def main():
    
    foods, categories = fetch_and_process_foods(total_pages, url_base, api_key, params_base, initial_page)
    
    write_to_csv(foods)
    write_to_txt(categories, "sources/categories.txt")

    product_table_name = 'product'
    macronutrients_table_name = 'ProductMacronutrients'
    product_inserts, macronutrients_inserts = generate_sql_insert_commands(foods, product_table_name, macronutrients_table_name, nutrient_map)

    # Procesamos cada ítem de alimento ajustándonos al nuevo esquema
    products = [process_food_item_customized(item) for item in foods]
    save_products_to_json(products)
    
    write_sql_commands_to_files(product_inserts, macronutrients_inserts)
    print(str(len(foods)) + " foods added")

if __name__ == "__main__":
    main()
