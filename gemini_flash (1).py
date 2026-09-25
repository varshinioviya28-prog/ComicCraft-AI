import google.generativeai as genai

def generate_outline(prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(f"Generate a structured 5-panel comic outline for: {prompt}")
    return response.text
