@echo off
REM Ultra-simple launcher - double-click to transcribe!

title Transcribe Videos

REM Change to the script directory  
cd /d "%~dp0"

REM Start the interactive transcriber
".\.venv\Scripts\python.exe" interactive_transcriber.py

pause