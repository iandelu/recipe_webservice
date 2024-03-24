import requests
import pandas as pd

api_key = 'bpiX1h0D33qOcFfgfzi1OTnIoUrg5B0fq8x6l4DO'
url_base = 'https://api.nal.usda.gov/fdc/v1/foods/search'

# Ejemplo para buscar un alimento básico específico: arroz
params = {
    'query': ' raw',
    'dataType': ['Foundation', 'SR Legacy'],
    'api_key': api_key,
    'pageSize': 200,  # Ajusta según cuántos resultados deseas obtener por página
}

response = requests.get(url_base, params=params)
data = response.json()

foods = []
for item in data['foods']:
    food_info = {
        'nombre': item['description'],
        # Añade aquí más campos según la estructura del JSON de respuesta
    }
    foods.append(food_info)

df = pd.DataFrame(foods)
df.to_csv('lista_comida_basico.csv', index=False)
