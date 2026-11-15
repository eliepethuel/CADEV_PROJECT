# Exploitation — déploiement, administrateur, sauvegarde et restauration

Exigences liées : §13.4 (déploiement), §10.2 (sauvegarde avant mise en production réelle).

Pour la mise en ligne sur un serveur (HTTPS, nom de domaine), suivre [deploiement.md](deploiement.md).
Les commandes ci-dessous supposent la pile `docker-compose.yml` (services `db` et `backend`).
Adapter les noms de service ou d'utilisateur PostgreSQL à l'hébergement retenu.

## 1. Mise en service

1. Copier `.env.example` en `.env` et renseigner au minimum `DJANGO_SECRET_KEY` (valeur
   longue et aléatoire), `DJANGO_ALLOWED_HOSTS`, `CORS_ALLOWED_ORIGINS`,
   `CSRF_TRUSTED_ORIGINS`, `FRONTEND_URL` et un mot de passe PostgreSQL fort.
2. Derrière un proxy HTTPS, laisser à leur valeur par défaut `DJANGO_SECURE_SSL_REDIRECT`,
   `DJANGO_SECURE_HSTS_SECONDS`, `DJANGO_COOKIE_SECURE` et `AUTH_COOKIE_SECURE` (les valeurs
   « démo » du `docker-compose.yml` ne servent qu'en HTTP local).
3. Démarrer : `docker compose up --build -d`. Le conteneur attend la base, applique les
   migrations (`migrate`), collecte les fichiers statiques et charge les référentiels
   (`SEED_REFERENCE=1`). **Ne pas activer `SEED_DEMO` en production.**
4. Contrôler : `docker compose exec backend python manage.py check --deploy` puis
   `GET /api/v1/health/` (doit répondre `{"status": "ok", "database": "ok"}`).
5. Planifier les rappels d'événements, par exemple toutes les heures :
   `docker compose exec -T backend python manage.py send_event_reminders`.

Les migrations sont versionnées : à chaque mise à jour, sauvegarder (§3) **avant** de
redémarrer le conteneur, qui applique les nouvelles migrations au démarrage.

## 2. Créer le premier compte administrateur

```bash
docker compose exec backend python manage.py createsuperuser
```

La commande demande nom d'utilisateur, e-mail et mot de passe (politique de robustesse
appliquée). Le compte reçoit le rôle global `ADMIN` ; il donne accès à `/admin/` et aux
endpoints d'administration. Les rôles des autres membres (modérateur, administrateur) se
changent ensuite dans Django Admin, et chaque changement est journalisé (`AuditLog`).

## 3. Sauvegarder

Deux éléments à sauvegarder : la **base PostgreSQL** et les **médias** (avatars, logos).

```bash
make backup
```

équivaut à :

```bash
mkdir -p backups
docker compose exec -T db pg_dump -U afridev -d afridev -Fc > backups/afridev-AAAAMMJJ-HHMM.dump
docker compose cp backend:/app/media backups/media-AAAAMMJJ-HHMM
```

- Le format `-Fc` (archive compressée) permet une restauration sélective avec `pg_restore`.
- Recommandation : sauvegarde quotidienne, conservation de 7 sauvegardes quotidiennes et 4
  hebdomadaires, copie hors du serveur. Le dossier `backups/` n'est jamais versionné.
- Les sauvegardes contiennent des données personnelles : les stocker chiffrées et en accès
  restreint (§10.4).

## 4. Restaurer

**Toujours vérifier une sauvegarde dans une base temporaire avant de restaurer en place.**

Vérification (sans risque pour la base en service) :

```bash
docker compose exec -T db createdb -U afridev afridev_restore_check
docker compose exec -T db pg_restore -U afridev -d afridev_restore_check --no-owner < backups/FICHIER.dump
docker compose exec -T db psql -U afridev -d afridev_restore_check -tAc "select count(*) from accounts_user"
docker compose exec -T db dropdb -U afridev afridev_restore_check
```

Restauration en place (écrase les données actuelles) :

```bash
make restore DUMP=backups/FICHIER.dump
```

équivaut à :

```bash
docker compose stop backend
docker compose exec -T db pg_restore -U afridev -d afridev --clean --if-exists --no-owner < backups/FICHIER.dump
docker compose cp backups/media-AAAAMMJJ-HHMM/. backend:/app/media
docker compose start backend
```

Après restauration : `python manage.py rebuild_search_index` et
`python manage.py recompute_reputation` réalignent l'index de recherche et les scores, puis
contrôler `GET /api/v1/health/`.

Cette procédure a été vérifiée sur la pile Docker locale (sauvegarde, restauration dans une base
temporaire, comparaison du nombre de comptes, suppression de la base temporaire).

## 5. Journaux

En production, les journaux sont émis en JSON sur la sortie standard
(`docker compose logs backend`), sans mot de passe ni jeton : les clés sensibles du contexte
sont masquées par `common.logging.JSONFormatter`.
