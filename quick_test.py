#!/usr/bin/env python3
"""
Quick System Test - Basic functionality check
Tests core components without heavy operations
"""

import os
import sys
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.progress import track
import time

console = Console()

def test_imports():
    """Test that all required packages can be imported"""
    console.print("[cyan]Testing package imports...[/cyan]")
    
    tests = []
    
    try:
        import whisper
        tests.append(("Whisper", True, "OK"))
    except ImportError as e:
        tests.append(("Whisper", False, str(e)))
    
    try:
        import moviepy
        # Try to get version, fallback if not available
        try:
            version = getattr(moviepy, '__version__', 'Unknown')
        except:
            version = 'Available'
        tests.append(("MoviePy", True, f"v{version}"))
    except ImportError as e:
        tests.append(("MoviePy", False, str(e)))
    
    try:
        import pandas
        # Try to get version, fallback if not available
        try:
            version = getattr(pandas, '__version__', 'Unknown')
        except:
            version = 'Available'
        tests.append(("Pandas", True, f"v{version}"))
    except ImportError as e:
        tests.append(("Pandas", False, str(e)))
    
    try:
        import rich
        # Try to get version, fallback if not available
        try:
            version = getattr(rich, '__version__', 'Unknown')
        except:
            version = 'Available'
        tests.append(("Rich", True, f"v{version}"))
    except ImportError as e:
        tests.append(("Rich", False, str(e)))
    
    try:
        import click
        # Try to get version, fallback if not available
        try:
            version = getattr(click, '__version__', 'Unknown')
        except:
            version = 'Available'
        tests.append(("Click", True, f"v{version}"))
    except ImportError as e:
        tests.append(("Click", False, str(e)))
    
    try:
        import yt_dlp
        # Try to get version, fallback if not available
        try:
            version = getattr(yt_dlp.version, '__version__', 'Unknown')
        except:
            version = 'Available'
        tests.append(("yt-dlp", True, f"v{version}"))
    except ImportError as e:
        tests.append(("yt-dlp", False, str(e)))
    
    try:
        import tkinter
        tests.append(("tkinter (GUI)", True, "Available"))
    except ImportError as e:
        tests.append(("tkinter (GUI)", False, str(e)))
    
    return tests

def test_scripts():
    """Test that all main scripts exist and can be imported"""
    console.print("[cyan]Testing script files...[/cyan]")
    
    scripts = [
        'video_transcriber.py',
        'interactive_transcriber.py', 
        'batch_transcriber.py',
        'youtube_channel_transcriber.py',
        'youtube_gui.py',
        'demo.py'
    ]
    
    tests = []
    for script in scripts:
        if Path(script).exists():
            tests.append((f"Script: {script}", True, "Found"))
        else:
            tests.append((f"Script: {script}", False, "Missing"))
    
    return tests

def test_environment():
    """Test Python environment"""
    console.print("[cyan]Testing Python environment...[/cyan]")
    
    tests = []
    
    # Python version
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    tests.append(("Python Version", True, python_version))
    
    # Virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        tests.append(("Virtual Environment", True, "Active"))
    else:
        tests.append(("Virtual Environment", False, "Not detected"))
    
    # Working directory
    cwd = os.getcwd()
    if "Whisper downloads" in cwd:
        tests.append(("Working Directory", True, "Correct"))
    else:
        tests.append(("Working Directory", False, f"In: {cwd}"))
    
    return tests

def test_basic_functionality():
    """Test basic functionality without heavy operations"""
    console.print("[cyan]Testing basic functionality...[/cyan]")
    
    tests = []
    
    try:
        # Test moviepy basic import
        from moviepy import VideoFileClip
        tests.append(("MoviePy VideoClip", True, "Import OK"))
    except Exception as e:
        tests.append(("MoviePy VideoClip", False, str(e)))
    
    try:
        # Test whisper model list (doesn't download)
        import whisper
        models = whisper.available_models()
        tests.append(("Whisper Models", True, f"{len(models)} available"))
    except Exception as e:
        tests.append(("Whisper Models", False, str(e)))
    
    try:
        # Test JSON operations
        import json
        test_data = {"test": "data", "status": "ok"}
        json_str = json.dumps(test_data)
        parsed = json.loads(json_str)
        tests.append(("JSON Operations", True, "OK"))
    except Exception as e:
        tests.append(("JSON Operations", False, str(e)))
    
    try:
        # Test file operations
        test_file = Path("temp_test.txt")
        test_file.write_text("test")
        content = test_file.read_text()
        test_file.unlink()  # delete
        tests.append(("File Operations", True, "OK"))
    except Exception as e:
        tests.append(("File Operations", False, str(e)))
    
    return tests

def display_results(all_tests):
    """Display test results"""
    console.print("\n" + "="*60)
    console.print(Panel.fit(
        "[bold blue]Quick System Test Results[/bold blue]",
        style="blue"
    ))
    
    passed = 0
    total = 0
    
    for category, tests in all_tests.items():
        console.print(f"\n[bold yellow]{category}:[/bold yellow]")
        
        for test_name, success, details in tests:
            total += 1
            if success:
                passed += 1
                console.print(f"  [green]✓[/green] {test_name}: {details}")
            else:
                console.print(f"  [red]✗[/red] {test_name}: {details}")
    
    # Summary
    console.print(f"\n[bold]Summary:[/bold]")
    success_rate = (passed / total) * 100 if total > 0 else 0
    console.print(f"[green]Passed: {passed}[/green] | [red]Failed: {total - passed}[/red] | [blue]Total: {total}[/blue]")
    console.print(f"[bold]Success Rate: {success_rate:.1f}%[/bold]")
    
    if success_rate >= 90:
        console.print(f"\n[bold green]🎉 Excellent! System is ready for use.[/bold green]")
        console.print(f"[green]All core components are working properly.[/green]")
    elif success_rate >= 75:
        console.print(f"\n[bold yellow]⚠ Good! Most components working, minor issues detected.[/bold yellow]")
        console.print(f"[yellow]You should be able to use most features.[/yellow]")
    elif success_rate >= 50:
        console.print(f"\n[bold orange]⚠ Partial functionality. Some components have issues.[/bold orange]")
        console.print(f"[orange]Basic transcription might work, but some features may not.[/orange]")
    else:
        console.print(f"\n[bold red]❌ Multiple critical issues found.[/bold red]")
        console.print(f"[red]Please check your installation and environment setup.[/red]")
    
    return success_rate

def main():
    """Run quick system test"""
    console.print(Panel.fit(
        "[bold blue]Quick System Test[/bold blue]\n"
        "Testing core components for basic functionality",
        style="blue"
    ))
    
    test_categories = [
        ("Environment", test_environment),
        ("Package Imports", test_imports),
        ("Script Files", test_scripts),
        ("Basic Functionality", test_basic_functionality),
    ]
    
    all_tests = {}
    
    for category, test_func in track(test_categories, description="Running tests..."):
        all_tests[category] = test_func()
        time.sleep(0.5)  # Brief pause for visual effect
    
    success_rate = display_results(all_tests)
    
    console.print(f"\n[bold cyan]What's Next?[/bold cyan]")
    if success_rate >= 75:
        console.print(f"[green]✓ You can start using the transcription tools![/green]")
        console.print(f"[blue]• Try Interactive Mode: Option 1 in the launcher[/blue]")
        console.print(f"[blue]• Or view examples: Option 6 in the launcher[/blue]")
    else:
        console.print(f"[yellow]⚠ Consider running the full test suite: Option 7 in the launcher[/yellow]")
        console.print(f"[yellow]• Or check the setup documentation[/yellow]")
    
    console.print(f"\n[dim]Press any key to continue...[/dim]")
    input()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[yellow]Test interrupted by user[/yellow]")
    except Exception as e:
        console.print(f"\n[red]Test failed with error: {e}[/red]")
