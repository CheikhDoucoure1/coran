#!/bin/bash
# Script d'installation et de démarrage - Coran Sénégal
set -e

echo "============================================="
echo "  Coran Sénégal - Installation"
echo "============================================="

# Créer et activer l'environnement virtuel
echo ""
echo "→ Création de l'environnement virtuel..."
python3 -m venv venv
source venv/bin/activate

# Installer les dépendances
echo ""
echo "→ Installation des dépendances..."
pip install -r requirements.txt

# Migrations
echo ""
echo "→ Application des migrations..."
python manage.py migrate

# Charger les fixtures
echo ""
echo "→ Chargement des données de base..."
python manage.py loaddata fixtures/niveaux_scolaires.json
python manage.py loaddata fixtures/sourates_base.json

# Données de démonstration
echo ""
echo "→ Création des utilisateurs de démonstration..."
python manage.py initialiser_donnees

# Charger les versets des sourates de base
echo ""
echo "→ Chargement des versets..."
python manage.py charger_versets

# Collecter les fichiers statiques
echo ""
echo "→ Collecte des fichiers statiques..."
python manage.py collectstatic --noinput

echo ""
echo "============================================="
echo "  Installation terminée avec succès !"
echo "============================================="
echo ""
echo "Pour démarrer l'application :"
echo "  source venv/bin/activate"
echo "  python manage.py runserver"
echo ""
echo "Accès : http://127.0.0.1:8000/"
echo ""
echo "Comptes :"
echo "  Admin      : admin / admin123"
echo "  Enseignant : enseignant1 / demo1234"
echo "  Élève      : eleve1 / demo1234"
echo ""
echo "API REST : http://127.0.0.1:8000/api/"
echo "API Docs : http://127.0.0.1:8000/api/docs/"
echo "Admin    : http://127.0.0.1:8000/admin/"
