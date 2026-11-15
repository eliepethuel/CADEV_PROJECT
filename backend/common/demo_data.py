"""Données de démonstration **fictives** (§13.5).

Tous les membres, contenus et projets ci-dessous sont inventés pour la
démonstration ; les profils l'indiquent explicitement dans leur biographie.
"""

DEMO_PASSWORD = "Demo-AfriDev-2026"
DEMO_EMAIL_DOMAIN = "demo.afridev.local"
FICTIONAL_NOTICE = "Profil de démonstration fictif."

# username, nom affiché, rôle, pays, ville, niveau, disponibilité, domaines, langues,
# titre, compétences [(slug techno, niveau, années)], lien GitHub fictif ?
MEMBERS = [
    (
        "demo_admin",
        "Équipe AfriDev",
        "ADMIN",
        "CI",
        "Abidjan",
        "EXPERT",
        "NOT_AVAILABLE",
        ["projets-et-hackathons"],
        ["fr", "en"],
        "Administration de la plateforme",
        [],
        False,
    ),
    (
        "demo_moderateur",
        "Modération AfriDev",
        "MODERATOR",
        "SN",
        "Dakar",
        "ADVANCED",
        "NOT_AVAILABLE",
        ["carriere-formation-et-orientation"],
        ["fr"],
        "Modération communautaire",
        [],
        False,
    ),
    (
        "awa_diop",
        "Awa Diop",
        "MEMBER",
        "SN",
        "Dakar",
        "ADVANCED",
        "OPEN_TO_COLLABORATION",
        ["backend-et-api", "bases-de-donnees"],
        ["fr", "wo", "en"],
        "Développeuse backend Django",
        [
            ("python", "ADVANCED", 5),
            ("django", "ADVANCED", 4),
            ("postgresql", "INTERMEDIATE", 3),
            ("docker", "INTERMEDIATE", 2),
        ],
        True,
    ),
    (
        "kofi_mensah",
        "Kofi Mensah",
        "MEMBER",
        "GH",
        "Accra",
        "ADVANCED",
        "LOOKING_FOR_PROJECT",
        ["frontend-et-uiux", "developpement-web"],
        ["en", "fr"],
        "Développeur frontend React",
        [
            ("react", "ADVANCED", 4),
            ("typescript", "ADVANCED", 3),
            ("nextjs", "INTERMEDIATE", 2),
            ("tailwind-css", "ADVANCED", 2),
        ],
        True,
    ),
    (
        "ines_kabore",
        "Inès Kaboré",
        "MEMBER",
        "BF",
        "Ouagadougou",
        "INTERMEDIATE",
        "OPEN_TO_COLLABORATION",
        ["developpement-mobile"],
        ["fr"],
        "Développeuse mobile Flutter",
        [("flutter", "INTERMEDIATE", 2), ("dart", "INTERMEDIATE", 2), ("figma", "BEGINNER", 1)],
        False,
    ),
    (
        "moussa_traore",
        "Moussa Traoré",
        "MEMBER",
        "ML",
        "Bamako",
        "EXPERT",
        "AVAILABLE_FOR_MENTORING",
        ["reseaux-et-telecommunications", "cybersecurite"],
        ["fr", "bm"],
        "Ingénieur réseaux et sécurité",
        [("cisco", "EXPERT", 9), ("linux", "ADVANCED", 8), ("wireshark", "ADVANCED", 6)],
        False,
    ),
    (
        "amina_bello",
        "Amina Bello",
        "MEMBER",
        "NG",
        "Lagos",
        "ADVANCED",
        "OPEN_TO_COLLABORATION",
        ["data-et-intelligence-artificielle"],
        ["en", "ha"],
        "Data scientist",
        [
            ("python", "ADVANCED", 5),
            ("pandas", "ADVANCED", 4),
            ("scikit-learn", "INTERMEDIATE", 3),
            ("pytorch", "INTERMEDIATE", 2),
        ],
        True,
    ),
    (
        "yao_kouassi",
        "Yao Kouassi",
        "MEMBER",
        "CI",
        "Abidjan",
        "INTERMEDIATE",
        "LOOKING_FOR_PROJECT",
        ["developpement-web"],
        ["fr"],
        "Développeur full-stack Laravel",
        [("php", "INTERMEDIATE", 3), ("laravel", "INTERMEDIATE", 2), ("mysql", "INTERMEDIATE", 3)],
        False,
    ),
    (
        "fatou_ndiaye",
        "Fatou Ndiaye",
        "MEMBER",
        "SN",
        "Saint-Louis",
        "BEGINNER",
        "LOOKING_FOR_PROJECT",
        ["developpement-web"],
        ["fr", "wo"],
        "Étudiante en informatique",
        [("html", "INTERMEDIATE", 1), ("css", "INTERMEDIATE", 1), ("javascript", "BEGINNER", 1)],
        False,
    ),
    (
        "chinedu_okafor",
        "Chinedu Okafor",
        "MEMBER",
        "NG",
        "Abuja",
        "EXPERT",
        "AVAILABLE_FOR_MENTORING",
        ["cloud-et-devops"],
        ["en"],
        "Ingénieur DevOps",
        [
            ("kubernetes", "EXPERT", 6),
            ("docker", "EXPERT", 7),
            ("terraform", "ADVANCED", 4),
            ("aws", "ADVANCED", 5),
        ],
        True,
    ),
    (
        "salma_benali",
        "Salma Benali",
        "MEMBER",
        "MA",
        "Casablanca",
        "ADVANCED",
        "OPEN_TO_COLLABORATION",
        ["frontend-et-uiux"],
        ["fr", "ar", "en"],
        "Designer UI/UX",
        [("figma", "EXPERT", 6), ("css", "ADVANCED", 5)],
        False,
    ),
    (
        "jean_mukendi",
        "Jean Mukendi",
        "MEMBER",
        "CD",
        "Kinshasa",
        "INTERMEDIATE",
        "OPEN_TO_COLLABORATION",
        ["backend-et-api"],
        ["fr", "ln"],
        "Développeur Node.js",
        [("nodejs", "INTERMEDIATE", 3), ("express", "INTERMEDIATE", 2), ("mongodb", "BEGINNER", 1)],
        False,
    ),
    (
        "aicha_toure",
        "Aïcha Touré",
        "MEMBER",
        "GN",
        "Conakry",
        "BEGINNER",
        "LOOKING_FOR_PROJECT",
        ["data-et-intelligence-artificielle"],
        ["fr"],
        "Analyste de données junior",
        [("power-bi", "INTERMEDIATE", 1), ("python", "BEGINNER", 1)],
        False,
    ),
    (
        "tendai_moyo",
        "Tendai Moyo",
        "MEMBER",
        "ZW",
        "Harare",
        "ADVANCED",
        "NOT_AVAILABLE",
        ["developpement-mobile"],
        ["en"],
        "Développeur Android Kotlin",
        [("kotlin", "ADVANCED", 5), ("java", "ADVANCED", 6)],
        False,
    ),
    (
        "mariam_sow",
        "Mariam Sow",
        "MEMBER",
        "MR",
        "Nouakchott",
        "INTERMEDIATE",
        "OPEN_TO_COLLABORATION",
        ["cybersecurite"],
        ["fr", "ar"],
        "Analyste SOC",
        [
            ("kali-linux", "INTERMEDIATE", 2),
            ("burp-suite", "INTERMEDIATE", 2),
            ("linux", "INTERMEDIATE", 3),
        ],
        False,
    ),
    (
        "kwame_asante",
        "Kwame Asante",
        "MEMBER",
        "GH",
        "Kumasi",
        "EXPERT",
        "AVAILABLE_FOR_MENTORING",
        ["backend-et-api", "cloud-et-devops"],
        ["en"],
        "Architecte logiciel Go",
        [("go", "EXPERT", 7), ("postgresql", "ADVANCED", 8), ("redis", "ADVANCED", 5)],
        True,
    ),
    (
        "nadia_rakoto",
        "Nadia Rakoto",
        "MEMBER",
        "MG",
        "Antananarivo",
        "INTERMEDIATE",
        "OPEN_TO_COLLABORATION",
        ["developpement-web", "frontend-et-uiux"],
        ["fr"],
        "Intégratrice Vue.js",
        [("vuejs", "INTERMEDIATE", 2), ("javascript", "INTERMEDIATE", 3)],
        False,
    ),
    (
        "ibrahim_diallo",
        "Ibrahim Diallo",
        "MEMBER",
        "GN",
        "Kankan",
        "BEGINNER",
        "LOOKING_FOR_PROJECT",
        ["systemes-et-logiciels-libres"],
        ["fr", "ff"],
        "Autodidacte Linux",
        [("linux", "BEGINNER", 1), ("bash", "BEGINNER", 1)],
        False,
    ),
    (
        "zainab_hassan",
        "Zainab Hassan",
        "MEMBER",
        "KE",
        "Nairobi",
        "ADVANCED",
        "OPEN_TO_COLLABORATION",
        ["developpement-mobile", "backend-et-api"],
        ["en", "sw"],
        "Développeuse React Native",
        [("react-native", "ADVANCED", 3), ("nodejs", "ADVANCED", 4)],
        True,
    ),
    (
        "olivier_ngoma",
        "Olivier Ngoma",
        "MEMBER",
        "CG",
        "Brazzaville",
        "INTERMEDIATE",
        "NOT_AVAILABLE",
        ["bases-de-donnees"],
        ["fr", "ln"],
        "Administrateur de bases de données",
        [("postgresql", "INTERMEDIATE", 3), ("mysql", "ADVANCED", 5)],
        False,
    ),
    (
        "ama_owusu",
        "Ama Owusu",
        "MEMBER",
        "GH",
        "Tamale",
        "BEGINNER",
        "LOOKING_FOR_PROJECT",
        ["carriere-formation-et-orientation"],
        ["en"],
        "Reconversion vers le développement web",
        [("html", "BEGINNER", 1), ("css", "BEGINNER", 1)],
        False,
    ),
    (
        "spam_demo",
        "Compte de test",
        "MEMBER",
        "",
        "",
        "",
        "NOT_AVAILABLE",
        [],
        ["fr"],
        "Compte fictif servant à démontrer la modération",
        [],
        False,
    ),
]

# (auteur, type, catégorie, titre, contenu, technologies, tags)
POSTS = [
    # Publication signalée de la démo de modération : créée en premier pour rester en bas du fil.
    (
        "spam_demo",
        "DISCUSSION",
        "carriere-formation-et-orientation",
        "Gagnez 500 000 FCFA par jour sans travailler",
        "<p>Contenu de test pour la démonstration de la modération : offre trompeuse fictive.</p>",
        [],
        [],
    ),
    (
        "awa_diop",
        "QUESTION",
        "backend-et-api",
        "Comment éviter les requêtes N+1 dans une API Django REST Framework ?",
        "<p>Ma liste de publications déclenche une requête par auteur. J'utilise un "
        "<code>ModelSerializer</code> imbriqué. Quelle est la bonne approche ?</p>",
        ["django", "python"],
        ["performance"],
    ),
    (
        "fatou_ndiaye",
        "QUESTION",
        "developpement-web",
        "Par où commencer pour apprendre JavaScript après HTML et CSS ?",
        "<p>Je maîtrise les bases de HTML et CSS. Quelles ressources gratuites et quels petits "
        "projets conseillez-vous pour progresser en JavaScript ?</p>",
        ["javascript"],
        ["débutant", "ressources"],
    ),
    (
        "ibrahim_diallo",
        "QUESTION",
        "systemes-et-logiciels-libres",
        "Quelle distribution Linux pour un vieil ordinateur portable ?",
        "<p>J'ai un portable de 2014 avec 4 Go de RAM. Je veux apprendre l'administration "
        "système sans tout ralentir.</p>",
        ["linux"],
        ["débutant"],
    ),
    (
        "yao_kouassi",
        "QUESTION",
        "developpement-web",
        "Intégrer un paiement mobile money dans une application Laravel",
        "<p>Quelles sont les bonnes pratiques pour intégrer un agrégateur de paiement mobile "
        "money (callbacks, idempotence, journalisation) ?</p>",
        ["laravel", "php"],
        ["mobile money", "sécurité"],
    ),
    (
        "kofi_mensah",
        "DISCUSSION",
        "frontend-et-uiux",
        "Concevoir des interfaces légères pour les connexions instables",
        "<p>Partageons nos techniques : chargement progressif, images compressées, "
        "mise en cache, états hors ligne… Qu'est-ce qui marche chez vous ?</p>",
        ["react", "nextjs"],
        ["faible connectivité", "performance"],
    ),
    (
        "chinedu_okafor",
        "ARTICLE",
        "cloud-et-devops",
        "Déployer une application Django avec Docker Compose : guide pas à pas",
        "<h2>Objectif</h2><p>Un déploiement reproductible avec PostgreSQL, Gunicorn et des "
        "variables d'environnement.</p><h2>Étapes</h2><ol><li>Dockerfile multi-étapes</li>"
        "<li>Compose avec healthcheck</li><li>Migrations au démarrage</li></ol>",
        ["docker", "django"],
        ["déploiement", "bonnes pratiques"],
    ),
    (
        "moussa_traore",
        "DISCUSSION",
        "reseaux-et-telecommunications",
        "Retours d'expérience : sécuriser un réseau de campus universitaire",
        "<p>Segmentation VLAN, filtrage, supervision : quelles mesures avez-vous mises en place "
        "avec un budget limité ?</p>",
        ["cisco", "wireshark"],
        ["sécurité"],
    ),
    (
        "amina_bello",
        "DISCUSSION",
        "data-et-intelligence-artificielle",
        "Jeux de données ouverts sur l'agriculture en Afrique de l'Ouest",
        "<p>Je recense des jeux de données ouverts (pluviométrie, rendements, prix des marchés) "
        "pour un projet d'aide à la décision. Vos sources ?</p>",
        ["python", "pandas"],
        ["open source", "ressources"],
    ),
    (
        "demo_moderateur",
        "ANNOUNCEMENT",
        "projets-et-hackathons",
        "Bienvenue sur AfriDev Community : règles de la communauté",
        "<p>Respect, entraide et bienveillance. Signalez tout contenu inapproprié : l'équipe de "
        "modération le traitera.</p>",
        [],
        [],
    ),
    (
        "zainab_hassan",
        "QUESTION",
        "developpement-mobile",
        "React Native ou Flutter pour une application de santé communautaire ?",
        "<p>L'application doit fonctionner hors ligne et sur des téléphones d'entrée de gamme. "
        "Quels critères pour choisir ?</p>",
        ["react-native", "flutter"],
        ["faible connectivité"],
    ),
    (
        "aicha_toure",
        "QUESTION",
        "carriere-formation-et-orientation",
        "Comment préparer un premier entretien technique en data ?",
        "<p>J'ai un entretien pour un stage d'analyste de données. Quelles questions sont "
        "fréquentes et comment m'entraîner ?</p>",
        ["python"],
        ["entretien technique", "stage"],
    ),
]

# (titre de la question, auteur de la réponse, contenu, acceptée ?)
ANSWERS = [
    (
        "Comment éviter les requêtes N+1 dans une API Django REST Framework ?",
        "kwame_asante",
        "<p>Ajoutez <code>select_related('author')</code> pour les clés étrangères et "
        "<code>prefetch_related</code> pour les relations multiples dans le queryset de la vue. "
        "Vérifiez avec <code>django_assert_num_queries</code> dans vos tests.</p>",
        True,
    ),
    (
        "Comment éviter les requêtes N+1 dans une API Django REST Framework ?",
        "chinedu_okafor",
        "<p>Pensez aussi à annoter les compteurs (<code>Count</code>, sous-requêtes) plutôt que "
        "d'appeler <code>.count()</code> dans le sérialiseur.</p>",
        False,
    ),
    (
        "Par où commencer pour apprendre JavaScript après HTML et CSS ?",
        "kofi_mensah",
        "<p>Commencez par manipuler le DOM : une liste de tâches, puis un mini quiz. Ensuite, "
        "apprenez <code>fetch</code> pour appeler une API publique.</p>",
        True,
    ),
    (
        "Par où commencer pour apprendre JavaScript après HTML et CSS ?",
        "nadia_rakoto",
        "<p>La documentation MDN en français est excellente et gratuite. Fixez-vous un petit "
        "projet par semaine.</p>",
        False,
    ),
    (
        "Quelle distribution Linux pour un vieil ordinateur portable ?",
        "moussa_traore",
        "<p>Une distribution légère avec un environnement Xfce fera l'affaire. Installez-la en "
        "ligne de commande pour apprendre davantage.</p>",
        False,
    ),
    (
        "Intégrer un paiement mobile money dans une application Laravel",
        "awa_diop",
        "<p>Traitez chaque callback de façon idempotente (clé unique par transaction), vérifiez "
        "la signature et ne faites jamais confiance au montant envoyé par le client.</p>",
        False,
    ),
    (
        "React Native ou Flutter pour une application de santé communautaire ?",
        "ines_kabore",
        "<p>Flutter donne de bonnes performances sur l'entrée de gamme ; prévoyez une base locale "
        "et une synchronisation différée.</p>",
        False,
    ),
]

# (auteur, publication, contenu)
COMMENTS = [
    (
        "salma_benali",
        "Concevoir des interfaces légères pour les connexions instables",
        "Les squelettes de chargement améliorent beaucoup la perception de vitesse.",
    ),
    (
        "zainab_hassan",
        "Concevoir des interfaces légères pour les connexions instables",
        "Le mode hors ligne avec une file de synchronisation nous a sauvé la mise.",
    ),
    (
        "fatou_ndiaye",
        "Déployer une application Django avec Docker Compose : guide pas à pas",
        "Merci, très clair pour une débutante !",
    ),
    (
        "mariam_sow",
        "Retours d'expérience : sécuriser un réseau de campus universitaire",
        "Avez-vous mis en place un IDS open source ?",
    ),
]

# (propriétaire, nom, résumé, description, problème, objectifs, statut, catégorie,
#  technologies, mode, dépôt, rôles [(nom, description, places, technologies)])
PROJECTS = [
    (
        "awa_diop",
        "AgriMarché",
        "Prix des marchés agricoles en temps réel pour les producteurs",
        "<p>Plateforme qui collecte et diffuse les prix des produits agricoles par SMS et web.</p>",
        "Les producteurs vendent souvent sans connaître les prix des marchés voisins.",
        "Publier une première version web et un service SMS dans trois régions pilotes.",
        "RECRUITING",
        "projets-et-hackathons",
        ["django", "postgresql", "react"],
        "REMOTE",
        "https://github.com/demo-afridev/agrimarche",
        [
            (
                "Développeur·se frontend React",
                "Construire l'interface de consultation.",
                1,
                ["react", "typescript"],
            ),
            ("Designer UI/UX", "Concevoir des écrans simples et accessibles.", 1, ["figma"]),
        ],
    ),
    (
        "chinedu_okafor",
        "SantéLink",
        "Carnet de santé communautaire hors ligne",
        "<p>Application mobile pour les agents de santé communautaire, utilisable sans réseau.</p>",
        "Les données de suivi des patients sont dispersées sur papier.",
        "Prototype mobile hors ligne et tableau de bord de synthèse.",
        "IN_PROGRESS",
        "developpement-mobile",
        ["flutter", "nodejs", "postgresql"],
        "HYBRID",
        "https://github.com/demo-afridev/santelink",
        [("Développeur·se mobile Flutter", "Écrans de saisie hors ligne.", 2, ["flutter"])],
    ),
    (
        "moussa_traore",
        "CampusSecure",
        "Kit d'audit de sécurité pour réseaux de campus",
        "<p>Scripts et guides pour auditer rapidement un réseau universitaire.</p>",
        "Les universités manquent d'outils d'audit adaptés à leurs moyens.",
        "Publier un guide et une boîte à outils open source.",
        "RECRUITING",
        "cybersecurite",
        ["linux", "wireshark", "bash"],
        "REMOTE",
        "https://github.com/demo-afridev/campussecure",
        [("Analyste sécurité", "Rédiger les procédures d'audit.", 1, ["kali-linux"])],
    ),
    (
        "amina_bello",
        "PluvioData",
        "Prévision de pluviométrie pour les petits exploitants",
        "<p>Modèle de prévision à partir de données ouvertes, restitué par messages vocaux.</p>",
        "Les prévisions météo disponibles sont peu adaptées à l'échelle locale.",
        "Entraîner un premier modèle et tester la restitution vocale.",
        "IDEA",
        "data-et-intelligence-artificielle",
        ["python", "pandas", "scikit-learn"],
        "REMOTE",
        "",
        [],
    ),
]

# (projet, candidat, message, décision : ACCEPT / REJECT / PENDING, rôle demandé)
JOIN_REQUESTS = [
    (
        "AgriMarché",
        "kofi_mensah",
        "Je développe en React depuis quatre ans et l'agriculture me tient à cœur.",
        "ACCEPT",
        "Développeur·se frontend React",
    ),
    (
        "AgriMarché",
        "fatou_ndiaye",
        "Je suis étudiante et j'aimerais apprendre en contribuant à l'intégration.",
        "PENDING",
        None,
    ),
    (
        "SantéLink",
        "ines_kabore",
        "J'ai déjà réalisé deux applications Flutter avec synchronisation différée.",
        "ACCEPT",
        "Développeur·se mobile Flutter",
    ),
    (
        "CampusSecure",
        "ibrahim_diallo",
        "Je souhaite découvrir l'audit réseau et documenter les procédures.",
        "REJECT",
        None,
    ),
    (
        "CampusSecure",
        "mariam_sow",
        "Analyste SOC, je peux rédiger les procédures de détection et de réponse.",
        "PENDING",
        "Analyste sécurité",
    ),
]

# (projet, titre, assigné, statut, priorité)
TASKS = [
    ("AgriMarché", "Modéliser les marchés et les produits", "awa_diop", "DONE", "HIGH"),
    ("AgriMarché", "Créer l'API de consultation des prix", "awa_diop", "IN_PROGRESS", "HIGH"),
    ("AgriMarché", "Maquetter la page de consultation", "kofi_mensah", "TODO", "MEDIUM"),
    ("AgriMarché", "Rédiger le guide de contribution", None, "TODO", "LOW"),
    ("SantéLink", "Écran de saisie d'une visite", "ines_kabore", "IN_REVIEW", "HIGH"),
    ("SantéLink", "Synchronisation différée", "chinedu_okafor", "IN_PROGRESS", "HIGH"),
    ("CampusSecure", "Inventaire des outils d'audit", "moussa_traore", "TODO", "MEDIUM"),
]

# (signaleur, type de cible, référence, motif, précisions)
REPORTS = [
    (
        "awa_diop",
        "POST",
        "Gagnez 500 000 FCFA par jour sans travailler",
        "SCAM",
        "Offre trompeuse, probablement une arnaque.",
    ),
    ("kofi_mensah", "POST", "Gagnez 500 000 FCFA par jour sans travailler", "SPAM", ""),
    ("fatou_ndiaye", "PROFILE", "spam_demo", "SPAM", "Compte qui publie des offres douteuses."),
]

# (auteur, membre recommandé, contexte)
RECOMMENDATIONS = [
    (
        "awa_diop",
        "kofi_mensah",
        "Kofi a conçu toute l'interface d'AgriMarché avec rigueur et pédagogie.",
    ),
    (
        "chinedu_okafor",
        "ines_kabore",
        "Inès a livré la saisie hors ligne de SantéLink dans les délais.",
    ),
    (
        "kwame_asante",
        "awa_diop",
        "Awa a revu l'architecture de notre API et amélioré les performances.",
    ),
]

# --- P2 ----------------------------------------------------------------------------

# (nom, site, membre, vérifiée ?)
ORGANIZATIONS = [
    (
        "Fondation Code Afrique (fictive)",
        "https://fondation-code-afrique.example.org",
        "chinedu_okafor",
        True,
    ),
]

# (publieur, organisation ou None, nom libre, type, titre, mode, jours avant la date limite, soumettre ?)
OPPORTUNITIES = [
    (
        "chinedu_okafor",
        "Fondation Code Afrique (fictive)",
        "",
        "SCHOLARSHIP",
        "Bourse de formation cloud pour développeuses (fictive)",
        "REMOTE",
        30,
        True,
    ),
    (
        "chinedu_okafor",
        "Fondation Code Afrique (fictive)",
        "",
        "HACKATHON",
        "Hackathon santé numérique 2026 (fictif)",
        "HYBRID",
        15,
        True,
    ),
    (
        "yao_kouassi",
        None,
        "Agence Web Abidjan (fictive)",
        "INTERNSHIP",
        "Stage développeur Laravel à Abidjan (fictif)",
        "ONSITE",
        20,
        True,
    ),
]

# (mentor, titre, domaines, langues)
MENTORS = [
    (
        "moussa_traore",
        "Réseaux et cybersécurité : du campus à l'entreprise",
        ["reseaux-et-telecommunications", "cybersecurite"],
        ["fr"],
    ),
    (
        "kwame_asante",
        "Architecture backend et performance des API",
        ["backend-et-api"],
        ["en", "fr"],
    ),
    ("chinedu_okafor", "Carrière DevOps et cloud", ["cloud-et-devops"], ["en"]),
]

# (mentoré, mentor, objectif, accepter ?)
MENTORSHIPS = [
    (
        "fatou_ndiaye",
        "kwame_asante",
        "Comprendre comment structurer une API REST propre pour mon projet de fin d'études.",
        True,
    ),
    (
        "ibrahim_diallo",
        "moussa_traore",
        "Préparer une certification réseau et découvrir les métiers de la cybersécurité.",
        False,
    ),
]

# (responsable, nom, type, description, pays, ville, membres)
COMMUNITIES = [
    (
        "awa_diop",
        "Développeurs de Dakar",
        "CITY",
        "Rencontres, entraide et projets entre développeurs de Dakar.",
        "SN",
        "Dakar",
        ["fatou_ndiaye", "kofi_mensah"],
    ),
    (
        "moussa_traore",
        "Cybersécurité Afrique de l'Ouest",
        "DOMAIN",
        "Veille, retours d'expérience et bonnes pratiques de sécurité.",
        "",
        "",
        ["mariam_sow", "ibrahim_diallo"],
    ),
]

# (organisateur, communauté, titre, type, format, jours, inscrits)
EVENTS = [
    (
        "awa_diop",
        "Développeurs de Dakar",
        "Atelier en ligne : une API Django en une soirée",
        "WORKSHOP",
        "ONLINE",
        7,
        ["fatou_ndiaye", "kofi_mensah"],
    ),
    (
        "moussa_traore",
        "Cybersécurité Afrique de l'Ouest",
        "Webinaire : sécuriser un réseau de campus",
        "WEBINAR",
        "ONLINE",
        12,
        ["mariam_sow"],
    ),
]

# (expéditeur, destinataire, message)
CONVERSATIONS = [
    ("kofi_mensah", "awa_diop", "Salut Awa, je regarde l'API d'AgriMarché ce week-end !"),
]
