import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import requests

# URL de base de l'API FastAPI
API_URL = "http://127.0.0.1:8000"  # Endpoint fast api

st.title("Interface Streamlit pour Datasasia")

# Choisir l'action à effectuer
option = st.sidebar.selectbox(
    "Choisissez une action",
    [
        "Afficher toutes les entrées",
        "Afficher une entrée",
        "Ajouter une entrée",
        "Supprimer une entrée",
        "Visualisations des Données"
    ]
)

if option == "Afficher toutes les entrées":
    st.header("Toutes les entrées de Datasasia")
    try:
        response = requests.get(f"{API_URL}/datasasia")
        if response.status_code == 200:
            datas = response.json()
            st.dataframe(pd.DataFrame(datas))
        else:
            st.error(f"Erreur : {response.status_code} - {response.text}")
    except Exception as e:
        st.error(f"Erreur de connexion à l'API : {e}")

elif option == "Afficher une entrée":
    st.header("Afficher une entrée spécifique")
    datas_id = st.number_input("ID de l'entrée", min_value=1, step=1)
    if st.button("Rechercher"):
        try:
            response = requests.get(f"{API_URL}/datasasia/{datas_id}")
            if response.status_code == 200:
                st.write(response.json())
            else:
                st.error(f"Erreur : {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"Erreur de connexion à l'API : {e}")

elif option == "Ajouter une entrée":
    st.header("Ajouter une nouvelle entrée")
    adresse = st.text_input("Adresse")
    annee = st.number_input("Année", min_value=1900, max_value=2100, step=1)
    code_commune = st.number_input("Code Commune", min_value=0, step=1)
    nom_commune = st.text_input("Nom Commune")
    segment_de_client = st.text_input("Segment de Client")
    code_departement = st.number_input("Code Département", min_value=0, step=1)
    code_region = st.number_input("Code Région", min_value=0, step=1)
    nombre_de_logements = st.number_input("Nombre de Logements", min_value=0, step=1)
    consommation_annuelle_totale = st.number_input("Consommation Annuelle Totale")
    consommation_annuelle_moyenne_par_logement = st.number_input("Consommation Moyenne par Logement")
    consommation_annuelle_moyenne_commune = st.number_input("Consommation Moyenne Commune")
    
    if st.button("Ajouter"):
        data = {
            "adresse": adresse,
            "annee": annee,
            "code_commune": code_commune,
            "nom_commune": nom_commune,
            "segment_de_client": segment_de_client,
            "code_departement": code_departement,
            "code_region": code_region,
            "nombre_de_logements": nombre_de_logements,
            "consommation_annuelle_totale": consommation_annuelle_totale,
            "consommation_annuelle_moyenne_par_logement": consommation_annuelle_moyenne_par_logement,
            "consommation_annuelle_moyenne_commune": consommation_annuelle_moyenne_commune,
        }
        try:
            response = requests.post(f"{API_URL}/datasasia", json=data)
            if response.status_code == 200:
                st.success("Entrée ajoutée avec succès!")
            else:
                st.error(f"Erreur : {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"Erreur de connexion à l'API : {e}")

elif option == "Supprimer une entrée":
    st.header("Supprimer une entrée")
    datas_id = st.number_input("ID de l'entrée à supprimer", min_value=1, step=1)
    if st.button("Supprimer"):
        try:
            response = requests.delete(f"{API_URL}/datasasia/{datas_id}")
            if response.status_code == 200:
                st.success("Entrée supprimée avec succès!")
            else:
                st.error(f"Erreur : {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"Erreur de connexion à l'API : {e}")

elif option == "Visualisations des Données":
    st.header("Visualisations des Données de Consommation Énergétique")

    # Exemple de données pour les graphiques
    data = {
        "Année": [2015, 2016, 2017, 2018, 2019, 2020],
        "Consommation Totale (kWh)": [200, 220, 230, 250, 270, 300],
        "Consommation Moyenne par Logement": [120, 140, 150, 200, 240, 300],
        "Nombre de Logements": [10, 20, 30, 40, 50, 60],
        "Nom Commune": ["Paris", "Lyon", "Marseille", "Toulouse", "Nice", "Nantes"],
        "Segment": ["Résidentiel", "Commercial", "Industriel", "Agricole", "Résidentiel", "Commercial"],
    }

    df = pd.DataFrame(data)

    # Sélection du graphique
    graph_type = st.selectbox(
        "Choisissez un type de graphique",
        ["Histogramme", "Graphique Linéaire", "Graphique en Secteurs", "Nuage de Points"]
    )

    # Histogramme
    if graph_type == "Histogramme":
        st.subheader("Histogramme de la Consommation Moyenne")
        fig = px.histogram(
            df,
            x="Consommation Moyenne par Logement",
            nbins=5,
            title="Distribution des Consommations Moyennes",
            labels={"Consommation Moyenne par Logement": "Consommation Moyenne (kWh)"},
        )
        st.plotly_chart(fig)

    # Graphique linéaire
    elif graph_type == "Graphique Linéaire":
        st.subheader("Évolution de la Consommation Totale")
        fig, ax = plt.subplots()
        ax.plot(df["Année"], df["Consommation Totale (kWh)"], marker="o", linestyle="-")
        ax.set_title("Évolution de la Consommation Totale")
        ax.set_xlabel("Année")
        ax.set_ylabel("Consommation Totale (kWh)")
        st.pyplot(fig)

    # Graphique en secteurs
    elif graph_type == "Graphique en Secteurs":
        st.subheader("Répartition de la Consommation par Segment")
        segment_data = {
            "Segment": ["Résidentiel", "Commercial", "Industriel", "Agricole"],
            "Consommation Totale": [500, 300, 150, 50],
        }
        segment_df = pd.DataFrame(segment_data)
        fig = px.pie(
            segment_df,
            names="Segment",
            values="Consommation Totale",
            title="Répartition de la Consommation par Segment",
            hole=0.4,  # Donut chart
        )
        st.plotly_chart(fig)

    # Nuage de points
    elif graph_type == "Nuage de Points":
        st.subheader("Relation entre le Nombre de Logements et la Consommation Moyenne")
        fig = px.scatter(
            df,
            x="Nombre de Logements",
            y="Consommation Moyenne par Logement",
            size="Consommation Moyenne par Logement",
            color="Nom Commune",
            title="Relation entre Nombre de Logements et Consommation Moyenne",
            labels={
                "Nombre de Logements": "Nombre de Logements",
                "Consommation Moyenne par Logement": "Consommation Moyenne (kWh)",
            },
        )
        st.plotly_chart(fig)
