"""
Base per il sistema di agenti di Osireon.
Questo file contiene la classe base per gli agenti e l'interfaccia comune.
"""
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any

# Configurazione del logging
logger = logging.getLogger("osireon.agents")

class BaseAgent(ABC):
    """
    Classe base astratta per tutti gli agenti di Osireon.
    """
    
    def __init__(self, name: str):
        """
        Inizializza un agente.
        
        Args:
            name: Nome dell'agente.
        """
        self.name = name
        logger.info(f"Agente {name} inizializzato")
    
    @abstractmethod
    def analyze(self, input_data: Dict[str, Any], module_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analizza i dati di input e i risultati del modulo.
        
        Args:
            input_data: Dati di input originali della simulazione.
            module_result: Risultato dell'elaborazione del modulo.
            
        Returns:
            Dict[str, Any]: Risultato dell'analisi dell'agente.
        """
        pass
    
    def _log_analysis(self, analysis_result: Dict[str, Any]) -> None:
        """
        Registra il risultato dell'analisi nei log.
        
        Args:
            analysis_result: Risultato dell'analisi.
        """
        logger.info(f"Agente {self.name} ha completato l'analisi: {analysis_result}")

class AgentManager:
    """
    Gestore degli agenti che coordina l'esecuzione di tutti gli agenti.
    """
    
    def __init__(self):
        """
        Inizializza il gestore degli agenti.
        """
        self.agents = {}
        logger.info("AgentManager inizializzato")
    
    def register_agent(self, agent: BaseAgent) -> None:
        """
        Registra un agente nel gestore.
        
        Args:
            agent: Istanza dell'agente da registrare.
        """
        self.agents[agent.name] = agent
        logger.info(f"Agente {agent.name} registrato nel gestore")
    
    def run_agents(self, input_data: Dict[str, Any], module_result: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        """
        Esegue tutti gli agenti registrati sui dati di input e i risultati del modulo.
        
        Args:
            input_data: Dati di input originali della simulazione.
            module_result: Risultato dell'elaborazione del modulo.
            
        Returns:
            Dict[str, Dict[str, Any]]: Risultati dell'analisi di tutti gli agenti.
        """
        logger.info(f"Esecuzione di {len(self.agents)} agenti")
        
        results = {}
        for name, agent in self.agents.items():
            try:
                logger.info(f"Esecuzione dell'agente {name}")
                result = agent.analyze(input_data, module_result)
                results[name] = result
            except Exception as e:
                logger.error(f"Errore durante l'esecuzione dell'agente {name}: {str(e)}")
                results[name] = {
                    "status": "error",
                    "message": f"Errore durante l'analisi: {str(e)}",
                    "analysis": "Non disponibile a causa di un errore"
                }
        
        return results

# Istanza singleton del gestore degli agenti
agent_manager = AgentManager()
