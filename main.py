from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="API Gestione Libri")

# Definizione dello schema (corrisponde a 'components' in Swagger)
class Libro(BaseModel):
    id: int
    titolo: str
    autore: str

# Database finto in memoria
db_libri = [
    {"id": 1, "titolo": "Il Signore degli Anelli", "autore": "J.R.R. Tolkien"}
]

# --- GET: Recupera tutti i libri ---
@app.get("/libri", response_model=List[Libro])
def get_libri():
    return db_libri

# --- POST: Aggiunge un libro ---
@app.post("/libri", status_code=201)
def create_libro(libro: Libro):
    db_libri.append(libro.dict())
    return {"messaggio": "Libro creato con successo"}

# --- PUT: Aggiorna un libro ---
@app.put("/libri/{id}")
def update_libro(id: int, libro_aggiornato: Libro):
    for index, libro in enumerate(db_libri):
        if libro["id"] == id:
            db_libri[index] = libro_aggiornato.dict()
            return {"messaggio": "Libro aggiornato"}
    raise HTTPException(status_code=404, detail="Libro non trovato")

# --- DELETE: Elimina un libro ---
@app.delete("/libri/{id}", status_code=204)
def delete_libro(id: int):
    for index, libro in enumerate(db_libri):
        if libro["id"] == id:
            db_libri.pop(index)
            return
    raise HTTPException(status_code=404, detail="Libro non trovato")