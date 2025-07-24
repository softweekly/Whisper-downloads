#!/usr/bin/env python3
"""
Demo script for the Video Transcription Tool
Shows basic usage examples
"""

from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax

console = Console()

def show_demo():
    """Display demo information and usage examples"""
    
    console.print(Panel.fit(
        "[bold blue]Video Transcription Tool - Demo & Examples[/bold blue]\n"
        "Learn how to use the transcription tools",
        style="blue"
    ))
    
    console.print("\n[bold cyan]🎯 Quick Start Guide[/bold cyan]")
    console.print("1. [green]Interactive Mode[/green] (Easiest - Recommended for beginners)")
    console.print("2. [yellow]Command Line[/yellow] (For advanced users)")
    console.print("3. [magenta]Batch Processing[/magenta] (For multiple videos)")
    
    console.print("\n[bold cyan]📁 What you need:[/bold cyan]")
    console.print("• A video file (MP4, AVI, MOV, MKV, etc.)")
    console.print("• About 5-10 minutes for processing (depends on video length)")
    console.print("• Keywords you want to search for (optional)")
    
    # Interactive mode example
    console.print("\n[bold green]🎮 Method 1: Interactive Mode[/bold green]")
    interactive_code = r'''# Run this command:
.\.venv\Scripts\python.exe interactive_transcriber.py

# Then follow the prompts:
# 1. Enter video file path
# 2. Choose model size (recommend 'base')
# 3. Select output format (recommend 'txt')
# 4. Add keywords to search for
# 5. Get your results!'''
    
    console.print(Syntax(interactive_code, "bash", theme="monokai", line_numbers=True))
    
    # Command line examples
    console.print("\n[bold yellow]⚡ Method 2: Command Line Examples[/bold yellow]")
    
    console.print("\n[dim]Basic transcription:[/dim]")
    basic_code = r'''.\.venv\Scripts\python.exe video_transcriber.py "my_video.mp4"'''
    console.print(Syntax(basic_code, "bash", theme="monokai"))
    
    console.print("\n[dim]With keyword search:[/dim]")
    keyword_code = r'''.\.venv\Scripts\python.exe video_transcriber.py "lecture.mp4" --search "quantum" --search "physics"'''
    console.print(Syntax(keyword_code, "bash", theme="monokai"))
    
    console.print("\n[dim]High accuracy + CSV output:[/dim]")
    advanced_code = r'''.\.venv\Scripts\python.exe video_transcriber.py "interview.mp4" --model medium --format csv --search "important" --save-search'''
    console.print(Syntax(advanced_code, "bash", theme="monokai"))
    
    # Batch processing
    console.print("\n[bold magenta]📦 Method 3: Batch Processing[/bold magenta]")
    batch_code = r'''# Process all videos in a folder:
.\.venv\Scripts\python.exe batch_transcriber.py

# It will:
# 1. Find all video files in your chosen directory
# 2. Ask for processing settings
# 3. Process all videos with same settings
# 4. Generate a summary report'''
    
    console.print(Syntax(batch_code, "bash", theme="monokai", line_numbers=True))
    
    # Expected output
    console.print("\n[bold cyan]📋 What you'll get:[/bold cyan]")
    console.print("• [blue]Full transcript[/blue] with timestamps")
    console.print("• [green]Keyword search results[/green] (if you searched)")
    console.print("• [yellow]Easy-to-read format[/yellow] or spreadsheet-ready CSV")
    console.print("• [magenta]Context around keywords[/magenta] for better understanding")
    
    # File examples
    console.print("\n[bold cyan]📄 Output File Examples:[/bold cyan]")
    
    console.print("\n[dim]TXT format (human-readable):[/dim]")
    txt_example = '''[00:01:23 - 00:01:28] Welcome to today's presentation on artificial intelligence.
[00:01:28 - 00:01:35] We'll be discussing machine learning algorithms and their applications.
[00:01:35 - 00:01:42] First, let's understand what makes AI so powerful in modern technology.'''
    console.print(Syntax(txt_example, "text", theme="monokai"))
    
    console.print("\n[dim]Keyword search results:[/dim]")
    search_example = '''┏━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Time       ┃ Keyword       ┃ Context                                           ┃
┡━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ 00:01:28   │ machine       │ discussing **machine** learning algorithms and   │
│ 00:01:35   │ AI            │ understand what makes **AI** so powerful in      │
└────────────┴───────────────┴───────────────────────────────────────────────────┘'''
    console.print(search_example)
    
    # Tips
    console.print("\n[bold cyan]💡 Pro Tips:[/bold cyan]")
    console.print("• Start with the [green]interactive mode[/green] - it's much easier!")
    console.print("• Use [yellow]'base' model[/yellow] for good balance of speed and accuracy")
    console.print("• [blue]Clear audio[/blue] = better transcription results")
    console.print("• Try [magenta]multiple keywords[/magenta] to find everything you need")
    console.print("• Use [cyan]batch processing[/cyan] for multiple videos with same settings")
    
    console.print(f"\n[bold green]🚀 Ready to start? Run one of the commands above![/bold green]")
    console.print(f"[dim]Need help? Check the README.md file for detailed instructions.[/dim]")

if __name__ == '__main__':
    show_demo()
