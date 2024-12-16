from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split,cross_val_score
import numpy as np
from sklearn.metrics import r2_score, confusion_matrix, ConfusionMatrixDisplay
from sklearn.linear_model import LinearRegression, Lasso
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.metrics import roc_curve, auc
from  sklearn.model_selection  import  GridSearchCV
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import pandas as pd
import joblib
import time

# Lecture de data
data = pd.read_csv("../Data/clean_data.csv", sep=',')

# repartition de data train et test
x= data[['Temperature', 'Humidity', 'WindSpeed','GeneralDiffuseFlows', 'DiffuseFlows']]
y= data['PowerConsumption_Zone3']


# ,'PowerConsumption_Zone2', 'PowerConsumption_Zone3'
x_train,x_test,y_train,y_test= train_test_split(x, y, test_size=0.2, random_state= 42)

# scaler = StandardScaler()
# x_train = scaler.fit_transform(x_train)
# x_test = scaler.transform(x_test)
# Creer le model Random Forest
#rf_model = RandomForestRegressor()

# calcule hyperparmetres

gb_model = GradientBoostingRegressor(n_estimators=100, learning_rate=0.5, max_depth=5, random_state=42)

# parameter range definition

param_space = {
    'alpha': [0.1, 1.0, 10.0],  # Parámetro de regularización
    'fit_intercept': [True, False]  # Ajustar la intersección
    
    }
  
grid = GridSearchCV(regr, param_space,cv=10, refit=True, verbose=1)
# Entraînez le modèle en utilisant les ensembles d'entraînement
grid_search = grid.fit( x_train ,  y_train )

# Meilleur modèle et ses paramètres
best_model = grid_search.best_estimator_
print("Meilleurs paramètres :", grid_search.best_params_)

# Prediction
y_pred= best_model.predict(x_test)

# Evaluer le model
rmse = mean_squared_error(y_test, y_pred, squared=False)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
adjusted_r2 = 1 - (1 - r2) * (len(y_test) - 1) / (len(y_test) - x_test.shape[1] - 1)  # Ajuste de R²

print(f"RMSE : {rmse:.2f}")
print(f"MAE : {mae:.2f}")
print(f"R² : {r2:.2f}")

# validation coisse
cv_scores = cross_val_score(best_model, x_train, y_train, cv=10, scoring='r2', n_jobs=-1)
print("Scores R² en validation croisée :", cv_scores)
print("Score R² moyen :", np.mean(cv_scores))

# Sauvegarde du modèle
joblib.dump(best_model, '../models/Rgression_Lineal.pkl')
print("Modèle Random Forest Regression sauvegarder.")

plt.scatter(y_test, y_pred)
plt.xlabel("Valeurs Réelles")
plt.ylabel("Prédictions")
plt.title("Prédictions vs Valeurs Réelles")
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=2)  # Ligne de référence
plt.show()
