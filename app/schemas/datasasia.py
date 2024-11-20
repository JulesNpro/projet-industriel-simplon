"# Schéma Pydantic pour la table datasasia" 
from pydantic import BaseModel
from typing import Optional

class DatasasiaBase(BaseModel):
    annee: Optional[int]
    numero_de_voie: Optional[int]
    indice_de_repetition: Optional[str]
    type_de_voie: Optional[str]
    libelle_de_voie: Optional[str]
    code_commune: Optional[int]
    nom_commune: Optional[str]
    segment_de_client: Optional[str]
    nombre_de_logements: Optional[int]
    consommation_annuelle_totale: Optional[float]
    consommation_annuelle_moyenne_par_logement: Optional[float]
    consommation_annuelle_moyenne_commune: Optional[float]
    adresse: Optional[str]
    code_epci: Optional[int]
    code_departement: Optional[int]
    code_region: Optional[int]
    tri_des_adresses: Optional[str]

class DatasasiaCreate(DatasasiaBase):
    pass

class Datasasia(DatasasiaBase):
    id: int

    class Config:
        orm_mode = True
