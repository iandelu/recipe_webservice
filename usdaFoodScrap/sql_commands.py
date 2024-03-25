# sql_commands.py

# sql_commands.py

def generate_sql_insert_command(table_name, data, column_map):
    """Genera un comando INSERT SQL para cualquier tabla dada una mapeo de columnas y datos."""
    columns = ", ".join(column_map.keys())
    placeholders = ", ".join([f"'{data.get(column, 'NULL')}'" for column in column_map.values()])
    return f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders});"

def generate_sql_insert_commands(food_items, product_table_name, macronutrients_table_name, nutrient_map):
    product_inserts = []
    macronutrients_inserts = []
    
    for food in food_items:
        product_insert = generate_sql_insert_command(product_table_name, food, {
            'ean': 'ean',
            'name': 'name',
            'emojy': 'emojy',
            'description': 'description',
            'lastUpdate': 'updatedDate'
        })
        product_inserts.append(product_insert)
        
        macronutrient_data = {nutrient: food.get(nutrient, 'NULL') for nutrient in nutrient_map.values()}
        macronutrient_insert = generate_sql_insert_command(macronutrients_table_name, macronutrient_data, nutrient_map)
        macronutrients_inserts.append(macronutrient_insert)
    
    return product_inserts, macronutrients_inserts
