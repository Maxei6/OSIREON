"""
Modelli del database per Osireon.
Questo file contiene la definizione dei modelli SQLAlchemy per il database.
"""
import datetime
from typing import Dict, Any
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, JSON, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import os
from dotenv import load_dotenv

# Caricamento delle variabili d'ambiente
load_dotenv()

# Configurazione del database
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/osireon")

# Creazione della base per i modelli
Base = declarative_base()

class Simulation(Base):
    """
    Modello per le simulazioni eseguite.
    """
    __tablename__ = "simulations"
    
    id = Column(Integer, primary_key=True)
    country = Column(String(50), nullable=False)
    domain = Column(String(50), nullable=False)
    proposals = Column(JSON, nullable=False)
    constraints = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(String(20), default="pending")
    
    # Relazioni
    module_results = relationship("ModuleResult", back_populates="simulation", cascade="all, delete-orphan")
    agent_analyses = relationship("AgentAnalysis", back_populates="simulation", cascade="all, delete-orphan")
    ethics_checks = relationship("EthicsCheck", back_populates="simulation", cascade="all, delete-orphan")
    llm_logs = relationship("LLMLog", back_populates="simulation", cascade="all, delete-orphan")
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Converte il modello in un dizionario.
        
        Returns:
            Dict[str, Any]: Rappresentazione del modello come dizionario.
        """
        return {
            "id": self.id,
            "country": self.country,
            "domain": self.domain,
            "proposals": self.proposals,
            "constraints": self.constraints,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "status": self.status
        }

class ModuleResult(Base):
    """
    Modello per i risultati dei moduli.
    """
    __tablename__ = "module_results"
    
    id = Column(Integer, primary_key=True)
    simulation_id = Column(Integer, ForeignKey("simulations.id"), nullable=False)
    module_name = Column(String(100), nullable=False)
    result = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Relazioni
    simulation = relationship("Simulation", back_populates="module_results")
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Converte il modello in un dizionario.
        
        Returns:
            Dict[str, Any]: Rappresentazione del modello come dizionario.
        """
        return {
            "id": self.id,
            "simulation_id": self.simulation_id,
            "module_name": self.module_name,
            "result": self.result,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

class AgentAnalysis(Base):
    """
    Modello per le analisi degli agenti.
    """
    __tablename__ = "agent_analyses"
    
    id = Column(Integer, primary_key=True)
    simulation_id = Column(Integer, ForeignKey("simulations.id"), nullable=False)
    agent_name = Column(String(100), nullable=False)
    analysis = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Relazioni
    simulation = relationship("Simulation", back_populates="agent_analyses")
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Converte il modello in un dizionario.
        
        Returns:
            Dict[str, Any]: Rappresentazione del modello come dizionario.
        """
        return {
            "id": self.id,
            "simulation_id": self.simulation_id,
            "agent_name": self.agent_name,
            "analysis": self.analysis,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

class EthicsCheck(Base):
    """
    Modello per i controlli etici.
    """
    __tablename__ = "ethics_checks"
    
    id = Column(Integer, primary_key=True)
    simulation_id = Column(Integer, ForeignKey("simulations.id"), nullable=False)
    passed = Column(Boolean, nullable=False)
    violations = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Relazioni
    simulation = relationship("Simulation", back_populates="ethics_checks")
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Converte il modello in un dizionario.
        
        Returns:
            Dict[str, Any]: Rappresentazione del modello come dizionario.
        """
        return {
            "id": self.id,
            "simulation_id": self.simulation_id,
            "passed": self.passed,
            "violations": self.violations,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

class LLMLog(Base):
    """
    Modello per i log delle chiamate LLM.
    """
    __tablename__ = "llm_logs"
    
    id = Column(Integer, primary_key=True)
    simulation_id = Column(Integer, ForeignKey("simulations.id"), nullable=False)
    provider = Column(String(50), nullable=False)
    model = Column(String(50), nullable=False)
    prompt = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Relazioni
    simulation = relationship("Simulation", back_populates="llm_logs")
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Converte il modello in un dizionario.
        
        Returns:
            Dict[str, Any]: Rappresentazione del modello come dizionario.
        """
        return {
            "id": self.id,
            "simulation_id": self.simulation_id,
            "provider": self.provider,
            "model": self.model,
            "prompt": self.prompt,
            "response": self.response,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

# Funzione per creare le tabelle nel database
def create_tables():
    """
    Crea le tabelle nel database.
    """
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)

# Funzione per ottenere una sessione del database
def get_db_session():
    """
    Ottiene una sessione del database.
    
    Returns:
        Session: Sessione del database.
    """
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    return Session()
