from fastapi import FastAPI, Form, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
import os

app = FastAPI(title="ComicCraft AI Comic Creator")

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-pro')

# Pydantic schema for JSON validation
class PromptRequest(BaseModel):
    prompt: str
    character_name: str
    setting: str
    tone: str
    art_style: str

# Helper functions for workflow
def generate_outline(prompt):
    return f"Outline for {prompt}"

def generate_story(prompt):
    return f"Story and dialogues for {prompt}"

def generate_image(prompt):
    return f"Image prompt generated for {prompt}"

def build_comic_layout(story, image):
    return {"status": "layout_created"}

def save_pdf(layout):
    return "outputs/comic_output.pdf"

# Route 1: Main form generation endpoint
@app.post("/generate")
async def generate(
    prompt: str = Form(...),
    character_name: str = Form(...),
    setting: str = Form(...),
    tone: str = Form(...),
    art_style: str = Form(...)
):
    outline = generate_outline(prompt)
    story = generate_story(outline)
    image = generate_image(story)
    layout = build_comic_layout(story, image)
    pdf_path = save_pdf(layout)
    return {"status": "success", "pdf_path": pdf_path}

# Route 2: JSON API endpoint
@app.post("/generate-comic/json")
async def generate_comic_json(request: PromptRequest):
    formatted_prompt = f"Create comic for {request.prompt} with character {request.character_name}"
    response = model.generate_content(formatted_prompt)
    return {"status": "success", "data": response.text}

# Route 3: Test image endpoint
@app.get("/test-image")
async def test_image():
    return {"status": "image pipeline active"}
