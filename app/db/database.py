"# Connexion à la base de données avec SQLAlchemy" 
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Connexion à votre base de données MySQL distante
DATABASE_URL = "mysql+pymysql://if0_37743569:Simplon13@sql203.infinityfree.com/if0_37743569_sasdata"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Fonction pour obtenir une session de base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
