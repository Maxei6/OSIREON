"""
Sistema di caricamento dinamico dei moduli per Osireon.
Questo file contiene le funzioni per caricare dinamicamente i moduli di simulazione.
"""
import importlib
import logging
import os
from typing import Dict, Any, Callable, Optional

# Configurazione del logging
logger = logging.getLogger("osireon.modules")

class ModuleLoader:
    """
    Classe per il caricamento dinamico dei moduli di simulazione.
    """
    
    def __init__(self, modules_dir: str = "src/modules"):
        """
        Inizializza il loader dei moduli.
        
        Args:
            modules_dir: Directory contenente i moduli di simulazione.
        """
        self.modules_dir = modules_dir
        self.modules_cache: Dict[str, Callable] = {}
        logger.info(f"ModuleLoader inizializzato con directory: {modules_dir}")
    
    def get_module_path(self, country: str, domain: str) -> str:
        """
        Costruisce il percorso del modulo basato su paese e dominio.
        
        Args:
            country: Paese per cui caricare il modulo.
            domain: Dominio di policy per cui caricare il modulo.
            
        Returns:
            str: Percorso del modulo.
        """
        # Normalizza i nomi (lowercase e rimuovi spazi)
        country_code = country.lower()[:2]
        domain_name = domain.lower().replace(" ", "_")
        
        # Costruisci il nome del modulo
        module_name = f"{domain_name}_{country_code}"
        
        return module_name
    
    def load_module(self, country: str, domain: str) -> Optional[Callable]:
        """
        Carica dinamicamente un modulo di simulazione basato su paese e dominio.
        
        Args:
            country: Paese per cui caricare il modulo.
            domain: Dominio di policy per cui caricare il modulo.
            
        Returns:
            Callable: Funzione run del modulo caricato o None se il modulo non esiste.
        """
        module_name = self.get_module_path(country, domain)
        
        # Controlla se il modulo è già in cache
        if module_name in self.modules_cache:
            logger.info(f"Modulo {module_name} trovato in cache")
            return self.modules_cache[module_name]
        
        try:
            # Costruisci il percorso completo del modulo
            module_path = f"src.modules.{module_name}"
            
            # Importa il modulo dinamicamente
            module = importlib.import_module(module_path)
            
            # Verifica che il modulo abbia una funzione run
            if not hasattr(module, "run"):
                logger.error(f"Il modulo {module_name} non ha una funzione run")
                return None
            
            # Memorizza la funzione run nella cache
            self.modules_cache[module_name] = module.run
            
            logger.info(f"Modulo {module_name} caricato con successo")
            return module.run
            
        except ImportError as e:
            logger.error(f"Impossibile importare il modulo {module_name}: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Errore durante il caricamento del modulo {module_name}: {str(e)}")
            return None
    
    def run_module(self, country: str, domain: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Esegue un modulo di simulazione con i dati di input forniti.
        
        Args:
            country: Paese per cui eseguire la simulazione.
            domain: Dominio di policy per cui eseguire la simulazione.
            input_data: Dati di input per la simulazione.
            
        Returns:
            Dict[str, Any]: Risultato della simulazione o un risultato di errore.
        """
        module_func = self.load_module(country, domain)
        
        if module_func is None:
            logger.warning(f"Modulo per {domain} in {country} non trovato, utilizzo mock")
            return {
                "status": "error",
                "message": f"Modulo per {domain} in {country} non trovato",
                "result": {"mocked": True, "impact_score": 0.5}
            }
        
        try:
            # Esegui la funzione run del modulo
            result = module_func(input_data)
            logger.info(f"Modulo eseguito con successo: {result}")
            return result
        except Exception as e:
            logger.error(f"Errore durante l'esecuzione del modulo: {str(e)}")
            return {
                "status": "error",
                "message": f"Errore durante l'esecuzione: {str(e)}",
                "result": {"mocked": True, "error": True}
            }

# Istanza singleton del loader dei moduli
module_loader = ModuleLoader()
