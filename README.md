# Statistiques d'impact

Ce site répertorie les produits opérés par l'Opérateur de Produits Interministériels (OPI), ainsi que leurs statistiques d'impact.


## Installation 

- Clonez le repo et naviguez jusqu'à votre dossier local
- Copier le fichier .env avec `cp .env.example .env` et ajoutez les paramètres de votre postgresql local
- Dans un terminal, exécutez ensuite :
```bash
npm install
npm run build
npm run startDev
```

# Lancer les tests

Faites tourner les tests avec 
- `npx jest` pour lancer la suite de test
- `npx jest -- <chemin_vers_un_fichier_de_test>` pour les tests d'un fichier spécifique
