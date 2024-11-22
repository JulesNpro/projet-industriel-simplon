import pandas as pd


index = ['Adresse',
        'Année',
        'Code Commune',
        'Nom Commune',
        'Segment de client',
        'Code Département',
        'Code Région',
        'Nombre de logements',
        "Consommation annuelle totale de l'adresse (MWh)",
        "Consommation annuelle moyenne par logement de l'adresse (MWh)",
        "Consommation annuelle moyenne de la commune (MWh)"]


df = pd.read_csv("consommation-annuelle-residentielle-par-adresse.csv",sep=';')
df = df[index]
df = df.dropna()
df.to_csv("workable_data.csv")