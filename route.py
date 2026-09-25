from fastapi import FastAPI
import google.generativeai as genai

app = FastAPI(title="ComicCraft AI")

@app.get("/")
def home():
    return {"message": "ComicCraft AI Comic Creator Running"}
