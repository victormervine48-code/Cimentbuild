# PROMPT DÉPLOIEMENT CIMENTBUILD
Objectif : mettre CimentBuild en ligne de façon fiable.

Vérifier : dépôt GitHub, branche main, requirements.txt, render.yaml, SECRET_KEY, DEBUG=False, ALLOWED_HOSTS, CSRF_TRUSTED_ORIGINS, PostgreSQL, migrations, collectstatic, gunicorn, HTTPS, domaine et logs.

Ne jamais demander au propriétaire de publier une clé secrète dans le chat. Les secrets vont uniquement dans les variables d'environnement de l'hébergeur.
