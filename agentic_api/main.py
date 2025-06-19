from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pathlib import Path
import os
from dotenv import load_dotenv
import google.generativeai as genai
from db.chroma_store import save_version 
# from fastapi.responses import JSONResponse

# Load API Key
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Paths
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

# FastAPI app
app = FastAPI(title="Automated Book Workflow API")

# Input model
class TextInput(BaseModel):
    content: str

# Writer endpoint
@app.post("/write")
def write_chapter(data: TextInput):
    prompt = f"Rewrite the following content in a creative and engaging storytelling style:\n\n{data.content}"
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    result = response.text.strip()
    
    Path("data/chapter1_spun.txt").write_text(result, encoding="utf-8")
    return {"message": "Spun content saved", "spun": result}

# Reviewer endpoint
@app.post("/review")
def review_chapter(data: TextInput):
    prompt = f"Review and improve the following story for grammar, clarity, and flow:\n\n{data.content}"
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    result = response.text.strip()
    
    Path("data/chapter1_reviewed.txt").write_text(result, encoding="utf-8")
    return {"message": "Reviewed content saved", "reviewed": result}

# Finalize endpoint
# @app.post("/finalize")
# def save_final_version(data: TextInput):
#     Path("data/chapter1_final.txt").write_text(data.content, encoding="utf-8")
#     return {"message": "Final version saved"}
@app.post("/finalize")
def save_final_version(data: TextInput):
    Path("data/chapter1_final.txt").write_text(data.content, encoding="utf-8")
    version_id = save_version("chapter1", "final", data.content)  # ✅ Save and get ID
    return {"message": "Final version saved", "id": version_id}


class RatingInput(BaseModel):
    id: str
    reward: float

@app.post("/rate")
def rate_version(data: RatingInput):
    from chromadb import Client
    from chromadb.config import Settings

    chroma = Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory="chromadb_store"))
    collection = chroma.get_or_create_collection("book_versions")
    
    collection.update(
        ids=[data.id],
        metadatas=[{"reward": data.reward}]
    )
    return {"message": f"✅ Reward updated to {data.reward}"}

@app.get("/")
def read_root():
    return {"message": "FastAPI backend is running!"}

# @app.get("/get_version/{stage}")
# def get_version(stage: str):
#     file_map = {
#         "original": "data/chapter1.txt",
#         "spun": "data/chapter1_spun.txt",
#         "reviewed": "data/chapter1_reviewed.txt",
#         "final": "data/chapter1_final.txt"
#     }
#     path = file_map.get(stage)
#     if path and Path(path).exists():
#         return {"content": Path(path).read_text(encoding="utf-8")}
#     return JSONResponse(content={"error": "Content not found"}, status_code=404)

