PALABRAS_IDEA = ["idea", "sugiero", "podrías", "deberías", "prueba", "haz", "intent",
                 "agrega", "mejor", "tip", "truco", "consejo", "opinión", "creo que"]

def puntuar(comentario: dict) -> int:
    t = comentario["texto"].lower()
    puntaje = comentario["likes"]  # los likes pesan mucho
    puntaje += sum(3 for p in PALABRAS_IDEA if p in t)   # detecta aportes
    puntaje += 5 if len(t) > 60 else 0                   # comentarios elaborados
    puntaje -= 10 if "http" in t else 0                  # penaliza spam
    return puntaje

def mejores_ideas(comentarios: list[dict], n: int = 10) -> list[dict]:
    for c in comentarios:
        c["puntaje"] = puntuar(c)
        c["es_idea"] = any(p in c["texto"].lower() for p in PALABRAS_IDEA)
    return sorted(comentarios, key=lambda c: c["puntaje"], reverse=True)[:n]
  
