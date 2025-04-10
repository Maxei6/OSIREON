"""
Validatore etico per Osireon.
Questo file contiene l'implementazione del validatore di conformità etica.
"""
import json
import logging
import os
from typing import Dict, Any, List, Optional

# Configurazione del logging
logger = logging.getLogger("osireon.ethics")

class EthicsValidator:
    """
    Validatore di conformità etica per le proposte di policy.
    """
    
    def __init__(self, ruleset_path: str = "src/ethics/ruleset_it.json"):
        """
        Inizializza il validatore etico.
        
        Args:
            ruleset_path: Percorso del file JSON contenente le regole etiche.
        """
        self.ruleset_path = ruleset_path
        self.rules = self._load_rules()
        logger.info(f"EthicsValidator inizializzato con {len(self.rules)} regole")
    
    def _load_rules(self) -> List[Dict[str, Any]]:
        """
        Carica le regole etiche dal file JSON.
        
        Returns:
            List[Dict[str, Any]]: Lista delle regole etiche.
        """
        try:
            with open(self.ruleset_path, 'r') as file:
                ruleset = json.load(file)
                return ruleset.get("rules", [])
        except Exception as e:
            logger.error(f"Errore durante il caricamento delle regole etiche: {str(e)}")
            return []
    
    def validate(self, proposals: List[str], domain: str) -> Dict[str, Any]:
        """
        Valida le proposte di policy rispetto alle regole etiche.
        
        Args:
            proposals: Lista delle proposte di policy da validare.
            domain: Dominio delle proposte (es. economia, sociale).
            
        Returns:
            Dict[str, Any]: Risultato della validazione etica.
        """
        logger.info(f"Validazione etica di {len(proposals)} proposte nel dominio {domain}")
        
        if not self.rules:
            logger.warning("Nessuna regola etica caricata, impossibile eseguire la validazione")
            return {
                "passed": False,
                "message": "Nessuna regola etica disponibile",
                "violations": ["Impossibile eseguire la validazione etica: regole non disponibili"]
            }
        
        # Risultato complessivo della validazione
        validation_result = {
            "passed": True,
            "violations": [],
            "proposal_results": {}
        }
        
        # Valida ogni proposta
        for i, proposal in enumerate(proposals):
            proposal_key = f"proposal_{i+1}"
            proposal_result = self._validate_proposal(proposal, domain)
            
            # Aggiungi il risultato della proposta
            validation_result["proposal_results"][proposal_key] = proposal_result
            
            # Se la proposta ha violazioni, aggiungi alla lista complessiva
            if not proposal_result["passed"]:
                validation_result["passed"] = False
                for violation in proposal_result["violations"]:
                    if violation not in validation_result["violations"]:
                        validation_result["violations"].append(violation)
        
        # Aggiungi un messaggio complessivo
        if validation_result["passed"]:
            validation_result["message"] = "Tutte le proposte rispettano le regole etiche"
        else:
            validation_result["message"] = f"Rilevate {len(validation_result['violations'])} violazioni delle regole etiche"
        
        logger.info(f"Validazione etica completata: {validation_result['message']}")
        return validation_result
    
    def _validate_proposal(self, proposal: str, domain: str) -> Dict[str, Any]:
        """
        Valida una singola proposta rispetto alle regole etiche.
        
        Args:
            proposal: Proposta di policy da validare.
            domain: Dominio della proposta.
            
        Returns:
            Dict[str, Any]: Risultato della validazione della proposta.
        """
        # Risultato della validazione per questa proposta
        result = {
            "proposal": proposal,
            "passed": True,
            "violations": [],
            "rule_checks": []
        }
        
        # Controlla ogni regola
        for rule in self.rules:
            rule_check = self._check_rule(proposal, rule, domain)
            result["rule_checks"].append(rule_check)
            
            # Se la regola è violata, aggiungi alla lista delle violazioni
            if not rule_check["passed"]:
                result["passed"] = False
                violation = f"{rule['id']} - {rule['name']}: {rule_check['reason']}"
                result["violations"].append(violation)
        
        return result
    
    def _check_rule(self, proposal: str, rule: Dict[str, Any], domain: str) -> Dict[str, Any]:
        """
        Controlla se una proposta rispetta una regola etica.
        
        Args:
            proposal: Proposta di policy da controllare.
            rule: Regola etica da verificare.
            domain: Dominio della proposta.
            
        Returns:
            Dict[str, Any]: Risultato del controllo della regola.
        """
        # Implementazione mock - in una versione reale, qui ci sarebbe una logica più sofisticata
        # che potrebbe utilizzare NLP o LLM per analizzare la proposta
        
        rule_id = rule.get("id", "unknown")
        rule_name = rule.get("name", "Regola sconosciuta")
        rule_description = rule.get("description", "")
        rule_keywords = rule.get("keywords", [])
        rule_severity = rule.get("severity", "medium")
        
        # Controlla se la proposta contiene parole chiave negative associate alla regola
        proposal_lower = proposal.lower()
        
        # Simulazione di controllo basato su parole chiave e dominio
        # In una implementazione reale, questa logica sarebbe molto più sofisticata
        
        # Genera un risultato casuale ma deterministico basato sulla proposta e sulla regola
        # Questo è solo per simulazione, in una implementazione reale ci sarebbe una vera analisi
        passed = True
        reason = f"La proposta rispetta la regola '{rule_name}'"
        
        # Simulazione di alcune violazioni specifiche
        if rule_id == "rule_002" and "flat tax" in proposal_lower and domain.lower() == "economia":
            passed = False
            reason = "La proposta potrebbe aumentare il deficit pubblico senza adeguate compensazioni"
        elif rule_id == "rule_003" and any(kw in proposal_lower for kw in ["tassa", "riduzione", "taglio"]) and domain.lower() == "sociale":
            passed = False
            reason = "La proposta potrebbe aumentare le disuguaglianze sociali"
        elif rule_id == "rule_004" and any(kw in proposal_lower for kw in ["carbone", "petrolio", "gas"]) and not "rinnovabile" in proposal_lower:
            passed = False
            reason = "La proposta potrebbe avere un impatto negativo sull'ambiente"
        elif rule_id == "rule_008" and any(kw in proposal_lower for kw in ["dati", "monitoraggio", "sorveglianza"]):
            passed = False
            reason = "La proposta potrebbe violare la privacy dei cittadini"
        
        return {
            "rule_id": rule_id,
            "rule_name": rule_name,
            "passed": passed,
            "reason": reason,
            "severity": rule_severity
        }

# Istanza singleton del validatore etico
ethics_validator = EthicsValidator()
