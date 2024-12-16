import joblib

try:
    model = joblib.load("ml/random_forest_model.pkl")
    print("Modèle chargé avec succès :", model)
except Exception as e:
    print("Erreur lors du chargement :", e)