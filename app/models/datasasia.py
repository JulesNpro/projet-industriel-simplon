from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

# Déclaration de la base de données
Base = declarative_base()

class Datasasia(Base):
    __tablename__ = "datasasia"

    id = Column(Integer, primary_key=True, index=True)
    annee = Column("Année", Integer, nullable=False)
    numero_de_voie = Column("Numéro de voie", Integer, nullable=False)
    indice_de_repetition = Column("Indice de répétition", String(512), nullable=True)
    type_de_voie = Column("Type de voie", String(512), nullable=True)
    libelle_de_voie = Column("Libellé de voie", String(512), nullable=True)
    code_commune = Column("Code Commune", Integer, nullable=False)
    nom_commune = Column("Nom Commune", String(512), nullable=True)
    segment_de_client = Column("Segment de client", String(512), nullable=True)
    nombre_de_logements = Column("Nombre de logements", Integer, nullable=True)
    consommation_annuelle_totale = Column("Consommation annuelle totale de l'adresse", Float, nullable=True)
    consommation_annuelle_moyenne_par_logement = Column("Consommation annuelle moyenne par logement de l'adresse", Float, nullable=True)
    consommation_annuelle_moyenne_commune = Column("Consommation annuelle moyenne de la commune", Float, nullable=True)
    adresse = Column("Adresse", String(512), nullable=True)
    code_epci = Column("Code EPCI", Integer, nullable=False)
    code_departement = Column("Code Département", Integer, nullable=False)
    code_region = Column("Code Région", Integer, nullable=False)
    tri_des_adresses = Column("Tri des adresses", String(512), nullable=True)

    # Configuration des arguments de la table (ex : charset)
    __table_args__ = {
        'mysql_charset': 'utf8mb4'
    }
