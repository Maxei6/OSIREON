FROM python:3.10-slim

WORKDIR /app

# Copia i file di requisiti
COPY requirements.txt .

# Installa le dipendenze
RUN pip install --no-cache-dir -r requirements.txt

# Copia il codice sorgente
COPY src/ ./src/
COPY .env .

# Espone la porta specificata nell'env o la 8000 di default
EXPOSE 8000

# Comando per avviare l'applicazione
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
