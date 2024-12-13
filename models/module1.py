from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import linear_model  
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, confusion_matrix, ConfusionMatrixDisplay
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.metrics import roc_curve, auc
import pandas as pd
import joblib
import time


# Lecture de data
data = pd.read_csv("./Data/clean_data.csv", sep=',')

# repartition de data train et test
x= data[['Temperature', 'Humidity', 'WindSpeed','GeneralDiffuseFlows', 'DiffuseFlows']]
y= data['PowerConsumption_Zone3']
# ,'PowerConsumption_Zone2', 'PowerConsumption_Zone3'
x_train,x_test,y_train,y_test= train_test_split(x, y, test_size=0.2, random_state= 42)

# Creer le model Random Forest
rf_model = RandomForestRegressor(n_estimators=10, random_state=42)

# entrenament
rf_model.fit(x_train, y_train)

# Prediction
y_pred_random = rf_model.predict(x_test)

# Evaluer le model
mse = mean_squared_error(y_test, y_pred_random)
r2 = r2_score(y_test, y_pred_random)

print(f"Mean Squared Error: {mse}")
print(f"R^2 Score: {r2}")
