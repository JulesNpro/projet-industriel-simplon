from sqlalchemy import Column, Integer, String, Float, Text
from sqlalchemy.orm import declarative_base

# Base de déclaration pour les modèles
Base = declarative_base()

class Datasasia(Base):
    __tablename__ = "datasasia"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    adresse = Column("Adresse", Text, nullable=True)
    annee = Column("Année", Integer, nullable=True)
    code_commune = Column("Code Commune", Integer, nullable=True)
    nom_commune = Column("Nom Commune", Text, nullable=True)
    segment_de_client = Column("Segment de client", Text, nullable=True)
    code_departement = Column("Code Département", Float, nullable=True)
    code_region = Column("Code Région", Float, nullable=True)
    nombre_de_logements = Column("Nombre de logements", Integer, nullable=True)
    consommation_annuelle_totale = Column("Consommation annuelle totale de l'adresse (MWh)", Float, nullable=True)
    consommation_annuelle_moyenne_par_logement = Column("Consommation annuelle moyenne par logement de l'adresse (MWh)", Float, nullable=True)
    consommation_annuelle_moyenne_commune = Column("Consommation annuelle moyenne de la commune (MWh)", Float, nullable=True)
