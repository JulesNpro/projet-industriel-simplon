import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import MinMaxScaler, StandardScaler, RobustScaler

data = pd.read_csv("../dataset.csv", sep=';')
data_numerique=data.select_dtypes(include=[np.number])

# list des colonnes pour aplique methode robustscaler
list_robustscaler=['Nombre de logements',"Consommation annuelle totale de l'adresse (MWh)",
       "Consommation annuelle moyenne par logement de l'adresse (MWh)",
       "Consommation annuelle moyenne de la commune (MWh)"]

def robus_scaler(data, list_robustscaler):
    rbscaler = RobustScaler()
    for col in list_robustscaler:
        data_numerique[col] = rbscaler.fit_transform(data_numerique.loc[:,[col]])



 