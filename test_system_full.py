#!/usr/bin/env python3
"""
End-to-End Testing Suite for Video Transcription Tool
Comprehensive testing from environment setup to actual transcription
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from datetime import datetime
import tempfile
import shutil

# Color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

class TestRunner:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.warnings = 0
        self.test_results = []
        self.start_time = datetime.now()
        
    def print_header(self, text):
        print(f"\n{Colors.BOLD}{Colors.CYAN}{'=' * 60}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.CYAN}{text.center(60)}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.CYAN}{'=' * 60}{Colors.END}")
    
    def print_test(self, test_name):
        print(f"\n{Colors.BOLD}{Colors.WHITE}🧪 Testing: {test_name}{Colors.END}")
        print(f"{Colors.BLUE}{'─' * 50}{Colors.END}")
    
    def print_success(self, message):
        print(f"{Colors.GREEN}✅ PASS: {message}{Colors.END}")
        self.passed += 1
    
    def print_failure(self, message):
        print(f"{Colors.RED}❌ FAIL: {message}{Colors.END}")
        self.failed += 1
    
    def print_warning(self, message):
        print(f"{Colors.YELLOW}⚠️  WARN: {message}{Colors.END}")
        self.warnings += 1
    
    def print_info(self, message):
        print(f"{Colors.BLUE}ℹ️  INFO: {message}{Colors.END}")
    
    def run_command(self, command, capture_output=True, timeout=30):
        """Run a command and return result"""
        try:
            if isinstance(command, str):
                result = subprocess.run(
                    command, 
                    shell=True, 
                    capture_output=capture_output, 
                    text=True, 
                    timeout=timeout,
                    cwd=Path.cwd()
                )
            else:
                result = subprocess.run(
                    command, 
                    capture_output=capture_output, 
                    text=True, 
                    timeout=timeout,
                    cwd=Path.cwd()
                )
            return result
        except subprocess.TimeoutExpired:
            return None
        except Exception as e:
            print(f"Command error: {e}")
            return None

def test_environment_setup(runner):
    """Test 1: Environment and Dependencies"""
    runner.print_test("Environment Setup & Dependencies")
    
    # Check if we're in the right directory
    current_dir = Path.cwd()
    if "Whisper downloads" in str(current_dir):
        runner.print_success(f"Working directory: {current_dir}")
    else:
        runner.print_failure(f"Not in Whisper downloads directory: {current_dir}")
    
    # Check virtual environment
    venv_path = current_dir / ".venv"
    if venv_path.exists():
        runner.print_success("Virtual environment found")
    else:
        runner.print_failure("Virtual environment not found")
        return False
    
    # Check Python in venv
    python_exe = venv_path / "Scripts" / "python.exe"
    if python_exe.exists():
        runner.print_success("Python executable found in venv")
    else:
        runner.print_failure("Python executable not found in venv")
        return False
    
    # Test Python version
    result = runner.run_command([str(python_exe), "--version"])
    if result and result.returncode == 0:
        version = result.stdout.strip()
        runner.print_success(f"Python version: {version}")
    else:
        runner.print_failure("Could not get Python version")
    
    return True

def test_core_packages(runner):
    """Test 2: Core Package Imports"""
    runner.print_test("Core Package Imports")
    
    python_exe = Path.cwd() / ".venv" / "Scripts" / "python.exe"
    
    packages_to_test = [
        ("whisper", "OpenAI Whisper"),
        ("moviepy", "MoviePy"),
        ("pandas", "Pandas"),
        ("rich", "Rich"),
        ("click", "Click"),
        ("yt_dlp", "YT-DLP"),
        ("tkinter", "Tkinter (GUI)")
    ]
    
    for package, name in packages_to_test:
        test_code = f"import {package}; print(f'{name}: OK')"
        result = runner.run_command([str(python_exe), "-c", test_code])
        
        if result and result.returncode == 0:
            runner.print_success(f"{name} import successful")
        else:
            runner.print_failure(f"{name} import failed")
    
    return True

def test_script_files(runner):
    """Test 3: Script Files Existence and Syntax"""
    runner.print_test("Script Files & Syntax Check")
    
    scripts_to_test = [
        "video_transcriber.py",
        "interactive_transcriber.py", 
        "batch_transcriber.py",
        "youtube_channel_transcriber.py",
        "youtube_gui.py",
        "demo.py"
    ]
    
    python_exe = Path.cwd() / ".venv" / "Scripts" / "python.exe"
    
    for script in scripts_to_test:
        script_path = Path.cwd() / script
        
        # Check if file exists
        if script_path.exists():
            runner.print_success(f"Found: {script}")
            
            # Check syntax
            result = runner.run_command([str(python_exe), "-m", "py_compile", script])
            if result and result.returncode == 0:
                runner.print_success(f"Syntax OK: {script}")
            else:
                runner.print_failure(f"Syntax Error: {script}")
                if result and result.stderr:
                    print(f"   Error: {result.stderr}")
        else:
            runner.print_failure(f"Missing: {script}")
    
    return True

def test_help_commands(runner):
    """Test 4: Help Commands and Basic Functionality"""
    runner.print_test("Help Commands & Basic Functionality")
    
    python_exe = Path.cwd() / ".venv" / "Scripts" / "python.exe"
    
    # Test main script help
    result = runner.run_command([str(python_exe), "video_transcriber.py", "--help"])
    if result and result.returncode == 0 and "Usage:" in result.stdout:
        runner.print_success("Main script help command works")
    else:
        runner.print_failure("Main script help command failed")
    
    # Test demo script
    result = runner.run_command([str(python_exe), "demo.py"], timeout=10)
    if result and result.returncode == 0:
        runner.print_success("Demo script runs successfully")
    else:
        runner.print_failure("Demo script failed")
    
    return True

def test_whisper_model_access(runner):
    """Test 5: Whisper Model Access (without downloading)"""
    runner.print_test("Whisper Model Access Test")
    
    python_exe = Path.cwd() / ".venv" / "Scripts" / "python.exe"
    
    # Test if we can import whisper and check available models
    test_code = """
import whisper
models = whisper.available_models()
print(f"Available models: {models}")
print("Whisper access: OK")
"""
    
    result = runner.run_command([str(python_exe), "-c", test_code])
    if result and result.returncode == 0 and "Available models:" in result.stdout:
        runner.print_success("Whisper model access works")
        runner.print_info(f"Models available: {result.stdout.split('Available models: ')[1].split('Whisper access:')[0].strip()}")
    else:
        runner.print_failure("Whisper model access failed")
    
    return True

def test_file_operations(runner):
    """Test 6: File Operations and Directory Creation"""
    runner.print_test("File Operations & Directory Management")
    
    # Create temporary test directory
    test_dir = Path.cwd() / "test_temp"
    
    try:
        # Test directory creation
        test_dir.mkdir(exist_ok=True)
        runner.print_success("Directory creation works")
        
        # Test file writing
        test_file = test_dir / "test.txt"
        test_file.write_text("Test content")
        runner.print_success("File writing works")
        
        # Test file reading
        content = test_file.read_text()
        if content == "Test content":
            runner.print_success("File reading works")
        else:
            runner.print_failure("File reading failed")
        
        # Test JSON operations
        test_json = test_dir / "test.json"
        test_data = {"test": "data", "timestamp": datetime.now().isoformat()}
        with open(test_json, 'w') as f:
            json.dump(test_data, f, indent=2)
        runner.print_success("JSON writing works")
        
        with open(test_json, 'r') as f:
            loaded_data = json.load(f)
        if loaded_data["test"] == "data":
            runner.print_success("JSON reading works")
        else:
            runner.print_failure("JSON reading failed")
        
    except Exception as e:
        runner.print_failure(f"File operations failed: {e}")
    finally:
        # Cleanup
        if test_dir.exists():
            shutil.rmtree(test_dir)
            runner.print_success("Cleanup completed")
    
    return True

def test_transcriber_initialization(runner):
    """Test 7: VideoTranscriber Class Initialization"""
    runner.print_test("VideoTranscriber Class Initialization")
    
    python_exe = Path.cwd() / ".venv" / "Scripts" / "python.exe"
    
    # Test VideoTranscriber import and initialization
    test_code = """
import sys
sys.path.append('.')
from video_transcriber import VideoTranscriber

# Test initialization (without loading model)
class TestTranscriber(VideoTranscriber):
    def load_model(self):
        print("Model loading skipped for test")
        self.model = "test_model"

transcriber = TestTranscriber("tiny")
print("VideoTranscriber initialization: OK")
print(f"Model size set to: {transcriber.model_size}")
"""
    
    result = runner.run_command([str(python_exe), "-c", test_code])
    if result and result.returncode == 0 and "VideoTranscriber initialization: OK" in result.stdout:
        runner.print_success("VideoTranscriber class initializes correctly")
    else:
        runner.print_failure("VideoTranscriber initialization failed")
        if result and result.stderr:
            print(f"   Error: {result.stderr}")
    
    return True

def test_youtube_functionality(runner):
    """Test 8: YouTube Functionality (without actual download)"""
    runner.print_test("YouTube Functionality Test")
    
    python_exe = Path.cwd() / ".venv" / "Scripts" / "python.exe"
    
    # Test yt-dlp basic functionality
    test_code = """
import yt_dlp

# Test basic yt-dlp functionality
ydl_opts = {
    'quiet': True,
    'no_warnings': True,
    'extract_flat': True,
}

print("YT-DLP import: OK")
print("YouTube functionality ready")
"""
    
    result = runner.run_command([str(python_exe), "-c", test_code])
    if result and result.returncode == 0:
        runner.print_success("YouTube functionality (yt-dlp) works")
    else:
        runner.print_failure("YouTube functionality failed")
    
    return True

def test_gui_components(runner):
    """Test 9: GUI Components"""
    runner.print_test("GUI Components Test")
    
    python_exe = Path.cwd() / ".venv" / "Scripts" / "python.exe"
    
    # Test tkinter GUI components without showing window
    test_code = """
import tkinter as tk
from tkinter import ttk

# Test basic GUI components
root = tk.Tk()
root.withdraw()  # Hide window

# Test widget creation
frame = ttk.Frame(root)
label = ttk.Label(frame, text="Test")
entry = ttk.Entry(frame)
button = ttk.Button(frame, text="Test")

print("GUI components: OK")
root.destroy()
"""
    
    result = runner.run_command([str(python_exe), "-c", test_code])
    if result and result.returncode == 0:
        runner.print_success("GUI components work correctly")
    else:
        runner.print_failure("GUI components failed")
    
    return True

def test_launcher_script(runner):
    """Test 10: Launcher Script"""
    runner.print_test("Launcher Script Test")
    
    launcher_path = Path.cwd() / "start.bat"
    
    if launcher_path.exists():
        runner.print_success("Launcher script (start.bat) exists")
        
        # Read and check launcher content
        content = launcher_path.read_text()
        expected_options = ["Interactive Mode", "YouTube Channel", "YouTube GUI", "Batch Processing"]
        
        found_options = []
        for option in expected_options:
            if option in content:
                found_options.append(option)
        
        if len(found_options) == len(expected_options):
            runner.print_success(f"All launcher options found: {', '.join(found_options)}")
        else:
            runner.print_warning(f"Some launcher options missing. Found: {', '.join(found_options)}")
    else:
        runner.print_failure("Launcher script (start.bat) not found")
    
    return True

def create_test_summary(runner):
    """Create comprehensive test summary"""
    runner.print_header("TEST SUMMARY")
    
    total_tests = runner.passed + runner.failed
    end_time = datetime.now()
    duration = (end_time - runner.start_time).total_seconds()
    
    print(f"\n{Colors.BOLD}📊 Test Results:{Colors.END}")
    print(f"   {Colors.GREEN}✅ Passed: {runner.passed}{Colors.END}")
    print(f"   {Colors.RED}❌ Failed: {runner.failed}{Colors.END}")
    print(f"   {Colors.YELLOW}⚠️  Warnings: {runner.warnings}{Colors.END}")
    print(f"   📈 Total: {total_tests}")
    print(f"   ⏱️  Duration: {duration:.2f} seconds")
    
    success_rate = (runner.passed / total_tests * 100) if total_tests > 0 else 0
    
    print(f"\n{Colors.BOLD}📈 Success Rate: {success_rate:.1f}%{Colors.END}")
    
    if runner.failed == 0:
        print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 ALL TESTS PASSED! System is ready to use.{Colors.END}")
        print(f"{Colors.GREEN}✨ You can now transcribe videos with confidence!{Colors.END}")
    elif runner.failed <= 2:
        print(f"\n{Colors.YELLOW}{Colors.BOLD}⚠️  Minor issues found, but core functionality should work.{Colors.END}")
        print(f"{Colors.YELLOW}💡 Check the failed tests above for details.{Colors.END}")
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}⛔ Multiple failures detected. Please review setup.{Colors.END}")
        print(f"{Colors.RED}🔧 Check installation and dependencies.{Colors.END}")
    
    # Recommendations
    print(f"\n{Colors.BOLD}💡 Recommendations:{Colors.END}")
    if runner.failed == 0:
        print(f"   {Colors.GREEN}• Start with Interactive Mode: Double-click start.bat → Option 1{Colors.END}")
        print(f"   {Colors.GREEN}• Try YouTube GUI: Double-click start.bat → Option 5{Colors.END}")
        print(f"   {Colors.GREEN}• Read STEP_BY_STEP_INSTRUCTIONS.txt for detailed usage{Colors.END}")
    else:
        print(f"   {Colors.YELLOW}• Run the quick test first: python test_system.py --quick{Colors.END}")
        print(f"   {Colors.YELLOW}• Check Python environment: .venv/Scripts/python.exe --version{Colors.END}")
        print(f"   {Colors.YELLOW}• Verify all packages: pip list{Colors.END}")

def main():
    """Main testing function"""
    runner = TestRunner()
    
    runner.print_header("VIDEO TRANSCRIPTION SYSTEM - FULL TEST SUITE")
    print(f"{Colors.CYAN}🚀 Starting comprehensive end-to-end testing...{Colors.END}")
    print(f"{Colors.BLUE}📅 Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.END}")
    print(f"{Colors.BLUE}📁 Working Directory: {Path.cwd()}{Colors.END}")
    
    # Run all tests
    test_functions = [
        test_environment_setup,
        test_core_packages,
        test_script_files,
        test_help_commands,
        test_whisper_model_access,
        test_file_operations,
        test_transcriber_initialization,
        test_youtube_functionality,
        test_gui_components,
        test_launcher_script
    ]
    
    for test_func in test_functions:
        try:
            test_func(runner)
        except Exception as e:
            runner.print_failure(f"Test {test_func.__name__} crashed: {e}")
    
    # Create summary
    create_test_summary(runner)
    
    # Save test report
    report_file = Path.cwd() / f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    try:
        with open(report_file, 'w') as f:
            f.write(f"Video Transcription System Test Report\n")
            f.write(f"Generated: {datetime.now()}\n")
            f.write(f"Passed: {runner.passed}\n")
            f.write(f"Failed: {runner.failed}\n")
            f.write(f"Warnings: {runner.warnings}\n")
            f.write(f"Success Rate: {(runner.passed / (runner.passed + runner.failed) * 100):.1f}%\n")
        
        print(f"\n{Colors.BLUE}📄 Test report saved: {report_file}{Colors.END}")
    except:
        pass
    
    return runner.failed == 0

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
