# -*- mode: python ; coding: utf-8 -*-

"""
PyInstaller specification file for YouTube Stopper
This configures how the executable is built
"""

import sys
from pathlib import Path

# Get the directory where this spec file is located
spec_dir = Path(SPECPATH)

# Define the analysis settings
a = Analysis(
    # Main script to convert
    ['run.py'],
    
    # Additional paths to search for modules
    pathex=[str(spec_dir)],
    
    # Binary files to include (none needed for our app)
    binaries=[],
    
    # Data files to include
    datas=[
        # Include any data files your app needs
        # Format: ('source_path', 'destination_folder_in_exe')
    ],
    
    # Hidden imports that PyInstaller might miss
    hiddenimports=[
        'tkinter',
        'tkinter.ttk',
        'tkinter.messagebox',
        'pystray',
        'PIL',
        'PIL.Image',
        'PIL.ImageDraw',
        'psutil',
        'requests',
        'json',
        'threading',
        'subprocess',
    ],
    
    # Hooks directory (for custom import handling)
    hookspath=[],
    
    # Additional paths for hooksconfig
    hooksconfig={},
    
    # Runtime hooks
    runtime_hooks=[],
    
    # Modules to exclude (reduces file size)
    excludes=[
        'matplotlib',  # Not needed
        'numpy',       # Not needed
        'pandas',      # Not needed
        'scipy',       # Not needed
        'IPython',     # Not needed
        'jupyter',     # Not needed
    ],
    
    # Include all packages
    noarchive=False,
    
    # Optimize imports
    optimize=0,
)

# Create the PYZ archive
pyz = PYZ(a.pure)

# Create the executable
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    
    # Executable name
    name='YouTubeStopper',
    
    # Debug mode (set to False for release)
    debug=False,
    
    # Bootloader debug (set to False for release)
    bootloader_ignore_signals=False,
    
    # Strip debug symbols (reduces size)
    strip=False,
    
    # UPX compression (if available)
    upx=True,
    
    # UPX exclude patterns
    upx_exclude=[],
    
    # Runtime tmpdir
    runtime_tmpdir=None,
    
    # Console mode
    console=False,  # Set to False to hide console window
    
    # Disable traceback limit
    disable_windowed_traceback=False,
    
    # Icon file (we'll create this)
    icon='icon.ico',
    
    # Windows version info
    version='version_info.txt',
    
    # Manifest file
    manifest=None,
    
    # UAC admin privileges
    uac_admin=True,  # Request admin privileges
    
    # UAC UI access
    uac_uiaccess=False,
)

# Optional: Create a directory distribution instead of single file
# Uncomment the following if you prefer a directory with multiple files
# (faster startup, but multiple files to distribute)
"""
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='YouTubeStopper'
)
"""
