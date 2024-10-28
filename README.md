
![Logo Books Online](https://user.oc-static.com/upload/2020/09/22/1600779540759_Online%20bookstore-01.png)

Books Online

# Extraction des données du site "Books to Scrape"

Ce programme d'extraction est un script Python, exécutable à la demande, visant à récupérer les prix du site [Books to Scrape](http://books.toscrape.com/) au moment de son exécution.

## Caractéristiques du programme

- Récupération des prix, adresse URL et caractéristiques des livres.
- Exportation d'une ou plusieurs catégories de livre.
- Enregistrement des informations des livres au format CSV.
- Date d'enregistrement du fichier CSV reprise dans le nom du fichier.
- Enregistrement de l'image d'illustration de chaque livre au format JPG.

## Installation avec l'environnement virtuel
### 1e étape : Comment créer l'environnement virtuel ?
1. Dans l'__Explorateur de fichiers__, ouvrir votre dossier Windows "__Documents__"
2. Dans la barre d'adresse de la fenêtre __Explorateur de fichiers__ tapez `cmd` à la place de l'adresse `C:\Users\votre_nom\Documents` puis validez par "__Entrée__"
3. Tapez le texte ci-dessous dans l'__invite de commandes__.

```bash
  python -m venv "Scripts Python\Virtual Environment"
```
### 2e étape : Comment activer l'environnement virtuel ?
1. Tapez le texte ci-dessous dans l'__invite de commandes__.

```bash
  "Scripts Python\Virtual Environment\Scripts\activate.bat"
```
### 3e étape : Télécharger les fichiers du programme à partir de GitHub

1. Cliquez sur le bouton en vert nommé "__Code__"
2. Dans le menu déroulant, cliquez sur "__Download ZIP__"
4. Extraire le fichier "__project-2-web-scraping-main.zip__" qui vient d'être téléchargé dans le dossier "__Virtual Environment__"

### 4e étape : Installer les paquets Python

1. Tapez le texte ci-dessous dans l'__invite de commandes__.

```bash
  pip install -r "Scripts Python\Virtual Environment\project-2-web-scraping-main\requirements.txt"
```

>[!NOTE]
>La commande `pip` demande à l'installateur de paquets pour Python d'installer les paquets listés dans le fichier requirements.txt.

## 📖 Utilisation du programme et résultat

### Comment exécuter le script Python sous Windows ?

1. Dans l'__Explorateur de fichiers__, ouvrir votre dossier Windows "__Documents__"
2. Dans la barre d'adresse de la fenêtre __Explorateur de fichiers__ tapez `cmd` à la place de l'adresse `C:\Users\votre_nom\Documents` puis validez par "__Entrée__"
3. Tapez la texte ci-dessous dans l'__invite de commandes__.

```bash
  python "Scripts Python\Virtual Environment\project-2-web-scraping-main\project_web_scraping\WebScraping.py"
```

### Dans quels répertoires sont enregistrés les fichiers CSV et les images ?

- Les fichiers sont classés dans un répertoire nommé "__Books to Scrape__" créé par le script Python sur le bureau Windows.
- Dans ce répertoire "__Books to Scrape__", on trouvera un répertoire par catégorie de livre.
- Dans chaque répertoire "__nom_de_la_catégorie__", on trouvera un répertoire "__images__" et un fichier CSV.

## Exemple d'utilisation et résultat

### Exemple d'utilisation sur les catégories __Biography__ et __Business__

Cet exemple montre comment importer les livres des catégories __Biography__ et __Business__.

**Au démarrage, le script Python affiche une liste des catégories disponibles**

![Screenshot utilisation liste des catégories disponibles](<docs/Use/2024-10-27 15_28_07-C__Windows_System32_cmd.exe - python  project-2-web-scraping-main_project_web_sc.png>)

**Utilisez l'ascenseur de la fenêtre pour afficher les numéros des catégories __Biography__ et __Business__**

![Screenshot utilisation catégories 6 et 7](<docs/Use/2024-10-27 15_59_36-C__Windows_System32_cmd.exe - python  project-2-web-scraping-main_project_web_sc.png>)

**Saisir les deux numéros des catégories 6 et 7 séparés par une virgule**

![Screenshot utilisation saisie des catégories](<docs/Use/2024-10-27 16_03_26-C__Windows_System32_cmd.exe - python  project-2-web-scraping-main_project_web_sc.png>)

**Le script Python affiche un message "Fin du traitement"**

![Screenshot utilisation fin du traitement](<docs/Use/2024-10-27 16_43_01-C__Windows_System32_cmd.exe.png>)

### Exemple de résultat sur les catégories __Biography__ et __Business__
**Les dossiers catégories dans le dossier Books to Scrape**

![Screenshot résultat Dossier Books to Scrape](<docs/Result/2024-10-27 16_49_30-Books to Scrape.png>)

**Dossier de la catégorie des livres Business**

![Screenshot résultat Dossier de la catégorie Business](<docs/Result/2024-10-27 16_50_06-Business.png>)

**Dossier images des livres de la catégorie Business**

![Screenshot résultat Dossier images des livres](<docs/Result/2024-10-27 16_51_50-images.png>)

**Fichier CSV de la catégorie Business ouvert dans Excel**

![Screenshot résultat Fichier CSV ouvert dans Excel](<docs/Result/2024-10-27 16_53_32-2024-10-27 Catégorie Business Information Livres.csv - Excel.png>)

## Liens utiles sur Python

 - [User Guide - pip documentation - Requirements Files](https://pip.pypa.io/en/stable/user_guide/#requirements-files)
 - [Python venv: How To Create, Activate, Deactivate, And Delete](https://python.land/virtual-environments/virtualenv#How_to_create_a_Python_venv)

## Liens utiles sur GitHub

 - [Basic writing and formatting syntax - GitHub Docs](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax)
 - [readme.so](https://readme.so/fr)
