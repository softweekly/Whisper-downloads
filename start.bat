@echo off
REM Video Transcription Tool Launcher
REM Easy access to all tools

echo.
echo ==========================================
echo    Video Transcription Tool
echo    Powered by OpenAI Whisper
echo ==========================================
echo.
echo Choose an option:
echo.
echo 1. Interactive Mode (Recommended)
echo 2. Command Line Help
echo 3. Batch Processing 
echo 4. View Demo/Examples
echo 5. Exit
echo.

set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" (
    echo.
    echo Starting Interactive Mode...
    ".\.venv\Scripts\python.exe" interactive_transcriber.py
) else if "%choice%"=="2" (
    echo.
    echo Command Line Usage:
    echo.
    ".\.venv\Scripts\python.exe" video_transcriber.py --help
    echo.
    pause
) else if "%choice%"=="3" (
    echo.
    echo Starting Batch Processing...
    ".\.venv\Scripts\python.exe" batch_transcriber.py
) else if "%choice%"=="4" (
    echo.
    echo Showing Demo and Examples...
    ".\.venv\Scripts\python.exe" demo.py
    echo.
    pause
) else if "%choice%"=="5" (
    echo.
    echo Goodbye!
    exit /b
) else (
    echo.
    echo Invalid choice. Please try again.
    pause
    goto :start
)

echo.
echo Press any key to return to menu...
pause >nul
goto :start
