"""
Implementazione dell'AnalystAgent per Osireon.
Questo agente analizza i risultati della simulazione e fornisce un'analisi dettagliata.
"""
import logging
from typing import Dict, Any

from src.agents.base import BaseAgent

# Configurazione del logging
logger = logging.getLogger("osireon.agents.analyst")

class AnalystAgent(BaseAgent):
    """
    Agente che analizza i risultati della simulazione e fornisce un'analisi dettagliata.
    """
    
    def __init__(self):
        """
        Inizializza l'AnalystAgent.
        """
        super().__init__("AnalystAgent")
    
    def analyze(self, input_data: Dict[str, Any], module_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analizza i dati di input e i risultati del modulo.
        
        Args:
            input_data: Dati di input originali della simulazione.
            module_result: Risultato dell'elaborazione del modulo.
            
        Returns:
            Dict[str, Any]: Risultato dell'analisi dell'agente.
        """
        logger.info(f"AnalystAgent sta analizzando i risultati del modulo {module_result.get('module', 'sconosciuto')}")
        
        # Estrai informazioni rilevanti
        proposals = input_data.get("proposals", [])
        constraints = input_data.get("constraints", [])
        domain = input_data.get("domain", "")
        country = input_data.get("country", "")
        
        # Analisi mock - in una implementazione reale, qui ci sarebbe l'integrazione con LLM
        analysis = {
            "summary": f"Analisi delle {len(proposals)} proposte nel dominio {domain} per {country}",
            "key_findings": [],
            "recommendations": [],
            "detailed_analysis": {}
        }
        
        # Genera analisi per ogni proposta
        for i, proposal in enumerate(proposals):
            proposal_key = f"proposal_{i+1}"
            proposal_result = module_result.get("results", {}).get(proposal_key, {})
            
            # Estrai metriche rilevanti dal risultato del modulo
            impact_score = proposal_result.get("impact_score", proposal_result.get("social_impact_score", 0.5))
            feasibility = proposal_result.get("feasibility", proposal_result.get("acceptance_rate", 0.5))
            
            # Genera analisi per questa proposta
            proposal_analysis = {
                "proposal": proposal,
                "impact_assessment": f"La proposta ha un impatto stimato di {impact_score:.2f} su una scala da 0 a 1",
                "feasibility_assessment": f"La fattibilità della proposta è valutata a {feasibility:.2f} su una scala da 0 a 1",
                "constraints_analysis": self._analyze_constraints(proposal_result.get("constraints_check", [])),
                "recommendation": self._generate_recommendation(impact_score, feasibility)
            }
            
            # Aggiungi alla lista dei key findings
            if impact_score > 0.7:
                analysis["key_findings"].append(f"La proposta '{proposal}' ha un impatto potenzialmente elevato")
            
            # Aggiungi alla lista delle raccomandazioni
            analysis["recommendations"].append(proposal_analysis["recommendation"])
            
            # Aggiungi all'analisi dettagliata
            analysis["detailed_analysis"][proposal_key] = proposal_analysis
        
        # Aggiungi una conclusione generale
        analysis["conclusion"] = self._generate_conclusion(analysis["key_findings"], module_result)
        
        # Registra il completamento dell'analisi
        self._log_analysis(analysis)
        
        return analysis
    
    def _analyze_constraints(self, constraints_check: list) -> str:
        """
        Analizza i risultati del controllo dei vincoli.
        
        Args:
            constraints_check: Lista dei risultati del controllo dei vincoli.
            
        Returns:
            str: Analisi dei vincoli.
        """
        if not constraints_check:
            return "Nessun vincolo specificato per questa proposta."
        
        satisfied = sum(1 for c in constraints_check if c.get("satisfied", False))
        total = len(constraints_check)
        
        if satisfied == total:
            return f"La proposta soddisfa tutti i {total} vincoli specificati."
        elif satisfied == 0:
            return f"La proposta non soddisfa nessuno dei {total} vincoli specificati."
        else:
            return f"La proposta soddisfa {satisfied} dei {total} vincoli specificati."
    
    def _generate_recommendation(self, impact_score: float, feasibility: float) -> str:
        """
        Genera una raccomandazione basata sull'impatto e la fattibilità.
        
        Args:
            impact_score: Punteggio di impatto della proposta.
            feasibility: Punteggio di fattibilità della proposta.
            
        Returns:
            str: Raccomandazione generata.
        """
        if impact_score > 0.7 and feasibility > 0.7:
            return "Raccomandazione: Procedere con l'implementazione. Alto impatto e alta fattibilità."
        elif impact_score > 0.7 and feasibility <= 0.7:
            return "Raccomandazione: Considerare l'implementazione con cautela. Alto impatto ma fattibilità limitata."
        elif impact_score <= 0.7 and feasibility > 0.7:
            return "Raccomandazione: Valutare alternative. Facile da implementare ma impatto limitato."
        else:
            return "Raccomandazione: Riconsiderare la proposta. Basso impatto e bassa fattibilità."
    
    def _generate_conclusion(self, key_findings: list, module_result: Dict[str, Any]) -> str:
        """
        Genera una conclusione basata sui key findings e sul risultato del modulo.
        
        Args:
            key_findings: Lista dei principali risultati dell'analisi.
            module_result: Risultato dell'elaborazione del modulo.
            
        Returns:
            str: Conclusione generata.
        """
        if not key_findings:
            return "Nessuna delle proposte analizzate mostra un impatto significativo."
        
        overall_impact = module_result.get("overall_impact", module_result.get("overall_social_impact", 0.5))
        
        if overall_impact > 0.7:
            return f"Le proposte analizzate mostrano complessivamente un alto potenziale di impatto ({overall_impact:.2f}/1.0). Si raccomanda di procedere con le proposte ad alto impatto e alta fattibilità."
        elif overall_impact > 0.4:
            return f"Le proposte analizzate mostrano complessivamente un impatto moderato ({overall_impact:.2f}/1.0). Si raccomanda di rivedere e migliorare le proposte prima dell'implementazione."
        else:
            return f"Le proposte analizzate mostrano complessivamente un basso impatto ({overall_impact:.2f}/1.0). Si raccomanda di riconsiderare l'approccio e sviluppare nuove proposte."
