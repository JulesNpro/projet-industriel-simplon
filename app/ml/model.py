import joblib
import os
import pandas as pd

# Chemin vers le modèle sauvegardé
MODEL_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "model.pkl"))

def load_model():
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Modèle non trouvé à l'emplacement : {MODEL_PATH}")
    return joblib.load(MODEL_PATH)

def predict(input_data: dict):
    """
    Prédit les résultats basés sur les données en entrée.
    
    Args:
        input_data (dict): Dictionnaire contenant les features pour la prédiction.

    Returns:
        float: Prédiction du modèle.
    """
    model = load_model()
    # Convertir les données en DataFrame
    df = pd.DataFrame([input_data])
    prediction = model.predict(df)
    return prediction
