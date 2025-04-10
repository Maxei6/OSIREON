"""
Aggiornamento del file main.py per integrare l'endpoint /simulate.
"""
from fastapi import FastAPI
import logging
import os
from dotenv import load_dotenv
import uvicorn

# Importazione della configurazione dell'applicazione
from src.config.app import app
from src.api import router as api_router
from src.simulate import router as simulate_router

# Registrazione dei router
app.include_router(api_router, prefix="")
app.include_router(simulate_router, prefix="")

# Punto di ingresso per l'esecuzione diretta
if __name__ == "__main__":
    # Caricamento delle variabili d'ambiente
    load_dotenv()
    
    # Avvio del server
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    debug = os.getenv("DEBUG", "True").lower() == "true"
    
    uvicorn.run("main:app", host=host, port=port, reload=debug)
