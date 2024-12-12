import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app
import streamlit as st
import requests

# URL de base de FastAPI (simulée pour le test)
API_URL = "http://127.0.0.1:8000"

@pytest.fixture
def fastapi_client():
    return TestClient(app)

# Test d'intégration Streamlit ↔ FastAPI
@patch("requests.get")
@patch("requests.post")
@patch("requests.delete")
def test_streamlit_fastapi_integration(mock_delete, mock_post, mock_get, fastapi_client):
    # 1. Mock des endpoints FastAPI
    # Mock GET /datasasia
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = [
        {"id": 1, "adresse": "123 rue Exemple", "annee": 2022, "code_commune": 75056}
    ]

    # Mock POST /datasasia
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {
        "id": 2,
        "adresse": "456 rue Test",
        "annee": 2023,
        "code_commune": 69001
    }

    # Mock DELETE /datasasia/{id}
    mock_delete.return_value.status_code = 200
    mock_delete.return_value.json.return_value = {"message": "Donnée supprimée avec succès"}

    # 2. Simuler une interaction avec Streamlit
    with patch("streamlit.dataframe") as mock_dataframe:
        # Tester l'affichage de toutes les entrées (GET /datasasia)
        response = requests.get(f"{API_URL}/datasasia")
        assert response.status_code == 200
        assert len(response.json()) > 0
        st.dataframe(response.json())
        mock_dataframe.assert_called_once_with(response.json())

    with patch("streamlit.success") as mock_success:
        # Tester l'ajout d'une entrée (POST /datasasia)
        data_to_add = {
            "adresse": "456 rue Test",
            "annee": 2023,
            "code_commune": 69001,
            "nom_commune": "Lyon",
            "segment_de_client": "Résidentiel",
            "code_departement": 69,
            "code_region": 1,
            "nombre_de_logements": 10,
            "consommation_annuelle_totale": 100.0,
            "consommation_annuelle_moyenne_par_logement": 10.0,
            "consommation_annuelle_moyenne_commune": 50.0,
        }
        response = requests.post(f"{API_URL}/datasasia", json=data_to_add)
        assert response.status_code == 200
        st.success("Entrée ajoutée avec succès!")
        mock_success.assert_called_once_with("Entrée ajoutée avec succès!")

    with patch("streamlit.error") as mock_error:
        # Tester la suppression d'une entrée inexistante (DELETE /datasasia/{id})
        mock_delete.return_value.status_code = 404
        response = requests.delete(f"{API_URL}/datasasia/99")  # ID inexistant
        assert response.status_code == 404
        st.error("Erreur : Donnée introuvable")
        mock_error.assert_called_once_with("Erreur : Donnée introuvable")
