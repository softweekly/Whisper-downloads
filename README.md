# Video Transcription Tool with Keyword Search

A powerful Python tool that uses OpenAI Whisper to transcribe videos and search for keywords with timestamps. Perfect for analyzing meeting recordings, lectures, interviews, and any video content.

## Features

- 🎥 **Video Transcription**: Convert any video to text using OpenAI Whisper
- 🔍 **Keyword Search**: Find specific words/phrases with timestamps
- ⏰ **Precise Timestamps**: Get exact timing for every word and phrase
- 📝 **Multiple Formats**: Export as TXT, CSV, or JSON
- 🎯 **Context Highlighting**: See keywords highlighted in context
- 🚀 **Batch Processing**: Process multiple videos at once
- 💻 **Interactive Interface**: Easy-to-use command-line interface

## Installation

1. **Clone or download this repository**
2. **Navigate to the project directory**
3. **The virtual environment is already set up!**

## Usage

### Method 1: Interactive Mode (Recommended for beginners)

```bash
.\.venv\Scripts\python.exe interactive_transcriber.py
```

This will guide you through the process step by step:
- Select your video file
- Choose model size (base recommended)
- Pick output format
- Enter keywords to search for
- Get beautifully formatted results

### Method 2: Command Line Interface

```bash
.\.venv\Scripts\python.exe video_transcriber.py "path/to/your/video.mp4" --search "keyword1" --search "keyword2"
```

**Options:**
- `--model`, `-m`: Choose model size (tiny, base, small, medium, large)
- `--output-dir`, `-o`: Specify output directory
- `--format`, `-f`: Choose format (txt, csv, json)
- `--search`, `-s`: Add keywords to search for (use multiple times)
- `--context`, `-c`: Number of context words around keywords
- `--save-search`: Save search results to separate file

**Examples:**

Basic transcription:
```bash
.\.venv\Scripts\python.exe video_transcriber.py "meeting.mp4"
```

With keyword search:
```bash
.\.venv\Scripts\python.exe video_transcriber.py "lecture.mp4" --search "quantum" --search "physics" --format csv
```

High accuracy transcription:
```bash
.\.venv\Scripts\python.exe video_transcriber.py "interview.mp4" --model large --format json
```

### Method 3: Batch Processing

Process multiple videos at once:

```bash
.\.venv\Scripts\python.exe batch_transcriber.py
```

This will:
- Find all video files in a directory
- Process them with the same settings
- Generate a summary report
- Search for keywords across all videos

## Supported Video Formats

- MP4, AVI, MOV, MKV, WMV, FLV, WebM, M4V
- Any format supported by MoviePy/FFmpeg

## Model Sizes

| Model  | Size  | Speed    | Accuracy | Best For |
|--------|-------|----------|----------|----------|
| tiny   | 39MB  | Fastest  | Basic    | Quick tests |
| base   | 142MB | Fast     | Good     | **Recommended** |
| small  | 466MB | Medium   | Better   | Important content |
| medium | 1.5GB | Slow     | High     | Professional use |
| large  | 2.9GB | Slowest  | Best     | Critical accuracy |

## Output Formats

### TXT Format
```
[00:01:23 - 00:01:28] Welcome to today's presentation on artificial intelligence.
[00:01:28 - 00:01:35] We'll be discussing the latest developments in machine learning.
```

### CSV Format
Spreadsheet-compatible with columns:
- start_time, end_time, formatted_start, formatted_end, text

### JSON Format
Raw data with full timestamp information for programmatic use.

## Keyword Search Features

- **Case-insensitive**: Finds "AI", "ai", "Ai"
- **Context highlighting**: Shows words around matches
- **Precise timing**: Exact timestamps for each occurrence
- **Multiple keywords**: Search for several terms at once
- **Export results**: Save search results separately

## Example Output

When searching for "machine learning":

```
┏━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Time       ┃ Keyword       ┃ Context                                                      ┃
┡━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ 00:01:28   │ machine       │ discussing the latest developments in **machine** learning   │
│ 00:05:42   │ learning      │ algorithms used in **machine** **learning** applications    │
│ 00:12:15   │ machine       │ benefits of **machine** **learning** in healthcare         │
└────────────┴───────────────┴──────────────────────────────────────────────────────────────┘
```

## Tips for Best Results

1. **Choose the right model**:
   - Use `base` for most cases
   - Use `small` or `medium` for important content
   - Use `large` only when you need maximum accuracy

2. **Audio quality matters**:
   - Clear audio = better transcription
   - Reduce background noise when possible

3. **Keywords**:
   - Use specific terms rather than common words
   - Try variations (e.g., "AI", "artificial intelligence")

4. **File organization**:
   - Keep video files in organized folders
   - Use descriptive filenames

## Troubleshooting

**"Model not found" error:**
- The model will download automatically on first use
- Ensure you have internet connection for initial download

**"FFmpeg not found" error:**
- The package should include FFmpeg automatically
- If issues persist, try reinstalling moviepy

**Slow processing:**
- Use smaller model size (tiny/base)
- Process shorter video segments
- Close other applications

**Poor transcription quality:**
- Try a larger model (small/medium/large)
- Improve audio quality
- Check if language is supported

## File Structure

After processing, you'll have:
```
your_video_transcript.txt      # Main transcript
your_video_search_results.json # Keyword search results (if used)
batch_results_YYYYMMDD.json   # Batch processing summary (if used)
```

## Technical Requirements

- Windows (PowerShell support)
- Python 3.8+ (included in venv)
- ~4GB free space for large models
- Internet connection (for initial model download)

## Need Help?

The interactive mode (`interactive_transcriber.py`) is the easiest way to get started. It will guide you through every step and explain the options.

---

**Happy transcribing! 🎬📝**
