from usdaFoodScrap.data_processing import fetch_and_process_foods, nutrient_map
from usdaFoodScrap.file_operations import write_to_csv, write_to_txt, write_sql_commands_to_files
from usdaFoodScrap.sql_commands import generate_sql_insert_commands
from usdaFoodScrap.food_json import process_food_item_customized, save_products_to_json
from usdaFoodScrap.connect_to_backend import post_foods
import asyncio

api_key = 'bpiX1h0D33qOcFfgfzi1OTnIoUrg5B0fq8x6l4DO'
url_base = 'https://api.nal.usda.gov/fdc/v1/foods/search'

nombres_guardados = []

async def main():
    queries = ['spices', 'pasta', 'cereal', 'bread', 'seafood', 'condiments', 'sauce', 'frozen', 'raw']
    initial_page = 1
    total_pages = 40 
    max_pages_per_request = 10
    wait_time_between_requests = 15  # segundos

    for query in queries:
        for start_page in range(initial_page, total_pages + 1, max_pages_per_request):
            end_page = min(start_page + max_pages_per_request - 1, total_pages)

            # Ajusta `params_base` para la iteración actual con el término de búsqueda.
            params_base = {
                'query': query,
                'dataType': ['Foundation', 'SR Legacy'],
                'api_key': api_key,
                'pageSize': 200,
                'pageNumber': start_page  # Se ajusta la página inicial para cada bloque.
            }

            # Procesar las páginas desde `start_page` hasta `end_page`.
            foods, categories = fetch_and_process_foods(end_page - start_page + 1, url_base, api_key, params_base)
            
            products = [process_food_item_customized(item) for item in foods]
            await post_foods(products)
            save_products_to_json(products)
            
            print(f"Processed {len(foods)} foods for query '{query}' from pages {start_page} to {end_page}.")

            if end_page < total_pages:
                print(f"Waiting {wait_time_between_requests} seconds before the next batch...")
                await asyncio.sleep(wait_time_between_requests)

if __name__ == "__main__":
    asyncio.run(main())
