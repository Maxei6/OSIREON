"""
Connettore LLM per Osireon.
Questo file contiene l'implementazione del connettore per i modelli di linguaggio.
"""
import logging
import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Caricamento delle variabili d'ambiente
load_dotenv()

# Configurazione del logging
logger = logging.getLogger("osireon.llm")

class LLMConnector:
    """
    Connettore per i modelli di linguaggio (LLM).
    Supporta diversi provider come OpenAI e DeepSeek.
    """
    
    def __init__(self):
        """
        Inizializza il connettore LLM.
        """
        self.default_provider = os.getenv("LLM_PROVIDER", "openai")
        self.default_model = os.getenv("LLM_MODEL", "gpt-4")
        self.default_temperature = float(os.getenv("LLM_TEMPERATURE", "0.7"))
        
        # Carica le chiavi API dai file di configurazione
        self.api_keys = {
            "openai": os.getenv("OPENAI_API_KEY", ""),
            "deepseek": os.getenv("DEEPSEEK_API_KEY", "")
        }
        
        logger.info(f"LLMConnector inizializzato con provider predefinito: {self.default_provider}")
    
    def call_llm(self, prompt: str, provider: Optional[str] = None, 
                model: Optional[str] = None, temperature: Optional[float] = None) -> str:
        """
        Chiama un modello di linguaggio con il prompt specificato.
        
        Args:
            prompt: Il prompt da inviare al modello.
            provider: Il provider da utilizzare (openai, deepseek). Se None, usa il default.
            model: Il modello specifico da utilizzare. Se None, usa il default.
            temperature: La temperatura da utilizzare. Se None, usa il default.
            
        Returns:
            str: La risposta generata dal modello.
        """
        # Usa i valori predefiniti se non specificati
        provider = provider or self.default_provider
        model = model or self.default_model
        temperature = temperature if temperature is not None else self.default_temperature
        
        logger.info(f"Chiamata a LLM con provider: {provider}, modello: {model}, temperatura: {temperature}")
        logger.info(f"Prompt: {prompt[:100]}...")
        
        # Implementazione mock - in una versione reale, qui ci sarebbe la chiamata effettiva all'API
        try:
            # Simula una risposta basata sul provider e sul prompt
            response = self._mock_response(provider, prompt)
            
            logger.info(f"Risposta LLM ricevuta: {response[:100]}...")
            return response
            
        except Exception as e:
            logger.error(f"Errore durante la chiamata a LLM: {str(e)}")
            return f"Errore: {str(e)}"
    
    def _mock_response(self, provider: str, prompt: str) -> str:
        """
        Genera una risposta mock basata sul provider e sul prompt.
        
        Args:
            provider: Il provider LLM.
            prompt: Il prompt inviato.
            
        Returns:
            str: Una risposta mock.
        """
        # Estrai alcune parole chiave dal prompt per simulare una risposta contestuale
        keywords = [word for word in prompt.lower().split() if len(word) > 4]
        keywords = keywords[:5] if keywords else ["policy", "analisi"]
        
        if "economia" in prompt.lower() or "economic" in prompt.lower():
            if provider.lower() == "openai":
                return f"Analisi economica delle policy proposte: Le policy {', '.join(keywords)} potrebbero avere un impatto significativo sull'economia. È importante considerare gli effetti a lungo termine e le possibili conseguenze non intenzionali. Si consiglia un'implementazione graduale con monitoraggio continuo degli indicatori economici chiave."
            else:  # deepseek o altro
                return f"Valutazione economica: Le misure proposte relative a {', '.join(keywords)} presentano opportunità e sfide. Da un lato, potrebbero stimolare la crescita in settori specifici, dall'altro potrebbero creare squilibri se non adeguatamente calibrate. Un approccio basato sui dati è essenziale per il successo."
        
        elif "sociale" in prompt.lower() or "social" in prompt.lower():
            if provider.lower() == "openai":
                return f"Analisi sociale delle policy proposte: Le policy relative a {', '.join(keywords)} potrebbero influenzare significativamente il tessuto sociale. È fondamentale considerare l'impatto su diversi gruppi demografici e garantire che i benefici siano distribuiti equamente. Si raccomanda un ampio coinvolgimento degli stakeholder nella fase di implementazione."
            else:  # deepseek o altro
                return f"Valutazione dell'impatto sociale: Le proposte riguardanti {', '.join(keywords)} hanno il potenziale di trasformare aspetti importanti della società. L'efficacia dipenderà dalla capacità di adattarsi ai contesti locali e rispondere ai feedback delle comunità coinvolte. Un monitoraggio continuo è essenziale."
        
        else:
            if provider.lower() == "openai":
                return f"Analisi generale delle policy proposte: Le policy relative a {', '.join(keywords)} presentano un mix di opportunità e sfide. È consigliabile un'implementazione iterativa con cicli di feedback regolari per adattare l'approccio in base ai risultati osservati. La trasparenza e la comunicazione chiara sono fondamentali per il successo."
            else:  # deepseek o altro
                return f"Valutazione complessiva: Le proposte su {', '.join(keywords)} richiedono un'attenta considerazione delle interdipendenze tra diversi settori. Un approccio sistemico che consideri gli effetti a cascata è essenziale. Si raccomanda di stabilire metriche chiare di successo e meccanismi di revisione periodica."

# Istanza singleton del connettore LLM
llm_connector = LLMConnector()
