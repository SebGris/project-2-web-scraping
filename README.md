
![Logo](https://user.oc-static.com/upload/2020/09/22/1600779540759_Online%20bookstore-01.png)

Books Online

# Extraction des données du site "Books to Scrape"

Ce programme d'extraction est un script Python, exécutable à la demande, visant à récupérer les prix du site [Books to Scrape](http://books.toscrape.com/) au moment de son exécution.

## ❓ Caractéristiques du programme

- Récupération des prix, adresse URL et caractéristiques des livres
- Exportation d'une ou plusieurs catégories de livre
- Enregistrement des informations des livres au format CSV
- Enregistrement de l'image d'illustration de chaque livre au format JPG

## 🤔 Installation

Suiviez les 3 grandes étapes ci-dessous :

### 1e étape : Télécharger les fichiers du programme à partir de GitHub

1. Cliquez sur le bouton en vert nommé "__Code__"
2. Dans le menu déroulant, cliquez sur "__Download ZIP__"
3. Créer un dossier "__Scripts Python__" dans votre dossier Windows "__Documents__"
4. Extraire le fichier "__project-2-web-scraping-main.zip__" qui vient d'être téléchargé dans le dossier "__Scripts Python__"

### 2e étape : Lancer le programme Windows __Invite de commandes__

1. Dans l'__Explorateur de fichiers__, ouvrir le dossier "__Scripts Python__" (précédemment créé dans le dossier "__Documents__")
2. Dans la barre d'adresse de la fenêtre "__Scripts Python__" tapez `cmd` à la place de l'adresse `C:\Users\votre_nom\Documents\Scripts Python` puis validez par "__Entrée__"
3. Une nouvelle fenêtre s'ouvre, c'est l'__invite de commandes__ de Windows
 
### 3e étape : Commande pour installer des paquets Python

1. Tapez le texte ci-dessous dans l'__invite de commandes__.

```bash
  cd project-2-web-scraping-main\project_web_scraping
  pip install -r requirements.txt
```

>[!NOTE]
>La commande `cd` est utilisée pour modifier le répertoire de travail actuel.
>La commande `pip` demande à l'installateur de paquets pour Python d'installer les paquets listés dans le fichier requirements.txt.

## 📖 Utilisation du programme

### Comment exécuter le script Python sous Windows ?

- Dans l'__Explorateur de fichiers__, ouvrir le dossier "project_web_scraping"
- Dans la barre d'adresse de la fenêtre "project_web_scraping" tapez `cmd` à la place de l'adresse "C:\Users\votre_nom\Documents\Scripts Python\project-2-web-scraping-main\project_web_scraping" puis validez par "Entrée"
- Tapez la texte ci-dessous dans l'__invite de commandes__.

```bash
  pip python WebScraping.py
```

## 🧐 Exemple

## 📚 Python - Liens utiles

 - [User Guide - pip documentation - Requirements Files](https://pip.pypa.io/en/stable/user_guide/#requirements-files)

## 📚 GitHub - Liens utiles

 - [Basic writing and formatting syntax - GitHub Docs](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax#footnotes)
 - [readme.so](https://readme.so/fr)