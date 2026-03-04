import sqlite3
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(title="API Gestione Libri")

DB_PATH = Path("biblioteca.db")

# Definizione dello schema (corrisponde a 'components' in Swagger)
class Libro(BaseModel):
    id: int
    titolo: str
    autore: str

def get_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


@app.on_event("startup")
def init_db() -> None:
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS libri (
                id INTEGER PRIMARY KEY,
                titolo TEXT NOT NULL,
                autore TEXT NOT NULL
            )
            """
        )

        existing = connection.execute("SELECT COUNT(*) AS total FROM libri").fetchone()["total"]
        if existing == 0:
            connection.execute(
                "INSERT INTO libri (id, titolo, autore) VALUES (?, ?, ?)",
                (1, "Il Signore degli Anelli", "J.R.R. Tolkien"),
            )
        connection.commit()

# --- GET: Recupera tutti i libri ---
@app.get("/libri", response_model=List[Libro])
def get_libri():
    with get_connection() as connection:
        rows = connection.execute("SELECT id, titolo, autore FROM libri ORDER BY id").fetchall()
    return [dict(row) for row in rows]

# --- POST: Aggiunge un libro ---
@app.post("/libri", status_code=201)
def create_libro(libro: Libro):
    with get_connection() as connection:
        payload = libro.model_dump()
        try:
            connection.execute(
                "INSERT INTO libri (id, titolo, autore) VALUES (?, ?, ?)",
                (payload["id"], payload["titolo"], payload["autore"]),
            )
        except sqlite3.IntegrityError:
            raise HTTPException(status_code=409, detail="Esiste già un libro con questo id")
        connection.commit()
    return {"messaggio": "Libro creato con successo"}

# --- PUT: Aggiorna un libro ---
@app.put("/libri/{id}")
def update_libro(id: int, libro_aggiornato: Libro):
    payload = libro_aggiornato.model_dump()
    with get_connection() as connection:
        try:
            result = connection.execute(
                "UPDATE libri SET id = ?, titolo = ?, autore = ? WHERE id = ?",
                (payload["id"], payload["titolo"], payload["autore"], id),
            )
        except sqlite3.IntegrityError:
            raise HTTPException(status_code=409, detail="Esiste già un libro con questo id")
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Libro non trovato")
        connection.commit()
    return {"messaggio": "Libro aggiornato"}

# --- DELETE: Elimina un libro ---
@app.delete("/libri/{id}", status_code=204)
def delete_libro(id: int):
    with get_connection() as connection:
        result = connection.execute("DELETE FROM libri WHERE id = ?", (id,))
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Libro non trovato")
        connection.commit()