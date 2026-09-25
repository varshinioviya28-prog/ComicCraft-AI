from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
import google.generativeai as genai

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# Configure Google Gemini API
# genai.configure(api_key="YOUR_API_KEY")

@router.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.post("/generate")
async def generate_comic(request: Request, prompt: str = Form(...)):
    # Gemini Model Logic
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(f"Create a comic panel script for: {prompt}")
    return templates.TemplateResponse("index.html", {"request": request, "result": response.text})
