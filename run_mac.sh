#!/bin/bash
cd "$(dirname "$0")"
pip3 install -r requirements.txt -q
echo "Iniciando servidor em http://localhost:5001"
echo "Pressione Ctrl+C para parar"
python3 app.py
