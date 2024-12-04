import pytest
import requests

API_URL = "http://127.0.0.1:8000"

def test_get_all_entries():
    response = requests.get(f"{API_URL}/datasasia")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_single_entry():
    response = requests.get(f"{API_URL}/datasasia/1")
    if response.status_code == 200:
        data = response.json()
        assert isinstance(data, dict)
        assert "id" in data
    else:
        assert response.status_code == 404  # Assurez-vous que l'ID 1 existe dans la base

def test_add_entry():
    data = {
        "adresse": "Test Adresse",
        "annee": 2022,
        "code_commune": 12345,
        "nom_commune": "Commune Test",
        "segment_de_client": "Résidentiel",
        "code_departement": 75,
        "code_region": 11,
        "nombre_de_logements": 10,
        "consommation_annuelle_totale": 100.0,
        "consommation_annuelle_moyenne_par_logement": 10.0,
        "consommation_annuelle_moyenne_commune": 50.0,
    }
    response = requests.post(f"{API_URL}/datasasia", json=data)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["adresse"] == "Test Adresse"

def test_delete_entry():
    # Créez une entrée pour la tester
    data = {
        "adresse": "Adresse à Supprimer",
        "annee": 2022,
        "code_commune": 12345,
        "nom_commune": "Commune à Supprimer",
        "segment_de_client": "Résidentiel",
        "code_departement": 75,
        "code_region": 11,
        "nombre_de_logements": 10,
        "consommation_annuelle_totale": 100.0,
        "consommation_annuelle_moyenne_par_logement": 10.0,
        "consommation_annuelle_moyenne_commune": 50.0,
    }
    create_response = requests.post(f"{API_URL}/datasasia", json=data)
    entry_id = create_response.json()["id"]

    # Supprimez l'entrée créée
    delete_response = requests.delete(f"{API_URL}/datasasia/{entry_id}")
    assert delete_response.status_code == 200
