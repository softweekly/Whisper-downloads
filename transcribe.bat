@echo off
REM Ultra-simple launcher - double-click to transcribe!

title Transcribe Videos

echo.
echo ==========================================
echo    Video Transcription App
echo ==========================================
echo.
echo QUICK TIP: Place videos in the 'videos_to_transcribe' folder
echo            Then just enter the filename when prompted!
echo.
echo Starting app...
echo.

REM Change to the script directory  
cd /d "%~dp0"

REM Check if virtual environment exists
if not exist ".venv\Scripts\python.exe" (
    echo ERROR: Virtual environment not found!
    echo.
    echo Please run setup first:
    echo   1. Open PowerShell in this folder
    echo   2. Run: python -m venv .venv
    echo   3. Run: .\.venv\Scripts\Activate.ps1
    echo   4. Run: pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

REM Start the interactive transcriber
".\.venv\Scripts\python.exe" interactive_transcriber.py

echo.
pause