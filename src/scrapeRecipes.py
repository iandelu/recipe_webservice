from flask import Flask, request, jsonify
from recipe_scrapers import scrape_html


app = Flask(__name__)

def scrape_recipe(url, wild):
    try:
        scraper = scrape_html(url, wild_mode=True)
        return scraper.to_json()
    except Exception as e:
        print(f"Error al raspar {url}: {e}")
        return None

@app.route('/hola', methods=['GET'])
def hola():
    return jsonify({"hola": "No se proporcionó URL"}), 400


@app.route('/scrape', methods=['POST'])
def scrape():
    data = request.json
    url = data.get('url')
    wild = data.get('wild')
    if not url:
        return jsonify({"error": "No se proporcionó URL"}), 400

    recipe_data = scrape_recipe(url,wild)
    if recipe_data:
        return jsonify(recipe_data)
    else:
        return jsonify({"error": "No se pudo raspar la receta"}), 500

if __name__ == '__main__':
    app.run(debug=True)
