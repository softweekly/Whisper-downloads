#!/bin/bash
# Video Transcription App - Full Menu (Linux/Mac)
# Menu-driven interface for all features

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check virtual environment
if [ ! -d ".venv" ]; then
    echo -e "${RED}Error: Virtual environment not found!${NC}"
    echo -e "${YELLOW}Please run: python3 -m venv .venv${NC}"
    exit 1
fi

source .venv/bin/activate

while true; do
    clear
    echo ""
    echo "=========================================="
    echo "    Video Transcription Tool"
    echo "    Powered by OpenAI Whisper"
    echo "=========================================="
    echo ""
    echo "Choose an option:"
    echo ""
    echo "1. Interactive Mode (Recommended)"
    echo "2. Command Line Help"
    echo "3. Batch Processing"
    echo "4. YouTube Channel Transcriber"
    echo "5. View Demo/Examples"
    echo "6. Run System Test"
    echo "7. Exit"
    echo ""
    read -p "Enter your choice (1-7): " choice
    
    case $choice in
        1)
            echo ""
            echo -e "${GREEN}Starting Interactive Mode...${NC}"
            python interactive_transcriber.py
            ;;
        2)
            echo ""
            python video_transcriber.py --help
            ;;
        3)
            echo ""
            echo -e "${GREEN}Starting Batch Processing...${NC}"
            python batch_transcriber.py
            ;;
        4)
            echo ""
            echo -e "${GREEN}Starting YouTube Channel Transcriber...${NC}"
            python youtube_channel_transcriber.py
            ;;
        5)
            echo ""
            python demo.py
            ;;
        6)
            echo ""
            echo -e "${GREEN}Running System Test...${NC}"
            python test_system_full.py
            ;;
        7)
            echo ""
            echo -e "${GREEN}Goodbye!${NC}"
            exit 0
            ;;
        *)
            echo ""
            echo -e "${RED}Invalid choice. Please try again.${NC}"
            ;;
    esac
    
    echo ""
    read -p "Press Enter to continue..."
done