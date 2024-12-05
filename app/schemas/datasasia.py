from typing import Optional
from pydantic import BaseModel

class DatasasiaBase(BaseModel):
    adresse: Optional[str]
    annee: Optional[int]
    code_commune: Optional[int]
    nom_commune: Optional[str]
    segment_de_client: Optional[str]
    code_departement: Optional[float]
    code_region: Optional[float]
    nombre_de_logements: Optional[int]
    consommation_annuelle_totale: Optional[float]
    consommation_annuelle_moyenne_par_logement: Optional[float]
    consommation_annuelle_moyenne_commune: Optional[float]

class DatasasiaCreate(DatasasiaBase):
    pass

class DatasasiaUpdate(DatasasiaBase):
    """Permet de mettre à jour partiellement une entrée."""
    pass

class Datasasia(DatasasiaBase):
    id: int

    class Config:
        from_attributes = True
