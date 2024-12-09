import openai
import streamlit as st
from googletrans import Translator

# OpenAI API-sleutel
openai.api_key = "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"

# Initialiseer Google Translate API
translator = Translator()

# Functie om verhalen te genereren met OpenAI GPT-4
def generate_story(child_name, favorite_animal, theme, length="short"):
    prompt = (
        f"Write a {length} children's story about {child_name}, who loves {favorite_animal}, "
        f"with a theme of {theme}. The story should have a clear beginning, middle, and a happy ending."
    )
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a creative story generator for children."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500 if length == "long" else 500,
            temperature=0.8
        )
        story = response["choices"][0]["message"]["content"].strip()
        # Controleer of het verhaal goed eindigt
        if story[-1] not in ".!?":
            story += " And they all lived happily ever after."
        return story
    except Exception as e:
        return f"Error generating story: {e}"

# Functie om een illustratie te genereren met OpenAI DALL·E
def generate_illustration(prompt):
    try:
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="512x512"
        )
        return response['data'][0]['url']
    except Exception as e:
        return f"Error generating illustration: {e}"

# Streamlit UI
st.title("StoryNest: Personalized Stories for Children")
st.sidebar.header("Settings")

# Gebruikersinvoer
child_name = st.sidebar.text_input("Child's Name", "Emma")
favorite_animal = st.sidebar.text_input("Favorite Animal", "Rabbit")
theme = st.sidebar.text_input("Story Theme", "Winter Adventure")
length = st.sidebar.selectbox("Story Length", ["short", "long"])
language = st.sidebar.selectbox("Language", ["en", "fr", "es", "de", "nl"])

# Knop om verhaal te genereren
if st.sidebar.button("Generate Story"):
    st.write("### Generated Story")
    story = generate_story(child_name, favorite_animal, theme, length)

    # Verhaal vertalen
    if language != "en":
        story = translator.translate(story, src="en", dest=language).text

    st.write(story)

    # Illustratie genereren
    st.write("### Generated Illustration")
    illustration_prompt = f"A magical and child-friendly scene of {child_name} and a {favorite_animal} in a {theme} setting."
    illustration_url = generate_illustration(illustration_prompt)

    if "Error" not in illustration_url:
        st.image(illustration_url, caption="Generated Illustration")
    else:
        st.write("Failed to generate illustration.")
