# connexion à la base de données

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine(
    "sqlite:///./data/vinyls.db",   # --> lien vers la base de données
    connect_args = {"check_same_thread":False}, 
    echo = True) # --> permet d'afficher toutes les requêtes SQL (à ne pas mettre en prod car affiche énormément de logs)

SessionLocal = sessionmaker(    # on crée un session pour faire des requètes à la BDD.
    autocommit = False,         # pas de commit automatique.
    autoflush = False,          # SQLAlchemy n’envoie pas automatiquement les modifications à la BDD.
    bind = engine)              # lier la session à cette connexion à la BDD. La session saura quelle BDD utiliser pour exécuter les requêtes.

Base = declarative_base()       # génère une classe parente spéciale qui sert de base aux entités (models)


# fonction pour créer une session pour faire des interactions avec la BDD
def get_db():
    db = SessionLocal() # crée une nouvelle session connecté à la BDD 
    try:
        yield db    # garantit que la session reste ouverte pendant toute la durée d'exécution de la route
    finally:
        db.close()  # ferme la session

