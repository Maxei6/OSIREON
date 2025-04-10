"""
Modelli di dati per l'API Osireon.
Questo file contiene le definizioni dei modelli Pydantic utilizzati per la validazione dei dati.
"""
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class SimulationRequest(BaseModel):
    """
    Modello per la richiesta di simulazione.
    
    Attributes:
        country: Il paese per cui eseguire la simulazione.
        domain: Il dominio di policy (es. economia, sociale).
        proposals: Lista di proposte di policy da simulare.
        constraints: Lista di vincoli da considerare nella simulazione.
    """
    country: str = Field(..., description="Paese per cui eseguire la simulazione")
    domain: str = Field(..., description="Dominio di policy (es. economia, sociale)")
    proposals: List[str] = Field(..., description="Lista di proposte di policy da simulare")
    constraints: List[str] = Field(..., description="Lista di vincoli da considerare nella simulazione")

class ModuleResult(BaseModel):
    """
    Modello per il risultato dell'elaborazione di un modulo.
    
    Attributes:
        module_name: Nome del modulo che ha generato il risultato.
        result: Risultato dell'elaborazione del modulo.
    """
    module_name: str
    result: Dict[str, Any]

class AgentAnalysis(BaseModel):
    """
    Modello per l'analisi generata da un agente.
    
    Attributes:
        agent_name: Nome dell'agente che ha generato l'analisi.
        analysis: Contenuto dell'analisi.
    """
    agent_name: str
    analysis: str

class EthicsCheck(BaseModel):
    """
    Modello per il risultato del controllo etico.
    
    Attributes:
        passed: Indica se il controllo etico è stato superato.
        violations: Lista di eventuali violazioni etiche riscontrate.
    """
    passed: bool
    violations: Optional[List[str]] = None

class SimulationResponse(BaseModel):
    """
    Modello per la risposta di simulazione.
    
    Attributes:
        result: Risultato della simulazione.
        agent_analyses: Lista di analisi generate dagli agenti.
        ethics_check: Risultato del controllo etico.
    """
    result: ModuleResult
    agent_analyses: List[AgentAnalysis]
    ethics_check: EthicsCheck
