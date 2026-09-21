# Connecteurs et intégrations CimentBuild

## GitHub
Le dépôt source est destiné à GitHub. Toutes les modifications du code doivent rester traçables par commits.

## Hébergement
Render est prévu comme option de déploiement grâce à render.yaml. Le déploiement réel nécessite l'autorisation du compte d'hébergement et la configuration des variables.

## Base de données
PostgreSQL est prévu pour la production. SQLite peut servir au développement local.

## Paiements
Les modes d'interface sont préparés, mais aucun paiement réel n'est activé sans compte marchand et API officiels.

## Notifications
Une future intégration peut utiliser email, SMS ou WhatsApp, mais elle nécessite le fournisseur choisi et ses identifiants officiels.

## Domaine
Un domaine personnalisé peut être relié après déploiement. Le domaine ne doit jamais être inventé.

## Sécurité
Les secrets ne sont jamais stockés dans GitHub. Utiliser les variables d'environnement de l'hébergeur.
