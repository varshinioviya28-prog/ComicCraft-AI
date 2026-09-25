import os

def generate_story(prompt):
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return "Gemini API key not configured."

    return f"Story prompt received: {prompt}"
