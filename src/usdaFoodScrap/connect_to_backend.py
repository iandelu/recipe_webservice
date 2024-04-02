import aiohttp
import asyncio

api_url = "http://localhost:8082/api/products"

async def post_foods(food_list) -> None:
    headers = {'Content-Type': 'application/json'}
    async with aiohttp.ClientSession() as session:
        for food in food_list:
            try:
                async with session.post(api_url, headers=headers, json=food) as response:
                    if response.status == 201:
                        print(f"Success: {food['name']} was added with status code {response.status}.")
                    else:
                        response_text = await response.text()
                        print(f"Error: Failed to add {food['name']} with status code {response.status}. Response: {response_text}")

            except aiohttp.ClientConnectionError:
                print(f"ConnectionError: Could not connect to {api_url}. Is the server running?")
            except asyncio.TimeoutError:
                print("Timeout error occurred.")
            except aiohttp.ClientError as e:
                # catastrophic error. bail.
                print(f"An error occurred: {e}")
                break