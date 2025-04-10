"""
Configurazione dell'applicazione FastAPI per Osireon.
Questo file contiene la configurazione principale dell'applicazione.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import os
from dotenv import load_dotenv

# Caricamento delle variabili d'ambiente
load_dotenv()

# Configurazione del logging
logging.basicConfig(
    level=getattr(logging, os.getenv("LOG_LEVEL", "INFO")),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("osireon")

def create_app() -> FastAPI:
    """
    Crea e configura l'applicazione FastAPI.
    
    Returns:
        FastAPI: L'istanza configurata dell'applicazione FastAPI.
    """
    app = FastAPI(
        title="Osireon API",
        description="API per la piattaforma Osireon di simulazione di policy",
        version="0.1.0",
    )
    
    # Configurazione CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In produzione, specificare i domini consentiti
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Registrazione degli eventi di avvio e spegnimento
    @app.on_event("startup")
    async def startup_event():
        logger.info("Avvio dell'applicazione Osireon")
    
    @app.on_event("shutdown")
    async def shutdown_event():
        logger.info("Arresto dell'applicazione Osireon")
    
    return app

# Creazione dell'istanza dell'applicazione
app = create_app()
