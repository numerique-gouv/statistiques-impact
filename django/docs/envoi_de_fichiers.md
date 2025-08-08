# Comment envoyer un fichier pour traitement sur notre API ?

## Pourquoi un envoi de fichiers ?

Certains indicateurs ne sont pas récupérés automatiquement par notre API en début de mois mais générés à partir de fichiers qui nous sont envoyés. C'est notamment le cas des indicateurs de France Transfert. Vous trouverez ci-dessous quelques explications pour configurer vos appels.

## Format d'appel

```bash
curl -L 'http://stats.beta.numerique.gouv.fr/api/products/france-transfert/submission/' 
-H 'Content-Type: text/csv' 
-H 'x-api-key: <votre-clé-secrète>' 
-H 'Content-Disposition: attachment; filename=ip-127-0-0-1_FranceTransfert_2025-07-14_upload_stats.csv' 
-d '@/home/marie/Dev/operateur/statistiques-impact/django/core/tests/api/examples/ip-127-0-0-1_FranceTransfert_2025-07-24_upload_stats.csv'
```

> [!NOTE]   
> Le nom du fichier doit être renseigné à nouveau dans le header `Content-Disposition`.

En cas de succès, l'API renvoie l'indicateur créé. En cas d'erreur, elle renvoie une erreur explicite (notamment en cas de tentative de doublon).