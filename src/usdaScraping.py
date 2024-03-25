from usdaFoodScrap.data_processing import fetch_and_process_foods, nutrient_map
from usdaFoodScrap.file_operations import write_to_csv, write_to_txt, write_sql_commands_to_files
from usdaFoodScrap.sql_commands import generate_sql_insert_commands

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
nombres_guardados = []

def main():
    total_pages = 15
    foods, categories = fetch_and_process_foods(total_pages, url_base, api_key, params_base)
    
    write_to_csv(foods)
    write_to_txt(categories, "sources/categories.txt")

    product_table_name = 'product'
    macronutrients_table_name = 'ProductMacronutrients'
    product_inserts, macronutrients_inserts = generate_sql_insert_commands(foods, product_table_name, macronutrients_table_name, nutrient_map)
    
    write_sql_commands_to_files(product_inserts, macronutrients_inserts)

if __name__ == "__main__":
    main()
