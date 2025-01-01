import toml
import openai
import flask
print("Flask geïnstalleerd:", flask.__version__)


# Laad de configuratie vanuit config.toml
config = toml.load("config.toml")
openai.api_key = config["api"]["key"]

app = Flask(__name__)

# Test API endpoint
@app.route("/generate_story", methods=["POST"])
def generate_story():
    try:
        data = request.json
        child_name = data.get("child_name", "A child")
        favorite_animal = data.get("favorite_animal", "an animal")
        theme = data.get("theme", "a theme")

        prompt = f"Write a children's story about {child_name}, who loves {favorite_animal}, with a theme of {theme}."

        # Gebruik OpenAI API om een verhaal te genereren
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Gebruik GPT-4 of een ander beschikbaar model
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0.7
        )
        story = response["choices"][0]["message"]["content"]

        return jsonify({"story": story})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
