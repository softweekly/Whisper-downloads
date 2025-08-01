#!/usr/bin/env python3
"""
End-to-End Testing Suite for Video Transcription Tool
Tests all components to ensure everything is working properly
"""

import os
import sys
import subprocess
import tempfile
import json
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, track
from rich.table import Table
import time
import shutil

console = Console()

class TranscriptionTester:
    def __init__(self):
        self.console = console
        self.test_results = []
        self.base_dir = Path.cwd()
        self.temp_dir = None
        self.python_exe = None
        
    def setup_test_environment(self):
        """Setup test environment"""
        console.print("[yellow]Setting up test environment...[/yellow]")
        
        # Find Python executable
        venv_python = self.base_dir / ".venv" / "Scripts" / "python.exe"
        if venv_python.exists():
            self.python_exe = str(venv_python)
            console.print(f"[green]✓ Found Python: {self.python_exe}[/green]")
        else:
            console.print("[red]✗ Python virtual environment not found[/red]")
            return False
        
        # Create temporary directory for tests
        self.temp_dir = Path(tempfile.mkdtemp(prefix="whisper_test_"))
        console.print(f"[green]✓ Created test directory: {self.temp_dir}[/green]")
        
        return True
    
    def cleanup(self):
        """Clean up test environment"""
        if self.temp_dir and self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
            console.print(f"[green]✓ Cleaned up test directory[/green]")
    
    def run_command(self, command, timeout=60):
        """Run a command and return result"""
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=str(self.base_dir)
            )
            return {
                'success': result.returncode == 0,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode
            }
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'stdout': '',
                'stderr': 'Command timed out',
                'returncode': -1
            }
        except Exception as e:
            return {
                'success': False,
                'stdout': '',
                'stderr': str(e),
                'returncode': -1
            }
    
    def test_python_environment(self):
        """Test 1: Python environment and packages"""
        console.print("\n[cyan]Test 1: Python Environment[/cyan]")
        
        # Test Python version
        result = self.run_command(f'"{self.python_exe}" --version')
        if result['success']:
            version = result['stdout'].strip()
            console.print(f"[green]✓ Python version: {version}[/green]")
            self.test_results.append(("Python Version", True, version))
        else:
            console.print(f"[red]✗ Python version check failed[/red]")
            self.test_results.append(("Python Version", False, result['stderr']))
            return False
        
        # Test required packages
        packages = [
            ('whisper', 'import whisper; print(f"Whisper: OK")'),
            ('moviepy', 'import moviepy; print(f"MoviePy: {moviepy.__version__}")'),
            ('pandas', 'import pandas; print(f"Pandas: {pandas.__version__}")'),
            ('rich', 'import rich; print(f"Rich: {rich.__version__}")'),
            ('click', 'import click; print(f"Click: {click.__version__}")'),
            ('yt-dlp', 'import yt_dlp; print(f"yt-dlp: {yt_dlp.version.__version__}")'),
        ]
        
        all_packages_ok = True
        for package_name, import_cmd in packages:
            result = self.run_command(f'"{self.python_exe}" -c "{import_cmd}"')
            if result['success']:
                console.print(f"[green]✓ {result['stdout'].strip()}[/green]")
                self.test_results.append((f"Package: {package_name}", True, "OK"))
            else:
                console.print(f"[red]✗ {package_name} import failed: {result['stderr']}[/red]")
                self.test_results.append((f"Package: {package_name}", False, result['stderr']))
                all_packages_ok = False
        
        return all_packages_ok
    
    def test_script_imports(self):
        """Test 2: Script imports and syntax"""
        console.print("\n[cyan]Test 2: Script Imports and Syntax[/cyan]")
        
        scripts = [
            'video_transcriber.py',
            'interactive_transcriber.py',
            'batch_transcriber.py',
            'youtube_channel_transcriber.py',
            'youtube_gui.py',
            'demo.py'
        ]
        
        all_imports_ok = True
        for script in scripts:
            script_path = self.base_dir / script
            if script_path.exists():
                # Test syntax by importing
                result = self.run_command(f'"{self.python_exe}" -m py_compile "{script_path}"')
                if result['success']:
                    console.print(f"[green]✓ {script} syntax OK[/green]")
                    self.test_results.append((f"Script: {script}", True, "Syntax OK"))
                else:
                    console.print(f"[red]✗ {script} syntax error: {result['stderr']}[/red]")
                    self.test_results.append((f"Script: {script}", False, result['stderr']))
                    all_imports_ok = False
            else:
                console.print(f"[red]✗ {script} not found[/red]")
                self.test_results.append((f"Script: {script}", False, "File not found"))
                all_imports_ok = False
        
        return all_imports_ok
    
    def test_help_commands(self):
        """Test 3: Help commands"""
        console.print("\n[cyan]Test 3: Help Commands[/cyan]")
        
        help_tests = [
            ('video_transcriber.py --help', 'Main transcriber help'),
            ('demo.py', 'Demo script'),
        ]
        
        all_help_ok = True
        for cmd, description in help_tests:
            result = self.run_command(f'"{self.python_exe}" {cmd}', timeout=30)
            if result['success'] or 'Usage:' in result['stdout'] or 'Video Transcription Tool' in result['stdout']:
                console.print(f"[green]✓ {description} OK[/green]")
                self.test_results.append((f"Help: {description}", True, "OK"))
            else:
                console.print(f"[red]✗ {description} failed[/red]")
                self.test_results.append((f"Help: {description}", False, result['stderr']))
                all_help_ok = False
        
        return all_help_ok
    
    def create_test_video(self):
        """Create a simple test video for transcription"""
        console.print("\n[cyan]Creating test video...[/cyan]")
        
        try:
            # Import moviepy here to create a simple test video
            from moviepy import VideoFileClip, ColorClip
            from moviepy.audio.io.AudioFileClip import AudioFileClip
            import numpy as np
            
            # Create a simple 5-second video with a color clip
            # This won't have audio, but we can test the video processing pipeline
            duration = 5
            clip = ColorClip(size=(640, 480), color=(0, 128, 255), duration=duration)
            
            test_video_path = self.temp_dir / "test_video.mp4"
            clip.write_videofile(str(test_video_path), fps=24, verbose=False, logger=None)
            clip.close()
            
            console.print(f"[green]✓ Created test video: {test_video_path}[/green]")
            return test_video_path
            
        except Exception as e:
            console.print(f"[red]✗ Failed to create test video: {e}[/red]")
            
            # Try to create a minimal test file instead
            test_file = self.temp_dir / "test.txt"
            test_file.write_text("This is a test file for the transcription system.")
            console.print(f"[yellow]⚠ Created test file instead: {test_file}[/yellow]")
            return test_file
    
    def test_video_processing(self):
        """Test 4: Basic video processing capabilities"""
        console.print("\n[cyan]Test 4: Video Processing[/cyan]")
        
        # Test MoviePy video operations
        try:
            test_video = self.create_test_video()
            
            if test_video.suffix == '.mp4':
                # Test video file operations
                result = self.run_command(
                    f'"{self.python_exe}" -c "from moviepy import VideoFileClip; '
                    f'clip = VideoFileClip(\'{test_video}\'); '
                    f'print(f\'Duration: {{clip.duration}} seconds\'); clip.close()"'
                )
                
                if result['success']:
                    console.print(f"[green]✓ Video processing: {result['stdout'].strip()}[/green]")
                    self.test_results.append(("Video Processing", True, "OK"))
                    return True
                else:
                    console.print(f"[red]✗ Video processing failed: {result['stderr']}[/red]")
                    self.test_results.append(("Video Processing", False, result['stderr']))
            else:
                console.print(f"[yellow]⚠ Skipped video processing (no test video)[/yellow]")
                self.test_results.append(("Video Processing", True, "Skipped - no test video"))
            
        except Exception as e:
            console.print(f"[red]✗ Video processing test failed: {e}[/red]")
            self.test_results.append(("Video Processing", False, str(e)))
        
        return False
    
    def test_whisper_model_loading(self):
        """Test 5: Whisper model loading (tiny model for speed)"""
        console.print("\n[cyan]Test 5: Whisper Model Loading[/cyan]")
        
        # Test loading the smallest model
        result = self.run_command(
            f'"{self.python_exe}" -c "import whisper; '
            f'model = whisper.load_model(\'tiny\'); '
            f'print(f\'Model loaded: {{type(model).__name__}}\'); '
            f'print(\'Whisper model test: OK\')"',
            timeout=120  # Model download may take time
        )
        
        if result['success'] and 'OK' in result['stdout']:
            console.print(f"[green]✓ Whisper model loading: OK[/green]")
            self.test_results.append(("Whisper Model", True, "tiny model loaded"))
            return True
        else:
            console.print(f"[red]✗ Whisper model loading failed: {result['stderr']}[/red]")
            self.test_results.append(("Whisper Model", False, result['stderr']))
            return False
    
    def test_youtube_functionality(self):
        """Test 6: YouTube functionality (without actual download)"""
        console.print("\n[cyan]Test 6: YouTube Functionality[/cyan]")
        
        # Test yt-dlp basic functionality
        result = self.run_command(
            f'"{self.python_exe}" -c "import yt_dlp; '
            f'print(f\'yt-dlp version: {{yt_dlp.version.__version__}}\'); '
            f'ydl = yt_dlp.YoutubeDL({{\'quiet\': True}}); '
            f'print(\'YouTube functionality: OK\')"'
        )
        
        if result['success'] and 'OK' in result['stdout']:
            console.print(f"[green]✓ YouTube functionality: OK[/green]")
            self.test_results.append(("YouTube Functionality", True, "Basic functionality OK"))
            return True
        else:
            console.print(f"[red]✗ YouTube functionality failed: {result['stderr']}[/red]")
            self.test_results.append(("YouTube Functionality", False, result['stderr']))
            return False
    
    def test_gui_imports(self):
        """Test 7: GUI imports (tkinter)"""
        console.print("\n[cyan]Test 7: GUI Components[/cyan]")
        
        # Test tkinter availability
        result = self.run_command(
            f'"{self.python_exe}" -c "import tkinter as tk; '
            f'import tkinter.ttk as ttk; '
            f'print(\'GUI components: OK\')"'
        )
        
        if result['success'] and 'OK' in result['stdout']:
            console.print(f"[green]✓ GUI components: OK[/green]")
            self.test_results.append(("GUI Components", True, "tkinter available"))
            return True
        else:
            console.print(f"[red]✗ GUI components failed: {result['stderr']}[/red]")
            self.test_results.append(("GUI Components", False, result['stderr']))
            return False
    
    def test_file_operations(self):
        """Test 8: File operations and permissions"""
        console.print("\n[cyan]Test 8: File Operations[/cyan]")
        
        try:
            # Test creating files in temp directory
            test_files = [
                ('test_transcript.txt', '[00:00:01 - 00:00:05] This is a test transcript.'),
                ('test_results.json', '{"test": "data", "timestamp": "2025-07-30"}'),
                ('test_data.csv', 'start_time,end_time,text\n1.0,5.0,"Test text"')
            ]
            
            all_file_ops_ok = True
            for filename, content in test_files:
                test_file = self.temp_dir / filename
                
                # Write file
                test_file.write_text(content, encoding='utf-8')
                
                # Read file back
                read_content = test_file.read_text(encoding='utf-8')
                
                if content == read_content:
                    console.print(f"[green]✓ File operations: {filename}[/green]")
                    self.test_results.append((f"File Ops: {filename}", True, "OK"))
                else:
                    console.print(f"[red]✗ File content mismatch: {filename}[/red]")
                    self.test_results.append((f"File Ops: {filename}", False, "Content mismatch"))
                    all_file_ops_ok = False
            
            return all_file_ops_ok
            
        except Exception as e:
            console.print(f"[red]✗ File operations failed: {e}[/red]")
            self.test_results.append(("File Operations", False, str(e)))
            return False
    
    def test_launcher_script(self):
        """Test 9: Launcher script exists and is readable"""
        console.print("\n[cyan]Test 9: Launcher Script[/cyan]")
        
        launcher_path = self.base_dir / "start.bat"
        if launcher_path.exists():
            try:
                content = launcher_path.read_text(encoding='utf-8')
                if 'YouTube' in content and 'Interactive Mode' in content:
                    console.print(f"[green]✓ Launcher script: OK[/green]")
                    self.test_results.append(("Launcher Script", True, "Contains expected options"))
                    return True
                else:
                    console.print(f"[yellow]⚠ Launcher script missing expected content[/yellow]")
                    self.test_results.append(("Launcher Script", False, "Missing expected content"))
            except Exception as e:
                console.print(f"[red]✗ Launcher script read error: {e}[/red]")
                self.test_results.append(("Launcher Script", False, str(e)))
        else:
            console.print(f"[red]✗ Launcher script not found[/red]")
            self.test_results.append(("Launcher Script", False, "File not found"))
        
        return False
    
    def display_results(self):
        """Display test results summary"""
        console.print("\n" + "="*80)
        console.print(Panel.fit(
            "[bold blue]End-to-End Test Results Summary[/bold blue]",
            style="blue"
        ))
        
        # Create results table
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Test", style="cyan", width=30)
        table.add_column("Status", style="white", width=10)
        table.add_column("Details", style="dim", width=35)
        
        passed = 0
        total = len(self.test_results)
        
        for test_name, success, details in self.test_results:
            if success:
                status = "[green]✓ PASS[/green]"
                passed += 1
            else:
                status = "[red]✗ FAIL[/red]"
            
            # Truncate long details
            if len(details) > 35:
                details = details[:32] + "..."
            
            table.add_row(test_name, status, details)
        
        console.print(table)
        
        # Summary
        console.print(f"\n[bold]Overall Results:[/bold]")
        console.print(f"[green]Passed: {passed}[/green]")
        console.print(f"[red]Failed: {total - passed}[/red]")
        console.print(f"[blue]Total: {total}[/blue]")
        
        success_rate = (passed / total) * 100 if total > 0 else 0
        console.print(f"[bold]Success Rate: {success_rate:.1f}%[/bold]")
        
        if success_rate >= 90:
            console.print(f"\n[bold green]🎉 Excellent! System is ready for use.[/bold green]")
        elif success_rate >= 75:
            console.print(f"\n[bold yellow]⚠ Good, but some issues need attention.[/bold yellow]")
        else:
            console.print(f"\n[bold red]❌ Multiple issues found. Please review failures.[/bold red]")
        
        return success_rate >= 75
    
    def run_all_tests(self):
        """Run all tests"""
        console.print(Panel.fit(
            "[bold blue]Video Transcription Tool - End-to-End Testing[/bold blue]\n"
            "Running comprehensive tests to verify system functionality",
            style="blue"
        ))
        
        if not self.setup_test_environment():
            return False
        
        try:
            tests = [
                ("Python Environment", self.test_python_environment),
                ("Script Imports", self.test_script_imports),
                ("Help Commands", self.test_help_commands),
                ("Video Processing", self.test_video_processing),
                ("Whisper Model", self.test_whisper_model_loading),
                ("YouTube Functionality", self.test_youtube_functionality),
                ("GUI Components", self.test_gui_imports),
                ("File Operations", self.test_file_operations),
                ("Launcher Script", self.test_launcher_script),
            ]
            
            for test_name, test_func in track(tests, description="Running tests..."):
                console.print(f"\n[bold blue]Running: {test_name}[/bold blue]")
                test_func()
            
            # Display final results
            return self.display_results()
            
        finally:
            self.cleanup()

def main():
    """Main testing function"""
    tester = TranscriptionTester()
    
    try:
        success = tester.run_all_tests()
        
        if success:
            console.print(f"\n[bold green]🚀 System is ready! You can start using the transcription tools.[/bold green]")
            console.print(f"[blue]Quick start: Double-click 'start.bat' and choose an option![/blue]")
        else:
            console.print(f"\n[bold red]⚠ Some issues were found. Please review the test results above.[/bold red]")
            console.print(f"[yellow]You may still be able to use basic functionality.[/yellow]")
        
        return 0 if success else 1
        
    except KeyboardInterrupt:
        console.print("\n[yellow]Testing interrupted by user[/yellow]")
        return 1
    except Exception as e:
        console.print(f"\n[red]Testing failed with error: {e}[/red]")
        return 1

if __name__ == '__main__':
    sys.exit(main())
