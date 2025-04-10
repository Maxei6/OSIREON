"""
Implementazione del CriticAgent per Osireon.
Questo agente valuta criticamente i risultati della simulazione e fornisce feedback.
"""
import logging
from typing import Dict, Any

from src.agents.base import BaseAgent

# Configurazione del logging
logger = logging.getLogger("osireon.agents.critic")

class CriticAgent(BaseAgent):
    """
    Agente che valuta criticamente i risultati della simulazione e fornisce feedback.
    """
    
    def __init__(self):
        """
        Inizializza il CriticAgent.
        """
        super().__init__("CriticAgent")
    
    def analyze(self, input_data: Dict[str, Any], module_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analizza criticamente i dati di input e i risultati del modulo.
        
        Args:
            input_data: Dati di input originali della simulazione.
            module_result: Risultato dell'elaborazione del modulo.
            
        Returns:
            Dict[str, Any]: Risultato dell'analisi critica dell'agente.
        """
        logger.info(f"CriticAgent sta valutando criticamente i risultati del modulo {module_result.get('module', 'sconosciuto')}")
        
        # Estrai informazioni rilevanti
        proposals = input_data.get("proposals", [])
        constraints = input_data.get("constraints", [])
        domain = input_data.get("domain", "")
        
        # Analisi critica mock - in una implementazione reale, qui ci sarebbe l'integrazione con LLM
        critique = {
            "summary": f"Valutazione critica delle {len(proposals)} proposte nel dominio {domain}",
            "potential_issues": [],
            "alternative_perspectives": [],
            "detailed_critique": {}
        }
        
        # Genera critica per ogni proposta
        for i, proposal in enumerate(proposals):
            proposal_key = f"proposal_{i+1}"
            proposal_result = module_result.get("results", {}).get(proposal_key, {})
            
            # Estrai metriche rilevanti dal risultato del modulo
            impact_score = proposal_result.get("impact_score", proposal_result.get("social_impact_score", 0.5))
            feasibility = proposal_result.get("feasibility", proposal_result.get("acceptance_rate", 0.5))
            constraints_check = proposal_result.get("constraints_check", [])
            
            # Genera critica per questa proposta
            proposal_critique = {
                "proposal": proposal,
                "critique_points": self._generate_critique_points(proposal, impact_score, feasibility),
                "constraints_critique": self._critique_constraints(constraints_check),
                "alternative_approach": self._suggest_alternative(proposal, domain)
            }
            
            # Aggiungi alla lista dei potential issues
            if impact_score < 0.5 or feasibility < 0.5:
                critique["potential_issues"].append(
                    f"La proposta '{proposal}' presenta problemi di {'impatto' if impact_score < 0.5 else 'fattibilità'}"
                )
            
            # Aggiungi alla lista delle prospettive alternative
            critique["alternative_perspectives"].append(proposal_critique["alternative_approach"])
            
            # Aggiungi alla critica dettagliata
            critique["detailed_critique"][proposal_key] = proposal_critique
        
        # Aggiungi una valutazione complessiva
        critique["overall_assessment"] = self._generate_overall_assessment(critique["potential_issues"], module_result)
        
        # Registra il completamento dell'analisi critica
        self._log_analysis(critique)
        
        return critique
    
    def _generate_critique_points(self, proposal: str, impact_score: float, feasibility: float) -> list:
        """
        Genera punti di critica basati sull'impatto e la fattibilità.
        
        Args:
            proposal: La proposta da criticare.
            impact_score: Punteggio di impatto della proposta.
            feasibility: Punteggio di fattibilità della proposta.
            
        Returns:
            list: Lista di punti di critica.
        """
        critique_points = []
        
        # Critica basata sull'impatto
        if impact_score < 0.3:
            critique_points.append("L'impatto previsto è estremamente basso, suggerendo che la proposta potrebbe non essere efficace.")
        elif impact_score < 0.6:
            critique_points.append("L'impatto previsto è moderato, ma potrebbe non giustificare le risorse necessarie per l'implementazione.")
        
        # Critica basata sulla fattibilità
        if feasibility < 0.3:
            critique_points.append("La fattibilità è molto bassa, indicando significative barriere all'implementazione.")
        elif feasibility < 0.6:
            critique_points.append("La fattibilità è moderata, con potenziali ostacoli che potrebbero compromettere il successo.")
        
        # Aggiungi un punto di critica generico se non ci sono altri punti
        if not critique_points:
            critique_points.append("Nonostante i buoni punteggi, la proposta potrebbe non considerare adeguatamente tutti gli stakeholder.")
        
        # Aggiungi un punto di critica sulla completezza
        critique_points.append("La proposta potrebbe beneficiare di una definizione più dettagliata degli obiettivi e delle metriche di successo.")
        
        return critique_points
    
    def _critique_constraints(self, constraints_check: list) -> str:
        """
        Critica i risultati del controllo dei vincoli.
        
        Args:
            constraints_check: Lista dei risultati del controllo dei vincoli.
            
        Returns:
            str: Critica dei vincoli.
        """
        if not constraints_check:
            return "La mancanza di vincoli specificati rende difficile valutare la fattibilità reale della proposta."
        
        unsatisfied = sum(1 for c in constraints_check if not c.get("satisfied", True))
        total = len(constraints_check)
        
        if unsatisfied == 0:
            return "Sebbene la proposta soddisfi formalmente tutti i vincoli, potrebbero esserci vincoli impliciti non considerati."
        elif unsatisfied == total:
            return f"La proposta non soddisfa nessuno dei {total} vincoli, suggerendo una fondamentale incompatibilità con i requisiti."
        else:
            return f"La proposta non soddisfa {unsatisfied} dei {total} vincoli, richiedendo una significativa revisione prima dell'implementazione."
    
    def _suggest_alternative(self, proposal: str, domain: str) -> str:
        """
        Suggerisce un approccio alternativo alla proposta.
        
        Args:
            proposal: La proposta originale.
            domain: Il dominio della proposta.
            
        Returns:
            str: Suggerimento di un approccio alternativo.
        """
        # Suggerimenti mock basati sul dominio
        if domain.lower() == "economia":
            return f"Invece di '{proposal}', si potrebbe considerare un approccio graduale con incentivi fiscali mirati e monitoraggio continuo degli effetti."
        elif domain.lower() == "sociale":
            return f"Anziché '{proposal}', si potrebbe esplorare un programma pilota in aree selezionate con forte coinvolgimento della comunità locale."
        else:
            return f"Un'alternativa a '{proposal}' potrebbe essere un approccio più flessibile che permetta adattamenti basati sui feedback durante l'implementazione."
    
    def _generate_overall_assessment(self, potential_issues: list, module_result: Dict[str, Any]) -> str:
        """
        Genera una valutazione complessiva basata sui problemi potenziali e sul risultato del modulo.
        
        Args:
            potential_issues: Lista dei problemi potenziali identificati.
            module_result: Risultato dell'elaborazione del modulo.
            
        Returns:
            str: Valutazione complessiva generata.
        """
        if not potential_issues:
            return "Sebbene le proposte non presentino problemi evidenti, è consigliabile considerare prospettive diverse e potenziali effetti a lungo termine non catturati dal modello."
        
        overall_impact = module_result.get("overall_impact", module_result.get("overall_social_impact", 0.5))
        
        if len(potential_issues) > len(module_result.get("results", {})) / 2:
            return f"La maggior parte delle proposte presenta problemi significativi. Si consiglia una revisione sostanziale dell'approccio complessivo, considerando l'impatto generale limitato ({overall_impact:.2f}/1.0)."
        else:
            return f"Alcune proposte presentano problemi che dovrebbero essere affrontati. Nel complesso, l'impatto previsto ({overall_impact:.2f}/1.0) potrebbe essere migliorato con revisioni mirate e considerando approcci alternativi."
