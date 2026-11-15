# Refonte du frontend — notes de travail

Relevé issu d'une revue de l'interface (32 écrans, ordinateur 1440 px et mobile 390 px,
application lancée avec les données de démonstration). À utiliser comme liste de contrôle
pour la refonte, qui partira d'une maquette de référence.

## Cadre de la refonte

- **Ton visé** : professionnel, sobre, élégant ; simple mais vivant. Éviter l'esthétique
  « générée » : lueurs néon, dégradés partout, effets de verre, halos sur chaque carte.
- **Couleurs** : palette harmonieuse et restreinte, une seule couleur d'accent utilisée avec
  parcimonie ; contrastes vérifiés.
- **Typographie** : une police soignée et lisible, hiérarchie nette (titres, corps, légendes).
- **À conserver** : la carte de l'Afrique en matrice de points de la page d'accueil
  (`frontend/src/components/motion/AfricaNetwork.tsx`) et le titre d'accroche.
- **Mouvement** : quelques animations utiles (retour d'action, transitions), pas d'effet
  décoratif permanent ; respecter « réduire les animations ».

## Ce qui fonctionne et doit survivre à la refonte

- Aucun débordement horizontal sur mobile, sur aucun écran.
- Formulaires : libellés reliés aux champs, erreurs affichées sous le champ concerné.
- Navigation au clavier avec focus visible, lien « Aller au contenu ».
- Tableau des tâches : glisser-déposer avec repli par sélecteur de statut (indispensable
  au tactile, où le glisser-déposer natif ne fonctionne pas).
- Page d'accueil : accroche claire, chiffres réels, appels à l'action visibles.

## Défauts à corriger

### Navigation et en-tête

- Les liens « Tableau de bord », « Paramètres du profil » et « Se déconnecter » flottent en
  petit sous l'en-tête. Les regrouper dans un menu ouvert depuis l'avatar.
- Deux boutons « Publier » visibles en même temps sur le fil (en-tête et page).
- Le pied de page remonte au milieu de l'écran sur les pages courtes (tâches, opportunités,
  page 404) : le caler en bas de la fenêtre.
- Pas de fil d'Ariane ni de lien retour homogène sur les pages de détail.

### Listes et filtres

- Sur mobile, les quatre filtres empilés du fil occupent tout le premier écran avant la
  première publication : les replier derrière un bouton « Filtrer ».
- Pagination absente ou peu visible sur les listes longues (annuaire, fil).
- Les cartes de publication se ressemblent toutes ; la hiérarchie entre titre, extrait et
  métadonnées est faible, et les pages intérieures sont visuellement uniformes.

### Textes

- Pluriels entre parenthèses partout : « 0 réponse(s) », « 1 membre(s) », « 4 an(s) »,
  « 1 rôle(s) recherché(s) ». Accorder selon le nombre.
- Dates trop détaillées : « Membre depuis 15 nov. 2026, 15:06 » ; préférer une date seule ou
  une durée relative (« il y a 2 jours »).
- Libellés ambigus au tableau de bord (« Réponses (dont acceptées) » avec un seul chiffre).
- Liens de profil affichés bruts (« github ») au lieu d'un libellé et d'une icône.

### États et retours

- États vides peu engageants (opportunités, messages, colonnes vides du tableau des tâches) :
  ajouter une phrase d'explication et une action.
- Page 404 minimale.
- Photo de profil par défaut à l'inscription : un « ? » dans un grand disque orange.
- Le chiffre « 1 » de la police de titres se lit mal dans les compteurs.

### Données de démonstration

- Trop peu de contenu pour faire vivre certains écrans : une seule tâche dans le tableau du
  projet CampusSecure, deux opportunités, peu de messages. Enrichir `backend/common/demo_data.py`.

## Méthode proposée

1. Fixer les fondations à partir de la maquette : couleurs, typographie, espacements, rayons,
   ombres (variables de `frontend/src/app/globals.css`).
2. Refaire les composants de base (`frontend/src/components/ui/`) puis l'en-tête et le pied
   de page.
3. Reprendre les écrans par ordre d'importance pour la démonstration : accueil, fil,
   publication, annuaire et profil, projets et tâches, puis le reste.
4. Vérifier chaque écran sur mobile et sur ordinateur avant de passer au suivant.
