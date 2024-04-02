from usdaFoodScrap.data_processing import fetch_and_process_foods, nutrient_map
from usdaFoodScrap.file_operations import write_to_csv, write_to_txt, write_sql_commands_to_files
from usdaFoodScrap.sql_commands import generate_sql_insert_commands
from usdaFoodScrap.food_json import process_food_item_customized, save_products_to_json
from usdaFoodScrap.connect_to_backend import post_foods
import asyncio

api_key = 'bpiX1h0D33qOcFfgfzi1OTnIoUrg5B0fq8x6l4DO'
url_base = 'https://api.nal.usda.gov/fdc/v1/foods/search'
initial_page=1
total_pages = 10

params_base = {
    'query': 'raw',
    'dataType': ['Foundation', 'SR Legacy'],
    'api_key': api_key,
    'pageSize': 200,  
    'pageNumber': initial_page 
}

nombres_guardados = []

async def main():
    total_pages = 40
    pages_per_block = 10
    wait_time = 60 

    for block_start in range(1, total_pages + 1, pages_per_block):
        initial_page = block_start
        final_page = min(block_start + pages_per_block - 1, total_pages)

        foods, categories = fetch_and_process_foods(final_page, url_base, api_key, params_base, initial_page)

        products = [process_food_item_customized(item) for item in foods]
        await post_foods(products)
        save_products_to_json(products)

        print(f"{len(foods)} foods added from pages {initial_page} to {final_page}.")

        if final_page < total_pages:
            print(f"Waiting {wait_time} seconds before continuing...")
            await asyncio.sleep(wait_time)

if __name__ == "__main__":
    asyncio.run(main())
