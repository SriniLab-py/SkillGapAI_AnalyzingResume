"""
Database Configuration Module
Handles SQLAlchemy engine and session management
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import Base
import os

# Database file path
DATABASE_URL = "sqlite:///skill_gap_ai.db"

# Create engine
engine = create_engine(DATABASE_URL, echo=False, connect_args={"check_same_thread": False})

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Initialize database - create all tables"""
    Base.metadata.create_all(bind=engine)

def get_session():
    """Get a new database session"""
    return SessionLocal()