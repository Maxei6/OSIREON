"""
Script di test per l'endpoint /simulate di Osireon.
Questo script invia una richiesta di esempio all'endpoint e verifica la risposta.
"""
import requests
import json
import sys

# URL dell'endpoint (quando l'applicazione è in esecuzione)
API_URL = "http://localhost:8000/simulate"

# Dati di esempio per il test
test_data = {
  "country": "Italy",
  "domain": "Economia",
  "proposals": ["Flat tax al 20%", "Reddito universale"],
  "constraints": ["Nessun aumento del debito pubblico"]
}

def test_simulate_endpoint():
    """
    Testa l'endpoint /simulate con dati di esempio.
    """
    print("Inviando richiesta di test all'endpoint /simulate...")
    
    try:
        # Invia la richiesta POST
        response = requests.post(API_URL, json=test_data)
        
        # Verifica il codice di stato
        print(f"Codice di stato: {response.status_code}")
        
        if response.status_code == 200:
            # Analizza la risposta JSON
            result = response.json()
            
            # Salva la risposta in un file per riferimento
            with open("test_response.json", "w") as f:
                json.dump(result, f, indent=2)
            
            print("Test completato con successo!")
            print("Risposta salvata in test_response.json")
            
            # Verifica la struttura della risposta
            verify_response_structure(result)
            
            return True
        else:
            print(f"Errore: {response.text}")
            return False
            
    except Exception as e:
        print(f"Errore durante il test: {str(e)}")
        return False

def verify_response_structure(response):
    """
    Verifica che la risposta abbia la struttura attesa.
    
    Args:
        response: Risposta JSON dall'endpoint.
    """
    print("\nVerifica della struttura della risposta:")
    
    # Verifica la presenza dei campi principali
    required_fields = ["simulation_id", "result", "agent_analyses", "ethics_check"]
    for field in required_fields:
        if field in response:
            print(f"✓ Campo '{field}' presente")
        else:
            print(f"✗ Campo '{field}' mancante")
    
    # Verifica la struttura del risultato del modulo
    if "result" in response and "module_name" in response["result"]:
        print(f"✓ Risultato del modulo: {response['result']['module_name']}")
    
    # Verifica la presenza di analisi degli agenti
    if "agent_analyses" in response:
        print(f"✓ Numero di analisi degli agenti: {len(response['agent_analyses'])}")
    
    # Verifica il controllo etico
    if "ethics_check" in response and "passed" in response["ethics_check"]:
        passed = response["ethics_check"]["passed"]
        print(f"✓ Controllo etico: {'Superato' if passed else 'Non superato'}")
        
        if not passed and "violations" in response["ethics_check"]:
            print(f"  Violazioni rilevate: {len(response['ethics_check']['violations'])}")

if __name__ == "__main__":
    test_simulate_endpoint()
