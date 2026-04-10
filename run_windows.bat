@echo off
cd /d "%~dp0"
pip install -r requirements.txt -q
echo Iniciando servidor em http://localhost:5001
echo Pressione Ctrl+C para parar
python app.py
pause
