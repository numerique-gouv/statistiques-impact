# Comment envoyer un fichier pour traitement sur notre API ?

## Pourquoi un envoi de fichiers

Certains indicateurs ne sont pas récupérés par les soins de notre API mais sont générés à partir de fichiers qui nous sont envoyés. C'est notamment le cas des indicateurs de France Transfert.

## Format d'appel 

```bash
curl -L 'http://stats.beta.numerique.gouv.fr/api/products/france-transfert/submission/' 
-H 'Content-Type: text/csv' 
-H 'x-api-key: <votre-clé-secrète>' 
-H 'Content-Disposition: attachment; filename=ip-machine1_FranceTransfert_2025-07-14_upload_stats.csv' 
-d '@/home/marie/Dev/operateur/statistiques-impact/django/core/tests/api/examples/ip-machine1_FranceTransfert_2025-07-24_upload_stats.csv'
```

> [!NOTE]   
> Le nom du fichier DOIT être renseigné à nouveau dans le header `Content-Disposition`.
