import pickle
import os

# Récupère le chemin du dossier où se trouve le fichier actuel
base_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(base_dir, 'modeljose.pkl')

# Chargez le fichier
with open(model_path, 'rb') as file:
    # Votre code pour lire le modèle

    model = pickle.load(file)
print(model)