@echo off
echo Starting Data Pipeline...

echo Step 1: Crawling...
python src/crawler.py
if %ERRORLEVEL% NEQ 0 (
    echo Crawling failed.
    exit /b %ERRORLEVEL%
)

echo Step 2: Processing...
python src/processor.py
if %ERRORLEVEL% NEQ 0 (
    echo Processing failed.
    exit /b %ERRORLEVEL%
)

echo Step 3: Aggregating...
python src/aggregator.py
if %ERRORLEVEL% NEQ 0 (
    echo Aggregation failed.
    exit /b %ERRORLEVEL%
)

echo Pipeline executed successfully.
pause
