# Composants tiers et licences

Inventaire à reprendre dans la déclaration de soumission (règlement, article 6 « Composants
tiers »). Les versions sont celles figées dans [`requirements/`](../requirements) et
[`frontend/package-lock.json`](../frontend/package-lock.json).

Le code de l'application (dossiers `backend/` et `frontend/src/`), la carte de l'Afrique
(tracé simplifié réalisé pour le projet) et les données de démonstration (fictives) sont des
créations de l'équipe.

## Point d'attention : pilote PostgreSQL sous LGPL

| Composant | Licence | Rôle |
|---|---|---|
| psycopg 3.3.9 et psycopg-binary 3.3.9 | **LGPL-3.0** | Pilote PostgreSQL utilisé par Django |

Le règlement cite la LGPL parmi les licences à réciprocité. psycopg est utilisé tel quel,
sans modification, comme bibliothèque importée : la LGPL n'impose alors aucune obligation sur
le code de l'application. Django ne propose toutefois aucun pilote PostgreSQL sous licence
permissive (psycopg2 est lui aussi sous LGPL). **Ce point doit être confirmé par écrit auprès
de l'organisateur avant la soumission.** Sans accord, il faudrait changer de moteur de base
de données, ce qui remet en cause la recherche plein texte.

## Backend — composants exécutés en production

| Composant | Version | Licence |
|---|---|---|
| Python | 3.12 | PSF-2.0 |
| Django | 5.2.19 | BSD-3-Clause |
| Django REST Framework | 3.18.3 | BSD-3-Clause |
| djangorestframework-simplejwt | 5.5.1 | MIT |
| PyJWT | 2.15.1 | MIT |
| django-cors-headers | 4.9.0 | MIT |
| django-environ | 0.14.0 | MIT |
| django-filter | 26.2 | BSD-3-Clause |
| drf-spectacular | 0.30.0 | BSD-3-Clause |
| django-jazzmin | 3.0.5 | MIT |
| nh3 | 0.3.7 | MIT |
| Pillow | 13.0.0 | MIT-CMU |
| WhiteNoise | 6.12.0 | MIT |
| Gunicorn | 27.0.1 | MIT |
| psycopg, psycopg-binary | 3.3.9 | LGPL-3.0 (voir ci-dessus) |
| asgiref, sqlparse | 3.13.0, 0.6.1 | BSD-3-Clause |
| inflection, jsonschema, jsonschema-specifications, referencing, rpds-py, attrs, PyYAML | — | MIT |
| uritemplate | 4.2.0 | BSD-3-Clause ou Apache-2.0 |
| packaging | 26.3 | Apache-2.0 ou BSD-2-Clause |
| typing_extensions | 4.16.0 | PSF-2.0 |

Ressources embarquées par Django Admin et Jazzmin : AdminLTE, Bootstrap, Bootswatch, jQuery,
Select2 et XRegExp (MIT) ; Font Awesome Free (icônes CC BY 4.0, polices SIL OFL 1.1, code MIT).

## Frontend — composants livrés au navigateur ou exécutés par le serveur

| Composant | Version | Licence |
|---|---|---|
| Next.js | 16.4.6 | MIT |
| React, React DOM, scheduler | 19.3.1 | MIT |
| Motion (motion, framer-motion, motion-dom, motion-utils) | 14.9.0 | MIT |
| styled-jsx, client-only, @next/env | — | MIT |
| @swc/helpers | 0.5.23 | Apache-2.0 |
| tslib | 2.9.1 | 0BSD |
| Polices Inter et Space Grotesk | — | SIL Open Font License 1.1 |

`sharp` (Apache-2.0) et sa bibliothèque `libvips` (LGPL-3.0) sont une dépendance
**optionnelle** de Next.js pour l'optimisation d'images. L'application ne l'utilise pas :
l'optimiseur est désactivé dans [`next.config.ts`](../frontend/next.config.ts), le paquet est
supprimé pendant la construction de l'image ([`frontend/Dockerfile`](../frontend/Dockerfile))
et il est exclu de la sortie `standalone`. Il n'est donc ni installé ni distribué.

## Outils de développement (non livrés)

| Outil | Licence |
|---|---|
| pytest, pytest-django, pytest-cov, factory_boy, Faker, ruff, pre-commit | MIT ou BSD |
| coverage | Apache-2.0 |
| TypeScript | Apache-2.0 |
| ESLint, eslint-config-next, Vitest, Tailwind CSS, PostCSS | MIT |
| lightningcss (compilation CSS de Tailwind), axe-core (règles d'accessibilité d'ESLint) | MPL-2.0 |
| caniuse-lite (données de compatibilité des navigateurs) | CC BY 4.0 |

Les outils sous MPL-2.0 servent uniquement à la construction et au contrôle du code ; aucun
de leurs fichiers n'est modifié ni livré avec l'application.

## Infrastructure

| Composant | Licence |
|---|---|
| PostgreSQL 16 | Licence PostgreSQL (permissive) |
| Caddy 2 (proxy HTTPS) | Apache-2.0 |
| Node.js 22 | MIT |
| Docker Engine | Apache-2.0 |

## Vérifier l'inventaire

Dépendances Python installées :

```bash
pip install pip-licenses && pip-licenses --format=markdown
```

Dépendances JavaScript : le champ `license` de chaque paquet figure dans
`frontend/package-lock.json`.
