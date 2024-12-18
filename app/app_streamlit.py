import streamlit as st
import pandas as pd
import logging
import joblib
import requests
import os

# Configuration du logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("streamlit_app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("streamlit_logger")

# Chemin vers le modèle de prédiction
MODEL_PATH = "ml/modeljose.pkl"

# Chargement du modèle
try:
    model = joblib.load(MODEL_PATH)
    if not hasattr(model, "predict"):
        raise TypeError("Le modèle chargé n'est pas compatible avec la méthode 'predict'.")
    logger.info("Modèle chargé avec succès.")
except FileNotFoundError:
    st.error("Le fichier du modèle est introuvable. Vérifiez le chemin.")
    logger.error("Le fichier du modèle est introuvable. Vérifiez le chemin.")
    model = None
except Exception as e:
    st.error(f"Erreur lors du chargement du modèle : {e}")
    logger.exception("Erreur lors du chargement du modèle.")
    model = None

# URL de l'API FastAPI
API_URL = "http://127.0.0.1:8000"

# Définir le chemin de l'image Ahmed.jpg
image_url = "https://raw.githubusercontent.com/JulesNpro/hostimage/main/ahmed.jpg"

# Personnalisation de l'interface
st.set_page_config(
    page_title="Datasasia Dashboard",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Titre principal avec style
st.markdown(
    """<div style="text-align: center; margin-bottom: 20px;">
    <h1 style="color: #4CAF50;">Datasasia Dashboard</h1>
    <p style="font-size: 18px;">Gérez vos données et effectuez des prédictions en toute simplicité.</p>
    </div>""",
    unsafe_allow_html=True,
)

# Fonction pour simuler un popup d'image
def display_image_popup():
    st.markdown(
        f"""
        <div style="text-align: center; margin-top: 20px;">
            <img src="{image_url}" 
                 alt="Ahmed" style="width: 300px; height: auto; border: 2px solid #4CAF50; border-radius: 10px;">
        </div>
        """,
        unsafe_allow_html=True
    )

# Barre latérale
st.sidebar.title("Navigation")
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

# Afficher toutes les entrées
if option == "Afficher toutes les entrées":
    st.header("Toutes les entrées de Datasasia")
    try:
        response = requests.get(f"{API_URL}/datasasia")
        if response.status_code == 200:
            datas = response.json()
            if datas:
                df = pd.DataFrame(datas)
                st.dataframe(df, use_container_width=True)
                logger.info("Données récupérées et affichées avec succès.")
            else:
                st.warning("Aucune donnée disponible.")
        else:
            st.error(f"Erreur : {response.status_code} - {response.text}")
            logger.error(f"Erreur lors de la récupération des données : {response.text}")
    except Exception as e:
        st.error(f"Erreur de connexion à l'API : {e}")
        logger.exception("Erreur de connexion à l'API.")

# Afficher une entrée spécifique
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

# Ajouter une nouvelle entrée
elif option == "Ajouter une entrée":
    st.header("Ajouter une nouvelle entrée")
    with st.form("add_entry_form"):
        data_name = st.text_input("Nom")
        data_value = st.number_input("Valeur", format="%.2f")
        submitted = st.form_submit_button("Ajouter")

        if submitted:
            try:
                payload = {"name": data_name, "value": data_value}
                response = requests.post(f"{API_URL}/datasasia", json=payload)
                if response.status_code == 200:
                    st.success("Entrée ajoutée avec succès.")
                    display_image_popup()
                    logger.info("Entrée ajoutée avec succès.")
                else:
                    st.error(f"Erreur : {response.status_code} - {response.text}")
                    logger.error(f"Erreur lors de l'ajout de l'entrée : {response.text}")
            except Exception as e:
                st.error(f"Erreur de connexion à l'API : {e}")
                logger.exception("Erreur de connexion à l'API.")

# Supprimer une entrée
elif option == "Supprimer une entrée":
    st.header("Supprimer une entrée")
    datas_id = st.number_input("ID de l'entrée à supprimer", min_value=1, step=1)
    if st.button("Supprimer"):
        try:
            response = requests.delete(f"{API_URL}/datasasia/{datas_id}")
            if response.status_code == 200:
                st.success("Entrée supprimée avec succès.")
                display_image_popup()
                logger.info("Entrée supprimée avec succès.")
            else:
                st.error(f"Erreur : {response.status_code} - {response.text}")
                logger.error(f"Erreur lors de la suppression de l'entrée {datas_id} : {response.text}")
        except Exception as e:
            st.error(f"Erreur de connexion à l'API : {e}")
            logger.exception("Erreur de connexion à l'API.")

# Prédictions
elif option == "Prédictions":
    st.header("Prédictions sur la Consommation Énergétique")
    if model is not None:
        with st.form("prediction_form"):
            temperature = st.number_input("Temperature (°C)", format="%.2f")
            humidity = st.number_input("Humidity (%)", format="%.2f")
            windspeed = st.number_input("WindSpeed (m/s)", format="%.2f")
            general_diffuse_flows = st.number_input("General Diffuse Flows", format="%.2f")
            diffuse_flows = st.number_input("Diffuse Flows", format="%.2f")

            submitted = st.form_submit_button("Faire une prédiction")

            if submitted:
                try:
                    input_data = pd.DataFrame({
                        "Temperature": [temperature],
                        "Humidity": [humidity],
                        "WindSpeed": [windspeed],
                        "GeneralDiffuseFlows": [general_diffuse_flows],
                        "DiffuseFlows": [diffuse_flows]
                    })

                    prediction = model.predict(input_data)
                    st.success(f"Prédiction réussie : {prediction[0]:.2f} kWh")
                    display_image_popup()
                    logger.info(f"Prédiction réussie : {prediction[0]:.2f} kWh")
                except Exception as e:
                    st.error(f"Erreur lors de la prédiction : {e}")
                    logger.exception("Erreur lors de la prédiction.")
    else:
        st.error("Modèle non disponible pour les prédictions.")
