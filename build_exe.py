#!/usr/bin/env python3
"""
Build script for YouTube Stopper executable
Creates a standalone executable using PyInstaller with optimizations
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def print_step(step_name):
    """Print a formatted step indicator"""
    print(f"\n{'='*60}")
    print(f"🔧 {step_name}")
    print(f"{'='*60}")

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"Running: {description}")
    print(f"Command: {command}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        if result.stdout:
            print(f"Output: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        if e.stdout:
            print(f"Stdout: {e.stdout}")
        if e.stderr:
            print(f"Stderr: {e.stderr}")
        return False

def clean_build_directories():
    """Remove old build artifacts"""
    print_step("Cleaning Build Directories")
    
    dirs_to_clean = ['build', 'dist']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            print(f"Removing {dir_name}/")
            shutil.rmtree(dir_name)
        else:
            print(f"{dir_name}/ doesn't exist, skipping")

def check_dependencies():
    """Check if all required dependencies are installed"""
    print_step("Checking Dependencies")
    
    required_packages = ['pyinstaller', 'pystray', 'Pillow', 'psutil']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.lower().replace('-', '_'))
            print(f"✅ {package} is installed")
        except ImportError:
            print(f"❌ {package} is missing")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n❌ Missing packages: {', '.join(missing_packages)}")
        print("Please install missing packages with: pip install -r requirements.txt")
        return False
    
    print("✅ All dependencies are installed")
    return True

def create_spec_file():
    """Create PyInstaller spec file with optimizations"""
    print_step("Creating PyInstaller Spec File")
    
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'tkinter',
        'tkinter.messagebox',
        'pystray',
        'PIL',
        'PIL.Image',
        'psutil',
        'requests',
        'motivation_widget',
        'pomodoro_widget',
        'youtube_stopper'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'pygame',
        'playsound',
        'numpy',
        'scipy',
        'pandas'
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='YouTubeStopper',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Set to False for GUI app
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    uac_admin=True,  # Request admin privileges
)
'''
    
    with open('youtube_stopper.spec', 'w') as f:
        f.write(spec_content)
    
    print("✅ Created youtube_stopper.spec")

def build_executable():
    """Build the executable using PyInstaller"""
    print_step("Building Executable with PyInstaller")
    
    # Build command
    command = "pyinstaller --clean youtube_stopper.spec"
    
    if not run_command(command, "Building executable"):
        return False
    
    # Check if executable was created
    exe_path = Path("dist/YouTubeStopper.exe")
    if exe_path.exists():
        size_mb = exe_path.stat().st_size / (1024 * 1024)
        print(f"✅ Executable created successfully!")
        print(f"📁 Location: {exe_path.absolute()}")
        print(f"📊 Size: {size_mb:.1f} MB")
        return True
    else:
        print("❌ Executable was not created")
        return False

def create_launcher_batch():
    """Create a batch file launcher for easy execution"""
    print_step("Creating Launcher Batch File")
    
    launcher_content = '''@echo off
title YouTube Stopper Launcher
echo.
echo ================================================
echo          YouTube Stopper Launcher
echo ================================================
echo.
echo Starting YouTube Stopper with administrator privileges...
echo.

REM Check if running as administrator
net session >nul 2>&1
if %errorLevel% == 0 (
    echo Already running as administrator.
    goto run_app
) else (
    echo Requesting administrator privileges...
    goto request_admin
)

:request_admin
powershell -Command "Start-Process -FilePath '%~dp0YouTubeStopper.exe' -Verb RunAs"
goto end

:run_app
"%~dp0YouTubeStopper.exe"

:end
echo.
echo YouTube Stopper has been launched.
pause
'''
    
    with open('dist/launcher.bat', 'w') as f:
        f.write(launcher_content)
    
    print("✅ Created launcher.bat in dist/ folder")

def create_readme_for_distribution():
    """Create a simplified README for the executable distribution"""
    print_step("Creating Distribution README")
    
    readme_content = '''# YouTube Stopper - Executable Distribution

## Quick Start

1. **Run the Application**
   - Double-click `launcher.bat` for automatic admin privileges
   - Or right-click `YouTubeStopper.exe` → "Run as Administrator"

2. **First Run**
   - Windows will ask for administrator permissions (required for hosts file modification)
   - Click "Yes" to allow the application to block YouTube

## Features

- **YouTube Blocking**: Blocks major YouTube domains system-wide
- **Motivation Messages**: Inspiring quotes that change every 5-10 seconds  
- **Pomodoro Timer**: 25-minute focus sessions with break management
- **Cross-Platform**: Works on Windows and Unix systems

## Usage

- The application will show a GUI with motivation messages and Pomodoro timer
- Use the core blocking functionality through the command-line interface
- All changes to system files are automatically backed up

## Troubleshooting

### "Administrator Rights Required"
- Right-click the application and select "Run as Administrator"
- Or use the provided `launcher.bat` file

### "Antivirus Warning"
- Some antivirus software may flag the app due to hosts file modification
- This is normal behavior - the app needs to modify system files to block websites
- Add an exception for the YouTube Stopper folder if needed

### "App Won't Start"
- Make sure you have Windows 10/11
- Try running `launcher.bat` instead of the executable directly
- Check Windows Event Viewer for detailed error messages

## Files Included

- `YouTubeStopper.exe` - Main application (requires admin privileges)
- `launcher.bat` - Easy launcher with automatic admin elevation
- `README_DIST.md` - This file

## Support

For issues, questions, or source code:
https://github.com/aymalkhalid/youtube_stopper

## License

Copyright (c) 2025 - Aymal Khalid Khan
Attribution-NonCommercial License (CC BY-NC style)
Free for personal and educational use.
'''
    
    with open('dist/README_DIST.md', 'w') as f:
        f.write(readme_content)
    
    print("✅ Created README_DIST.md in dist/ folder")

def create_distribution_package():
    """Create a complete distribution package"""
    print_step("Creating Distribution Package")
    
    # Create package directory
    package_dir = Path("dist/YouTubeStopper_Package")
    if package_dir.exists():
        shutil.rmtree(package_dir)
    
    package_dir.mkdir()
    
    # Copy files to package
    files_to_copy = [
        ("dist/YouTubeStopper.exe", "YouTubeStopper.exe"),
        ("dist/launcher.bat", "launcher.bat"),
        ("dist/README_DIST.md", "README.md"),
        ("LICENSE", "LICENSE.txt")
    ]
    
    for src, dst in files_to_copy:
        if os.path.exists(src):
            shutil.copy2(src, package_dir / dst)
            print(f"✅ Copied {src} → {dst}")
        else:
            print(f"⚠️  File not found: {src}")
    
    print(f"✅ Package created at: {package_dir.absolute()}")
    
    # Calculate total package size
    total_size = sum(f.stat().st_size for f in package_dir.rglob('*') if f.is_file())
    print(f"📊 Total package size: {total_size / (1024 * 1024):.1f} MB")

def main():
    """Main build process"""
    print("🎯 YouTube Stopper Executable Builder")
    print("=====================================")
    
    # Change to script directory
    script_dir = Path(__file__).parent.absolute()
    os.chdir(script_dir)
    print(f"Working directory: {script_dir}")
    
    # Check if we're in the right directory
    if not Path("app.py").exists():
        print("❌ Error: app.py not found. Make sure you're running this from the project root.")
        sys.exit(1)
    
    # Execute build steps
    steps = [
        (clean_build_directories, "Clean build directories"),
        (check_dependencies, "Check dependencies"),
        (create_spec_file, "Create PyInstaller spec file"),
        (build_executable, "Build executable"),
        (create_launcher_batch, "Create launcher batch file"),
        (create_readme_for_distribution, "Create distribution README"),
        (create_distribution_package, "Create distribution package")
    ]
    
    for step_func, step_name in steps:
        try:
            success = step_func()
            if success is False:
                print(f"❌ Build failed at step: {step_name}")
                sys.exit(1)
        except Exception as e:
            print(f"❌ Error in step '{step_name}': {e}")
            sys.exit(1)
    
    print_step("Build Complete!")
    print("✅ Your executable is ready!")
    print("\n📁 Distribution files:")
    print("   - dist/YouTubeStopper.exe (main executable)")
    print("   - dist/launcher.bat (easy launcher)")
    print("   - dist/YouTubeStopper_Package/ (complete package)")
    print("\n🚀 To test: Run 'dist/launcher.bat' or 'dist/YouTubeStopper.exe' as administrator")
    print("\n📦 To distribute: Share the 'YouTubeStopper_Package' folder")

if __name__ == "__main__":
    main()
