@echo off

:: Chemin racine où les fichiers seront créés
set BASE_DIR=app

:: Création des dossiers
mkdir %BASE_DIR%
mkdir %BASE_DIR%\api
mkdir %BASE_DIR%\api\v1
mkdir %BASE_DIR%\core
mkdir %BASE_DIR%\db
mkdir %BASE_DIR%\db\migrations
mkdir %BASE_DIR%\models
mkdir %BASE_DIR%\schemas
mkdir %BASE_DIR%\services
mkdir %BASE_DIR%\tests

:: Création des fichiers initiaux
:: Fichiers dans la racine
type nul > %BASE_DIR%\__init__.py
echo "# Point d'entrée de l'application FastAPI" > %BASE_DIR%\main.py
echo "from fastapi import FastAPI" >> %BASE_DIR%\main.py
echo "app = FastAPI()" >> %BASE_DIR%\main.py

:: API
type nul > %BASE_DIR%\api\__init__.py
type nul > %BASE_DIR%\api\v1\__init__.py
echo "# Définition des routes principales" > %BASE_DIR%\api\v1\routes.py
echo "# Autres routes éventuelles" > %BASE_DIR%\api\v1\other.py

:: Core
type nul > %BASE_DIR%\core\__init__.py
echo "# Configuration centrale (ex: DB URL, clés secrètes)" > %BASE_DIR%\core\config.py
echo "# Gestion de la sécurité (auth, JWT, etc.)" > %BASE_DIR%\core\security.py

:: DB
type nul > %BASE_DIR%\db\__init__.py
echo "# Connexion à la base de données avec SQLAlchemy" > %BASE_DIR%\db\database.py

:: Models
type nul > %BASE_DIR%\models\__init__.py
echo "# Modèle pour la table datasasia" > %BASE_DIR%\models\datasasia.py

:: Schemas
type nul > %BASE_DIR%\schemas\__init__.py
echo "# Schéma Pydantic pour la table datasasia" > %BASE_DIR%\schemas\datasasia.py

:: Services
type nul > %BASE_DIR%\services\__init__.py
echo "# Logique métier pour la table datasasia" > %BASE_DIR%\services\datasasia_service.py

:: Tests
type nul > %BASE_DIR%\tests\__init__.py
echo "# Tests des endpoints FastAPI" > %BASE_DIR%\tests\test_main.py
echo "# Tests pour la base de données" > %BASE_DIR%\tests\test_database.py

echo "Structure du dossier 'app/' générée avec succès !"
pause
