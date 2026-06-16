@echo off
REM Stock Price Prediction - GitHub Setup Script
REM This script will initialize Git, add files, and prepare for pushing to GitHub

echo.
echo ========================================
echo Stock Price Prediction - GitHub Setup
echo ========================================
echo.

REM Initialize Git repository
echo [1/4] Initializing Git repository...
git init

REM Configure Git (replace with your actual name and email)
echo [2/4] Configuring Git user...
git config user.name "Your Name"
git config user.email "your.email@example.com"

REM Add all files
echo [3/4] Adding files to Git...
git add .

REM Create initial commit
echo [4/4] Creating initial commit...
git commit -m "Initial commit: Stock price prediction app with Streamlit"

REM Rename branch to main
git branch -M main

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Create a new repository on GitHub: https://github.com/new
echo    - Repository name: stock-price-prediction
echo    - Choose "Public"
echo    - Click "Create repository"
echo.
echo 2. Copy the HTTPS URL from GitHub (looks like):
echo    https://github.com/YOUR_USERNAME/stock-price-prediction.git
echo.
echo 3. Run these commands in PowerShell:
echo    git remote add origin [PASTE_YOUR_URL_HERE]
echo    git push -u origin main
echo.
echo 4. Your app will then be deployable to Streamlit Cloud!
echo.
pause
