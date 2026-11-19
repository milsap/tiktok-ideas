import sqlite3
from contextlib import closing

DB = "comentarios.db"

def init_db():
    with closing(sqlite3.connect(DB)) as conn, conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS comentarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            video_url TEXT,
            usuario TEXT,
            texto TEXT,
            likes INTEGER DEFAULT 0,
            es_idea INTEGER DEFAULT 0,
            puntaje INTEGER DEFAULT 0
        )""")

def guardar(video_url, comentarios):
    with closing(sqlite3.connect(DB)) as conn, conn:
        conn.executemany(
            "INSERT INTO comentarios (video_url, usuario, texto, likes) VALUES (?,?,?,?)",
            [(video_url, c["usuario"], c["texto"], c["likes"]) for c in comentarios]
        )

def listar(video_url):
    with closing(sqlite3.connect(DB)) as conn:
        return [dict(zip(["id","usuario","texto","likes","es_idea","puntaje"], r))
                for r in conn.execute(
                    "SELECT id, usuario, texto, likes, es_idea, puntaje FROM comentarios WHERE video_url=?",
                    (video_url,))]
      
