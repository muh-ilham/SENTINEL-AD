@echo off
title SENTINEL-AD Launcher
echo ============================================================
echo   Menjalankan SENTINEL-AD: TNI AD Cognitive Defense System
echo ============================================================
echo.
call .\.venv\Scripts\activate.bat
streamlit run app.py
pause
