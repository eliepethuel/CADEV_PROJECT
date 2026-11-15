# Mise en ligne

Le règlement impose une solution **déployée et accessible en ligne**. Ce guide met le site,
l'API, l'administration et la base de données en ligne sur **un seul serveur Linux**, avec
HTTPS automatique, grâce à [`docker-compose.prod.yml`](../docker-compose.prod.yml).

```
Internet ──HTTPS──▶ Caddy (ports 80/443)
                      ├─ /api/  /admin/  /static/  /media/ ──▶ API Django (Gunicorn)
                      └─ tout le reste ───────────────────────▶ site Next.js
                                                 API ──▶ PostgreSQL
```

Le site et l'API partagent le même domaine : le cookie de session fonctionne sans réglage
particulier et aucune configuration CORS n'est nécessaire.

## 1. Prérequis

- Un serveur Linux (2 Go de mémoire recommandés) avec une adresse IP publique, ports **80**
  et **443** ouverts.
- Docker et le greffon Compose installés sur ce serveur.
- Un nom de domaine pointant vers l'adresse IP du serveur (enregistrement DNS de type A).
  Sans nom de domaine, utiliser `ADRESSE-IP.sslip.io` (par exemple `203.0.113.10.sslip.io`) :
  ce nom pointe automatiquement vers l'adresse IP indiquée et permet d'obtenir un vrai
  certificat HTTPS.

## 2. Configuration

Sur le serveur :

```bash
git clone https://github.com/eliepethuel/CADEV_PROJECT.git
cd CADEV_PROJECT
cp .env.example .env
```

Renseigner au minimum, dans `.env` :

| Variable | Valeur |
|---|---|
| `DOMAIN` | nom de domaine du site, sans `https://` |
| `DJANGO_SECRET_KEY` | valeur longue et aléatoire : `python3 -c "import secrets; print(secrets.token_urlsafe(64))"` |
| `POSTGRES_PASSWORD` | mot de passe fort pour la base |
| `SEED_DEMO` | `1` pour charger les comptes et contenus de démonstration au démarrage |

Les autres variables de `.env.example` peuvent garder leur valeur. Pour envoyer de vrais
e-mails (vérification d'adresse, mot de passe oublié), renseigner les variables `EMAIL_*`
avec `EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend`.

## 3. Démarrage

```bash
docker compose -f docker-compose.prod.yml up --build -d
```

Le premier démarrage construit les images, applique les migrations, collecte les fichiers
statiques et charge les référentiels. Caddy obtient ensuite le certificat HTTPS (quelques
secondes ; le domaine doit déjà pointer vers le serveur).

Créer le compte administrateur réel :

```bash
docker compose -f docker-compose.prod.yml exec backend python manage.py createsuperuser
```

## 4. Vérification

| Adresse | Résultat attendu |
|---|---|
| `https://DOMAIN/` | page d'accueil |
| `https://DOMAIN/api/v1/health/` | `{"status": "ok", "database": "ok"}` |
| `https://DOMAIN/api/docs/` | documentation interactive de l'API |
| `https://DOMAIN/admin/` | administration |

```bash
docker compose -f docker-compose.prod.yml ps
docker compose -f docker-compose.prod.yml logs -f backend proxy
```

## 5. Mise à jour

```bash
git pull
docker compose -f docker-compose.prod.yml up --build -d
```

Sauvegarder la base avant chaque mise à jour : voir [operations.md](operations.md) (ajouter
`-f docker-compose.prod.yml` aux commandes `docker compose`).

## 6. Utiliser une base PostgreSQL gérée

Pour une base hébergée à part, ajouter dans `.env` :

```bash
PROD_DATABASE_URL=postgres://UTILISATEUR:MOT_DE_PASSE@HOTE:5432/BASE
```

L'API utilise alors cette base ; le service `db` local reste démarré mais inutilisé. La base
doit être en **PostgreSQL 16** et autoriser les extensions `unaccent` et `pg_trgm`, créées par
les migrations (recherche plein texte). Une base gérée seule ne suffit pas à mettre le site
en ligne : il faut toujours un serveur pour exécuter le site et l'API.

## 7. Points de vigilance

- Les comptes de démonstration partagent un mot de passe public : ne laisser `SEED_DEMO=1`
  que pour l'évaluation.
- Les médias (photos de profil) sont stockés dans le volume `media_data` et servis par
  Django ; les inclure dans les sauvegardes.
- Les rappels d'événements demandent une tâche planifiée (cron) :
  `docker compose -f docker-compose.prod.yml exec -T backend python manage.py send_event_reminders`.
- `NEXT_PUBLIC_API_BASE_URL` est figée dans l'image du site : après un changement de
  `DOMAIN`, reconstruire avec `--build`.
