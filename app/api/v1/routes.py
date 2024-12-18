from fastapi import APIRouter, HTTPException
from app.ml.model import predict  # Assurez-vous que le chemin est correct
import pandas as pd  # Pour formater les données

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
        # Convertir les données en DataFrame ou tableau 2D
        input_data = pd.DataFrame([data])

        # Appel de la fonction `predict`
        result = predict(input_data.values)  # Converti en tableau Numpy

        return {"prediction": result[0]}  # Retourne la première valeur de la prédiction
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
