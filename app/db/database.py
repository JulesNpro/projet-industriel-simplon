from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# URL de connexion avec encodage des caractères spéciaux pour le mot de passe
DATABASE_URL = "mysql+pymysql://freedb_simplon13:MyjK%40J33Hf%23zR7S@sql.freedb.tech/freedb_datasasia"

# Configuration du moteur SQLAlchemy
engine = create_engine(DATABASE_URL)

# Configuration de la session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base pour les modèles SQLAlchemy
Base = declarative_base()

# Fonction pour obtenir une session de base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
