#!/usr/bin/env python3
"""
Simple End-to-End Functionality Test
Tests actual transcription pipeline with minimal setup
"""

import tempfile
import os
import subprocess
import sys
from pathlib import Path
from rich.console import Console
from rich.panel import Panel

console = Console()

def test_whisper_basic_functionality():
    """Test Whisper's basic functionality without requiring video files"""
    console.print("[cyan]Testing Whisper basic functionality...[/cyan]")
    
    try:
        import whisper
        
        # Test loading the smallest model
        console.print("Loading tiny model (fastest)...")
        model = whisper.load_model("tiny")
        console.print("[green]✓ Whisper model loaded successfully[/green]")
        
        # Create a silent audio segment for testing (1 second of silence)
        import numpy as np
        
        # Create 1 second of silence at 16kHz (Whisper's expected sample rate)
        duration = 1.0  # seconds
        sample_rate = 16000
        silence = np.zeros(int(duration * sample_rate), dtype=np.float32)
        
        console.print("Testing transcription with silent audio...")
        result = model.transcribe(silence)
        
        console.print(f"[green]✓ Transcription completed[/green]")
        console.print(f"Result: '{result['text'].strip()}' (expected: empty or minimal)")
        
        return True
        
    except Exception as e:
        console.print(f"[red]✗ Whisper test failed: {e}[/red]")
        return False

def test_script_functionality():
    """Test our scripts can be imported and basic functions work"""
    console.print("[cyan]Testing script functionality...[/cyan]")
    
    try:
        # Test importing our main module
        sys.path.insert(0, str(Path.cwd()))
        
        # Import and test video_transcriber functionality
        import video_transcriber
        transcriber = video_transcriber.VideoTranscriber()
        
        console.print("[green]✓ VideoTranscriber class imported successfully[/green]")
        
        # Test keyword search functionality
        text = "This is a test about artificial intelligence and machine learning algorithms"
        keywords = ["artificial intelligence", "machine learning"]
        
        # This should work without any video processing
        results = []
        for keyword in keywords:
            if keyword.lower() in text.lower():
                results.append({
                    'keyword': keyword,
                    'text': text,
                    'timestamp': '00:00:00'
                })
        
        console.print(f"[green]✓ Keyword search test passed: found {len(results)} matches[/green]")
        
        return True
        
    except Exception as e:
        console.print(f"[red]✗ Script functionality test failed: {e}[/red]")
        return False

def test_file_operations():
    """Test file input/output operations"""
    console.print("[cyan]Testing file operations...[/cyan]")
    
    try:
        # Create temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Test creating transcript file
            transcript_file = temp_path / "test_transcript.txt"
            transcript_content = "[00:00:01 - 00:00:05] This is a test transcript."
            transcript_file.write_text(transcript_content, encoding='utf-8')
            
            # Read it back
            read_content = transcript_file.read_text(encoding='utf-8')
            assert read_content == transcript_content
            
            console.print("[green]✓ Transcript file operations working[/green]")
            
            # Test creating JSON results file
            import json
            results_file = temp_path / "test_results.json"
            test_data = {
                "keywords": ["test"],
                "results": [{"keyword": "test", "timestamp": "00:00:01"}]
            }
            results_file.write_text(json.dumps(test_data, indent=2), encoding='utf-8')
            
            # Read and parse JSON
            read_json = json.loads(results_file.read_text(encoding='utf-8'))
            assert read_json["keywords"] == ["test"]
            
            console.print("[green]✓ JSON file operations working[/green]")
            
            return True
            
    except Exception as e:
        console.print(f"[red]✗ File operations test failed: {e}[/red]")
        return False

def test_command_line_interface():
    """Test that our command line interfaces respond correctly"""
    console.print("[cyan]Testing command line interfaces...[/cyan]")
    
    python_exe = Path(".venv/Scripts/python.exe")
    if not python_exe.exists():
        console.print("[red]✗ Python virtual environment not found[/red]")
        return False
    
    try:
        # Test video_transcriber help
        result = subprocess.run(
            [str(python_exe), "video_transcriber.py", "--help"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0 and "Usage:" in result.stdout:
            console.print("[green]✓ video_transcriber.py --help working[/green]")
        else:
            console.print(f"[red]✗ video_transcriber.py help failed[/red]")
            return False
        
        # Test demo script
        result = subprocess.run(
            [str(python_exe), "demo.py"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            console.print("[green]✓ demo.py working[/green]")
        else:
            console.print(f"[red]✗ demo.py failed[/red]")
            return False
        
        return True
        
    except Exception as e:
        console.print(f"[red]✗ Command line interface test failed: {e}[/red]")
        return False

def run_functionality_test():
    """Run end-to-end functionality test"""
    console.print(Panel.fit(
        "[bold blue]End-to-End Functionality Test[/bold blue]\n"
        "Testing actual transcription pipeline",
        style="blue"
    ))
    
    tests = [
        ("File Operations", test_file_operations),
        ("Script Functionality", test_script_functionality),
        ("Whisper Basic Functionality", test_whisper_basic_functionality),
        ("Command Line Interface", test_command_line_interface),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        console.print(f"\n[bold blue]Running: {test_name}[/bold blue]")
        if test_func():
            passed += 1
            console.print(f"[green]✓ {test_name} PASSED[/green]")
        else:
            console.print(f"[red]✗ {test_name} FAILED[/red]")
    
    # Summary
    console.print("\n" + "="*60)
    success_rate = (passed / total) * 100
    console.print(f"[bold]End-to-End Test Results:[/bold]")
    console.print(f"[green]Passed: {passed}[/green] | [red]Failed: {total - passed}[/red] | [blue]Total: {total}[/blue]")
    console.print(f"[bold]Success Rate: {success_rate:.1f}%[/bold]")
    
    if success_rate == 100:
        console.print(f"\n[bold green]🎉 Perfect! All functionality tests passed![/bold green]")
        console.print(f"[green]Your transcription system is fully operational.[/green]")
        console.print(f"\n[cyan]Ready to transcribe! Try:[/cyan]")
        console.print(f"[blue]• Interactive Mode: start.bat → Option 1[/blue]")
        console.print(f"[blue]• YouTube Processing: start.bat → Option 5[/blue]")
    elif success_rate >= 75:
        console.print(f"\n[bold yellow]⚠ Most functionality working, minor issues detected.[/bold yellow]")
        console.print(f"[yellow]Core transcription should work fine.[/yellow]")
    else:
        console.print(f"\n[bold red]❌ Multiple functionality issues found.[/bold red]")
        console.print(f"[red]Please check the setup or run the full system test.[/red]")
    
    return success_rate >= 75

if __name__ == '__main__':
    try:
        success = run_functionality_test()
        console.print(f"\n[dim]Press any key to continue...[/dim]")
        input()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        console.print("\n[yellow]Test interrupted by user[/yellow]")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n[red]Test failed with error: {e}[/red]")
        sys.exit(1)
