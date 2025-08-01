#!/usr/bin/env python3
"""
YouTube Channel Transcriber - GUI Version
Easy-to-use graphical interface for downloading and transcribing YouTube channels
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import queue
from pathlib import Path
import json
from datetime import datetime

# Import our YouTube transcriber
from youtube_channel_transcriber import YouTubeChannelTranscriber

class YouTubeTranscriberGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Channel Transcriber")
        self.root.geometry("800x700")
        self.root.resizable(True, True)
        
        self.transcriber = YouTubeChannelTranscriber()
        self.processing = False
        self.message_queue = queue.Queue()
        
        self.setup_ui()
        self.check_messages()
    
    def setup_ui(self):
        """Setup the user interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="YouTube Channel Transcriber", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Channel URL input
        ttk.Label(main_frame, text="YouTube Channel URL:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.channel_url = tk.StringVar()
        channel_entry = ttk.Entry(main_frame, textvariable=self.channel_url, width=60)
        channel_entry.grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Keywords input
        ttk.Label(main_frame, text="Keywords (comma-separated):").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.keywords = tk.StringVar()
        keywords_entry = ttk.Entry(main_frame, textvariable=self.keywords, width=60)
        keywords_entry.grid(row=2, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Settings frame
        settings_frame = ttk.LabelFrame(main_frame, text="Settings", padding="10")
        settings_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        settings_frame.columnconfigure(1, weight=1)
        
        # Max videos
        ttk.Label(settings_frame, text="Max Videos:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.max_videos = tk.StringVar(value="5")
        max_videos_spin = ttk.Spinbox(settings_frame, from_=1, to=50, textvariable=self.max_videos, width=10)
        max_videos_spin.grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # Duration limit
        ttk.Label(settings_frame, text="Max Duration (minutes):").grid(row=0, column=2, sticky=tk.W, pady=5, padx=(20, 0))
        self.duration_limit = tk.StringVar(value="30")
        duration_spin = ttk.Spinbox(settings_frame, from_=1, to=180, textvariable=self.duration_limit, width=10)
        duration_spin.grid(row=0, column=3, sticky=tk.W, pady=5)
        
        # Model selection
        ttk.Label(settings_frame, text="Model Quality:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.model_size = tk.StringVar(value="base")
        model_combo = ttk.Combobox(settings_frame, textvariable=self.model_size, 
                                  values=["tiny", "base", "small", "medium"], 
                                  state="readonly", width=15)
        model_combo.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Output directory
        ttk.Label(settings_frame, text="Output Directory:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.output_dir = tk.StringVar(value=str(Path.cwd() / "youtube_downloads"))
        output_entry = ttk.Entry(settings_frame, textvariable=self.output_dir, width=40)
        output_entry.grid(row=2, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        browse_btn = ttk.Button(settings_frame, text="Browse", command=self.browse_output_dir)
        browse_btn.grid(row=2, column=3, sticky=tk.W, pady=5, padx=(5, 0))
        
        # Control buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=3, pady=20)
        
        self.start_btn = ttk.Button(button_frame, text="Start Processing", 
                                   command=self.start_processing, style="Accent.TButton")
        self.start_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_btn = ttk.Button(button_frame, text="Stop", 
                                  command=self.stop_processing, state="disabled")
        self.stop_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.clear_btn = ttk.Button(button_frame, text="Clear Log", command=self.clear_log)
        self.clear_btn.pack(side=tk.LEFT)
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        # Log area
        log_frame = ttk.LabelFrame(main_frame, text="Processing Log", padding="5")
        log_frame.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15, width=80)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights for resizing
        main_frame.rowconfigure(6, weight=1)
    
    def browse_output_dir(self):
        """Browse for output directory"""
        directory = filedialog.askdirectory(
            title="Select Output Directory",
            initialdir=self.output_dir.get()
        )
        if directory:
            self.output_dir.set(directory)
    
    def log_message(self, message, level="info"):
        """Add message to log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        if level == "error":
            formatted_msg = f"[{timestamp}] ERROR: {message}\n"
        elif level == "success":
            formatted_msg = f"[{timestamp}] SUCCESS: {message}\n"
        elif level == "warning":
            formatted_msg = f"[{timestamp}] WARNING: {message}\n"
        else:
            formatted_msg = f"[{timestamp}] {message}\n"
        
        self.message_queue.put(formatted_msg)
    
    def check_messages(self):
        """Check for messages from worker thread"""
        try:
            while True:
                message = self.message_queue.get_nowait()
                self.log_text.insert(tk.END, message)
                self.log_text.see(tk.END)
        except queue.Empty:
            pass
        
        # Schedule next check
        self.root.after(100, self.check_messages)
    
    def clear_log(self):
        """Clear the log text"""
        self.log_text.delete(1.0, tk.END)
    
    def validate_inputs(self):
        """Validate user inputs"""
        if not self.channel_url.get().strip():
            messagebox.showerror("Error", "Please enter a YouTube channel URL")
            return False
        
        try:
            max_vids = int(self.max_videos.get())
            if max_vids < 1 or max_vids > 50:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Error", "Max videos must be between 1 and 50")
            return False
        
        try:
            duration = int(self.duration_limit.get())
            if duration < 1:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Error", "Duration limit must be a positive number")
            return False
        
        return True
    
    def start_processing(self):
        """Start the processing in a separate thread"""
        if not self.validate_inputs():
            return
        
        if self.processing:
            messagebox.showwarning("Warning", "Processing is already running")
            return
        
        self.processing = True
        self.start_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        self.progress.start()
        
        # Start processing thread
        thread = threading.Thread(target=self.process_channel, daemon=True)
        thread.start()
    
    def stop_processing(self):
        """Stop the processing"""
        self.processing = False
        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        self.progress.stop()
        self.log_message("Processing stopped by user", "warning")
    
    def process_channel(self):
        """Process the YouTube channel (runs in separate thread)"""
        try:
            # Get inputs
            channel_url = self.channel_url.get().strip()
            keywords_input = self.keywords.get().strip()
            keywords = [k.strip() for k in keywords_input.split(',') if k.strip()] if keywords_input else []
            max_videos = int(self.max_videos.get())
            duration_limit = int(self.duration_limit.get())
            model_size = self.model_size.get()
            output_dir = self.output_dir.get()
            
            self.log_message(f"Starting processing for channel: {channel_url}")
            
            # Setup transcriber
            self.transcriber.setup_directories(output_dir)
            
            # Get channel info
            self.log_message("Getting channel information...")
            channel_info = self.transcriber.get_channel_info(channel_url)
            
            if not channel_info:
                self.log_message("Could not access channel. Please check the URL.", "error")
                return
            
            self.log_message(f"Found channel: {channel_info['title']}", "success")
            self.log_message(f"Available videos: {channel_info['video_count']}")
            
            # Filter videos
            self.log_message("Filtering videos...")
            filtered_videos = self.transcriber.filter_videos(
                channel_info['entries'],
                max_videos=max_videos,
                duration_limit=duration_limit
            )
            
            if not filtered_videos:
                self.log_message("No videos match your criteria.", "error")
                return
            
            self.log_message(f"Selected {len(filtered_videos)} videos to process", "success")
            
            if keywords:
                self.log_message(f"Will search for keywords: {', '.join(keywords)}")
            
            # Process videos
            results = []
            video_dir = self.transcriber.download_dir / "videos"
            
            for i, video_entry in enumerate(filtered_videos):
                if not self.processing:  # Check if stopped
                    break
                
                video_url = f"https://www.youtube.com/watch?v={video_entry['id']}"
                video_title = video_entry.get('title', 'Unknown')
                
                self.log_message(f"Processing ({i+1}/{len(filtered_videos)}): {video_title}")
                
                try:
                    # Download video
                    self.log_message(f"Downloading: {video_title}")
                    video_info = self.transcriber.download_video(video_url, video_dir)
                    
                    if video_info:
                        # Transcribe and search
                        self.log_message(f"Transcribing: {video_info['title']}")
                        result = self.transcriber.transcribe_and_search(video_info, keywords, model_size)
                        
                        if result:
                            results.append(result)
                            self.log_message(f"Completed: {video_info['title']}", "success")
                            
                            if keywords and result['matches']:
                                self.log_message(f"Found {len(result['matches'])} keyword matches")
                        else:
                            self.log_message(f"Failed to transcribe: {video_info['title']}", "error")
                    else:
                        self.log_message(f"Failed to download video", "error")
                        
                except Exception as e:
                    self.log_message(f"Error processing video: {e}", "error")
            
            if self.processing:  # Only show summary if not stopped
                # Display summary
                self.log_message(f"\n=== PROCESSING COMPLETE ===", "success")
                self.log_message(f"Total videos processed: {len(results)}")
                
                if keywords:
                    total_matches = sum(len(r['matches']) for r in results if r['matches'])
                    self.log_message(f"Total keyword matches found: {total_matches}")
                
                self.log_message(f"Files saved to: {self.transcriber.download_dir}")
                
                # Save summary
                summary_file = self.transcriber.download_dir / f"channel_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                summary_data = {
                    'channel_info': channel_info,
                    'keywords': keywords,
                    'model_used': model_size,
                    'processing_date': datetime.now().isoformat(),
                    'total_videos': len(results),
                    'total_matches': sum(len(r['matches']) for r in results if r['matches']),
                }
                
                with open(summary_file, 'w', encoding='utf-8') as f:
                    json.dump(summary_data, f, indent=2, ensure_ascii=False)
                
                self.log_message(f"Summary saved to: {summary_file}")
        
        except Exception as e:
            self.log_message(f"Unexpected error: {e}", "error")
        
        finally:
            # Reset UI state
            self.processing = False
            self.root.after(0, lambda: [
                self.start_btn.config(state="normal"),
                self.stop_btn.config(state="disabled"),
                self.progress.stop()
            ])

def main():
    """Main function"""
    root = tk.Tk()
    
    # Set theme (if available)
    try:
        style = ttk.Style()
        # Use a modern theme if available
        available_themes = style.theme_names()
        if 'clam' in available_themes:
            style.theme_use('clam')
        elif 'alt' in available_themes:
            style.theme_use('alt')
    except:
        pass
    
    app = YouTubeTranscriberGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()
