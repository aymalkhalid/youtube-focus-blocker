#!/usr/bin/env python3
"""
YouTube Stopper - Startup Script
Run this file to start the YouTube Stopper application
"""

import sys
import os
from pathlib import Path

# Add the current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

try:
    from gui import YouTubeStopperGUI
    
    print("🎯 Starting YouTube Stopper...")
    print("📝 Remember: This app needs administrator privileges to work properly!")
    print("💡 Tip: Right-click and 'Run as Administrator' for full functionality")
    print("-" * 60)
    
    app = YouTubeStopperGUI()
    app.run()
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("💡 Make sure all required packages are installed:")
    print("   pip install pystray Pillow psutil requests")
    
except Exception as e:
    print(f"❌ Error starting application: {e}")
    print("🔧 Try running as administrator or check the requirements")
    
input("\nPress Enter to exit...")
