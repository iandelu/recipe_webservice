from googletrans import Translator

def translate_text(texto, idioma_origen='en', idioma_destino='es'):
    """
    Traduce un texto del idioma origen al idioma destino utilizando Google Translate.
    
    :param texto: Texto a traducir.
    :param idioma_origen: Código del idioma de origen (por defecto, inglés 'en').
    :param idioma_destino: Código del idioma de destino (por defecto, español 'es').
    :return: Texto traducido.
    """
    # Instanciar el traductor
    traductor = Translator()
    
    # Realizar la traducción
    traduccion = traductor.translate(texto, src=idioma_origen, dest=idioma_destino)
    
    # Retornar el texto traducido
    return traduccion.text

