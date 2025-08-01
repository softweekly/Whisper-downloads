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
echo 4. YouTube Channel Transcriber (NEW!)
echo 5. YouTube GUI (Easy Interface)
echo 6. View Demo/Examples
echo 7. Quick Test (Basic functionality check)
echo 8. Full System Test (Complete verification)
echo 9. Exit
echo.

set /p choice="Enter your choice (1-9): "

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
    echo Starting YouTube Channel Transcriber...
    ".\.venv\Scripts\python.exe" youtube_channel_transcriber.py
) else if "%choice%"=="5" (
    echo.
    echo Starting YouTube GUI...
    ".\.venv\Scripts\python.exe" youtube_gui.py
) else if "%choice%"=="6" (
    echo.
    echo Showing Demo and Examples...
    ".\.venv\Scripts\python.exe" demo.py
    echo.
    pause
) else if "%choice%"=="7" (
    echo.
    echo Running Quick Test...
    ".\.venv\Scripts\python.exe" quick_test.py
    echo.
    pause
) else if "%choice%"=="8" (
    echo.
    echo Running Full System Test...
    ".\.venv\Scripts\python.exe" test_system_full.py
    echo.
    pause
) else if "%choice%"=="9" (
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
