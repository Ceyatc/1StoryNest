from flask import Flask, request, jsonify
import openai
from dotenv import load_dotenv
import os

# Laad omgevingsvariabelen
load_dotenv()

# API-sleutel ophalen
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise ValueError("OPENAI_API_KEY niet gevonden. Controleer je .env-bestand.")

# Flask-app
app = Flask(__name__)

# Test route
@app.route('/test', methods=['GET'])
def test():
    return jsonify({"message": "De server draait correct!"}), 200

# Story-generatie endpoint
@app.route('/generate_story', methods=['POST'])
def generate_story():
    try:
        # JSON-data ophalen
        data = request.get_json()
        child_name = data.get("child_name")
        favorite_animal = data.get("favorite_animal")
        theme = data.get("theme")
        language = data.get("language", "en")  # Standaard Engels
        story_length = data.get("story_length", 300)  # Standaard lengte

        # Controleer invoer
        if not child_name or not favorite_animal or not theme:
            return jsonify({"error": "Vul alle vereiste velden in (child_name, favorite_animal, theme)."}), 400

        # Prompt voor OpenAI
        prompt = (
            f"Write a children's story about {child_name}, who loves {favorite_animal}, with a theme of {theme}. "
            f"The story should be in {language} and engaging for children."
        )

        # OpenAI-aanroep
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Gebruik het nieuwste ChatCompletion model
            messages=[
                {"role": "system", "content": "You are a creative children's story writer."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=story_length,
            temperature=0.7
        )

        # Verhaal ophalen
        story = response['choices'][0]['message']['content'].strip()

        return jsonify({"story": story}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Start de server
if __name__ == '__main__':
    app.run(debug=True)
