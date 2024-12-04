from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.db.database import Base, get_db
from app.models.datasasia import Datasasia
from fastapi.testclient import TestClient
from app.main import app

# Configuration pour la base de données
DATABASE_URL = "mysql+pymysql://freedb_simplon13:MyjK%40J33Hf%23zR7S@sql.freedb.tech/freedb_datasasia"
engine = create_engine(DATABASE_URL, pool_pre_ping=True)  # pool_pre_ping pour éviter les connexions cassées
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Fonction pour initialiser la base de données pour les tests
def init_db():
    try:
        # Crée les tables si elles n'existent pas encore
        Base.metadata.create_all(bind=engine)
        print("Tables créées avec succès.")
    except Exception as e:
        print(f"Erreur lors de l'initialisation de la base de données : {e}")

# Fonction pour tester les routes FastAPI
def test_routes():
    # Remplace la dépendance `get_db` pour utiliser la session actuelle
    def override_get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    client = TestClient(app)

    # Test : Créer une nouvelle entrée
    response = client.post(
        "/datasasia",
        json={
            "adresse": "123 rue Exemple",
            "annee": 2022,
            "code_commune": 12345,
            "nom_commune": "Commune Exemple",
            "segment_de_client": "Résidentiel",
            "code_departement": 75,
            "code_region": 11,
            "nombre_de_logements": 10,
            "consommation_annuelle_totale": 100.0,
            "consommation_annuelle_moyenne_par_logement": 10.0,
            "consommation_annuelle_moyenne_commune": 50.0
        }
    )
    assert response.status_code == 200
    print("POST /datasasia : OK")

    # Récupérer l'ID de la nouvelle entrée
    data_id = response.json()["id"]

    # Test : Récupérer toutes les données
    response = client.get("/datasasia")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    print("GET /datasasia : OK")

    # Test : Récupérer une entrée spécifique
    response = client.get(f"/datasasia/{data_id}")
    assert response.status_code == 200
    print(f"GET /datasasia/{data_id} : OK")

    # Test : Supprimer une entrée
    response = client.delete(f"/datasasia/{data_id}")
    assert response.status_code == 200
    print(f"DELETE /datasasia/{data_id} : OK")

# Initialiser la base et exécuter les tests
if __name__ == "__main__":
    init_db()
    test_routes()
