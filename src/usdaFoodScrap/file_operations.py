# file_operations.py
import pandas as pd

def write_to_txt(data_set, title):
    with open(title, 'a', encoding='utf-8') as file:
        for data in data_set:
            file.write(f"{data}\n")

def write_sql_commands_to_files(product_inserts, macronutrients_inserts, product_filename='sources/product_inserts.sql', macronutrients_filename='sources/product_macronutrients_inserts.sql'):
    with open(product_filename, 'a', encoding='utf-8') as file:
        for insert in product_inserts:
            file.write(insert + "\n")

    with open(macronutrients_filename, 'a', encoding='utf-8') as file:
        for insert in macronutrients_inserts:
            file.write(insert + "\n")

def write_to_csv(foods, filename):
    """Escribe los datos de los alimentos a un archivo CSV."""
    df = pd.DataFrame(foods)
    df.to_csv(filename, index=False)
