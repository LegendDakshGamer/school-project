import streamlit as st
import json
from dotenv import load_dotenv
from openai import OpenAI

# Load .env file
load_dotenv()

# Initialize client (API key will auto-load from .env)
client = OpenAI()

# Example JSON structure to guide model
response_json = """
{
  "questions": [
    {
      "difficulty": "easy | medium | hard",
      "question": "Generated question text here."
    }
  ]
}
"""

prompt_template = """
You are an AI question generator.

Text Provided:
"{text_input}"

Task:
- Generate exactly 2 non-repeated conceptual questions based on the text.
- Questions must match the difficulty level: "{difficulty}".
- Format output ONLY using the JSON example below.

JSON Response Format:
{response_json}
"""

def generate_questions(text_input, difficulty):
    prompt = prompt_template.format(
        text_input=text_input,
        difficulty=difficulty,
        response_json=response_json
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",  # FIXED MODEL
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500
    )

    return json.loads(response.choices[0].message.content)

def main():
    st.title("AI Question Generator")

    text_input = st.text_area("Enter text for generating questions:")

    difficulty = st.selectbox(
        "Select difficulty:",
        ["Easy", "Medium", "Hard"]
    ).lower()

    if st.button("Generate Questions"):
        try:
            result = generate_questions(text_input, difficulty)

            for q in result["questions"]:
                st.write(f"**({q['difficulty'].capitalize()})** {q['question']}")

        except Exception as e:
            st.error(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
