@echo off
cd /d %~dp0
pip install -r requirements.txt
python get_nltk_data.py
pause