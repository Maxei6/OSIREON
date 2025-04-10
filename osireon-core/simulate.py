"""
Implementazione dell'endpoint /simulate per Osireon.
Questo file contiene la logica completa dell'endpoint di simulazione.
"""
import logging
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from typing import Dict, Any, List

from src.utils.models import SimulationRequest, SimulationResponse, ModuleResult, AgentAnalysis, EthicsCheck
from src.modules.loader import module_loader
from src.agents import run_agent_analysis
from src.ethics.validator import ethics_validator
from src.db.database import db_manager

# Configurazione del logging
logger = logging.getLogger("osireon.simulate")

# Creazione del router
router = APIRouter(tags=["simulation"])

@router.post("/simulate")
async def simulate(request: SimulationRequest, background_tasks: BackgroundTasks) -> Dict[str, Any]:
    """
    Endpoint principale per eseguire una simulazione di policy.
    
    Args:
        request: Richiesta di simulazione contenente paese, dominio, proposte e vincoli.
        background_tasks: Gestore delle attività in background.
        
    Returns:
        Dict[str, Any]: Risultato della simulazione, analisi degli agenti e controllo etico.
    """
    logger.info(f"Ricevuta richiesta di simulazione: {request.dict()}")
    
    try:
        # Inizializza il database se necessario
        if not db_manager.initialized:
            db_manager.initialize()
        
        # Crea una nuova simulazione nel database
        simulation_id = db_manager.create_simulation(
            country=request.country,
            domain=request.domain,
            proposals=request.proposals,
            constraints=request.constraints
        )
        
        if not simulation_id:
            raise HTTPException(status_code=500, detail="Errore durante la creazione della simulazione nel database")
        
        # Aggiorna lo stato della simulazione
        db_manager.update_simulation_status(simulation_id, "processing")
        
        # Prepara i dati di input per il modulo
        input_data = {
            "country": request.country,
            "domain": request.domain,
            "proposals": request.proposals,
            "constraints": request.constraints
        }
        
        # Esegui il modulo appropriato
        module_name = module_loader.get_module_path(request.country, request.domain)
        module_result = module_loader.run_module(request.country, request.domain, input_data)
        
        # Salva il risultato del modulo nel database
        db_manager.save_module_result(simulation_id, module_name, module_result)
        
        # Esegui l'analisi con gli agenti
        agent_results = run_agent_analysis(input_data, module_result)
        
        # Salva le analisi degli agenti nel database
        for agent_name, analysis in agent_results.items():
            db_manager.save_agent_analysis(simulation_id, agent_name, analysis)
        
        # Esegui la validazione etica
        ethics_result = ethics_validator.validate(request.proposals, request.domain)
        
        # Salva il risultato del controllo etico nel database
        db_manager.save_ethics_check(
            simulation_id, 
            ethics_result["passed"], 
            ethics_result.get("violations", [])
        )
        
        # Aggiorna lo stato della simulazione
        db_manager.update_simulation_status(simulation_id, "completed")
        
        # Prepara la risposta
        module_result_model = ModuleResult(
            module_name=module_name,
            result=module_result
        )
        
        agent_analyses_models = [
            AgentAnalysis(
                agent_name=agent_name,
                analysis=analysis.get("summary", "") + "\n\n" + analysis.get("conclusion", "")
            )
            for agent_name, analysis in agent_results.items()
        ]
        
        ethics_check_model = EthicsCheck(
            passed=ethics_result["passed"],
            violations=ethics_result.get("violations", None)
        )
        
        # Costruisci la risposta completa
        response = {
            "simulation_id": simulation_id,
            "result": module_result_model.dict(),
            "agent_analyses": [aa.dict() for aa in agent_analyses_models],
            "ethics_check": ethics_check_model.dict()
        }
        
        logger.info(f"Simulazione completata con successo: {response}")
        return response
        
    except Exception as e:
        logger.error(f"Errore durante la simulazione: {str(e)}")
        
        # Se abbiamo un ID di simulazione, aggiorna lo stato a "error"
        if 'simulation_id' in locals():
            db_manager.update_simulation_status(simulation_id, "error")
        
        raise HTTPException(status_code=500, detail=f"Errore durante la simulazione: {str(e)}")

# Funzione per ottenere i risultati di una simulazione precedente
@router.get("/simulate/{simulation_id}")
async def get_simulation_results(simulation_id: int) -> Dict[str, Any]:
    """
    Ottiene i risultati di una simulazione precedente.
    
    Args:
        simulation_id: ID della simulazione.
        
    Returns:
        Dict[str, Any]: Risultati completi della simulazione.
    """
    logger.info(f"Richiesta di risultati per la simulazione {simulation_id}")
    
    try:
        # Inizializza il database se necessario
        if not db_manager.initialized:
            db_manager.initialize()
        
        # Ottieni i risultati della simulazione
        results = db_manager.get_simulation_results(simulation_id)
        
        if "error" in results:
            raise HTTPException(status_code=404, detail=results["error"])
        
        logger.info(f"Risultati della simulazione {simulation_id} recuperati con successo")
        return results
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Errore durante il recupero dei risultati della simulazione: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Errore durante il recupero dei risultati: {str(e)}")
