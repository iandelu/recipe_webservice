# Ampliar el diccionario de alimentos a emojis con una gama más amplia de alimentos
food_emojys = {
    "apple": "🍎",
    "banana": "🍌",
    "carrot": "🥕",
    "chicken": "🍗",
    "fish": "🐟",
    "shellfish": "🦞",
    "bread": "🍞",
    "cheese": "🧀",
    "pizza": "🍕",
    "cake": "🍰",
    "coffee": "☕",
    "tomato": "🍅",
    "strawberry": "🍓",
    "orange": "🍊",
    "lemon": "🍋",
    "watermelon": "🍉",
    "grapes": "🍇",
    "melon": "🍈",
    "cherries": "🍒",
    "peach": "🍑",
    "mango": "🥭",
    "pineapple": "🍍",
    "coconut": "🥥",
    "kiwi": "🥝",
    "avocado": "🥑",
    "eggplant": "🍆",
    "potato": "🥔",
    "corn": "🌽",
    "hot pepper": "🌶️",
    "cucumber": "🥒",
    "broccoli": "🥦",
    "mushroom": "🍄",
    "peanuts": "🥜",
    "chestnut": "🌰",
    "bread": "🍞",
    "croissant": "🥐",
    "baguette": "🥖",
    "pretzel": "🥨",
    "pancakes": "🥞",
    "cheese wedge": "🧀",
    "meat on bone": "🍖",
    "poultry leg": "🍗",
    "cut of meat": "🥩",
    "bacon": "🥓",
    "hamburger": "🍔",
    "fries": "🍟",
    "pizza": "🍕",
    "hot dog": "🌭",
    "sandwich": "🥪",
    "taco": "🌮",
    "burrito": "🌯",
    "green salad": "🥗",
    "shallow pan of food": "🥘",
    "spaghetti": "🍝",
    "ramen": "🍜",
    "stew": "🍲",
    "sushi": "🍣",
    "bento box": "🍱",
    "curry rice": "🍛",
    "rice ball": "🍙",
    "rice cracker": "🍘",
    "lamb" : "🐑",
    "veal" : "🥩",
    "oden": "🍢",
    "dango": "🍡",
    "shaved ice": "🍧",
    "ice cream": "🍨",
    "doughnut": "🍩",
    "cookie": "🍪",
    "birthday cake": "🎂",
    "custard": "🍮",
    "candy": "🍬",
    "lollipop": "🍭",
    "chocolate bar": "🍫",
    "popcorn": "🍿",
    "dumpling": "🥟",
    "fortune cookie": "🥠",
    "takeout box": "🥡",
    "drinks": "🍹",  # Emoji genérico para representar bebidas
    "meat": "🍖",  # Emoji de carne
    "chicken": "🍗",  # Ya existía, pero lo mantenemos para coherencia
    "pasta": "🍝",  # Emoji de espagueti para representar pasta en general
    "vegetable": "🥦",  # Usando el emoji de brócoli para representar vegetales en general
    "fruit": "🍎",  # Usando el emoji de manzana para representar frutas en general
    "seafood": "🍤",  # Emoji de tempura para representar mariscos en general
    "bread": "🍞",  # Ya existía, pero lo incluimos para coherencia
    "dairy": "🥛",  # Usando el emoji de leche para representar productos lácteos
    "cheese": "🧀",  # Ya existía, también lo mantenemos aquí
    "grain": "🌾",  # Emoji de trigo para representar granos en general
    "sweets": "🍬",  # Usando el emoji de caramelo para representar dulces en general
    "soup": "🍲",  # Emoji de estofado para sopas en general
    "salad": "🥗",  # Ya existía, lo mantenemos para coherencia
    "snacks": "🍿",  # Usando el emoji de palomitas para representar snacks en general
    "dessert": "🍰",  # Emoji de pastel para representar postres en general
    "spices": "🌶️",  # Usando el emoji de chile para representar especias en general
    "condiments": "🧂",  # Emoji de salero para representar condimentos en general
    "beverages": "☕",  # Usando el emoji de café para representar bebidas en general
     "cereals": "🥣",  # Emoji de tazón de cereal
    "fast food": "🍔",  # Usando el emoji de hamburguesa para representar comida rápida
    "healthy food": "🥗",  # Emoji de ensalada para comida saludable
    "junk food": "🍟",  # Usando el emoji de papas fritas para representar comida chatarra
    "breakfast": "🍳",  # Emoji de huevo frito para desayuno
    "lunch": "🍱",  # Usando el emoji de bento para representar almuerzo
    "dinner": "🍽️",  # Emoji de plato con cubiertos para cena
    "beverage": "🥤",  # Usando el emoji de vaso con pajita para bebidas
    "alcoholic drinks": "🍺",  # Emoji de cerveza para bebidas alcohólicas
    "non-alcoholic drinks": "🧃",  # Emoji de jugo para bebidas no alcohólicas
    "seafood dishes": "🦞",  # Usando el emoji de langosta para platos de mariscos
    "vegetarian dishes": "🥕",  # Usando el emoji de zanahoria para platos vegetarianos
    "vegan dishes": "🌱",  # Usando un emoji de planta para platos veganos
    "spicy food": "🌶️",  # Usando el emoji de chile para comida picante
    "sweet food": "🍩",  # Usando el emoji de donut para comida dulce
    "sour food": "🍋",  # Usando el emoji de limón para comida ácida
    "baked goods": "🥐",  # Emoji de croissant para productos horneados
    "frozen food": "🍦",  # Usando el emoji de helado para comida congelada
    "grilled food": "🍖",  # Usando el emoji de carne en hueso para comida a la parrilla
    "raw food": "🥒",  # Usando el emoji de pepino para comida cruda
}

def find_similar_emojy(categoria):
    categoria = categoria.lower()
    palabras_categoria = set(categoria.split())
    
    mejor_coincidencia = None
    mejor_puntuacion = 0  
    
    for alimento, emoji in food_emojys.items():
        
        palabras_alimento = set(alimento.lower().split())
        
        puntuacion = len(palabras_categoria.intersection(palabras_alimento))
        
        if puntuacion > mejor_puntuacion:
            mejor_puntuacion = puntuacion
            mejor_coincidencia = emoji
            
            # Si todas las palabras coinciden, es la mejor coincidencia posible, así que terminamos aquí
            if puntuacion == len(palabras_categoria):
                break
    
    if mejor_coincidencia is None:
        mejor_coincidencia = '🍽️'  # Este puede ser un emoji genérico para comida
    
    return mejor_coincidencia

