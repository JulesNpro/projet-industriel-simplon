import streamlit as st
import pandas as pd
import plotly.express as px
import logging
import pickle
import datetime
import requests

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

# Charger le modèle de prédiction
MODEL_PATH = "ml/modeljose.pkl"  # Chemin vers votre modèle
try:
    with open(MODEL_PATH, "rb") as file:
        model = pickle.load(file)
        logger.info("Modèle chargé avec succès.")
except Exception as e:
    logger.error(f"Erreur lors du chargement du modèle : {e}")
    st.error("Impossible de charger le modèle de prédiction. Vérifiez le fichier PKL.")

# URL de base de l'API FastAPI
API_URL = "http://127.0.0.1:8000"

# Titre de l'application
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

# **Afficher toutes les entrées**
if option == "Afficher toutes les entrées":
    st.header("Toutes les entrées de Datasasia")
    try:
        response = requests.get(f"{API_URL}/datasasia")
        if response.status_code == 200:
            datas = response.json()
            if datas:
                df = pd.DataFrame(datas)
                st.dataframe(df)
                logger.info("Données récupérées et affichées avec succès.")
            else:
                st.warning("Aucune donnée disponible.")
        else:
            st.error(f"Erreur : {response.status_code} - {response.text}")
            logger.error(f"Erreur lors de la récupération des données : {response.text}")
    except Exception as e:
        st.error(f"Erreur de connexion à l'API : {e}")
        logger.exception("Erreur de connexion à l'API.")

# **Afficher une entrée spécifique**
elif option == "Afficher une entrée":
    st.header("Afficher une entrée spécifique")
    datas_id = st.number_input("ID de l'entrée", min_value=1, step=1)
    if st.button("Rechercher"):
        try:
            response = requests.get(f"{API_URL}/datasasia/{datas_id}")
            if response.status_code == 200:
                st.json(response.json())
                logger.info(f"Entrée avec ID {datas_id} récupérée avec succès.")
            else:
                st.error(f"Erreur : {response.status_code} - {response.text}")
                logger.error(f"Erreur lors de la récupération de l'entrée {datas_id} : {response.text}")
        except Exception as e:
            st.error(f"Erreur de connexion à l'API : {e}")
            logger.exception("Erreur de connexion à l'API.")

# **Prédictions sur la consommation énergétique**
elif option == "Prédictions":
    st.header("Prédictions sur la Consommation Énergétique")
    
    # Entrée utilisateur pour les variables nécessaires à la prédiction
    st.subheader("Entrez les données nécessaires pour la prédiction :")
    temperature = st.number_input("Temperature (°C)", format="%.2f")
    humidity = st.number_input("Humidity (%)", format="%.2f")
    windspeed = st.number_input("WindSpeed (m/s)", format="%.2f")
    general_diffuse_flows = st.number_input("General Diffuse Flows", format="%.2f")
    diffuse_flows = st.number_input("Diffuse Flows", format="%.2f")

    # Bouton pour exécuter la prédiction
    if st.button("Faire une prédiction"):
        try:
            # Préparer les données pour le modèle
            input_data = pd.DataFrame({
                "Temperature": [temperature],
                "Humidity": [humidity],
                "WindSpeed": [windspeed],
                "GeneralDiffuseFlows": [general_diffuse_flows],
                "DiffuseFlows": [diffuse_flows]
            })

            # Faire une prédiction
            prediction = model.predict(input_data)

            # Afficher le résultat
            st.success(f"Prédiction : La consommation énergétique prévue est de {prediction[0]:.2f} kWh")
            logger.info(f"Prédiction réussie : {prediction[0]:.2f} kWh")
        except Exception as e:
            st.error(f"Erreur lors de la prédiction : {e}")
            logger.exception("Erreur lors de la prédiction.")
