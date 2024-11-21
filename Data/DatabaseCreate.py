import sqlite3


con = sqlite3.connect("Data/data.db")

cur = con.cursor()

# cur.execute(
#     """
#     CREATE TABLE Annees (
#     ID_Annee INT PRIMARY KEY,
#     Annee INT);
#     """)

# cur.execute(
#     """
#     CREATE TABLE Regions (
#     ID_Region INT PRIMARY KEY,
#     CodeRegion INT,
#     NomRegion VARCHAR
#     );
#     """)



# cur.execute(
#     """
#     CREATE TABLE Departements (
#     ID_Departement INT PRIMARY KEY,
#     CodeDepartement INT,
#     NomDepartement VARCHAR,
#     ID_Region INT,
#     FOREIGN KEY (ID_Region) REFERENCES Regions(ID_Region)
#     );
#     """)

# cur.execute(
#     """
#     CREATE TABLE Communes (
#     ID_Commune INT PRIMARY KEY,
#     CodeCommune INT,
#     NomCommune VARCHAR,
#     ConsommationMoyenneCommune DECIMAL,
#     ID_Departement INT,
#     FOREIGN KEY (ID_Departement) REFERENCES Departements(ID_Departement)
#     );
#     """)



# cur.execute(
#     """
#     CREATE TABLE ClientsSegment (
#     ID_Segment INT PRIMARY KEY,
#     SegmentClient VARCHAR
#     );
#     """)


# cur.execute(
#     """
#     CREATE TABLE Logements (
#     ID_Logement INT PRIMARY KEY,
#     ID_Commune INT,
#     Adresse VARCHAR,
#     NombreLogements INT,
#     FOREIGN KEY (ID_Commune) REFERENCES Communes(ID_Commune)
#     );
#     """
# )

cur.execute(
    """
    CREATE TABLE ConsommationParSegmentAnnee (
    ID_Consommation INT PRIMARY KEY,
    ID_Annee INT,
    ID_Segment INT,
    ID_Logement INT,
    
    ConsommationMoyenneParLogement DECIMAL,   
    
    FOREIGN KEY (ID_Logement) REFERENCES Logements(ID_Logement)
    FOREIGN KEY (ID_Annee) REFERENCES Annees(ID_Annee),
    FOREIGN KEY (ID_Segment) REFERENCES SegmentsClients(ID_Segment)
    );
    """
    )

