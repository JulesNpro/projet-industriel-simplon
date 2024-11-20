"# Point d'entrée de l'application FastAPI" 
"from fastapi import FastAPI" 
"app = FastAPI()" 
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db, engine
from app.schemas.datasasia import Datasasia, DatasasiaCreate
from app.models.datasasia import Base, Datasasia
# Crée les tables dans la base de données
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Route pour obtenir toutes les entrées
@app.get("/datasasia", response_model=list[Datasasia])
def get_all_datas(db: Session = Depends(get_db)):
    return db.query(Datasasia).all()

# Route pour obtenir une seule entrée
@app.get("/datasasia/{datas_id}", response_model=Datasasia)
def get_data(datas_id: int, db: Session = Depends(get_db)):
    data = db.query(Datasasia).filter(Datasasia.id == datas_id).first()
    if not data:
        raise HTTPException(status_code=404, detail="Donnée non trouvée")
    return data

# Route pour ajouter une nouvelle entrée
@app.post("/datasasia", response_model=Datasasia)
def create_data(data: DatasasiaCreate, db: Session = Depends(get_db)):
    db_data = Datasasia(**data.dict())
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data

# Route pour supprimer une entrée
@app.delete("/datasasia/{datas_id}")
def delete_data(datas_id: int, db: Session = Depends(get_db)):
    data = db.query(Datasasia).filter(Datasasia.id == datas_id).first()
    if not data:
        raise HTTPException(status_code=404, detail="Donnée non trouvée")
    db.delete(data)
    db.commit()
    return {"message": "Donnée supprimée avec succès"}
