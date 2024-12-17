from sklearn.model_selection import train_test_split,cross_val_score
import numpy as np
from sklearn.metrics import r2_score, confusion_matrix, ConfusionMatrixDisplay
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.metrics import roc_curve, auc
from  sklearn.model_selection  import  GridSearchCV
import pandas as pd
import joblib
import time

# Lecture de data
data = pd.read_csv("../data/clean_data.csv", sep=',')

# repartition de data train et test
x= data[['Temperature', 'Humidity', 'WindSpeed','GeneralDiffuseFlows', 'DiffuseFlows']]
y= data['PowerConsumption_Zone3']

# ,'PowerConsumption_Zone2', 'PowerConsumption_Zone3'
x_train,x_test,y_train,y_test= train_test_split(x, y, test_size=0.2, random_state= 42)

# Creer le model Random Forest
#rf_model = RandomForestRegressor()

# calcule hyperparmetres

ml  = RandomForestRegressor(n_estimators=10, random_state=42)

# parameter range definition
 
param_space = {
    'n_estimators': [10, 50],  # Número de árboles en el bosque
    'max_depth': [3,5],  # Profundidad máxima del árbol
    'min_samples_split': [2,],  # Mínimo número de muestras requeridas para dividir un nodo
    'min_samples_leaf': [1, 2],  # Mínimo número de muestras requeridas para estar en un nodo hoja
    
    }
  
grid  =  GridSearchCV ( ml ,  param_space ,  refit  =  True ,  verbose=1 )
  
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


print(f"RMSE : {rmse:.2f}")
print(f"MAE : {mae:.2f}")
print(f"R² : {r2:.2f}")

# validation coisse
cv_scores = cross_val_score(best_model, x_train, y_train, cv=10, scoring='r2', n_jobs=-1)
print("Scores R² en validation croisée :", cv_scores)
print("Score R² moyen :", np.mean(cv_scores))

# Sauvegarde du modèle
joblib.dump(best_model, '../models/Random_Forest_Reg.pkl')
print("Modèle Random Forest Regression sauvegarder.")
