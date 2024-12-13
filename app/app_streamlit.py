import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import requests
import logging

# Configuration du logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("streamlit_app.log"),  # Logs dans un fichier
        logging.StreamHandler()  # Logs dans la console
    ]
)
logger = logging.getLogger("streamlit_logger")

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
        "Visualisations des Données",
        "Prédictions"
    ]
)

logger.info(f"Action sélectionnée : {option}")

if option == "Afficher toutes les entrées":
    st.header("Toutes les entrées de Datasasia")
    try:
        response = requests.get(f"{API_URL}/datasasia")
        if response.status_code == 200:
            datas = response.json()
            st.dataframe(pd.DataFrame(datas))
            logger.info("Données récupérées avec succès.")
        else:
            st.error(f"Erreur : {response.status_code} - {response.text}")
            logger.error(f"Erreur lors de la récupération des données : {response.text}")
    except Exception as e:
        st.error(f"Erreur de connexion à l'API : {e}")
        logger.exception("Erreur de connexion à l'API")

elif option == "Afficher une entrée":
    st.header("Afficher une entrée spécifique")
    datas_id = st.number_input("ID de l'entrée", min_value=1, step=1)
    if st.button("Rechercher"):
        try:
            response = requests.get(f"{API_URL}/datasasia/{datas_id}")
            if response.status_code == 200:
                st.write(response.json())
                logger.info(f"Entrée avec ID {datas_id} récupérée avec succès.")
            else:
                st.error(f"Erreur : {response.status_code} - {response.text}")
                logger.error(f"Erreur lors de la récupération de l'entrée {datas_id} : {response.text}")
        except Exception as e:
            st.error(f"Erreur de connexion à l'API : {e}")
            logger.exception(f"Erreur de connexion à l'API lors de la récupération de l'entrée {datas_id}")

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
                logger.info("Nouvelle entrée ajoutée avec succès.")
            else:
                st.error(f"Erreur : {response.status_code} - {response.text}")
                logger.error(f"Erreur lors de l'ajout d'une entrée : {response.text}")
        except Exception as e:
            st.error(f"Erreur de connexion à l'API : {e}")
            logger.exception("Erreur de connexion à l'API lors de l'ajout d'une entrée")

elif option == "Supprimer une entrée":
    st.header("Supprimer une entrée")
    datas_id = st.number_input("ID de l'entrée à supprimer", min_value=1, step=1)
    if st.button("Supprimer"):
        try:
            response = requests.delete(f"{API_URL}/datasasia/{datas_id}")
            if response.status_code == 200:
                st.success("Entrée supprimée avec succès!")
                logger.info(f"Entrée avec ID {datas_id} supprimée avec succès.")
            else:
                st.error(f"Erreur : {response.status_code} - {response.text}")
                logger.error(f"Erreur lors de la suppression de l'entrée {datas_id} : {response.text}")
        except Exception as e:
            st.error(f"Erreur de connexion à l'API : {e}")
            logger.exception(f"Erreur de connexion à l'API lors de la suppression de l'entrée {datas_id}")

elif option == "Visualisations des Données":
    st.header("Visualisations des Données de Consommation Énergétique")
    try:
        response = requests.get(f"{API_URL}/datasasia")
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data)
            st.write("Données récupérées :")
            st.dataframe(df)

            graph_type = st.selectbox(
                "Choisissez un type de graphique",
                ["Histogramme", "Graphique Linéaire", "Graphique en Secteurs", "Nuage de Points"]
            )

            if graph_type == "Histogramme":
                st.subheader("Histogramme de la Consommation Moyenne")
                fig = px.histogram(df, x="consommation_annuelle_moyenne_par_logement", title="Distribution des Consommations Moyennes")
                st.plotly_chart(fig)

            elif graph_type == "Graphique Linéaire":
                st.subheader("Évolution de la Consommation Totale")
                fig = px.line(df, x="annee", y="consommation_annuelle_totale", title="Évolution de la Consommation Totale")
                st.plotly_chart(fig)

            elif graph_type == "Graphique en Secteurs":
                st.subheader("Répartition des Consommations par Segment")
                fig = px.pie(df, names="segment_de_client", values="consommation_annuelle_totale", title="Répartition des Consommations")
                st.plotly_chart(fig)

            elif graph_type == "Nuage de Points":
                st.subheader("Relation entre Logements et Consommation Moyenne")
                fig = px.scatter(df, x="nombre_de_logements", y="consommation_annuelle_moyenne_par_logement", title="Relation Logements vs Consommation")
                st.plotly_chart(fig)

            logger.info("Visualisations affichées avec succès.")
        else:
            st.error(f"Erreur : {response.status_code} - {response.text}")
            logger.error(f"Erreur lors de la récupération des données pour visualisation : {response.text}")
    except Exception as e:
        st.error(f"Erreur de connexion à l'API : {e}")
        logger.exception("Erreur lors de la visualisation des données")

elif option == "Prédictions":
    st.header("Prédictions sur la Consommation Moyenne")
    annee = st.number_input("Année", min_value=1900, max_value=2100, step=1, value=2023)
    nombre_de_logements = st.number_input("Nombre de Logements", min_value=1, step=1, value=10)

    if st.button("Faire une prédiction"):
        input_data = {"Année": annee, "Nombre de Logements": nombre_de_logements}
        try:
            response = requests.post(f"{API_URL}/predict", json=input_data)
            if response.status_code == 200:
                result = response.json()
                st.success(f"Prédiction : {result['prediction']:.2f} kWh")
                logger.info(f"Prédiction effectuée avec succès : {result}")
            else:
                st.error(f"Erreur : {response.status_code} - {response.text}")
                logger.error(f"Erreur lors de la prédiction : {response.text}")
        except Exception as e:
            st.error(f"Erreur de connexion à l'API : {e}")
            logger.exception("Erreur de connexion à l'API lors de la prédiction")
