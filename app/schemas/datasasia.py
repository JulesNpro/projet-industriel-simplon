from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class DatasasiaBase(BaseModel):
    adresse: Optional[str] = Field(None, title="Adresse", description="Adresse de la donnée")
    annee: Optional[int] = Field(None, title="Année", description="Année concernée par les données")
    code_commune: Optional[int] = Field(None, title="Code Commune", description="Code de la commune")
    nom_commune: Optional[str] = Field(None, title="Nom Commune", description="Nom de la commune")
    segment_de_client: Optional[str] = Field(None, title="Segment de Client", description="Segment de clientèle")
    code_departement: Optional[float] = Field(None, title="Code Département", description="Code du département")
    code_region: Optional[float] = Field(None, title="Code Région", description="Code de la région")
    nombre_de_logements: Optional[int] = Field(None, title="Nombre de Logements", description="Nombre total de logements")
    consommation_annuelle_totale: Optional[float] = Field(None, title="Consommation Année Totale", description="Consommation totale en MWh")
    consommation_annuelle_moyenne_par_logement: Optional[float] = Field(None, title="Consommation Moyenne par Logement", description="Consommation moyenne par logement en MWh")
    consommation_annuelle_moyenne_commune: Optional[float] = Field(None, title="Consommation Moyenne Commune", description="Consommation moyenne de la commune en MWh")

    # Mise à jour pour Pydantic 2.0+
    model_config = ConfigDict(from_attributes=True)

class DatasasiaCreate(DatasasiaBase):
    pass

class Datasasia(DatasasiaBase):
    id: int = Field(..., title="ID", description="Identifiant unique")
