@echo off
echo Initializing Git repository...
git init
if %ERRORLEVEL% NEQ 0 (
    echo Error: Git is not installed or not in your PATH.
    pause
    exit /b
)

echo Adding files...
git add .

echo Committing files...
git commit -m "Initial commit: Data Pipeline implementation"

echo Renaming branch to main...
git branch -M main

echo Adding remote origin...
git remote add origin https://github.com/vaibhavgaikwad0072/ml_pipeline.git

echo Pushing to GitHub...
git push -u origin main

echo Done!
pause
