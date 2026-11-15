# SPEC — Film A « Une question qui va loin »

GOAL:    le jury retient qu'une seule question posée sur AfriDev Community mène à une équipe
         entre deux pays, puis à des opportunités : le parcours entier de la plateforme.
OUTPUT:  HyperFrames, 1920 × 1080, 30 i/s.
TIME:    ≈ 46 s × 30 = ≈ 1 380 images. La voix off (Kokoro, Siwis, vitesse 0,95) est l'horloge :
         chaque plan démarre 0,35 s avant le premier mot de sa ligne.
LOOK:    sol nuit #050b08 avec une grille 48 px à 3,5 % d'opacité qui s'efface vers le bas ;
         encre #e9f2ed, texte secondaire #93a79e ; matière unique : l'interface réelle du site
         (panneaux #0d1813, bordures #1e3029, rayon 24 px) et la carte de l'Afrique en points
         (#3fae86, rayon 0,58 dans un repère 100 × 104).
         Accent émeraude #34d399 sur l'action en cours ; ocre #fbbf24 réservée au fil rouge
         (Dakar, la question d'Awa, l'opportunité) — un seul élément ocre à l'écran à la fois.
         Titres : Space Grotesk 700, 96–132 px, interlettrage −3 % ; corps : Inter 400/700, 28–40 px.
         Profondeur : ombre portée 0 40px 90px rgba(0,0,0,.55) sous l'interface ; pas de grain.
OBJECTS: la carte de la question (vraie carte de publication du fil : pastille « Question » ocre,
         catégorie « Backend et API », titre, technologies en monospace) ; la réponse acceptée de
         Kwame Asante avec ses deux extraits de code ; la carte de profil de Kofi Mensah
         (Accra, React, TypeScript, Next.js) ; la demande pour rejoindre (message réel, rôle
         « Développeur·se frontend React ») ; le tableau des tâches d'AgriMarché (5 colonnes, vraies
         tâches) ; les cartes d'opportunités (titres réels, mentions « fictif » conservées) ;
         un curseur blanc de 64 px ; le monogramme « A » sur carré émeraude.
MOTION:  arrivées expo.out 0,7–0,9 s ; déplacements de caméra power2.inOut 0,6–1,2 s ;
         sorties power3.in, 40 % plus courtes ; décalages : mots 80 ms, cartes 60 ms, points de la
         carte en vague sur 1,4 s. Ressort (damping 0,75) seulement sur les pastilles qui se posent.
         Flou de mouvement 8–14 px sur les mouvements rapides. Un seul mouvement héros par plan.
SHOTS:
  1  0,0–4,6   nuit : le continent se dessine en vague, Dakar s'allume en ocre ; la caméra plonge
               dans Dakar (zoom ×9) et le point devient la carte de la question. VO a01.
  2  4,6–8,2   flot : la carte rapetisse dans une colonne de messages anonymes qui défilent vite ;
               elle est poussée hors champ et s'éteint. VO a02.
  3  8,2–12,0  révélation : le flot se fige, inondation de couleur nuit → interface du site ;
               le mot-symbole « AfriDev Community » se pose mot par mot, la carte de la question
               revient, propre, dans le fil. VO a03.
  4  12,0–17,2 réponse : page de la question ; la réponse de Kwame Asante monte, ses extraits de
               code s'écrivent ; le curseur clique « Accepter cette réponse » ; la pastille
               « ✓ Résolue » se pose (pop). VO a04.
  5  17,2–21,6 recherche : la pastille glisse vers l'annuaire ; le filtre Technologie passe à
               « React » ; les cartes de profils arrivent en cascade. VO a05.
  6  21,6–24,4 Kofi : la carte de Kofi grossit ×1,6 ; un arc ocre file de Dakar à Accra sur une
               mini-carte. VO a06.
  7  24,4–28,6 équipe : la demande de Kofi ; clic sur « Accepter » ; la notification « Demande
               acceptée » ; l'avatar de Kofi rejoint l'équipe d'AgriMarché. VO a07.
  8  28,6–32,6 tâches : tableau d'AgriMarché ; « Maquetter la page de consultation » glisse de
               « À faire » à « En cours », les compteurs changent. VO a08.
  9  32,6–36,4 opportunités : les cartes d'opportunités se rangent, la plus proche s'agrandit avec
               sa date limite. VO a09.
  10 36,4–41,0 apothéose : recul sur la carte entière ; Awa à Dakar, Kofi à Accra, leur arc, puis
               tous les arcs du continent se dessinent et les villes s'allument. VO a10.
  11 41,0–46,5 fin : le monogramme se remplit, « AfriDev. » s'écrit, la frise DISCUSSION →
               OPPORTUNITÉ se trace ; « CADEV 2026 » tient 2,5 s. VO a11.
BANNED:  vide sombre avec petits éléments flottants au centre ; halos et particules décoratifs ;
         dégradés violets ; trois cartes alignées en guise de démonstration ; titre sur capture
         assombrie ; logo dans un coin ; tout qui entre en fondu et glisse vers le haut ;
         texte qui bouge pendant la lecture ; boucles « respiration » ; interface inclinée en 3D ;
         chiffres inventés ; tout libellé absent de l'application.
QA:      1,0 (vague de points) · 4,4 (carte de la question en grand) · 7,0 (flot) · 10,5
         (mot-symbole) · 15,5 (pastille Résolue) · 20,5 (profils React) · 23,5 (arc Dakar–Accra)
         · 27,5 (demande acceptée) · 31,5 (carte dans En cours) · 35,5 (opportunités) · 40,0
         (carte illuminée) · 45,5 (carte de fin lisible).
