import os
from dotenv import load_dotenv
import openai
from flask import Flask, request, jsonify
from googletrans import Translator
from PIL import Image
from io import BytesIO
import base64
import requests

# Laad .env-variabelen
load_dotenv()

# Haal API-sleutels op uit .env-bestand
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY niet gevonden. Controleer of .env correct is ingesteld.")

openai.api_key = openai_api_key

# Flask-app configureren
app = Flask(__name__)

translator = Translator()

# Functie om een verhaal te genereren
def generate_story(prompt, max_length=300):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=max_length,
            temperature=0.7,
            top_p=0.9
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Fout bij genereren verhaal: {e}"

# Functie om een illustratie te genereren
def generate_illustration(prompt):
    try:
        dalle_response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="1024x1024"
        )
        image_url = dalle_response['data'][0]['url']
        return image_url
    except Exception as e:
        return f"Fout bij genereren illustratie: {e}"

# Route voor verhaal genereren
@app.route("/generate_story", methods=["POST"])
def generate_story_endpoint():
    data = request.json
    if not data or "child_name" not in data or "favorite_animal" not in data or "theme" not in data:
        return jsonify({"error": "Ontbrekende gegevens. Vereist: child_name, favorite_animal, theme"}), 400
    
    child_name = data["child_name"]
    favorite_animal = data["favorite_animal"]
    theme = data["theme"]
    language = data.get("language", "en")  # Standaardtaal is Engels
    
    # Genereer het verhaal
    story_prompt = f"Write a children's story about {child_name}, who loves {favorite_animal}, with a theme of {theme}."
    story = generate_story(story_prompt)
    
    # Vertaal het verhaal indien nodig
    if language != "en":
        try:
            translated_story = translator.translate(story, src="en", dest=language).text
        except Exception as e:
            return jsonify({"error": f"Fout bij vertalen: {e}"}), 500
    else:
        translated_story = story

    # Genereer illustratie
    illustration_prompt = f"A high-quality children's book illustration featuring {favorite_animal} in a {theme} setting."
    illustration_url = generate_illustration(illustration_prompt)
    
    if "Fout" in illustration_url:
        return jsonify({"error": illustration_url}), 500

    return jsonify({"story": translated_story, "illustration_url": illustration_url})

# Start de Flask-server
if __name__ == "__main__":
    app.run(debug=True)
