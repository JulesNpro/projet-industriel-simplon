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

# Charger le modèle Random Forest (PKL)
MODEL_PATH = "ml\random_forest_model.pkl"  # Remplace par le chemin exact vers ton fichier PKL
try:
    with open(MODEL_PATH, "rb") as file:
        model = pickle.load(file)
        logger.info("Modèle Random Forest chargé avec succès.")
except Exception as e:
    logger.error(f"Erreur lors du chargement du modèle : {e}")
    st.error("Impossible de charger le modèle de prédiction. Vérifiez le fichier PKL.")

# URL de base de l'API FastAPI
API_URL = "http://127.0.0.1:8000"  # Lien vers ton API FastAPI

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

# **Afficher toutes les entrées depuis l'API**
if option == "Afficher toutes les entrées":
    st.header("Toutes les entrées de Datasasia")
    try:
        # Récupération des données depuis l'API
        response = requests.get(f"{API_URL}/datasasia")
        if response.status_code == 200:
            datas = response.json()
            df = pd.DataFrame(datas)
            st.dataframe(df)
            logger.info("Données récupérées avec succès depuis l'API.")
        else:
            st.error(f"Erreur : {response.status_code} - {response.text}")
            logger.error(f"Erreur lors de la récupération des données : {response.text}")
    except Exception as e:
        st.error(f"Erreur de connexion à l'API : {e}")
        logger.exception("Erreur de connexion à l'API lors de la récupération des données.")

# **Afficher une entrée spécifique**
elif option == "Afficher une entrée":
    st.header("Afficher une entrée spécifique")
    datas_id = st.number_input("ID de l'entrée", min_value=1, step=1)
    if st.button("Rechercher"):
        try:
            # Récupération de l'entrée spécifique depuis l'API
            response = requests.get(f"{API_URL}/datasasia/{datas_id}")
            if response.status_code == 200:
                data = response.json()
                st.json(data)
                logger.info(f"Entrée avec ID {datas_id} récupérée avec succès.")
            else:
                st.error(f"Erreur : {response.status_code} - {response.text}")
                logger.error(f"Erreur lors de la récupération de l'entrée {datas_id} : {response.text}")
        except Exception as e:
            st.error(f"Erreur de connexion à l'API : {e}")
            logger.exception(f"Erreur lors de la récupération de l'entrée {datas_id}.")

# **Ajouter une nouvelle entrée**
elif option == "Ajouter une entrée":
    st.header("Ajouter une nouvelle entrée")
    datetime_input = st.text_input("Datetime (format : YYYY-MM-DD HH:MM:SS)")
    temperature = st.number_input("Temperature (°C)", format="%.2f")
    humidity = st.number_input("Humidity (%)", format="%.2f")
    windspeed = st.number_input("WindSpeed (m/s)", format="%.2f")
    general_diffuse_flows = st.number_input("General Diffuse Flows", format="%.2f")
    diffuse_flows = st.number_input("Diffuse Flows", format="%.2f")
    power_consumption_zone1 = st.number_input("Power Consumption Zone 1 (kWh)", format="%.2f")
    power_consumption_zone2 = st.number_input("Power Consumption Zone 2 (kWh)", format="%.2f")
    power_consumption_zone3 = st.number_input("Power Consumption Zone 3 (kWh)", format="%.2f")

    if st.button("Ajouter"):
        data = {
            "datetime": datetime_input,
            "temperature": temperature,
            "humidity": humidity,
            "windspeed": windspeed,
            "general_diffuse_flows": general_diffuse_flows,
            "diffuse_flows": diffuse_flows,
            "power_consumption_zone1": power_consumption_zone1,
            "power_consumption_zone2": power_consumption_zone2,
            "power_consumption_zone3": power_consumption_zone3
        }
        try:
            response = requests.post(f"{API_URL}/datasasia", json=data)
            if response.status_code == 200:
                st.success("Entrée ajoutée avec succès.")
                logger.info("Nouvelle entrée ajoutée avec succès.")
            else:
                st.error(f"Erreur : {response.status_code} - {response.text}")
                logger.error(f"Erreur lors de l'ajout d'une entrée : {response.text}")
        except Exception as e:
            st.error(f"Erreur de connexion à l'API : {e}")
            logger.exception("Erreur lors de l'ajout d'une entrée.")

# **Supprimer une entrée**
elif option == "Supprimer une entrée":
    st.header("Supprimer une entrée")
    datas_id = st.number_input("ID de l'entrée à supprimer", min_value=1, step=1)
    if st.button("Supprimer"):
        try:
            response = requests.delete(f"{API_URL}/datasasia/{datas_id}")
            if response.status_code == 200:
                st.success("Entrée supprimée avec succès.")
                logger.info(f"Entrée avec ID {datas_id} supprimée avec succès.")
            else:
                st.error(f"Erreur : {response.status_code} - {response.text}")
                logger.error(f"Erreur lors de la suppression de l'entrée {datas_id} : {response.text}")
        except Exception as e:
            st.error(f"Erreur de connexion à l'API : {e}")
            logger.exception(f"Erreur lors de la suppression de l'entrée {datas_id}.")

# **Visualisation des données**
elif option == "Visualisations des Données":
    st.header("Visualisations des Données")
    try:
        response = requests.get(f"{API_URL}/datasasia")
        if response.status_code == 200:
            data = pd.DataFrame(response.json())
            st.write("Données récupérées :")
            st.dataframe(data)

            # Graphique de visualisation
            graph_type = st.selectbox(
                "Choisissez un type de graphique",
                ["Histogramme", "Graphique Linéaire"]
            )

            if graph_type == "Histogramme":
                st.subheader("Histogramme des températures")
                fig = px.histogram(data, x="temperature", title="Distribution des températures")
                st.plotly_chart(fig)

            elif graph_type == "Graphique Linéaire":
                st.subheader("Évolution de la consommation Zone 1")
                fig = px.line(data, x="datetime", y="power_consumption_zone1", title="Consommation Zone 1")
                st.plotly_chart(fig)
        else:
            st.error(f"Erreur : {response.status_code} - {response.text}")
            logger.error(f"Erreur lors de la récupération des données pour visualisation : {response.text}")
    except Exception as e:
        st.error(f"Erreur de connexion à l'API : {e}")
        logger.exception("Erreur lors de la visualisation des données.")

# **Prédictions**
elif option == "Prédictions":
    st.header("Prédictions sur la Consommation Énergétique")
    datetime_input = st.date_input("Date", datetime.date.today())
    time_input = st.time_input("Heure", datetime.datetime.now().time())
    temperature = st.number_input("Temperature (°C)", format="%.2f")
    humidity = st.number_input("Humidity (%)", format="%.2f")
    windspeed = st.number_input("WindSpeed (m/s)", format="%.2f")
    general_diffuse_flows = st.number_input("General Diffuse Flows", format="%.2f")
    diffuse_flows = st.number_input("Diffuse Flows", format="%.2f")

    if st.button("Prédire la consommation énergétique"):
        try:
            datetime_combined = datetime.datetime.combine(datetime_input, time_input)
            input_data = pd.DataFrame({
                "datetime": [datetime_combined.strftime("%Y-%m-%d %H:%M:%S")],
                "temperature": [temperature],
                "humidity": [humidity],
                "windspeed": [windspeed],
                "general_diffuse_flows": [general_diffuse_flows],
                "diffuse_flows": [diffuse_flows]
            })
            input_data_model = input_data.drop(columns=["datetime"])
            prediction = model.predict(input_data_model)
            st.success(f"Prédiction : La consommation énergétique prévue est de {prediction[0]:.2f} kWh")
            logger.info(f"Prédiction réussie : {prediction[0]:.2f} kWh")
        except Exception as e:
            st.error(f"Erreur lors de la prédiction : {e}")
            logger.exception("Erreur lors de la prédiction.")
