@echo off
REM Installation initiale de l'app SP6 (venv + dependances)
cd /d "%~dp0"

IF NOT EXIST venv (
    python -m venv venv
)

call venv\Scripts\activate.bat
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo.
echo Installation terminee. Tu peux maintenant lancer update_and_run_sp6.bat
pause
