import google.generativeai as genai

def generate_story(outline):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(f"Expand this outline into comic narration and dialogues: {outline}")
    return response.text
