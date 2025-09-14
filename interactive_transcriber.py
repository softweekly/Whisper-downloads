#!/usr/bin/env python3
"""
Interactive Video Transcriber
Easy-to-use interface for video transcription and keyword search
"""

import os
import sys
from pathlib import Path
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich.text import Text
import json

# Import our main transcriber
from video_transcriber import VideoTranscriber

console = Console()

def get_video_file():
    """Get video file path from user"""
    while True:
        video_path = Prompt.ask("\n[cyan]Enter the path to your video file[/cyan]")
        
        if not video_path:
            console.print("[red]Please enter a valid path[/red]")
            continue
            
        video_path = Path(video_path.strip('"').strip("'"))
        
        if video_path.exists():
            # Check if it's likely a video file
            video_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm', '.m4v'}
            if video_path.suffix.lower() in video_extensions:
                return video_path
            else:
                console.print(f"[yellow]Warning: {video_path.suffix} might not be a supported video format[/yellow]")
                if Confirm.ask("Continue anyway?"):
                    return video_path
        else:
            console.print(f"[red]File not found: {video_path}[/red]")

def get_model_choice():
    """Get Whisper model choice from user"""
    console.print("\n[cyan]Choose Whisper model size:[/cyan]")
    console.print("1. tiny    - Fastest, least accurate")
    console.print("2. base    - Good balance (recommended)")
    console.print("3. small   - Better accuracy, slower")
    console.print("4. medium  - High accuracy, much slower")
    console.print("5. large   - Best accuracy, very slow")
    
    while True:
        choice = Prompt.ask("\nSelect model", choices=["1", "2", "3", "4", "5"], default="2")
        models = {"1": "tiny", "2": "base", "3": "small", "4": "medium", "5": "large"}
        return models[choice]

def get_output_format():
    """Get output format choice from user"""
    console.print("\n[cyan]Choose output format:[/cyan]")
    console.print("1. txt - Human readable with timestamps")
    console.print("2. csv - Spreadsheet format")
    console.print("3. json - Raw data format")
    
    while True:
        choice = Prompt.ask("\nSelect format", choices=["1", "2", "3"], default="1")
        formats = {"1": "txt", "2": "csv", "3": "json"}
        return formats[choice]

def get_keywords():
    """Get keywords for search from user"""
    if not Confirm.ask("\n[cyan]Do you want to search for specific keywords?[/cyan]"):
        return []
    
    keywords = []
    console.print("\n[yellow]Enter keywords one by one. Press Enter with empty input to finish.[/yellow]")
    
    while True:
        keyword = Prompt.ask(f"Keyword #{len(keywords) + 1} (or press Enter to finish)").strip()
        if not keyword:
            break
        keywords.append(keyword)
        console.print(f"[green]Added: {keyword}[/green]")
    
    return keywords

def main():
    """Main interactive function"""
    console.print(Panel.fit(
        "[bold blue]Interactive Video Transcriber[/bold blue]\n"
        "Easy video transcription with keyword search\n"
        "Powered by OpenAI Whisper",
        style="blue"
    ))
    
    try:
        # New: Ask for source type
        source_type = Prompt.ask("\n[cyan]Choose video source:[/cyan]", choices=["local", "youtube"], default="local", show_choices=True)
        
        if source_type == "local":
            video_path = get_video_file()
            is_youtube = False
        else:
            # Get YouTube URL
            while True:
                yt_url = Prompt.ask("\n[cyan]Enter YouTube video URL[/cyan]").strip()
                if yt_url.startswith("http") and "youtube.com" in yt_url:
                    break
                console.print("[red]Please enter a valid YouTube URL[/red]")
            is_youtube = True
            video_path = yt_url
        
        model_size = get_model_choice()
        output_format = get_output_format()
        keywords = get_keywords()
        
        # Ask about output directory
        output_dir = None
        if not is_youtube:
            default_dir = video_path.parent
        else:
            default_dir = Path.cwd()
        if Confirm.ask(f"\n[cyan]Save output to folder ({default_dir})?[/cyan]", default=True):
            output_dir = default_dir
        else:
            output_dir_str = Prompt.ask("Enter output directory path")
            output_dir = Path(output_dir_str.strip('"').strip("'"))
            output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize and run transcriber
        console.print(f"\n[yellow]Starting transcription...[/yellow]")
        if is_youtube:
            console.print(f"YouTube URL: {video_path}")
        else:
            console.print(f"Video: {video_path.name}")
        console.print(f"Model: {model_size}")
        console.print(f"Format: {output_format}")
        if keywords:
            console.print(f"Keywords: {', '.join(keywords)}")
        
        transcriber = VideoTranscriber(model_size=model_size)
        
        # Transcribe
        if is_youtube:
            transcript_data = transcriber.transcribe_youtube(video_path, str(output_dir))
            transcript_file = output_dir / "youtube_transcript." + output_format
        else:
            transcript_data = transcriber.transcribe_video(str(video_path), str(output_dir))
            transcript_file = output_dir / f"{video_path.stem}_transcript.{output_format}"
        
        if not transcript_data:
            console.print("[red]Transcription failed![/red]")
            return
        
        # Save transcript
        transcriber.save_transcript(transcript_data, transcript_file, output_format)
        
        # Search for keywords
        if keywords:
            console.print(f"\n[yellow]Searching for keywords...[/yellow]")
            context_words = 5
            matches = transcriber.search_keywords(transcript_data, keywords, context_words)
            transcriber.display_search_results(matches, keywords)
            
            # Save search results
            if matches and Confirm.ask("\n[cyan]Save search results to file?[/cyan]"):
                search_file = output_dir / ("youtube_search_results.json" if is_youtube else f"{video_path.stem}_search_results.json")
                search_data = {
                    'video_file': str(video_path),
                    'keywords': keywords,
                    'matches': matches
                }
                with open(search_file, 'w', encoding='utf-8') as f:
                    json.dump(search_data, f, indent=2, ensure_ascii=False)
                console.print(f"[green]✓ Search results saved to {search_file}[/green]")
        
        # Summary
        console.print(f"\n[green]✓ Processing complete![/green]")
        console.print(f"[blue]Transcript saved: {transcript_file}[/blue]")
        
        if keywords and 'matches' in locals():
            console.print(f"[blue]Keyword matches found: {len(matches)}[/blue]")
        
        # Ask if user wants to process another video
        if Confirm.ask("\n[cyan]Process another video?[/cyan]"):
            main()
            
    except KeyboardInterrupt:
        console.print("\n[yellow]Process interrupted by user[/yellow]")
    except Exception as e:
        console.print(f"\n[red]Error: {e}[/red]")

if __name__ == '__main__':
    main()
