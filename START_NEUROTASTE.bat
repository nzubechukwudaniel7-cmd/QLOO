@echo off
title NeuroTaste Qloo Clinical Console
cd /d "c:\Users\USER\Documents\QLOO"
echo ======================================================================
echo Starting NeuroTaste Qloo Memory Care Agent...
echo Opening in browser: http://localhost:8000
echo ======================================================================
start "" cmd /c "timeout /t 2 /nobreak >nul && start http://localhost:8000"
python run.py
pause
