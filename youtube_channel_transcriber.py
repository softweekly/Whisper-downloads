#!/usr/bin/env python3
"""
YouTube Channel Transcriber
Download videos from a YouTube channel and transcribe them with keyword search
"""

import os
import sys
import yt_dlp
from pathlib import Path
from rich.console import Console
from rich.prompt import Prompt, Confirm, IntPrompt
from rich.panel import Panel
from rich.progress import Progress, track
from rich.table import Table
from rich.text import Text
import json
from datetime import datetime
import re

# Import our existing transcriber
from video_transcriber import VideoTranscriber

console = Console()

class YouTubeChannelTranscriber:
    def __init__(self):
        self.console = console
        self.download_dir = None
        self.transcriber = None
        
    def setup_directories(self, base_dir=None):
        """Setup download directories"""
        if base_dir is None:
            base_dir = Path.cwd() / "youtube_downloads"
        else:
            base_dir = Path(base_dir)
        
        base_dir.mkdir(exist_ok=True)
        self.download_dir = base_dir
        
        # Create subdirectories
        (base_dir / "videos").mkdir(exist_ok=True)
        (base_dir / "transcripts").mkdir(exist_ok=True)
        (base_dir / "search_results").mkdir(exist_ok=True)
        
        return base_dir
    
    def get_channel_info(self, channel_url):
        """Get information about a YouTube channel"""
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(channel_url, download=False)
                
                if info:
                    return {
                        'title': info.get('title', 'Unknown Channel'),
                        'uploader': info.get('uploader', 'Unknown'),
                        'description': info.get('description', ''),
                        'video_count': len(info.get('entries', [])),
                        'entries': info.get('entries', [])
                    }
        except Exception as e:
            console.print(f"[red]Error getting channel info: {e}[/red]")
            return None
    
    def filter_videos(self, entries, max_videos=None, days_back=None, duration_limit=None):
        """Filter videos based on user criteria"""
        filtered = []
        
        for entry in entries:
            # Skip if no video ID
            if not entry.get('id'):
                continue
                
            # Duration filter (if specified)
            if duration_limit and entry.get('duration'):
                if entry['duration'] > duration_limit * 60:  # Convert minutes to seconds
                    continue
            
            # Date filter (if specified) - simplified for now
            # Could be enhanced with actual date parsing
            
            filtered.append(entry)
            
            # Limit number of videos
            if max_videos and len(filtered) >= max_videos:
                break
        
        return filtered
    
    def download_video(self, video_url, output_dir):
        """Download a single video"""
        try:
            ydl_opts = {
                'outtmpl': str(output_dir / '%(title)s.%(ext)s'),
                'format': 'best[height<=720]',  # Limit quality for faster download
                'quiet': True,
                'no_warnings': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=True)
                
                if info:
                    # Find the downloaded file
                    title = info.get('title', 'unknown')
                    # Clean title for filename
                    clean_title = re.sub(r'[<>:"/\\|?*]', '_', title)
                    
                    # Find the actual downloaded file
                    for file in output_dir.glob(f"*{clean_title}*"):
                        if file.is_file() and file.suffix in ['.mp4', '.mkv', '.webm']:
                            return {
                                'file_path': file,
                                'title': title,
                                'duration': info.get('duration', 0),
                                'upload_date': info.get('upload_date', ''),
                                'view_count': info.get('view_count', 0),
                                'url': video_url
                            }
        except Exception as e:
            console.print(f"[red]Error downloading video: {e}[/red]")
            return None
    
    def transcribe_and_search(self, video_info, keywords, model_size="base"):
        """Transcribe video and search for keywords"""
        if not self.transcriber:
            self.transcriber = VideoTranscriber(model_size)
        
        video_path = video_info['file_path']
        
        # Transcribe
        transcript_data = self.transcriber.transcribe_video(
            str(video_path), 
            str(self.download_dir / "transcripts")
        )
        
        if not transcript_data:
            return None
        
        # Save transcript
        transcript_file = self.download_dir / "transcripts" / f"{video_path.stem}_transcript.txt"
        self.transcriber.save_transcript(transcript_data, transcript_file, 'txt')
        
        # Search for keywords
        matches = []
        if keywords:
            matches = self.transcriber.search_keywords(transcript_data, keywords, context_words=5)
            
            if matches:
                # Save search results
                search_file = self.download_dir / "search_results" / f"{video_path.stem}_search.json"
                search_data = {
                    'video_info': {
                        'title': video_info['title'],
                        'url': video_info['url'],
                        'duration': video_info['duration']
                    },
                    'keywords': keywords,
                    'matches': matches,
                    'timestamp': datetime.now().isoformat()
                }
                
                with open(search_file, 'w', encoding='utf-8') as f:
                    json.dump(search_data, f, indent=2, ensure_ascii=False)
        
        return {
            'transcript_file': transcript_file,
            'matches': matches,
            'video_info': video_info
        }
    
    def display_summary(self, results, keywords):
        """Display summary of all processed videos"""
        console.print(f"\n[green]✓ Processing Complete![/green]")
        console.print(f"[blue]Total videos processed: {len(results)}[/blue]")
        
        if keywords:
            total_matches = sum(len(r['matches']) for r in results if r['matches'])
            console.print(f"[blue]Total keyword matches: {total_matches}[/blue]")
            
            # Show summary table
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Video", style="cyan", width=40)
            table.add_column("Matches", style="yellow", width=10)
            table.add_column("Keywords Found", style="green", width=30)
            
            for result in results:
                if result and result['matches']:
                    keywords_found = list(set([m['keyword'] for m in result['matches']]))
                    table.add_row(
                        result['video_info']['title'][:37] + "..." if len(result['video_info']['title']) > 40 else result['video_info']['title'],
                        str(len(result['matches'])),
                        ", ".join(keywords_found)
                    )
            
            if table.rows:
                console.print(f"\n[cyan]Keyword Match Summary:[/cyan]")
                console.print(table)
        
        console.print(f"\n[blue]Files saved to: {self.download_dir}[/blue]")

def main():
    """Main interactive function"""
    console.print(Panel.fit(
        "[bold blue]YouTube Channel Transcriber[/bold blue]\n"
        "Download and transcribe videos from YouTube channels\n"
        "Search for keywords across all videos",
        style="blue"
    ))
    
    transcriber = YouTubeChannelTranscriber()
    
    try:
        # Get YouTube channel URL
        console.print("\n[cyan]YouTube Channel Information[/cyan]")
        channel_url = Prompt.ask("Enter YouTube channel URL or @username")
        
        # Normalize channel URL
        if not channel_url.startswith('http'):
            if channel_url.startswith('@'):
                channel_url = f"https://www.youtube.com/{channel_url}"
            else:
                channel_url = f"https://www.youtube.com/c/{channel_url}"
        
        console.print(f"\n[yellow]Getting channel information...[/yellow]")
        channel_info = transcriber.get_channel_info(channel_url)
        
        if not channel_info:
            console.print("[red]Could not access channel. Please check the URL.[/red]")
            return
        
        # Display channel info
        console.print(f"\n[green]✓ Found channel: {channel_info['title']}[/green]")
        console.print(f"[blue]Videos available: {channel_info['video_count']}[/blue]")
        
        if not Confirm.ask("Continue with this channel?"):
            return
        
        # Get filtering options
        console.print("\n[cyan]Video Selection Options[/cyan]")
        
        max_videos = IntPrompt.ask(
            "Maximum number of videos to process", 
            default=5, 
            show_default=True
        )
        
        duration_limit = IntPrompt.ask(
            "Maximum video duration (minutes, 0 for no limit)", 
            default=30, 
            show_default=True
        )
        duration_limit = duration_limit if duration_limit > 0 else None
        
        # Get keywords
        console.print("\n[cyan]Keyword Search Setup[/cyan]")
        keywords = []
        if Confirm.ask("Do you want to search for specific keywords?"):
            keywords_input = Prompt.ask("Enter keywords separated by commas")
            if keywords_input.strip():
                keywords = [k.strip() for k in keywords_input.split(',') if k.strip()]
                console.print(f"[green]Will search for: {', '.join(keywords)}[/green]")
        
        # Get model size
        console.print("\n[cyan]Transcription Quality[/cyan]")
        console.print("1. tiny    - Fastest")
        console.print("2. base    - Good balance (recommended)")
        console.print("3. small   - Better accuracy")
        console.print("4. medium  - High accuracy")
        
        model_choice = Prompt.ask("Choose model", choices=["1", "2", "3", "4"], default="2")
        models = {"1": "tiny", "2": "base", "3": "small", "4": "medium"}
        model_size = models[model_choice]
        
        # Setup directories
        output_dir = Prompt.ask(
            "Output directory", 
            default=str(Path.cwd() / "youtube_downloads")
        )
        transcriber.setup_directories(output_dir)
        
        # Filter videos
        console.print(f"\n[yellow]Filtering videos...[/yellow]")
        filtered_videos = transcriber.filter_videos(
            channel_info['entries'], 
            max_videos=max_videos,
            duration_limit=duration_limit
        )
        
        if not filtered_videos:
            console.print("[red]No videos match your criteria.[/red]")
            return
        
        console.print(f"[green]Selected {len(filtered_videos)} videos to process[/green]")
        
        if not Confirm.ask("Start downloading and transcribing?"):
            return
        
        # Process videos
        results = []
        video_dir = transcriber.download_dir / "videos"
        
        with Progress() as progress:
            task = progress.add_task("[cyan]Processing videos...", total=len(filtered_videos))
            
            for i, video_entry in enumerate(filtered_videos):
                video_url = f"https://www.youtube.com/watch?v={video_entry['id']}"
                progress.update(task, description=f"[cyan]Processing: {video_entry.get('title', 'Unknown')}")
                
                try:
                    # Download video
                    console.print(f"\n[yellow]Downloading: {video_entry.get('title', 'Unknown')}[/yellow]")
                    video_info = transcriber.download_video(video_url, video_dir)
                    
                    if video_info:
                        # Transcribe and search
                        console.print(f"[yellow]Transcribing: {video_info['title']}[/yellow]")
                        result = transcriber.transcribe_and_search(video_info, keywords, model_size)
                        
                        if result:
                            results.append(result)
                            console.print(f"[green]✓ Completed: {video_info['title']}[/green]")
                            
                            # Show keyword matches for this video
                            if keywords and result['matches']:
                                console.print(f"[blue]Found {len(result['matches'])} keyword matches[/blue]")
                        else:
                            console.print(f"[red]✗ Failed to transcribe: {video_info['title']}[/red]")
                    else:
                        console.print(f"[red]✗ Failed to download video[/red]")
                        
                except Exception as e:
                    console.print(f"[red]✗ Error processing video: {e}[/red]")
                
                progress.advance(task)
        
        # Display summary
        transcriber.display_summary(results, keywords)
        
        # Save overall summary
        summary_file = transcriber.download_dir / f"channel_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        summary_data = {
            'channel_info': channel_info,
            'keywords': keywords,
            'model_used': model_size,
            'processing_date': datetime.now().isoformat(),
            'total_videos': len(results),
            'total_matches': sum(len(r['matches']) for r in results if r['matches']),
            'videos_processed': [
                {
                    'title': r['video_info']['title'],
                    'url': r['video_info']['url'],
                    'matches_count': len(r['matches']) if r['matches'] else 0,
                    'transcript_file': str(r['transcript_file'])
                } for r in results if r
            ]
        }
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, indent=2, ensure_ascii=False)
        
        console.print(f"[green]Summary saved to: {summary_file}[/green]")
        
    except KeyboardInterrupt:
        console.print("\n[yellow]Process interrupted by user[/yellow]")
    except Exception as e:
        console.print(f"\n[red]Error: {e}[/red]")

if __name__ == '__main__':
    main()
