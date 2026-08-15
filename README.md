# Avenir en commun — site de mise en valeur du programme

Site statique (Astro) présentant les mesures du programme *L'Avenir en commun*
(La France insoumise, édition 2025), avec un système de filtres par profils
("Je suis jeune", "Je suis féministe", "Je suis républicain·e", "Je soutiens
les services publics", "Je suis rural·e") pour faire remonter les mesures
clés correspondant à chaque profil.

## Contenu de ce dépôt (état de départ)

```
avenir-en-commun/
├── data/
│   └── mesures.json          # 701 mesures extraites du PDF (généré depuis l'Excel)
├── scripts/
│   └── excel_to_json.py      # Reconvertit l'Excel qualifié en data/mesures.json
├── .github/workflows/
│   └── deploy.yml            # Build + déploiement automatique sur GitHub Pages
├── .gitignore
└── README.md
```

Le dossier `src/` (composants Astro, pages) n'existe pas encore : c'est la
prochaine étape, à construire avec Claude Code (voir plus bas).

## Origine des données

Les mesures ont été extraites du PDF officiel *L'Avenir en commun — Édition
2025* (831 mesures annoncées dans le programme ; 701 lignes retenues ici,
la différence s'expliquant par quelques mesures « chapeau » regroupant
plusieurs points en un seul paragraphe dans le PDF).

Colonnes du fichier Excel source (`avenir_en_commun_mesures.xlsx`, onglet
« Mesures ») :

- `axe` : le chapitre du programme (ex. « Chapitre 1 : Le pouvoir au peuple »)
- `sous_theme` : le sous-thème dans lequel s'inscrit la mesure
- `titre` : la mesure clé « chapeau »
- `texte_complet` : le texte de la mesure (une ligne par puce du PDF)
- `page_pdf` : la page source, pour vérification
- 5 colonnes `filtre_*` : à remplir (oui/non) pour qualifier chaque mesure
  par profil

## Étape 1 — Créer le dépôt GitHub

Tu as déjà un compte GitHub. Deux façons de créer le dépôt :

### Option A — Depuis l'interface GitHub (la plus simple)

1. Va sur [github.com/new](https://github.com/new)
2. Nom du dépôt : `avenir-en-commun` (ou le nom de ton choix)
3. Visibilité : Public (nécessaire pour GitHub Pages gratuit sur un dépôt
   personnel, sauf si tu as GitHub Pro)
4. Ne coche PAS "Add a README" (on a déjà le nôtre)
5. Clique sur "Create repository"
6. GitHub t'affiche des commandes du type :
   ```bash
   git remote add origin https://github.com/TON-PSEUDO/avenir-en-commun.git
   git branch -M main
   git push -u origin main
   ```

### Option B — Avec la commande `gh` (si tu as le GitHub CLI installé)

```bash
gh repo create avenir-en-commun --public --source=. --remote=origin
```

### Ensuite, en local (avec Claude Code ou ton terminal)

```bash
cd avenir-en-commun          # le dossier contenant ce README
git init
git add .
git commit -m "Initialisation du projet : données extraites + workflow de déploiement"
git remote add origin https://github.com/TON-PSEUDO/avenir-en-commun.git
git branch -M main
git push -u origin main
```

## Étape 2 — Activer GitHub Pages

1. Sur GitHub, va dans **Settings → Pages** du dépôt
2. Dans "Build and deployment", choisis la source **GitHub Actions**
   (le workflow `.github/workflows/deploy.yml` est déjà prêt et se
   déclenchera automatiquement dès qu'Astro sera en place et qu'un `npm run
   build` fonctionnera)

## Étape 3 — Construire le site avec Claude Code

Une fois le dépôt en ligne, ouvre le dossier avec Claude Code et demande-lui
de scaffolder le site Astro : structure `src/pages`, `src/components`
(`FilterSelector`, `MesureCard`), lecture de `data/mesures.json`, page
d'accueil avec sélecteur de profils, page de résultats filtrés.

## Étape 4 — Qualifier les mesures par filtre

Dans l'Excel (`avenir_en_commun_mesures.xlsx`), remplir les 5 colonnes
`filtre_*` pour les mesures clés (au minimum), puis relancer :

```bash
python scripts/excel_to_json.py avenir_en_commun_mesures.xlsx
```

pour régénérer `data/mesures.json`, committer et pousser — le site se
redéploie automatiquement.
