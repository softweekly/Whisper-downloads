@echo off
REM Simple Video Transcription App Launcher
REM Double-click to start transcribing videos!

title Video Transcription App

echo.
echo ==========================================
echo    Video Transcription App
echo    Powered by OpenAI Whisper
echo ==========================================
echo.
echo Starting Interactive Mode...
echo Choose between local video files or YouTube URLs!
echo.

REM Change to the script directory
cd /d "%~dp0"

REM Activate virtual environment and start interactive mode
".\.venv\Scripts\python.exe" interactive_transcriber.py

echo.
echo Transcription session ended.
pause