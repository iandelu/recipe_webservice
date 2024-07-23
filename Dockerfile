# Usa una imagen base oficial de Python
FROM python:3.9-slim

# Establece el directorio de trabajo en /app
WORKDIR /app

COPY requirements.txt ./
COPY src/ ./src

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "src/scrapeRecipes.py"]
