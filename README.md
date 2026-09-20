
## Mode Web (interface stylée)

Tu peux aussi lancer le cours via une **interface web moderne** avec Streamlit.

### Installation des dépendances

Dans le dossier du projet :

```bash
python -m venv venv
venv\Scripts\Activate.ps1   # Windows PowerShell
pip install streamlit
```

### Lancer l'application web

```bash
streamlit run sp6_app.py
```

Cela ouvre une interface dans ton navigateur (localhost) avec :
- choix d'épisode dans la barre latérale,
- champs de texte pour répondre aux questions,
- bouton pour enregistrer tes réponses dans un dossier dédié `SP6_progression_web` dans ton profil utilisateur.

Tu peux garder ta progression même si tu mets à jour le code en faisant un `git pull`, car les fichiers de progression sont enregistrés en dehors du dépôt (dans ton répertoire utilisateur).
