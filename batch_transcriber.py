#!/usr/bin/env python3
"""
Batch Video Transcriber
Process multiple video files at once
"""

import os
import sys
from pathlib import Path
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich.progress import Progress, track
import json
from datetime import datetime

# Import our main transcriber
from video_transcriber import VideoTranscriber

console = Console()

def find_video_files(directory, recursive=True):
    """Find all video files in a directory"""
    video_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm', '.m4v'}
    video_files = []
    
    search_path = Path(directory)
    
    if recursive:
        pattern = "**/*"
    else:
        pattern = "*"
    
    for file_path in search_path.glob(pattern):
        if file_path.is_file() and file_path.suffix.lower() in video_extensions:
            video_files.append(file_path)
    
    return sorted(video_files)

def batch_transcribe(video_files, model_size, output_format, keywords=None, output_base_dir=None):
    """Transcribe multiple video files"""
    transcriber = VideoTranscriber(model_size=model_size)
    
    results = {
        'processed': [],
        'failed': [],
        'keyword_matches': {},
        'start_time': datetime.now().isoformat()
    }
    
    with Progress() as progress:
        task = progress.add_task("[cyan]Processing videos...", total=len(video_files))
        
        for video_path in video_files:
            progress.update(task, description=f"[cyan]Processing: {video_path.name}")
            
            try:
                # Set output directory
                if output_base_dir:
                    output_dir = Path(output_base_dir) / video_path.stem
                    output_dir.mkdir(parents=True, exist_ok=True)
                else:
                    output_dir = video_path.parent
                
                # Transcribe video
                transcript_data = transcriber.transcribe_video(str(video_path), str(output_dir))
                
                if transcript_data:
                    # Save transcript
                    transcript_file = output_dir / f"{video_path.stem}_transcript.{output_format}"
                    if transcriber.save_transcript(transcript_data, transcript_file, output_format):
                        
                        result_info = {
                            'video_file': str(video_path),
                            'transcript_file': str(transcript_file),
                            'success': True,
                            'duration': transcript_data.get('text', ''),
                            'segments_count': len(transcript_data.get('segments', []))
                        }
                        
                        # Search for keywords if provided
                        if keywords:
                            matches = transcriber.search_keywords(transcript_data, keywords, context_words=5)
                            if matches:
                                results['keyword_matches'][str(video_path)] = matches
                                result_info['keyword_matches'] = len(matches)
                                
                                # Save search results
                                search_file = output_dir / f"{video_path.stem}_search_results.json"
                                search_data = {
                                    'video_file': str(video_path),
                                    'keywords': keywords,
                                    'matches': matches
                                }
                                with open(search_file, 'w', encoding='utf-8') as f:
                                    json.dump(search_data, f, indent=2, ensure_ascii=False)
                                result_info['search_results_file'] = str(search_file)
                        
                        results['processed'].append(result_info)
                        console.print(f"[green]✓ {video_path.name}[/green]")
                    else:
                        raise Exception("Failed to save transcript")
                else:
                    raise Exception("Transcription failed")
                    
            except Exception as e:
                error_info = {
                    'video_file': str(video_path),
                    'error': str(e),
                    'success': False
                }
                results['failed'].append(error_info)
                console.print(f"[red]✗ {video_path.name}: {e}[/red]")
            
            progress.advance(task)
    
    results['end_time'] = datetime.now().isoformat()
    return results

def main():
    """Main batch processing function"""
    console.print(Panel.fit(
        "[bold blue]Batch Video Transcriber[/bold blue]\n"
        "Process multiple video files at once\n"
        "Powered by OpenAI Whisper",
        style="blue"
    ))
    
    try:
        # Get source directory
        source_dir = Prompt.ask("\n[cyan]Enter directory containing video files[/cyan]")
        source_path = Path(source_dir.strip('"').strip("'"))
        
        if not source_path.exists() or not source_path.is_dir():
            console.print(f"[red]Directory not found: {source_path}[/red]")
            return
        
        # Search for video files
        recursive = Confirm.ask("Search subdirectories recursively?", default=True)
        video_files = find_video_files(source_path, recursive)
        
        if not video_files:
            console.print("[yellow]No video files found in the specified directory[/yellow]")
            return
        
        console.print(f"\n[green]Found {len(video_files)} video files:[/green]")
        for i, video_file in enumerate(video_files[:10], 1):  # Show first 10
            console.print(f"  {i}. {video_file.name}")
        
        if len(video_files) > 10:
            console.print(f"  ... and {len(video_files) - 10} more")
        
        if not Confirm.ask(f"\nProcess all {len(video_files)} files?"):
            return
        
        # Get processing options
        console.print("\n[cyan]Choose Whisper model size:[/cyan]")
        console.print("1. tiny    - Fastest, least accurate")
        console.print("2. base    - Good balance (recommended)")
        console.print("3. small   - Better accuracy, slower")
        console.print("4. medium  - High accuracy, much slower")
        console.print("5. large   - Best accuracy, very slow")
        
        model_choice = Prompt.ask("Select model", choices=["1", "2", "3", "4", "5"], default="2")
        models = {"1": "tiny", "2": "base", "3": "small", "4": "medium", "5": "large"}
        model_size = models[model_choice]
        
        # Output format
        console.print("\n[cyan]Choose output format:[/cyan]")
        format_choice = Prompt.ask("Format", choices=["txt", "csv", "json"], default="txt")
        
        # Keywords
        keywords = []
        if Confirm.ask("\n[cyan]Search for keywords in all videos?[/cyan]"):
            console.print("[yellow]Enter keywords separated by commas:[/yellow]")
            keywords_input = Prompt.ask("Keywords")
            if keywords_input.strip():
                keywords = [k.strip() for k in keywords_input.split(',') if k.strip()]
        
        # Output directory
        output_base_dir = None
        if Confirm.ask("\n[cyan]Save all outputs to a separate directory?[/cyan]"):
            output_dir_str = Prompt.ask("Output directory path")
            output_base_dir = Path(output_dir_str.strip('"').strip("'"))
            output_base_dir.mkdir(parents=True, exist_ok=True)
        
        # Process files
        console.print(f"\n[yellow]Starting batch processing...[/yellow]")
        console.print(f"Files: {len(video_files)}")
        console.print(f"Model: {model_size}")
        console.print(f"Format: {format_choice}")
        if keywords:
            console.print(f"Keywords: {', '.join(keywords)}")
        
        results = batch_transcribe(
            video_files, 
            model_size, 
            format_choice, 
            keywords if keywords else None,
            output_base_dir
        )
        
        # Save batch results
        batch_results_file = (output_base_dir or source_path) / f"batch_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(batch_results_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        # Display summary
        console.print(f"\n[green]✓ Batch processing complete![/green]")
        console.print(f"[blue]Successfully processed: {len(results['processed'])}[/blue]")
        console.print(f"[blue]Failed: {len(results['failed'])}[/blue]")
        
        if keywords and results['keyword_matches']:
            total_matches = sum(len(matches) for matches in results['keyword_matches'].values())
            console.print(f"[blue]Total keyword matches: {total_matches}[/blue]")
        
        console.print(f"[blue]Batch results saved: {batch_results_file}[/blue]")
        
        # Show failed files if any
        if results['failed']:
            console.print(f"\n[red]Failed files:[/red]")
            for failed in results['failed']:
                console.print(f"  • {Path(failed['video_file']).name}: {failed['error']}")
        
    except KeyboardInterrupt:
        console.print("\n[yellow]Process interrupted by user[/yellow]")
    except Exception as e:
        console.print(f"\n[red]Error: {e}[/red]")

if __name__ == '__main__':
    main()
