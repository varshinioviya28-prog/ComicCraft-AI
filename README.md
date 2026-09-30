# 📖 ComicCraft — AI Comic Story Creator

A FastAPI web app matching the ComicCraft workflow: create a story from a prompt, choose character/setting/tone/art style, generate four comic panels, preview them, download a PDF, and see an export-success page.

## Included
- Home/create page
- Story prompt, character, setting, tone and art-style controls
- Four-panel comic preview
- Panel title, image, scene description, caption, narration and image-prompt reference
- Download Your Comic as PDF
- Comic Exported Successfully page
- FastAPI `/docs`
- `/generate-comic/json`, `/generate`, `/download-pdf`, `/export-success`, `/test-image`, `/health`
- Tests, Procfile and Render config

## Run
```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Open http://127.0.0.1:8000 and API docs at http://127.0.0.1:8000/docs.

## GitHub
Create a repository such as `comiccraft-ai-comic-story-creator`, upload all folders/files, then optionally use:
```bash
git init
git add .
git commit -m "Initial ComicCraft project"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/comiccraft-ai-comic-story-creator.git
git push -u origin main
```

## Note about AI
This is a fully runnable, API-key-free demo. The story/panel generation is implemented locally so it can be demonstrated without a paid AI provider. `generate()` in `app/main.py` is the integration point if a real LLM/image API is added later.
