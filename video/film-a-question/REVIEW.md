# Film A « Une question qui va loin » — revue

Durée : 46 s · 1920 × 1080 · 30 i/s.

## Images vérifiées (planches de captures)
- 1 s : le continent se dessine en vague ; 4,4 s : la question d'Awa en grand.
- 6,5 s : le flot de messages emporte la question ; 10,2 s : « AfriDev Community » se pose.
- 16,6 s : réponse de Kwame acceptée, pastille « ✓ Résolue » ; 21,3 s : filtre React.
- 24 s : arc Dakar → Accra ; 27,8 s : demande de Kofi acceptée, il rejoint l'équipe.
- 31,6 s : la tâche de Kofi glisse dans « En cours » (dépôt mesuré, compteurs 1 / 2).
- 34,5 s : opportunités ; 39 s : tout le continent relié ; 44,5 s : carte de fin.

## Corrigé pendant la revue
- Avatars sans initiales (règle `.who span` trop large) ; dépôt du tableau des tâches ; texte sous 28 px ;
  interlettrage animé ; première image presque noire.

## Son
- Voix off : Kokoro, voix française Siwis (vitesse 0,95), générée en local. Niveaux mesurés, pas écoutés.
- Pas de musique : le disque de la machine était plein (0 octet libre) et MusicGen n'a pas pu tourner ;
  le modèle téléchargé à moitié a été supprimé. Une musique peut être ajoutée plus tard (piste `<audio>` à 0,14).
- Bruitages fournis par HyperFrames, placés une image après leur action (pic mesuré avec ffmpeg).

## Contrôle
- `hyperframes check` : aucune erreur. Restent des avertissements « line_unread » assumés (flot de messages
  illisible exprès, éléments en transition).
