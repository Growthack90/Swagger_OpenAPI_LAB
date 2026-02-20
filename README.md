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


### 2. L'App Python (Il Server Reale)

Per trasformare lo Swagger in una vera applicazione Python, useremo `FastAPI`. È il framework moderno più simile a `Swagger`, tanto che genera la documentazione automaticamente.

Apri un altro terminale, ed installa le librerie necessarie:
```powerhell
pip install fastapi uvicorn
```

**Avviare e Testare l'App**
```powerhell
uvicorn main:app --reload
```

Vai su `http://127.0.0.1:8000/docs`.

La cosa incredibile? FastAPI ha letto il tuo codice Python e ha generato una pagina Swagger identica a quella che stavi scrivendo a mano!
