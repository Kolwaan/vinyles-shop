import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from models.database import Base, get_db

from main import app

engine = create_engine("sqlite:///./data/test.db", connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


# Fixture qui crée une BDD SQLite temporaire pour les tests.
# Les tests restent isolés les uns des autes car on repart sur une BDD vide.
@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)   # Création des tables 
    session = TestingSessionLocal()         # Ouvre une session vers la BDD de test
    try:
        yield session                       # Fournit la session au test
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine) # Supprime toutes les tables après le test
        
        
        
# Pour travailler sur la BDD de test
@pytest.fixture(scope="function")
def client(db_session):             # Reçoit db_session en paramètre
    def override_get_db():
        try:
            yield db_session        # Remplace la vraie BDD par la BDD de test
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db  # Injection de la substitution
    yield TestClient(app)
    app.dependency_overrides.clear()
    
    
# Données de test pour un utilisateur
@pytest.fixture
def test_user_data():
    return {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword123"
    }
    
    
# Données de test pour une collection
@pytest.fixture
def test_collection_data():
    return {
        "title": "Ma collection Rock",
        "description": "Mes vinyles rock préférés"
    }