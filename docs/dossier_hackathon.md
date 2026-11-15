# AfriDev Community — Dossier de présentation

**CADEV 2026 · Plateforme communautaire et collaborative des développeurs africains**

> Échanger. Se connecter. Construire.

| | |
|---|---|
| Projet | AfriDev Community |
| Concours | CADEV 2026 |
| Équipe | *[à compléter : noms, rôles et contacts des membres]* |
| Dépôt du code | https://github.com/eliepethuel/CADEV_PROJECT |
| Version présentée | branche `main`, novembre 2026 |
| Démonstration | locale, en une commande Docker (voir §9) |

---

## 1. Résumé

AfriDev Community est une plateforme web qui accompagne les développeurs africains de la
**discussion** jusqu'à l'**opportunité** :

`DISCUSSION → RENCONTRE → ÉQUIPE → PROJET → RÉALISATION → OPPORTUNITÉ`

Un développeur y pose une question technique adaptée à son contexte, trouve des pairs qui
utilisent les mêmes technologies, rejoint ou lance un projet, s'organise avec son équipe sur un
tableau de tâches, puis accède à des opportunités (emplois, stages, bourses, hackathons), à du
mentorat et à des événements.

Le livrable comprend :

- une **API REST** Django complète, testée (509 tests, 97 % de couverture) et documentée (OpenAPI) ;
- une **application web** Next.js animée, responsive et accessible (32 écrans) ;
- une **administration** sur mesure, avec indicateurs en direct et outils de modération ;
- un **environnement de démonstration** reproductible (Docker, comptes et données fictives).

## 2. Le problème

Les développeurs africains sont nombreux, inventifs et de plus en plus connectés, mais leurs
échanges restent dispersés :

- les grands forums internationaux répondent mal aux **contraintes locales** (connexion
  instable, paiement mobile, hébergement, langues, réglementation) ;
- les groupes de messagerie instantanée **ne capitalisent pas** les réponses : la même question
  revient sans cesse et rien n'est cherchable ;
- il est difficile de **trouver des pairs** compétents dans une technologie, un pays ou une
  ville pour **monter une équipe** ;
- les **opportunités** (emplois, stages, bourses, hackathons) circulent de façon informelle,
  sans vérification, ce qui favorise les offres trompeuses ;
- le passage de **l'idée au projet réalisé** manque d'outils simples et gratuits.

## 3. La solution

Une seule plateforme qui relie quatre besoins habituellement séparés.

| Besoin | Réponse d'AfriDev Community |
|---|---|
| **Échanger** | Fil communautaire, questions/réponses avec réponse acceptée, articles, votes, favoris, recherche plein texte en français |
| **Se connecter** | Profils développeurs avec photo, annuaire filtrable (technologie, pays, niveau, disponibilité), abonnements, recommandations, messagerie privée, communautés par pays/ville/université/technologie |
| **Construire** | Appels à collaboration, rôles recherchés, demandes pour rejoindre, espace projet, tableau de tâches en glisser-déposer, jalons et activité |
| **Progresser** | Opportunités vérifiées, mentorat, événements, réputation et badges fondés sur des contributions réelles |

**Ce qui nous distingue**

- **Le parcours complet** : une question peut mener à une rencontre, puis à un projet, puis à
  une opportunité, sans changer d'outil.
- **La confiance** : modération avec journal d'audit, organisations vérifiées, annonces
  relues avant publication, signalement possible partout.
- **Le contexte africain** : pays et villes du continent, technologies locales (paiement
  mobile, etc.), contenu en français, interface légère et responsive.
- **Une réputation honnête** : chaque point est explicable et provient d'une action utile
  (réponse acceptée, contribution à un projet, etc.).

## 4. Public cible

- Développeurs débutants et étudiants qui cherchent de l'aide et un premier projet.
- Développeurs confirmés qui veulent partager, encadrer et recruter des coéquipiers.
- Porteurs de projets et startups qui constituent une équipe.
- Organisations, écoles et partenaires qui publient des opportunités et des événements.
- Modérateurs et administrateurs de la communauté.

## 5. Fonctionnalités livrées

Toutes les exigences **P0 (MVP)** du cahier des charges sont couvertes, ainsi que presque tout
le **P1** et l'ensemble du **P2**.

| Niveau | Couverture | Détail |
|---|---|---|
| P0 — MVP | **14 / 14** | Comptes et récupération, profils, fil, publications, commentaires et réponses, votes, catégories et technologies, recherche, appels à collaboration, demandes pour rejoindre, espace projet, signalement, administration, interface responsive |
| P1 — Important | **13 / 15** | Tout sauf les pièces jointes de projet ; l'interface anglaise est préparée mais pas traduite |
| P2 — Extensions | **10 / 10** | Opportunités, candidatures, organisations vérifiées, mentorat, communautés, événements, messagerie, recommandations, portfolio, e-mails de notification |

### Écrans de l'application web

| Domaine | Écrans |
|---|---|
| Accueil | Héro animé (carte de l'Afrique), statistiques en direct, discussions et projets récents |
| Compte | Inscription avec photo de profil, connexion, mot de passe oublié, réinitialisation, vérification et changement d'adresse e-mail |
| Communauté | Fil, questions, publication, détail avec commentaires/réponses, votes, favoris, signalement |
| Réseau | Annuaire des développeurs, profil public, paramètres du profil et des compétences, messagerie |
| Projets | Liste et recherche, création, page projet, rôles recherchés, demandes, tableau de tâches |
| Progression | Opportunités et candidature, événements et inscription, communautés, mentorat |
| Personnel | Tableau de bord (réputation, activité, recommandations), notifications |
| Modération | File des signalements avec décisions journalisées |

### Administration

L'administration Django a été entièrement repensée (thème Jazzmin personnalisé) :

- page de connexion animée aux couleurs du site ;
- tableau de bord avec indicateurs en direct (membres, publications, projets, signalements et
  annonces à traiter, événements à venir) et courbes d'activité sur 14 jours ;
- actions journalisées : désactiver ou réactiver des comptes, vérifier des organisations,
  publier ou refuser des annonces, traiter des signalements ;
- journal d'audit consultable, non modifiable.

## 6. Expérience utilisateur et design

L'identité « **Nuit & Ocre** » (vert émeraude et ocre sur fond nuit) évoque à la fois la
technologie et le continent.

- **Accueil** : carte de l'Afrique en matrice de points ; des villes pulsent et des arcs
  lumineux relient les développeurs. Titre révélé mot par mot, compteurs animés, bandeau de
  technologies, frise du parcours pilotée par le défilement.
- **Micro-interactions** : vote avec rebond, favori avec gerbe de particules, boutons
  magnétiques, cartes avec halo qui suit le curseur, apparitions en cascade, transitions de page.
- **Tableau de tâches** : glisser-déposer avec mise à jour immédiate et retour arrière
  automatique si l'action est refusée.
- **Accessibilité** : navigation au clavier, libellés pour les lecteurs d'écran, contrastes
  adaptés, respect du réglage système « réduire les animations ».
- **Responsive** : chaque écran est utilisable sur mobile.

## 7. Architecture technique

```
┌──────────────────────────┐   HTTPS / JSON    ┌───────────────────────────┐
│ Application web Next.js  │ ────────────────▶ │ API REST Django (DRF)     │
│ React 19 · Tailwind 4    │ ◀──────────────── │ 15 modules métier         │
│ Motion (animations)      │  JWT + cookie     │ OpenAPI / Swagger         │
└──────────────────────────┘   HttpOnly        └─────────────┬─────────────┘
                                                             │
                     ┌────────────────────────┐   ┌──────────▼──────────────┐
                     │ Administration Jazzmin │──▶│ PostgreSQL 16           │
                     │ (staff, modération)    │   │ recherche plein texte   │
                     └────────────────────────┘   └─────────────────────────┘
```

| Couche | Choix |
|---|---|
| Backend | Python 3.12, Django 5.2 LTS, Django REST Framework 3.18 |
| Base de données | PostgreSQL 16 : recherche plein texte en français sans accents, trigrammes |
| Authentification | JWT : jeton d'accès en mémoire (15 min), jeton de rafraîchissement en cookie `HttpOnly` avec rotation et liste noire |
| Frontend | Next.js 16 (App Router), React 19, TypeScript, Tailwind CSS 4, Motion |
| Administration | Django Admin + Jazzmin, thème et animations sur mesure |
| Exécution | Docker multi-étapes, utilisateurs non-root, Gunicorn, WhiteNoise |
| Qualité | pytest, Vitest, ruff, ESLint, TypeScript strict, GitHub Actions |

**Organisation du code** : monolithe modulaire, une application par domaine (comptes,
profils, catalogue, communauté, recherche, projets, notifications, réseau, réputation,
opportunités, mentorat, communautés, événements, messagerie, modération). La logique métier
est regroupée dans des services, les lectures complexes dans des sélecteurs, et les vues restent
fines. Les décisions structurantes sont documentées dans `docs/adr/`.

## 8. Sécurité, confidentialité et qualité

**Sécurité**

- Mots de passe hachés, validés par les règles de Django ; jamais stockés en clair.
- Jeton de rafraîchissement inaccessible au JavaScript (cookie `HttpOnly`), contrôle de
  l'origine des requêtes, CORS restreint.
- Permissions vérifiées côté serveur pour chaque action et chaque rôle (membre, auteur, rôles
  de projet, modérateur, administrateur), protections contre l'accès aux objets d'autrui.
- Contenus riches assainis (liste blanche HTML), images contrôlées et réencodées.
- Limites de débit sur la connexion, l'inscription, l'envoi de messages, etc.
- Toutes les décisions de modération et changements de rôle sont journalisés.
- Réglages de production vérifiés par `check --deploy` ; aucun secret dans le dépôt.

**Confidentialité**

- Profil public ou privé, champs masquables (ville, disponibilité, liens, réputation).
- Jamais d'adresse précise ; e-mails jamais exposés publiquement.
- Blocage et signalement dans la messagerie.

**Qualité**

- **509 tests backend**, couverture **97 %** (seuil imposé en CI : 85 %) ; 16 tests frontend.
- Scénarios de bout en bout rejoués via l'API, permissions testées rôle par rôle.
- Intégration continue : lint, migrations, contrôle de déploiement, schéma OpenAPI, tests,
  build du frontend et construction des deux images Docker.

## 9. Démonstration

**Lancer la démo** (prérequis : Docker Desktop) :

```bash
cp .env.example .env
docker compose up --build -d
docker compose exec backend python manage.py seed_demo
```

| Adresse | Contenu |
|---|---|
| http://localhost:3000 | Application web |
| http://localhost:8000/admin/ | Administration |
| http://localhost:8000/api/docs/ | Documentation interactive de l'API |

**Comptes fictifs** (mot de passe commun `Demo-AfriDev-2026`) : `awa_diop` (membre, propriétaire
du projet AgriMarché), `yao_kouassi` (candidat à un projet), `moussa_traore` (propriétaire de
CampusSecure), `demo_moderateur` (modérateur), `demo_admin` (administrateur).

**Scénario conseillé (environ 6 minutes)**

1. **Accueil** : carte animée, statistiques en direct, parcours de la discussion à l'opportunité.
2. **Échanger** : connexion `awa_diop` → fil → question « N+1 » avec réponse acceptée → vote
   et favori.
3. **Se connecter** : annuaire filtré sur React → profil d'un développeur → envoi d'un message.
4. **Construire** : connexion `yao_kouassi` → projet CampusSecure → demande pour rejoindre ;
   connexion `moussa_traore` → acceptation de la demande → tableau de tâches en glisser-déposer.
5. **Progresser** : opportunités (partenaire vérifié, date limite), événements, mentorat,
   tableau de bord personnel avec recommandations.
6. **Confiance** : connexion `demo_moderateur` → file de modération → décision journalisée ;
   administration `demo_admin` → indicateurs en direct et journal d'audit.

## 10. Limites actuelles et feuille de route

**Limites assumées**

- Pas d'envoi d'e-mails réels sans configuration SMTP : en démonstration, les liens
  (vérification, réinitialisation) apparaissent dans les journaux du serveur.
- Pas de temps réel : notifications et messages se rafraîchissent automatiquement à intervalle
  régulier.
- Pièces jointes de projet non livrées ; interface anglaise préparée mais non traduite.
- Pas de déploiement public : la démonstration est locale.

**Prochaines étapes**

- Court terme : traduction anglaise, pièces jointes, mise en ligne sur un hébergeur africain ou
  international, envoi d'e-mails réels.
- Moyen terme : temps réel (WebSocket), application mobile ou PWA hors ligne, connexion avec
  GitHub.
- Long terme : analyse des contributions, validation des compétences par des tests, assistant
  intelligent, statistiques avancées pour les partenaires.

## 11. Impact visé

- **Capitaliser le savoir** : des réponses techniques en français, cherchables et réutilisables.
- **Créer des équipes** : faire émerger des projets entre développeurs de pays différents.
- **Sécuriser l'accès aux opportunités** : annonces relues, organisations vérifiées.
- **Valoriser les talents** : une réputation fondée sur des contributions réelles et visibles.

## 12. Annexes

| Document | Contenu |
|---|---|
| `README.md` | Installation, commandes, variables, couverture des exigences |
| `docs/guide_utilisation.md` | Guide d'utilisation pas à pas |
| `docs/cahier_des_charges.md` | Spécification de référence |
| `docs/api.md` | Guide d'intégration de l'API |
| `docs/moderation.md` | Politique et outils de modération |
| `docs/reputation.md` | Règles de réputation et badges |
| `docs/operations.md` | Déploiement, sauvegarde, restauration |
| `docs/adr/` | Décisions d'architecture |

*Toutes les données de démonstration (personnes, organisations, annonces) sont fictives.*
