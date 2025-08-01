# YouTube Channel Transcription Guide

## 🎥 NEW FEATURE: YouTube Channel Transcription

Now you can automatically download videos from any YouTube channel and transcribe them with keyword search!

---

## 🚀 Two Ways to Use YouTube Transcription

### Method 1: Graphical Interface (Easiest)

**Launch the GUI:**
```bash
.\.venv\Scripts\python.exe youtube_gui.py
```
Or use the launcher: Double-click `start.bat` → Choose option 5

**What you'll see:**
- Easy form to fill out
- Channel URL input
- Keywords input (comma-separated)
- Settings for max videos, duration, quality
- Real-time processing log
- Progress indicator

**How to use:**
1. Paste YouTube channel URL (e.g., `https://www.youtube.com/@channelname`)
2. Enter keywords separated by commas (e.g., `AI, machine learning, neural networks`)
3. Set maximum videos to process (1-50)
4. Set maximum duration per video (minutes)
5. Choose model quality (base recommended)
6. Select output directory
7. Click "Start Processing"
8. Watch the real-time log for progress

### Method 2: Interactive Command Line

**Launch the interactive mode:**
```bash
.\.venv\Scripts\python.exe youtube_channel_transcriber.py
```
Or use the launcher: Double-click `start.bat` → Choose option 4

**Step-by-step prompts:**
1. Enter channel URL or @username
2. Choose max videos to process
3. Set duration limit
4. Enter keywords for search
5. Select transcription quality
6. Choose output directory
7. Confirm and start processing

---

## 📝 Supported YouTube URL Formats

✅ **Full channel URLs:**
- `https://www.youtube.com/@channelname`
- `https://www.youtube.com/c/channelname`
- `https://www.youtube.com/channel/UCxxxxxxx`

✅ **Short formats:**
- `@channelname` (will be converted automatically)
- `channelname` (will be converted automatically)

---

## 🎯 How It Works

1. **Channel Analysis** - Scans the channel for available videos
2. **Video Filtering** - Applies your criteria (max videos, duration limit)
3. **Download** - Downloads videos in good quality (720p max for speed)
4. **Audio Extraction** - Extracts audio from each video
5. **Transcription** - Uses Whisper AI to convert speech to text
6. **Keyword Search** - Finds your keywords with timestamps and context
7. **Results Generation** - Creates organized output files

---

## 📁 Output Structure

After processing, you'll get a organized folder structure:

```
youtube_downloads/
├── videos/                          # Downloaded video files
│   ├── Video_Title_1.mp4
│   ├── Video_Title_2.mp4
│   └── ...
├── transcripts/                     # Full transcripts
│   ├── Video_Title_1_transcript.txt
│   ├── Video_Title_2_transcript.txt
│   └── ...
├── search_results/                  # Keyword search results
│   ├── Video_Title_1_search.json
│   ├── Video_Title_2_search.json
│   └── ...
└── channel_summary_YYYYMMDD_HHMMSS.json  # Overall summary
```

---

## 📄 File Examples

### Transcript File
```
[00:01:23 - 00:01:28] Welcome to today's AI tutorial.
[00:01:28 - 00:01:35] We'll explore machine learning algorithms.
[00:01:35 - 00:01:42] First, let's understand neural networks.
```

### Search Results JSON
```json
{
  "video_info": {
    "title": "Introduction to AI",
    "url": "https://www.youtube.com/watch?v=abcd1234",
    "duration": 1800
  },
  "keywords": ["AI", "machine learning"],
  "matches": [
    {
      "keyword": "AI",
      "timestamp": 83.5,
      "formatted_time": "00:01:23",
      "context": "Welcome to today's **AI** tutorial where we'll explore"
    }
  ]
}
```

### Channel Summary
```json
{
  "channel_info": {
    "title": "AI Education Channel",
    "video_count": 150
  },
  "keywords": ["AI", "machine learning", "neural networks"],
  "total_videos": 5,
  "total_matches": 47,
  "processing_date": "2025-07-30T14:30:00"
}
```

---

## ⚙️ Settings Guide

### Model Quality Options
- **tiny** - Fastest processing, basic accuracy (good for testing)
- **base** - Good balance of speed and accuracy (recommended)
- **small** - Better accuracy, slower processing
- **medium** - High accuracy, much slower processing

### Filtering Options
- **Max Videos** - Limit how many videos to process (1-50)
- **Duration Limit** - Skip videos longer than X minutes
- **Keywords** - What to search for in the transcripts

---

## 💡 Pro Tips for YouTube Transcription

### Choosing Channels
- **Educational channels** work best (clear speech)
- **Interview/podcast channels** are excellent
- **Tutorial channels** give great keyword results
- **Avoid music/entertainment** channels (poor transcription)

### Keyword Strategy
- **Be specific** - "machine learning" vs "learning"
- **Use variations** - "AI, artificial intelligence, neural networks"
- **Industry terms** - "regression, classification, deep learning"
- **Names/brands** - "TensorFlow, PyTorch, OpenAI"

### Processing Optimization
- **Start small** - Try 2-3 videos first
- **Use duration limits** - Long videos take much longer
- **Choose good audio** - Clear speakers = better transcription
- **Base model** - Good balance for most use cases

---

## 🔍 Example Use Cases

### 1. Research Assistant
- Channel: AI research channel
- Keywords: `neural networks, transformer, attention mechanism`
- Goal: Find technical explanations and timestamp references

### 2. Learning Content
- Channel: Programming tutorials
- Keywords: `Python, function, class, inheritance`
- Goal: Find specific programming concepts across videos

### 3. Business Intelligence
- Channel: Industry expert interviews
- Keywords: `market trends, revenue, growth, strategy`
- Goal: Extract business insights and quotes

### 4. Academic Research
- Channel: University lectures
- Keywords: `quantum computing, algorithm, complexity`
- Goal: Find relevant academic content with precise timestamps

---

## 🛠️ Troubleshooting YouTube Issues

### "Channel not found"
- Check the URL is correct
- Try different URL format (@username vs full URL)
- Ensure channel is public
- Check internet connection

### "No videos found"
- Channel might be empty or private
- Try increasing duration limit
- Check if channel has recent videos
- Some channels hide older content

### Download failures
- Video might be private/restricted
- Age-restricted content may fail
- Live streams can't be downloaded
- Some regions block certain content

### Slow processing
- Use smaller model (tiny/base)
- Reduce max videos
- Set shorter duration limit
- Close other applications

---

## 🎉 Quick Start Examples

### Academic Research
```
Channel: @StanfordOnline
Keywords: machine learning, neural networks, AI
Max Videos: 10
Duration: 60 minutes
Model: base
```

### Tech Tutorials
```
Channel: @programmingchannel
Keywords: Python, JavaScript, API, database
Max Videos: 5
Duration: 30 minutes
Model: base
```

### Business Content
```
Channel: @businessinsights
Keywords: strategy, revenue, market, growth
Max Videos: 8
Duration: 45 minutes
Model: small
```

---

**Ready to transcribe YouTube channels? Use the GUI (option 5) for the easiest experience! 🎬📝**
