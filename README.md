# Statistiques d'impact

Ce site répertorie les produits opérés par l'Opérateur de Produits Interministériels (OPI), ainsi que leurs statistiques d'impact.

## Imports automatiques

Le but principal de ce repo est d'organiser le "prélèvement" automatique des statistiques d'usage des différents produits de l'OPI. 

## Importer des valeurs passées

Pour les produits pour lesquels l'automatisation n'est pas encore mise en place, ou pour importer des données passées, des fichiers d'export nous sont parfois transmis. 

Pour importer dans la base de données des mesures contenues dans un fichier `.csv` ou `.json` sur votre ordinateur:

``` bash
# créer l'environnement, s'y déplacer et y installer les packages nécessaires (la première fois)
python -m venv venv
source venv/bin/activate
pip install requests | pip install pandas | pip install argparse 

# se connecter à l'environnement (toutes les autres fois)
source venv/bin/activate

# Executer le script
python src/scripts/importStats/import_stock.py <chemin_vers_votre_fichier>
```

Le script s'executera et ses logs contiendront:
- les données ajoutées
- les données non ajoutées mais concordantes avec l'existant
- les données non ajoutées car discordantes avec l'existant
