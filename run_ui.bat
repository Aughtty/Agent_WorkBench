@echo off
setlocal
chcp 65001 >nul
set PYTHONIOENCODING=utf-8
cd /d "%~dp0"
python -m streamlit run ui.py
if errorlevel 1 pause

