# Swagger - OpenAPI

## Funzionamento e dipendenze

### 1. Il Mock Server (Soluzione Rapida)

Il modo più veloce per testare lo `Swagger` senza scrivere codice è `Prism`.

Apri il terminale di VS Code.
Esegui questo comando (richiede Node.js):
```powerhell
npx @stoplight/prism-cli mock api-libreria.yaml
```

Il server sarà attivo su `http://127.0.0.1:4010`. Se provi a chiamare quell'URL, Prism leggerà il tuo file YAML e inventerà dei dati coerenti con lo schema.
Nota: in questo caso accedere a `http://127.0.0.1:4010/libri` per ricevere risposta di successo con `200`.

Importante: in modalità `mock`, Prism **non mantiene uno stato persistente** delle chiamate `POST/PUT/DELETE`.
Quindi una `POST` fatta su `http://127.0.0.1:4010/libri` non modifica davvero i dati letti dalla `GET` successiva.

Se vuoi passare da Prism ma usare i dati reali della tua app FastAPI, avvia Prism in modalità `proxy` verso `http://127.0.0.1:8000`:
```powerhell
npx @stoplight/prism-cli proxy api-libreria.yaml http://127.0.0.1:8000
```


### 2. L'App Python (Il Server Reale)

Per trasformare lo Swagger in una vera applicazione Python, useremo `FastAPI`. È il framework moderno più simile a `Swagger`, tanto che genera la documentazione automaticamente.


Apri un altro terminale, ed installa le librerie necessarie:
```powerhell
pip install fastapi uvicorn
```

Prima però installa l'ambiente virtuale:
```powerhell
python -m venv venv
.\venv\Scripts\activate

# per versioni specifiche di Python (per esempio 3.11)
py -3.11 -m venv venv
.\venv\Scripts\activate
```

**Avviare e Testare l'App**
```powerhell
uvicorn main:app --reload
```

Vai su `http://127.0.0.1:8000/docs`.

La cosa incredibile? FastAPI ha letto il tuo codice Python e ha generato una pagina Swagger identica a quella che stavi scrivendo a mano!

### 3. Persistenza dati (SQLite)

Ho creato un nuovo file che ha come base il `main.py` ma modificato chiamato `main_persistent.py`. Copia pure il contenuto di quest'ultimo ed inseriscilo nel file principale.

L'app FastAPI usa ora un database locale SQLite (`biblioteca.db`) nella cartella del progetto.

- Le operazioni `POST/PUT/DELETE` su `http://127.0.0.1:8000/libri` sono persistenti.
- Dopo un riavvio di `uvicorn`, i dati restano disponibili.

Per test rapido:
1. Fai una `POST` da `http://127.0.0.1:8000/docs`.
2. Esegui una `GET /libri` e verifica il nuovo record.
3. Riavvia il server e ripeti `GET /libri`: il record è ancora presente.
