# Vidéos de présentation AfriDev Community

Trois films de présentation (1920 × 1080, 30 i/s, voix off française), réalisés avec
[HyperFrames](https://hyperframes.heygen.com) : du HTML animé avec GSAP, rendu en MP4.
Les trois histoires possibles sont décrites dans [STORYLINES.md](STORYLINES.md).

| Projet | Film | Durée |
|---|---|---|
| [film-a-question](film-a-question) | « Une question qui va loin » : d'une question à Dakar à une équipe entre deux pays | 46 s |
| [film-b-carte](film-b-carte) | « La carte s'allume » : un vol au-dessus du continent, une étape par ville | 35,5 s |
| [film-c-six-mots](film-c-six-mots) | « Six mots » : DISCUSSION → OPPORTUNITÉ, un mot par étape | 37 s |

Chaque projet contient :

- `SPEC.md` : la fiche de réalisation (look, mouvements, plans minutés) ;
- `REVIEW.md` : ce qui a été vérifié image par image ;
- `index.html` : les scènes, la voix off et les bruitages ; `compositions/` : une scène par fichier ;
- `assets/` : voix off (Kokoro, voix Siwis), bruitages, police Space Grotesk, styles de l'interface.

Les écrans montrés reprennent les composants du site et les données de démonstration réelles
(toutes fictives).

## Prévisualiser et rendre

```bash
cd video/film-a-question
npx hyperframes preview      # aperçu interactif dans le navigateur
npx hyperframes check        # contrôle (format, mise en page, lisibilité)
npx hyperframes render --quality delivery -o ../rendus/film-a.mp4
```

Les films rendus (`rendus/`) ne sont pas versionnés.

## Limites

- Pas de musique de fond : à ajouter avec une piste `<audio>` (volume conseillé 0,14 sous la voix).
- Voix de synthèse locale (Kokoro) : une voix enregistrée ou une voix HeyGen sera plus naturelle ;
  remplacer les fichiers `assets/voice/*.wav` et ajuster les instants dans `index.html`.
