from fastapi import APIRouter, HTTPException
from app.ml.model import predict  # Assurez-vous que le chemin est correct

router = APIRouter()

@router.get("/datasasia")
def get_all_datas():
    return [{"id": 1, "message": "Test data"}]

@router.post("/predict")
def make_prediction(data: dict):
    """
    Endpoint pour faire une prédiction.

    Args:
        data (dict): Données d'entrée pour la prédiction.

    Returns:
        dict: Résultat de la prédiction.
    """
    try:
        result = predict(data)  # Appel de la fonction `predict` depuis `ml/model.py`
        return {"prediction": result[0]}  # Retourne la première valeur de la prédiction
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
