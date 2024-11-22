import sqlite3
import pandas as pd
import numpy as np
from FindNames import FindRegionName,FindDepartementName,FindRegionDepartement,FindDepartementCommune



df = pd.read_csv('Data/workable_data.csv')

con = sqlite3.connect('Data/data.db')

cur = con.cursor()

annees = df["Année"].unique()

sdcs = df["Segment de client"].unique()

regions = df["Code Région"].unique()

departements = df["Code Département"].unique()

communes = df["Code Commune"].unique()
nom_commune = df["Nom Commune"].unique()
commune_conso = df["Consommation annuelle moyenne de la commune (MWh)"].unique()


adress = df["Adresse"]
nombre_logements = df["Nombre de logements"]

conso_logement = df["Consommation annuelle moyenne par logement de l'adresse (MWh)"]

# for i,annee in enumerate(annees):
#     cur.execute("INSERT INTO Annees VALUES(?,?)",(i+1,int(annee)))




# for i,sdc in enumerate(sdcs):
#     cur.execute("INSERT INTO ClientsSegment VALUES(?,?)",(i+1,sdc))



# for i,region in enumerate(regions):
#     cur.execute("INSERT INTO Regions VALUES(?,?,?)",(i+1,int(region),FindRegionName(int(region))))



# for i,departement in enumerate(departements):
    
#     cur.execute(
#         "INSERT INTO Departements VALUES(?,?,?,?)",
#         (i+1,
#         int(departement),
#         FindDepartementName(int(departement)),
#         int(np.where(regions == FindRegionDepartement(df,departement))[0][0]+1)
#         ))


# for i in range(len(communes)):
    
#     cur.execute(
#         "INSERT INTO Communes VALUES(?,?,?,?,?)",
#         (i+1,
#         int(communes[i]),
#         nom_commune[i],
#         df["Consommation annuelle moyenne de la commune (MWh)"].iloc[np.where(df["Code Commune"] == communes[i])[0][0]],
#         int(np.where(departements == FindDepartementCommune(df,communes[i]))[0][0]+1)
#         ))
    

# for i in range(len(adress)):
#     cur.execute(
#         "INSERT INTO Logements VALUES(?,?,?,?)",
#         (i+1,
#         int(np.where(communes == df["Code Commune"][i])[0][0]+1),
#         adress[i],
#         int(nombre_logements[i]))
#     )
 

# for i,conso in enumerate(conso_logement):
#     cur.execute(
#         "INSERT INTO ConsommationParSegmentAnnee VALUES(?,?,?,?,?)",
#         (i+1,
#         int(np.where(annees == df["Année"][i])[0][0])+1,
#         int(np.where(sdcs == df["Segment de client"][i])[0][0])+1,
#         int(np.where(adress == df["Adresse"][i])[0][0])+1,
#         conso
#         )

#     )



con.commit()  


