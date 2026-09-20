# BTS CIEL – Cours interactif SP6

Ce dépôt public contient un **cours interactif en ligne de commande** pour la Situation professionnelle 6 du BTS CIEL, Bloc 2 (Exploitation et maintenance de réseaux informatiques).

Le script principal `cours_interactif_sp6_bts_ciel.py` propose 4 épisodes alignés avec les missions CNED (RLI, Modbus, Bluetooth, I2C) et pose les questions une par une, en enregistrant les réponses dans un fichier Markdown pour révision.

## Installation rapide

1. Cloner le dépôt sur ta machine :

```bash
git clone https://github.com/Gabawaru/bts-ciel-sp6-interactif.git
cd bts-ciel-sp6-interactif
```

2. (Optionnel) Créer un environnement virtuel Python :

```bash
python -m venv venv
venv\Scripts\Activate.ps1   # Windows PowerShell
```

3. Lancer le cours interactif :

```bash
python cours_interactif_sp6_bts_ciel.py
```

Un fichier `reponses_SP6_<Prénom>_<date>.md` sera créé automatiquement dans le dépôt avec toutes tes réponses.

## Utilisation

- Choisis un épisode (1 à 4) correspondant aux missions :
  - 1 : Hangar et réseaux locaux industriels (RLI)
  - 2 : Protocoles Modbus RTU/TCP
  - 3 : Chat Bluetooth PC ↔ Raspberry Pi
  - 4 : I2C, capteur Si7021 et dashboard Node-RED
- Réponds aux questions à ton rythme.
- Utilise les fichiers de réponses comme carnet de révision ou support pour tes propres fiches.

## Personnalisation

Tu peux modifier directement dans le script :
- les questions,
- les intitulés d'épisodes,
- la façon dont les réponses sont enregistrées (format Markdown, structure, etc.).

Plus tard, ce projet pourra évoluer vers :
- une version web (Flask, FastAPI, Streamlit),
- une intégration avec des scripts techniques (Wireshark, Raspberry Pi, etc.).
