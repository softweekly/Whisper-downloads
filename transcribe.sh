#!/bin/bash
# Video Transcription App - Linux/Mac Launcher
# Easy start script for transcribing videos

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo ""
echo "=========================================="
echo "    Video Transcription App"
echo "    Powered by OpenAI Whisper"
echo "=========================================="
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo -e "${RED}Error: Virtual environment not found!${NC}"
    echo -e "${YELLOW}Please run setup first:${NC}"
    echo "  python3 -m venv .venv"
    echo "  source .venv/bin/activate"
    echo "  pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment
echo -e "${CYAN}Activating virtual environment...${NC}"
source .venv/bin/activate

# Check if required packages are installed
if ! python -c "import whisper" 2>/dev/null; then
    echo -e "${RED}Error: Required packages not installed!${NC}"
    echo -e "${YELLOW}Installing packages...${NC}"
    pip install -r requirements.txt
fi

echo -e "${GREEN}Starting Interactive Mode...${NC}"
echo -e "${CYAN}Choose between local video files or YouTube URLs!${NC}"
echo ""

# Start the interactive transcriber
python interactive_transcriber.py

echo ""
echo -e "${GREEN}Transcription session ended.${NC}"
echo ""
read -p "Press Enter to exit..."