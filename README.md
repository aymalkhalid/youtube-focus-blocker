# 🎯 YouTube Stopper - Productivity App

A Python desktop application that helps you break the YouTube addiction cycle and stay focused on your goals.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Unix-lightgrey.svg)
![License](https://img.shields.io/badge/License-NonCommercial-green.svg)
![Status](https://img.shields.io/badge/Status-Functional-brightgreen.svg)

## ✅ **Core Features**
- **🔒 YouTube Blocking**: System-level blocking via hosts file modification
- **💪 Motivation Widget**: Dynamic rotating motivational messages 
- **🍅 Pomodoro Timer**: 25-minute focus timer with full controls
- **🛡️ Cross-Platform**: Windows and Unix administrator privilege management
- **🔄 Safe Operation**: Automatic backup and restoration of system files

## 🚀 Quick Start

### Prerequisites
- **Windows 10/11** or **Unix-like system** (Administrator privileges required)
- **Python 3.8+** installed

### Installation & Usage

1. **Clone or download this repository**
   ```bash
   git clone https://github.com/yourusername/youtube_stopper.git
   cd youtube_stopper
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```
   
   **Note**: The application will automatically request administrator privileges if needed.

### Testing Individual Components

```bash
# Test the core blocking functionality
python youtube_stopper.py

# Test the motivation widget
python -c "
import tkinter as tk
from motivation_widget import MotivationWidget
root = tk.Tk()
widget = MotivationWidget(root)
widget.pack()
root.mainloop()
"

# Test the Pomodoro timer
python -c "
import tkinter as tk
from pomodoro_widget import PomodoroWidget
root = tk.Tk()
widget = PomodoroWidget(root)
widget.pack()
root.mainloop()
"
```

## 💻 How It Works

### YouTube Domain Blocking
The application modifies the system's hosts file to redirect YouTube domains to localhost (`127.0.0.1`):

- **Blocked Domains**: `youtube.com`, `www.youtube.com`, `m.youtube.com`, `music.youtube.com`, `youtu.be`, `gaming.youtube.com`
- **Safe Modification**: Creates automatic backup before any changes
- **Cross-Platform**: Works on Windows (`C:\Windows\System32\drivers\etc\hosts`) and Unix (`/etc/hosts`)

### Administrator Privileges
- **Windows**: Uses PowerShell with `Start-Process -Verb RunAs` for UAC elevation
- **Unix**: Checks for root access using `os.getuid()`
- **Automatic**: Handles privilege elevation transparently

## 🛠️ Development

### Project Structure
```
youtube_stopper/
├── app.py                    # Main application entry point
├── youtube_stopper.py        # Core blocking logic
├── motivation_widget.py      # Motivational message widget
├── pomodoro_widget.py        # Pomodoro timer widget
├── requirements.txt          # Python dependencies
├── README.md                 # This documentation
├── LICENSE                   # License information
├── build_exe.py              # Build script for executables
├── build_simple.bat          # Simple batch build script
└── dist/                     # Distribution folder (after building)
    ├── YouTubeStopper.exe
    ├── launcher.bat
    └── README_DIST.md
```

### Key Components

#### `YouTubeBlocker` (youtube_stopper.py)
- Handles hosts file modification for YouTube domain blocking
- Manages administrator privilege requirements
- Creates automatic backups of hosts file before modification
- Supports both Windows and Unix-like systems

#### `MotivationWidget` (motivation_widget.py)
- Displays rotating motivational quotes
- Updates messages every 5-10 seconds randomly
- 10 built-in motivational messages

#### `PomodoroWidget` (pomodoro_widget.py)
- 25-minute Pomodoro technique implementation
- Timer controls: Start, pause, resume, and reset
- Visual feedback with real-time countdown display

## 🔧 Troubleshooting

### Common Issues

#### "Administrator Rights Required"
**Solution**: Right-click the application and select "Run as Administrator"

#### "Hosts File Permission Denied"
**Solution**: Ensure you're running as Administrator and antivirus isn't blocking

#### "App Closes Immediately"
**Solution**: Run from command line to see error messages or use debug mode

## 🎨 Customization

### Adding Custom Domains
Edit the `youtube_domains` list in `youtube_stopper.py`:
```python
self.youtube_domains = [
    'youtube.com',
    'www.youtube.com',
    'your-custom-domain.com'  # Add your domains here
]
```

### Custom Motivational Messages
Edit the `motivation_lines` list in `motivation_widget.py`:
```python
self.motivation_lines = [
    "Stay focused, your goals are within reach!",
    "Your custom message here!",
    # Add more messages...
]
```

### Pomodoro Timer Customization
Modify timer duration in `pomodoro_widget.py`:
```python
self.pomo_seconds_left = 25 * 60  # Change 25 to your preferred minutes
```

## 📦 Building Executable

### Quick Build (Windows)
```cmd
build_simple.bat
```

### Advanced Build
```bash
pip install -r requirements.txt
python build_exe.py
```

### Build Output
```
dist/
├── YouTubeStopper.exe          # Main executable
├── YouTubeStopper_Debug.exe    # Debug version
├── launcher.bat               # Easy launcher with admin privileges
└── README_DIST.md             # Distribution documentation
```

## 📋 Requirements

### System Requirements
- **Operating System**: Windows 10/11 or Unix-like system
- **Python Version**: 3.8 or higher
- **Privileges**: Administrator access required
- **Memory**: ~50MB RAM usage
- **Storage**: ~15MB disk space

### Python Dependencies
```
pystray>=0.19.4
Pillow>=9.0.0
psutil>=5.9.0
requests>=2.28.0
pyinstaller
```

## 📜 License

**Copyright (c) 2025 - Aymal Khalid Khan**

### You are free to:
- **Use** - Use this software for personal, educational, or non-commercial purposes
- **Study** - Examine the source code and learn from it
- **Modify** - Adapt and build upon the material for non-commercial purposes
- **Share** - Copy and redistribute the material

### Under the following conditions:
- **Attribution** - You must give appropriate credit to the original author
- **Non-Commercial** - You may not use the material for commercial purposes
- **Share Alike** - Distribute contributions under the same license

For commercial licensing: send2aymal@gmail.com

## 🤝 Contributing

We welcome contributions! Ways you can help:

1. **🐛 Bug Reports**: Open an issue with detailed reproduction steps
2. **💡 Feature Requests**: Suggest new functionality
3. **🔧 Code Contributions**: Submit pull requests with improvements
4. **📖 Documentation**: Help improve README and code comments

### Development Setup
```bash
git clone https://github.com/yourusername/youtube_stopper.git
cd youtube_stopper
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
python app.py
```

---

**Made with ❤️ for productivity enthusiasts who want to reclaim their time from endless YouTube scrolling!**
