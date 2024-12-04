from sqlalchemy import create_engine, text

# URL de connexion avec encodage des caractères spéciaux
DATABASE_URL = "mysql+pymysql://freedb_simplon13:MyjK%40J33Hf%23zR7S@sql.freedb.tech/freedb_datasasia"

try:
    # Crée une instance de moteur SQLAlchemy
    engine = create_engine(DATABASE_URL)
    with engine.connect() as connection:
        # Utilisez `text()` pour exécuter des commandes SQL brutes
        result = connection.execute(text("SELECT 1"))
        print("La base de données est connectée :", result.scalar())
except Exception as e:
    print("Erreur de connexion :", e)
