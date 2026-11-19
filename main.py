from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import database, scraper, analyzer

app = FastAPI(title="Extractor de comentarios TikTok")
database.init_db()

class Peticion(BaseModel):
    url: str

@app.post("/extraer")
def extraer(p: Peticion):
    if "tiktok.com" not in p.url:
        raise HTTPException(400, "URL no válida")
    try:
        comentarios = scraper.extraer(p.url)
    except Exception as e:
        raise HTTPException(502, f"Error extrayendo: {e}")
    if not comentarios:
        raise HTTPException(404, "Sin comentarios o video privado/eliminado")
    database.guardar(p.url, comentarios)
    ideas = analyzer.mejores_ideas(database.listar(p.url))
    return {"total": len(comentarios), "top_ideas": ideas}

app.mount("/", StaticFiles(directory="static", html=True), name="static")
