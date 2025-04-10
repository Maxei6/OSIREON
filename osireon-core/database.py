"""
Funzioni di accesso al database per Osireon.
Questo file contiene le funzioni per interagire con il database PostgreSQL.
"""
import logging
from typing import Dict, Any, List, Optional, Union
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from src.db.models import (
    Simulation, ModuleResult, AgentAnalysis, EthicsCheck, LLMLog,
    get_db_session, create_tables
)

# Configurazione del logging
logger = logging.getLogger("osireon.db")

class DatabaseManager:
    """
    Gestore del database per Osireon.
    """
    
    def __init__(self):
        """
        Inizializza il gestore del database.
        """
        self.initialized = False
        logger.info("DatabaseManager inizializzato")
    
    def initialize(self):
        """
        Inizializza il database creando le tabelle se non esistono.
        """
        if not self.initialized:
            try:
                create_tables()
                self.initialized = True
                logger.info("Database inizializzato con successo")
            except Exception as e:
                logger.error(f"Errore durante l'inizializzazione del database: {str(e)}")
                raise
    
    def create_simulation(self, country: str, domain: str, proposals: List[str], 
                         constraints: List[str]) -> Optional[int]:
        """
        Crea una nuova simulazione nel database.
        
        Args:
            country: Paese per cui eseguire la simulazione.
            domain: Dominio di policy.
            proposals: Lista di proposte di policy.
            constraints: Lista di vincoli.
            
        Returns:
            Optional[int]: ID della simulazione creata o None in caso di errore.
        """
        try:
            session = get_db_session()
            simulation = Simulation(
                country=country,
                domain=domain,
                proposals=proposals,
                constraints=constraints,
                status="pending"
            )
            session.add(simulation)
            session.commit()
            simulation_id = simulation.id
            session.close()
            
            logger.info(f"Creata simulazione con ID {simulation_id}")
            return simulation_id
        except SQLAlchemyError as e:
            logger.error(f"Errore durante la creazione della simulazione: {str(e)}")
            return None
    
    def update_simulation_status(self, simulation_id: int, status: str) -> bool:
        """
        Aggiorna lo stato di una simulazione.
        
        Args:
            simulation_id: ID della simulazione.
            status: Nuovo stato della simulazione.
            
        Returns:
            bool: True se l'aggiornamento è riuscito, False altrimenti.
        """
        try:
            session = get_db_session()
            simulation = session.query(Simulation).filter(Simulation.id == simulation_id).first()
            
            if not simulation:
                logger.warning(f"Simulazione con ID {simulation_id} non trovata")
                session.close()
                return False
            
            simulation.status = status
            session.commit()
            session.close()
            
            logger.info(f"Aggiornato stato della simulazione {simulation_id} a '{status}'")
            return True
        except SQLAlchemyError as e:
            logger.error(f"Errore durante l'aggiornamento dello stato della simulazione: {str(e)}")
            return False
    
    def save_module_result(self, simulation_id: int, module_name: str, result: Dict[str, Any]) -> Optional[int]:
        """
        Salva il risultato di un modulo.
        
        Args:
            simulation_id: ID della simulazione.
            module_name: Nome del modulo.
            result: Risultato del modulo.
            
        Returns:
            Optional[int]: ID del risultato salvato o None in caso di errore.
        """
        try:
            session = get_db_session()
            module_result = ModuleResult(
                simulation_id=simulation_id,
                module_name=module_name,
                result=result
            )
            session.add(module_result)
            session.commit()
            result_id = module_result.id
            session.close()
            
            logger.info(f"Salvato risultato del modulo {module_name} per la simulazione {simulation_id}")
            return result_id
        except SQLAlchemyError as e:
            logger.error(f"Errore durante il salvataggio del risultato del modulo: {str(e)}")
            return None
    
    def save_agent_analysis(self, simulation_id: int, agent_name: str, analysis: Dict[str, Any]) -> Optional[int]:
        """
        Salva l'analisi di un agente.
        
        Args:
            simulation_id: ID della simulazione.
            agent_name: Nome dell'agente.
            analysis: Analisi dell'agente.
            
        Returns:
            Optional[int]: ID dell'analisi salvata o None in caso di errore.
        """
        try:
            session = get_db_session()
            agent_analysis = AgentAnalysis(
                simulation_id=simulation_id,
                agent_name=agent_name,
                analysis=analysis
            )
            session.add(agent_analysis)
            session.commit()
            analysis_id = agent_analysis.id
            session.close()
            
            logger.info(f"Salvata analisi dell'agente {agent_name} per la simulazione {simulation_id}")
            return analysis_id
        except SQLAlchemyError as e:
            logger.error(f"Errore durante il salvataggio dell'analisi dell'agente: {str(e)}")
            return None
    
    def save_ethics_check(self, simulation_id: int, passed: bool, violations: Optional[List[str]] = None) -> Optional[int]:
        """
        Salva il risultato di un controllo etico.
        
        Args:
            simulation_id: ID della simulazione.
            passed: Indica se il controllo etico è stato superato.
            violations: Lista di eventuali violazioni etiche.
            
        Returns:
            Optional[int]: ID del controllo etico salvato o None in caso di errore.
        """
        try:
            session = get_db_session()
            ethics_check = EthicsCheck(
                simulation_id=simulation_id,
                passed=passed,
                violations=violations or []
            )
            session.add(ethics_check)
            session.commit()
            check_id = ethics_check.id
            session.close()
            
            logger.info(f"Salvato controllo etico per la simulazione {simulation_id}")
            return check_id
        except SQLAlchemyError as e:
            logger.error(f"Errore durante il salvataggio del controllo etico: {str(e)}")
            return None
    
    def save_llm_log(self, simulation_id: int, provider: str, model: str, 
                    prompt: str, response: str) -> Optional[int]:
        """
        Salva un log di chiamata LLM.
        
        Args:
            simulation_id: ID della simulazione.
            provider: Provider LLM.
            model: Modello LLM.
            prompt: Prompt inviato.
            response: Risposta ricevuta.
            
        Returns:
            Optional[int]: ID del log salvato o None in caso di errore.
        """
        try:
            session = get_db_session()
            llm_log = LLMLog(
                simulation_id=simulation_id,
                provider=provider,
                model=model,
                prompt=prompt,
                response=response
            )
            session.add(llm_log)
            session.commit()
            log_id = llm_log.id
            session.close()
            
            logger.info(f"Salvato log LLM per la simulazione {simulation_id}")
            return log_id
        except SQLAlchemyError as e:
            logger.error(f"Errore durante il salvataggio del log LLM: {str(e)}")
            return None
    
    def get_simulation(self, simulation_id: int) -> Optional[Dict[str, Any]]:
        """
        Ottiene i dettagli di una simulazione.
        
        Args:
            simulation_id: ID della simulazione.
            
        Returns:
            Optional[Dict[str, Any]]: Dettagli della simulazione o None se non trovata.
        """
        try:
            session = get_db_session()
            simulation = session.query(Simulation).filter(Simulation.id == simulation_id).first()
            
            if not simulation:
                logger.warning(f"Simulazione con ID {simulation_id} non trovata")
                session.close()
                return None
            
            result = simulation.to_dict()
            session.close()
            
            return result
        except SQLAlchemyError as e:
            logger.error(f"Errore durante il recupero della simulazione: {str(e)}")
            return None
    
    def get_simulation_results(self, simulation_id: int) -> Dict[str, Any]:
        """
        Ottiene tutti i risultati associati a una simulazione.
        
        Args:
            simulation_id: ID della simulazione.
            
        Returns:
            Dict[str, Any]: Risultati completi della simulazione.
        """
        try:
            session = get_db_session()
            
            # Ottieni la simulazione
            simulation = session.query(Simulation).filter(Simulation.id == simulation_id).first()
            if not simulation:
                logger.warning(f"Simulazione con ID {simulation_id} non trovata")
                session.close()
                return {"error": "Simulazione non trovata"}
            
            # Ottieni i risultati dei moduli
            module_results = session.query(ModuleResult).filter(ModuleResult.simulation_id == simulation_id).all()
            
            # Ottieni le analisi degli agenti
            agent_analyses = session.query(AgentAnalysis).filter(AgentAnalysis.simulation_id == simulation_id).all()
            
            # Ottieni i controlli etici
            ethics_checks = session.query(EthicsCheck).filter(EthicsCheck.simulation_id == simulation_id).all()
            
            # Costruisci il risultato completo
            result = {
                "simulation": simulation.to_dict(),
                "module_results": [mr.to_dict() for mr in module_results],
                "agent_analyses": [aa.to_dict() for aa in agent_analyses],
                "ethics_checks": [ec.to_dict() for ec in ethics_checks]
            }
            
            session.close()
            return result
        except SQLAlchemyError as e:
            logger.error(f"Errore durante il recupero dei risultati della simulazione: {str(e)}")
            return {"error": f"Errore database: {str(e)}"}

# Istanza singleton del gestore del database
db_manager = DatabaseManager()
