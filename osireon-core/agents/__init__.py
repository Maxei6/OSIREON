"""
Inizializzazione del sistema di agenti per Osireon.
Questo file registra gli agenti nel gestore e fornisce funzioni di utilità.
"""
import logging
from typing import Dict, Any

from src.agents.base import agent_manager, BaseAgent
from src.agents.analyst_agent import AnalystAgent
from src.agents.critic_agent import CriticAgent

# Configurazione del logging
logger = logging.getLogger("osireon.agents.init")

# Inizializzazione degli agenti
def initialize_agents():
    """
    Inizializza e registra tutti gli agenti nel gestore.
    """
    logger.info("Inizializzazione degli agenti")
    
    # Crea e registra l'AnalystAgent
    analyst = AnalystAgent()
    agent_manager.register_agent(analyst)
    
    # Crea e registra il CriticAgent
    critic = CriticAgent()
    agent_manager.register_agent(critic)
    
    logger.info(f"Registrati {len(agent_manager.agents)} agenti nel gestore")

# Funzione per eseguire l'analisi con tutti gli agenti
def run_agent_analysis(input_data: Dict[str, Any], module_result: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    """
    Esegue l'analisi con tutti gli agenti registrati.
    
    Args:
        input_data: Dati di input originali della simulazione.
        module_result: Risultato dell'elaborazione del modulo.
        
    Returns:
        Dict[str, Dict[str, Any]]: Risultati dell'analisi di tutti gli agenti.
    """
    # Assicurati che gli agenti siano inizializzati
    if not agent_manager.agents:
        initialize_agents()
    
    # Esegui l'analisi con tutti gli agenti
    return agent_manager.run_agents(input_data, module_result)

# Inizializza gli agenti all'importazione del modulo
initialize_agents()
