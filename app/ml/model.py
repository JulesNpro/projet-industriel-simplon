import os
import joblib

base_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(base_dir, 'modeljose.pkl')

# Charger le modèle
try:
    with open(model_path, 'rb') as file:
        model = joblib.load(file)
    print("Type du modèle chargé :", type(model))
    
    # Test de compatibilité
    if not hasattr(model, "predict"):
        raise TypeError("Le modèle chargé n'est pas compatible : il ne contient pas de méthode 'predict'.")
    else:
        print("Le modèle est compatible avec la méthode 'predict'.")
except FileNotFoundError as e:
    print(f"Erreur : Fichier non trouvé. Chemin : {model_path}")
    raise e
except TypeError as e:
    print(e)
    raise e

# Fonction de prédiction
def predict(input_data):
    if not hasattr(model, "predict"):
        raise AttributeError("Le modèle chargé ne dispose pas d'une méthode 'predict'.")
    return model.predict(input_data)

# Test de la fonction predict
if __name__ == "__main__":
    # Exemple de données d'entrée pour une prédiction
    try:
        input_data = [[5.1, 3.5, 1.4, 0.2, 2]]  # Remplacez par des données adaptées à votre modèle
        print("Données d'entrée :", input_data)
        
        # Tester la prédiction
        prediction = predict(input_data)
        print("Résultat de la prédiction :", prediction)
    except Exception as e:
        print("Erreur pendant la prédiction :", e)
