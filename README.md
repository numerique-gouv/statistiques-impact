# Statistiques d'usage

Ce site répertorie les produits opérés par l'Opérateur de Produits Interministériels (OPI), ainsi que leurs statistiques d'usage. 

## Installation 

- Clonez le repo et naviguez jusqu'à votre dossier local puis jusqu'au dossier `django/`
- Copier le fichier .env avec `cp .env.example .env` et ajoutez les paramètres de votre postgresql local
- Dans un terminal, préparez votre environnement Python avec les commandes suivantes:
```bash
# installez l'environnement django et activez-le
python -m venv venv
source venv/bin/activate

# installez les packages
pip install -r requirements.txt
```
- Appliquez le schéma de données à la base de données locale avec `python manage.py migrate`

## Lancement

Si nécessaire, réactivez l'environnement avec `source venv/bin/activate` puis exécutez `python manage.py runserver`. 
Votre server local sera joignable à l'url http://127.0.0.1:8000/

