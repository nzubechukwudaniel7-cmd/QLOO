@echo off
title Push NeuroTaste to GitHub (nzubechukwudaniel7-cmd/QLOO)
cd /d "c:\Users\USER\Documents\QLOO"

echo ======================================================================
echo   NEUROTASTE: AUTOMATED GITHUB REPOSITORY PUSHER
echo   Target: https://github.com/nzubechukwudaniel7-cmd/QLOO
echo ======================================================================
echo.

.\gh.exe auth status >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] One-time GitHub authentication needed.
    echo [!] Opening GitHub in your browser...
    echo.
    .\gh.exe auth login --web -p https --scopes "repo,read:org"
)

echo.
echo [*] Pushing all files, 3D brain engine, rPPG station, and documentation...
python push_repo.py

echo.
echo ======================================================================
echo If the push completed, refresh: https://github.com/nzubechukwudaniel7-cmd/QLOO
echo ======================================================================
pause
