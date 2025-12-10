# 🎬 Video Transcription App - Complete User Guide

## 📋 Table of Contents
1. [Quick Start (Windows)](#quick-start-windows)
2. [Quick Start (Linux/Mac)](#quick-start-linuxmac)
3. [First Time Setup](#first-time-setup)
4. [How to Use](#how-to-use)
5. [Troubleshooting](#troubleshooting)
6. [Advanced Features](#advanced-features)

---

## 🚀 Quick Start (Windows)

### The Easiest Way:
1. **Place your video** in the `videos_to_transcribe` folder
2. **Double-click** `transcribe.bat`
3. **Type** `local` and press Enter
4. **Type** the video filename (e.g., `my_video.mp4`)
5. **Follow the prompts** - the app will guide you!

### That's it! 🎉

---

## 🚀 Quick Start (Linux/Mac)

### The Easiest Way:
1. **Place your video** in the `videos_to_transcribe` folder
2. **Open Terminal** in this folder
3. **Run**: `chmod +x transcribe.sh` (first time only)
4. **Run**: `./transcribe.sh`
5. **Type** `local` and press Enter
6. **Type** the video filename (e.g., `my_video.mp4`)
7. **Follow the prompts** - the app will guide you!

---

## 🔧 First Time Setup

### Windows Users:

**Option 1: Already Set Up? Skip to "How to Use"**

**Option 2: Need to Set Up?**
1. Open PowerShell in this folder
2. Run these commands:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```
3. Done! Now double-click `transcribe.bat`

### Linux/Mac Users:

1. Open Terminal in this folder
2. Run these commands:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   chmod +x *.sh
   ```
3. Done! Now run `./transcribe.sh`

---

## 📖 How to Use

### Method 1: Local Video Files (Recommended for Beginners)

**Step 1: Prepare Your Video**
- Copy your video to the `videos_to_transcribe` folder
- Supported formats: MP4, AVI, MOV, MKV, WMV, FLV, WebM, M4V

**Step 2: Start the App**
- **Windows**: Double-click `transcribe.bat`
- **Linux/Mac**: Run `./transcribe.sh`

**Step 3: Choose Source**
- Type `local` and press Enter

**Step 4: Enter Filename**
- Type just the filename: `my_video.mp4`
- Or full path if outside the folder

**Step 5: Select Quality**
```
1. tiny    - Fastest (good for testing)
2. base    - Good balance ⭐ RECOMMENDED
3. small   - Better accuracy
4. medium  - High accuracy (slower)
5. large   - Best accuracy (very slow)
```
Choose 2 for most use cases.

**Step 6: Choose Output Format**
```
1. txt  - Easy to read ⭐ RECOMMENDED
2. csv  - Spreadsheet format
3. json - Raw data
```
Choose 1 for human-readable results.

**Step 7: Add Keywords (Optional)**
- Type keywords you want to find (e.g., "important", "deadline", "action")
- Press Enter without typing to skip
- The app will highlight these words with timestamps!

**Step 8: Wait for Results**
- The app will show progress
- Results saved in the same folder as your video
- Includes full transcript with timestamps
- Includes keyword matches if you searched for any

### Method 2: YouTube Videos

**Step 1: Get YouTube URL**
- Copy the full URL (e.g., `https://www.youtube.com/watch?v=...`)

**Step 2: Start the App**
- **Windows**: Double-click `transcribe.bat`
- **Linux/Mac**: Run `./transcribe.sh`

**Step 3: Choose Source**
- Type `youtube` and press Enter

**Step 4: Paste YouTube URL**
- Paste the full URL
- Press Enter

**Step 5: Follow Same Steps as Local Video**
- Choose quality (recommend: base)
- Choose format (recommend: txt)
- Add keywords if needed
- Wait for results!

### Method 3: Member-Only or Private YouTube Content

Some YouTube videos require authentication (members-only content, private videos, etc.). For these, you'll need a cookies file:

**Step 1: Export Cookies from Your Browser**

**Option A: Using Browser Extension (Easiest)**
1. Install a cookies export extension for your browser:
   - Chrome/Edge: "Get cookies.txt LOCALLY" or "cookies.txt"
   - Firefox: "cookies.txt"
2. Log into YouTube in your browser
3. Navigate to YouTube.com
4. Click the extension icon
5. Export cookies as `cookies.txt`

**Option B: Manual Export (Advanced)**
1. Open Developer Tools in your browser (F12)
2. Go to YouTube.com (logged in)
3. Go to Application/Storage → Cookies
4. Export cookies to `cookies.txt` in Netscape format

**Step 2: Place Cookies File**
- Save the `cookies.txt` file in this app's main folder
- The file should be named exactly: `cookies.txt`
- Place it in: `C:\Users\Soft\Desktop\Dev3\Whisper downloads\cookies.txt`

**Step 3: The App Will Auto-Detect Cookies**
- When you transcribe YouTube videos, the app will automatically use the cookies file
- This allows access to member-only or private content you have permission to view
- No extra steps needed - just ensure cookies.txt is in the main folder

**Important Security Notes:**
- ⚠️ **Keep cookies.txt private** - it contains your login session
- ⚠️ **Don't share cookies.txt** - it's like sharing your password
- ⚠️ **Update periodically** - cookies expire after a few weeks/months
- ⚠️ **Delete if not needed** - remove cookies.txt when done with private content

**Troubleshooting Cookies:**
- If still can't access: Re-export fresh cookies while logged into YouTube
- Make sure you're actually subscribed/member of the channel
- Check file is named exactly `cookies.txt` (not cookies.txt.txt)
- Ensure cookies.txt is in the main app folder, not a subfolder

---

## 🎯 Launcher Files Explained

### Windows Users:

| File | What It Does | When to Use |
|------|--------------|-------------|
| `transcribe.bat` | Quick start - goes directly to transcription | **Most Common** - Daily use |
| `quick_start.bat` | Same as above with a nicer interface | If you want a prettier startup |
| `start.bat` | Full menu with all options | When you need advanced features |

**Recommendation**: Use `transcribe.bat` for 90% of your needs.

### Linux/Mac Users:

| File | What It Does | When to Use |
|------|--------------|-------------|
| `transcribe.sh` | Quick start - goes directly to transcription | **Most Common** - Daily use |
| `start.sh` | Full menu with all options | When you need advanced features |

**Recommendation**: Use `./transcribe.sh` for 90% of your needs.

---

## 🛠️ Troubleshooting

### Windows Issues:

**Problem**: "Cannot run scripts on this system"
```powershell
# Solution: Run this in PowerShell as Administrator
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Problem**: "Python not found"
```
# Solution: Install Python 3.8 or higher from python.org
# Make sure to check "Add Python to PATH" during installation
```

**Problem**: "Video file not found"
```
# Solution: 
1. Make sure video is in videos_to_transcribe folder
2. Or use full path: C:\path\to\video.mp4
3. Use quotes if path has spaces: "C:\My Videos\video.mp4"
```

### Linux/Mac Issues:

**Problem**: "Permission denied"
```bash
# Solution: Make scripts executable
chmod +x *.sh
```

**Problem**: "Python3 not found"
```bash
# Ubuntu/Debian:
sudo apt-get install python3 python3-venv python3-pip

# Mac (using Homebrew):
brew install python3
```

**Problem**: "ffmpeg not found"
```bash
# Ubuntu/Debian:
sudo apt-get install ffmpeg

# Mac:
brew install ffmpeg
```

### Common Issues (All Platforms):

**Problem**: "Error extracting audio"
- **Solution**: The app now fixes this automatically. If it persists:
  - Make sure video file is not corrupted
  - Try converting to MP4 format
  - Check if video has audio track

**Problem**: "Transcription is in wrong language"
- **Solution**: Whisper auto-detects language. For better results:
  - Use higher quality model (small or medium)
  - Ensure clear audio quality in video

**Problem**: "Process is very slow"
- **Solution**: 
  - Use smaller model (tiny or base)
  - Smaller video = faster processing
  - Close other applications
  - First run downloads model (only happens once)

---

## 🎓 Advanced Features

### Full Menu Mode

**Windows**: Double-click `start.bat`
**Linux/Mac**: Run `./start.sh`

#### Available Options:

**1. Interactive Mode** - What we covered above

**2. Command Line Help** - For power users
```bash
# Example: Quick transcription with keywords
python video_transcriber.py video.mp4 --search "keyword1" --search "keyword2"
```

**3. Batch Processing** - Multiple videos at once
- Place multiple videos in a folder
- Process them all with same settings
- Great for transcribing a series

**4. YouTube Channel Transcriber** - Download whole channels
- Enter channel URL
- Choose number of videos
- **Filter for live streams only** ⭐
- Process all with keywords
- Perfect for lecture series or podcasts

**5. View Demo/Examples** - See all features and usage examples

**6. Run System Test** - Verify everything works correctly

### Command Line Examples (Advanced Users)

**Basic transcription:**
```bash
python video_transcriber.py my_video.mp4
```

**With keywords:**
```bash
python video_transcriber.py my_video.mp4 --search "important" --search "deadline"
```

**Different quality:**
```bash
python video_transcriber.py my_video.mp4 --model medium
```

**CSV output:**
```bash
python video_transcriber.py my_video.mp4 --format csv
```

**Custom output folder:**
```bash
python video_transcriber.py my_video.mp4 --output-dir C:\Transcripts
```

---

## 📁 Folder Structure Explained

```
Whisper downloads/
├── videos_to_transcribe/     ← PUT YOUR VIDEOS HERE!
│   └── README.txt            ← Instructions
├── youtube_downloads/         ← YouTube videos go here
│   ├── videos/
│   ├── transcripts/
│   └── search_results/
├── transcribe.bat            ← WINDOWS: CLICK THIS!
├── transcribe.sh             ← LINUX/MAC: RUN THIS!
├── start.bat                 ← Full menu (Windows)
├── start.sh                  ← Full menu (Linux/Mac)
└── .venv/                    ← Virtual environment (auto-created)
```

---

## 💡 Pro Tips

1. **Start with small videos** to test and understand the process
2. **Use 'base' model** for best balance of speed and accuracy
3. **Put videos in videos_to_transcribe folder** for easiest access
4. **Use keywords** to quickly find important parts of long videos
5. **TXT format** is best for reading, CSV for spreadsheets
6. **First run downloads the model** - be patient (one-time thing)
7. **Close other programs** when transcribing for better performance
8. **Better audio = better results** - ensure clear audio in videos

---

## ❓ FAQ

**Q: How long does transcription take?**
A: Roughly 1/3 to 1/2 of video length with 'base' model. A 1-hour video takes about 20-30 minutes.

**Q: Does it need internet?**
A: Only for first-time model download and YouTube videos. Local videos work offline after setup.

**Q: Can it transcribe any language?**
A: Yes! Whisper supports 90+ languages and auto-detects them.

**Q: How accurate is it?**
A: Very accurate with clear audio. Use 'medium' or 'large' model for best results.

**Q: Where are results saved?**
A: Same folder as your video by default. Look for files ending in `_transcript.txt` or `_transcript.csv`.

**Q: Can I transcribe multiple videos?**
A: Yes! Use "Batch Processing" from the full menu (`start.bat` or `start.sh`).

**Q: What if I get errors?**
A: Check the Troubleshooting section above. Most issues are quick fixes!

---

## 🆘 Still Need Help?

1. Run the system test: Choose option 6 from `start.bat`/`start.sh`
2. Check the error message carefully
3. Look in the Troubleshooting section
4. Make sure video file is not corrupted
5. Try with a different video to isolate the issue

---

## 🎉 You're Ready!

**Remember**: The easiest way is:
1. Drop video in `videos_to_transcribe` folder
2. Double-click `transcribe.bat` (Windows) or run `./transcribe.sh` (Linux/Mac)
3. Type `local`, enter filename, follow prompts
4. Get your transcript with timestamps!

**That's it! Enjoy transcribing! 🚀**