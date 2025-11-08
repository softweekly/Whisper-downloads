#!/usr/bin/env python3
"""
Video Transcription Tool with Keyword Search
Uses OpenAI Whisper for transcription and provides keyword search with timestamps
"""

import os
import sys
import click
import whisper
import pandas as pd
import re
from moviepy import VideoFileClip
from rich.console import Console
from rich.table import Table
from rich.progress import track
from rich.text import Text
from rich.panel import Panel
from pathlib import Path
import json
from datetime import datetime, timedelta

console = Console()

class VideoTranscriber:
    def __init__(self, model_size="base"):
        """Initialize the transcriber with specified Whisper model size"""
        self.model_size = model_size
        self.model = None
        self.load_model()
    
    def load_model(self):
        """Load the Whisper model"""
        console.print(f"[yellow]Loading Whisper model ({self.model_size})...[/yellow]")
        try:
            self.model = whisper.load_model(self.model_size)
            console.print(f"[green]✓ Model loaded successfully[/green]")
        except Exception as e:
            console.print(f"[red]✗ Error loading model: {e}[/red]")
            sys.exit(1)
    
    def extract_audio(self, video_path, audio_path):
        """Extract audio from video file"""
        console.print(f"[yellow]Extracting audio from video...[/yellow]")
        try:
            video = VideoFileClip(video_path)
            audio = video.audio
            audio.write_audiofile(audio_path, logger=None)
            audio.close()
            video.close()
            console.print(f"[green]✓ Audio extracted to {audio_path}[/green]")
            return True
        except Exception as e:
            console.print(f"[red]✗ Error extracting audio: {e}[/red]")
            return False
    
    def transcribe_video(self, video_path, output_dir=None):
        """Transcribe video file and return transcript with timestamps"""
        video_path = Path(video_path)
        
        if not video_path.exists():
            console.print(f"[red]✗ Video file not found: {video_path}[/red]")
            return None
        
        # Set output directory
        if output_dir is None:
            output_dir = video_path.parent
        else:
            output_dir = Path(output_dir)
        
        output_dir.mkdir(exist_ok=True)
        
        # Extract audio temporarily
        temp_audio = output_dir / f"{video_path.stem}_temp_audio.wav"
        
        if not self.extract_audio(str(video_path), str(temp_audio)):
            return None
        
        console.print(f"[yellow]Transcribing audio...[/yellow]")
        
        try:
            # Transcribe with timestamps
            result = self.model.transcribe(
                str(temp_audio),
                word_timestamps=True
            )
            
            # Clean up temporary audio file
            if temp_audio.exists():
                temp_audio.unlink()
            
            console.print(f"[green]✓ Transcription completed[/green]")
            return result
            
        except Exception as e:
            console.print(f"[red]✗ Error during transcription: {e}[/red]")
            # Clean up temporary audio file
            if temp_audio.exists():
                temp_audio.unlink()
            return None
    
    def format_timestamp(self, seconds):
        """Convert seconds to HH:MM:SS format"""
        td = timedelta(seconds=seconds)
        total_seconds = int(td.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
    def search_keywords(self, transcript_data, keywords, context_words=5):
        """Search for keywords in transcript and return matches with timestamps"""
        if not transcript_data or not keywords:
            return []
        
        matches = []
        
        for segment in transcript_data.get('segments', []):
            segment_text = segment.get('text', '').strip()
            words = segment.get('words', [])
            
            # Search for each keyword
            for keyword in keywords:
                # Case-insensitive search
                if re.search(re.escape(keyword), segment_text, re.IGNORECASE):
                    # Find the specific word positions
                    for word_info in words:
                        word_text = word_info.get('word', '').strip()
                        if re.search(re.escape(keyword), word_text, re.IGNORECASE):
                            start_time = word_info.get('start', segment.get('start', 0))
                            end_time = word_info.get('end', segment.get('end', 0))
                            
                            # Get context around the keyword
                            word_index = words.index(word_info)
                            context_start = max(0, word_index - context_words)
                            context_end = min(len(words), word_index + context_words + 1)
                            
                            context_words_list = []
                            for i in range(context_start, context_end):
                                word = words[i].get('word', '').strip()
                                if i == word_index:
                                    # Highlight the matched keyword
                                    word = f"**{word}**"
                                context_words_list.append(word)
                            
                            context_text = ' '.join(context_words_list)
                            
                            matches.append({
                                'keyword': keyword,
                                'timestamp': start_time,
                                'end_time': end_time,
                                'context': context_text,
                                'segment_text': segment_text,
                                'formatted_time': self.format_timestamp(start_time)
                            })
        
        # Sort matches by timestamp
        matches.sort(key=lambda x: x['timestamp'])
        return matches
    
    def save_transcript(self, transcript_data, output_path, format_type='json'):
        """Save transcript to file in specified format"""
        output_path = Path(output_path)
        
        try:
            if format_type.lower() == 'json':
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(transcript_data, f, indent=2, ensure_ascii=False)
            
            elif format_type.lower() == 'txt':
                with open(output_path, 'w', encoding='utf-8') as f:
                    for segment in transcript_data.get('segments', []):
                        start_time = self.format_timestamp(segment.get('start', 0))
                        end_time = self.format_timestamp(segment.get('end', 0))
                        text = segment.get('text', '').strip()
                        f.write(f"[{start_time} - {end_time}] {text}\n")
            
            elif format_type.lower() == 'csv':
                segments = []
                for segment in transcript_data.get('segments', []):
                    segments.append({
                        'start_time': segment.get('start', 0),
                        'end_time': segment.get('end', 0),
                        'formatted_start': self.format_timestamp(segment.get('start', 0)),
                        'formatted_end': self.format_timestamp(segment.get('end', 0)),
                        'text': segment.get('text', '').strip()
                    })
                
                df = pd.DataFrame(segments)
                df.to_csv(output_path, index=False, encoding='utf-8')
            
            console.print(f"[green]✓ Transcript saved to {output_path}[/green]")
            return True
            
        except Exception as e:
            console.print(f"[red]✗ Error saving transcript: {e}[/red]")
            return False
    
    def display_search_results(self, matches, keywords):
        """Display search results in a formatted table"""
        if not matches:
            console.print(f"[yellow]No matches found for keywords: {', '.join(keywords)}[/yellow]")
            return
        
        console.print(f"\n[green]Found {len(matches)} matches for keywords: {', '.join(keywords)}[/green]")
        
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Time", style="cyan", width=12)
        table.add_column("Keyword", style="yellow", width=15)
        table.add_column("Context", style="white", width=60)
        
        for match in matches:
            # Create highlighted context text
            context_text = Text(match['context'])
            table.add_row(
                match['formatted_time'],
                match['keyword'],
                match['context']
            )
        
        console.print(table)
        
        # Save search results to file
        return matches


@click.command()
@click.argument('video_path', type=click.Path(exists=True))
@click.option('--model', '-m', default='base', 
              type=click.Choice(['tiny', 'base', 'small', 'medium', 'large']),
              help='Whisper model size (default: base)')
@click.option('--output-dir', '-o', type=click.Path(), 
              help='Output directory for transcripts (default: same as video)')
@click.option('--format', '-f', 'output_format', default='txt',
              type=click.Choice(['json', 'txt', 'csv']),
              help='Output format (default: txt)')
@click.option('--search', '-s', multiple=True,
              help='Keywords to search for (can be used multiple times)')
@click.option('--context', '-c', default=5, type=int,
              help='Number of context words around keywords (default: 5)')
@click.option('--save-search', is_flag=True,
              help='Save search results to a separate file')
def main(video_path, model, output_dir, output_format, search, context, save_search):
    """
    Transcribe a video file using OpenAI Whisper and optionally search for keywords.
    
    VIDEO_PATH: Path to the video file to transcribe
    """
    
    console.print(Panel.fit(
        "[bold blue]Video Transcription Tool with Keyword Search[/bold blue]\n"
        "Powered by OpenAI Whisper",
        style="blue"
    ))
    
    # Initialize transcriber
    transcriber = VideoTranscriber(model_size=model)
    
    # Transcribe video
    transcript_data = transcriber.transcribe_video(video_path, output_dir)
    
    if not transcript_data:
        console.print("[red]Transcription failed![/red]")
        sys.exit(1)
    
    # Set up output paths
    video_path = Path(video_path)
    if output_dir:
        output_dir = Path(output_dir)
    else:
        output_dir = video_path.parent
    
    # Save transcript
    transcript_file = output_dir / f"{video_path.stem}_transcript.{output_format}"
    transcriber.save_transcript(transcript_data, transcript_file, output_format)
    
    # Search for keywords if provided
    if search:
        keywords = list(search)
        console.print(f"\n[yellow]Searching for keywords: {', '.join(keywords)}[/yellow]")
        
        matches = transcriber.search_keywords(transcript_data, keywords, context)
        transcriber.display_search_results(matches, keywords)
        
        # Save search results if requested
        if save_search and matches:
            search_file = output_dir / f"{video_path.stem}_search_results.json"
            try:
                search_data = {
                    'video_file': str(video_path),
                    'keywords': keywords,
                    'timestamp': datetime.now().isoformat(),
                    'matches': matches
                }
                with open(search_file, 'w', encoding='utf-8') as f:
                    json.dump(search_data, f, indent=2, ensure_ascii=False)
                console.print(f"[green]✓ Search results saved to {search_file}[/green]")
            except Exception as e:
                console.print(f"[red]✗ Error saving search results: {e}[/red]")
    
    console.print(f"\n[green]✓ Processing complete![/green]")
    console.print(f"[blue]Full transcript: {transcript_file}[/blue]")
    
    if search and matches:
        console.print(f"[blue]Found {len(matches)} keyword matches[/blue]")


if __name__ == '__main__':
    main()
