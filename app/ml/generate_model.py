import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import joblib
import os

# Exemple de données (vous pouvez remplacer par vos propres données)
data = {
    "Année": [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022],
    "Nombre de Logements": [10, 20, 30, 40, 50, 60, 70, 80],
    "Consommation Totale (kWh)": [200, 220, 240, 260, 280, 300, 320, 340]
}

# Conversion en DataFrame
df = pd.DataFrame(data)

# Variables indépendantes (X) et dépendante (y)
X = df[["Année", "Nombre de Logements"]]
y = df["Consommation Totale (kWh)"]

# Division des données en jeu d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entraînement du modèle
model = LinearRegression()
model.fit(X_train, y_train)

# Évaluation du modèle
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print(f"Erreur quadratique moyenne : {mse}")

# Sauvegarde du modèle dans un fichier .pkl
model_path = os.path.join(os.path.dirname(__file__), "model.pkl")
joblib.dump(model, model_path)
print(f"Modèle sauvegardé dans : {model_path}")
