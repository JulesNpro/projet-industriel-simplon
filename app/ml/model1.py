import requests
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.linear_model import Lasso
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import numpy as np
import joblib
import matplotlib.pyplot as plt
import logging

# Configuration du logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("model_training.log"),  # Logs dans un fichier
        logging.StreamHandler()  # Logs dans la console
    ]
)
logger = logging.getLogger("training_logger")

# URL de l'API
API_URL = "http://127.0.0.1:8000/datasasia"  # Remplacez par l'URL correcte de votre API

try:
    logger.info("Récupération des données depuis l'API...")
    response = requests.get(API_URL)
    if response.status_code == 200:
        data = pd.DataFrame(response.json())
        logger.info("Données récupérées avec succès.")
    else:
        logger.error(f"Erreur lors de la récupération des données : {response.status_code}")
        exit()
except Exception as e:
    logger.exception(f"Erreur de connexion à l'API : {e}")
    exit()

# Sélection des features et de la cible
features = ['temperature', 'humidity', 'windspeed', 'general_diffuse_flows', 'diffuse_flows']
target = 'power_consumption_zone3'

X = data[features]
y = data[target]

# Division des données en ensembles d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardisation des données
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Définition du modèle
model = Lasso()

# Définition de l'espace de paramètres pour la recherche GridSearchCV
param_space = {
    'alpha': [0.1, 1.0, 10.0],
    'fit_intercept': [True, False]
}

# Entraînement avec GridSearchCV
grid = GridSearchCV(model, param_space, cv=10, scoring='r2', refit=True, verbose=1)
logger.info("Entraînement du modèle en cours...")
grid_search = grid.fit(X_train, y_train)

# Meilleur modèle et ses paramètres
best_model = grid_search.best_estimator_
logger.info(f"Meilleurs paramètres : {grid_search.best_params_}")

# Prédictions sur les données de test
y_pred = best_model.predict(X_test)

# Évaluation du modèle
rmse = mean_squared_error(y_test, y_pred, squared=False)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
adjusted_r2 = 1 - (1 - r2) * (len(y_test) - 1) / (len(y_test) - X_test.shape[1] - 1)

logger.info(f"Évaluation du modèle :")
logger.info(f"RMSE : {rmse:.2f}")
logger.info(f"MAE : {mae:.2f}")
logger.info(f"R² : {r2:.2f}")
logger.info(f"R² ajusté : {adjusted_r2:.2f}")

# Validation croisée
cv_scores = cross_val_score(best_model, X_train, y_train, cv=10, scoring='r2')
logger.info(f"Scores R² en validation croisée : {cv_scores}")
logger.info(f"Score R² moyen : {np.mean(cv_scores):.2f}")

# Sauvegarde du modèle
MODEL_PATH = "lasso_regression_model.pkl"
joblib.dump(best_model, MODEL_PATH)
logger.info(f"Modèle sauvegardé dans : {MODEL_PATH}")

# Visualisation des prédictions
plt.figure(figsize=(8, 6))
plt.scatter(y_test, y_pred, alpha=0.7, color='blue')
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=2)
plt.xlabel("Valeurs réelles")
plt.ylabel("Valeurs prédites")
plt.title("Prédictions vs Valeurs réelles")
plt.grid()
plt.show()
