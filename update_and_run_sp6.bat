@echo off
REM Met a jour le projet depuis GitHub et lance la version web de l'app SP6
cd /d "%~dp0"

REM Mise a jour du code depuis GitHub
git pull

REM Activation de l'environnement virtuel
call venv\Scripts\activate.bat

REM Lancement de l'appli Streamlit
python -m streamlit run sp6_app.py
