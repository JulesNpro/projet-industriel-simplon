from fastapi import FastAPI, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.api.v1.routes import router as api_router
from app.db.database import get_db, engine
from app.models.datasasia import Base, Datasasia
from app.schemas.datasasia import Datasasia as DatasasiaSchema, DatasasiaCreate, DatasasiaUpdate
from app.ml.model import predict  # Assurez-vous que cette fonction existe et est correcte
import logging

# Création des tables dans la base de données
Base.metadata.create_all(bind=engine)

# Configuration du logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("fastapi_logger")

# Initialisation de l'application FastAPI
app = FastAPI()
app.include_router(api_router, prefix="/api/v1")

# Middleware pour journaliser toutes les requêtes
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Requête reçue : {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Réponse : {response.status_code}")
    return response

# Route pour obtenir toutes les entrées
@app.get("/datasasia", response_model=list[DatasasiaSchema])
def get_all_datas(db: Session = Depends(get_db)):
    logger.info("Requête pour obtenir toutes les entrées de Datasasia")
    return db.query(Datasasia).all()

# Route pour obtenir une seule entrée
@app.get("/datasasia/{datas_id}", response_model=DatasasiaSchema)
def get_data(datas_id: int, db: Session = Depends(get_db)):
    logger.info(f"Requête pour obtenir l'entrée avec ID {datas_id}")
    data = db.query(Datasasia).filter(Datasasia.id == datas_id).first()
    if not data:
        logger.error(f"Donnée avec ID {datas_id} non trouvée")
        raise HTTPException(status_code=404, detail="Donnée non trouvée")
    return data

# Route pour ajouter une nouvelle entrée
@app.post("/datasasia", response_model=DatasasiaSchema)
def create_data(data: DatasasiaCreate, db: Session = Depends(get_db)):
    logger.info(f"Requête pour ajouter une nouvelle entrée : {data.dict()}")
    db_data = Datasasia(**data.model_dump())
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data

# Route pour mettre à jour une entrée existante
@app.put("/datasasia/{datas_id}", response_model=DatasasiaSchema)
def update_data(datas_id: int, data: DatasasiaUpdate, db: Session = Depends(get_db)):
    logger.info(f"Requête pour mettre à jour l'entrée avec ID {datas_id} : {data.dict(exclude_unset=True)}")
    db_data = db.query(Datasasia).filter(Datasasia.id == datas_id).first()
    if not db_data:
        logger.error(f"Donnée avec ID {datas_id} non trouvée")
        raise HTTPException(status_code=404, detail="Donnée non trouvée")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(db_data, key, value)
    db.commit()
    db.refresh(db_data)
    return db_data

# Route pour supprimer une entrée
@app.delete("/datasasia/{datas_id}")
def delete_data(datas_id: int, db: Session = Depends(get_db)):
    logger.info(f"Requête pour supprimer l'entrée avec ID {datas_id}")
    data = db.query(Datasasia).filter(Datasasia.id == datas_id).first()
    if not data:
        logger.error(f"Donnée avec ID {datas_id} non trouvée")
        raise HTTPException(status_code=404, detail="Donnée non trouvée")
    db.delete(data)
    db.commit()
    return {"message": "Donnée supprimée avec succès"}

# Route pour effectuer une prédiction
@app.post("/predict")
def make_prediction(data: dict):
    """
    Endpoint pour effectuer une prédiction.
    Les données doivent inclure 'Année' et 'Nombre de Logements'.
    """
    logger.info(f"Requête de prédiction avec les données : {data}")
    try:
        prediction = predict(data)  # Utilise la fonction predict du modèle ML
        logger.info(f"Prédiction réussie : {prediction[0]}")
        return {"prediction": prediction[0]}
    except ValueError as e:
        logger.error(f"Erreur dans les données fournies : {e}")
        raise HTTPException(status_code=400, detail="Données invalides pour la prédiction.")
    except Exception as e:
        logger.error(f"Erreur interne : {e}")
        raise HTTPException(status_code=500, detail="Erreur interne pendant la prédiction.")
