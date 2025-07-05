# 🎯 YouTube Stopper - Productivity App

A modern Python desktop application that helps you break the YouTube addiction cycle and stay focused on your goals. **Currently in active development with core components complete!**

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Unix-lightgrey.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-In%20Development-orange.svg)
![Components](https://img.shields.io/badge/Components-Modular-brightgreen.svg)

## � **Current Application Status**

### 🚧 **Development Stage: Core Components Complete**

This YouTube Stopper application is currently in active development with the following components implemented:

#### ✅ **Completed Features:**
- **Core Blocking Engine**: Full YouTube domain blocking via hosts file modification
- **Cross-Platform Admin Handling**: Windows and Unix administrator privilege management
- **Motivation System**: Dynamic motivational messages with random timing
- **Pomodoro Timer**: Complete 25-minute focus timer with break management
- **Modular Architecture**: Clean separation between components for easy extension
- **Safety Features**: Automatic hosts file backup and restoration
- **Error Handling**: Robust error handling for all system operations

#### 🔧 **Current Development Focus:**
- **GUI Integration**: Combining all widgets into a unified interface
- **System Tray Support**: Background operation capabilities
- **Statistics Tracking**: Session and productivity data persistence
- **User Experience**: Polish and refinement of existing features

#### 📦 **Executable Distribution:**
- The README references executable distribution, but current focus is on source code development
- Build system and packaging will be implemented after core GUI completion

## 🌟 Features

### Core Functionality
- **🔒 Smart Website Blocking**: Blocks YouTube domains at the system level using hosts file modification
- **💪 Motivational Messages**: Dynamic rotating motivational quotes to encourage productivity
- **⏱️ Pomodoro Timer**: Built-in 25-minute focus timer with break management
- **🖥️ Cross-Platform Admin Handling**: Automatic privilege elevation on Windows and Unix systems
- **�️ Safe Hosts Modification**: Backs up your hosts file before any changes with automatic restoration

### Widget Components
- **� Motivation Widget**: Displays inspiring messages that change every 5-10 seconds
- **🍅 Pomodoro Widget**: Full-featured Pomodoro timer with start/pause/reset functionality
- **⚙️ Modular Design**: Each widget is a separate component for easy customization and extension

### Technical Features
- **🔄 Multi-Platform Support**: Works on Windows and Unix-like systems
- **� Robust Error Handling**: Comprehensive error handling for all system operations
- **💾 Automatic Backup**: Creates safety backups before modifying system files
- **🔧 Component Integration**: Clean separation between blocking logic and UI components

## 🚀 Quick Start

### 🐍 **Run from Source Code**
**Current development version - perfect for developers and testers**

#### Prerequisites
- **Windows 10/11** or **Unix-like system** (Administrator privileges required)
- **Python 3.8+** installed

#### Installation

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
   
   **Note**: The application will automatically request administrator privileges if needed using PowerShell on Windows systems.

### 🧪 **Testing Individual Components**

You can test individual components separately:

```bash
# Test the core blocking functionality
python youtube_stopper.py

# Test the motivation widget (requires GUI)
python -c "
import tkinter as tk
from motivation_widget import MotivationWidget
root = tk.Tk()
widget = MotivationWidget(root)
widget.pack()
root.mainloop()
"

# Test the Pomodoro timer (requires GUI)  
python -c "
import tkinter as tk
from pomodoro_widget import PomodoroWidget
root = tk.Tk()
widget = PomodoroWidget(root)
widget.pack()
root.mainloop()
"
```

### 🧪 **Development Usage**

#### Testing Core Blocking (Command Line)
```bash
python youtube_stopper.py
```

#### GUI Components Testing
The application includes modular widgets that can be tested independently:

- **Motivation Widget**: Displays rotating inspirational messages
- **Pomodoro Widget**: 25-minute focus timer with break management
- **Main App**: Integrates all components with admin privilege handling

#### File Locations (Current Implementation)
- **Hosts File**: `C:\Windows\System32\drivers\etc\hosts` (Windows) or `/etc/hosts` (Unix)
- **Backup File**: `%USERPROFILE%\youtube_stopper_hosts_backup.txt` (Windows) or `~/youtube_stopper_hosts_backup.txt` (Unix)

## 💻 **How It Works**

### � **Technical Implementation**

#### **YouTube Domain Blocking**
The application modifies the system's hosts file to redirect YouTube domains to localhost (`127.0.0.1`), effectively blocking access:

- **Blocked Domains**: `youtube.com`, `www.youtube.com`, `m.youtube.com`, `music.youtube.com`, `youtu.be`, `gaming.youtube.com`
- **Safe Modification**: Creates automatic backup before any changes
- **Cross-Platform**: Works on Windows (`C:\Windows\System32\drivers\etc\hosts`) and Unix (`/etc/hosts`)

#### **Administrator Privileges**
- **Windows**: Uses PowerShell with `Start-Process -Verb RunAs` for UAC elevation
- **Unix**: Checks for root access using `os.getuid()`
- **Automatic**: Handles privilege elevation transparently to the user

#### **Widget Architecture**
- **Modular Design**: Each component is a separate class for easy maintenance
- **Motivation Widget**: Self-contained tkinter Label with automatic message rotation
- **Pomodoro Widget**: Full-featured timer with pause/resume and break management

## 📖 How It Works

### Technical Implementation

#### 1. **Hosts File Blocking**
```python
# When blocking is enabled, these entries are added to the hosts file:
# Windows: C:\Windows\System32\drivers\etc\hosts
# Unix: /etc/hosts

127.0.0.1 youtube.com
127.0.0.1 www.youtube.com
127.0.0.1 m.youtube.com
127.0.0.1 music.youtube.com
127.0.0.1 youtu.be
127.0.0.1 gaming.youtube.com
```

#### 2. **Safe Modification Process**
1. **Backup Creation**: Original hosts file is backed up automatically
2. **Marker System**: Uses comments to identify YouTube Stopper entries
3. **Cross-Platform**: Handles Windows and Unix hosts file locations
4. **Rollback Capability**: Can safely remove only YouTube Stopper entries

#### 3. **Component Architecture**
- **YouTubeBlocker**: Core blocking functionality with admin privilege handling
- **MotivationWidget**: Self-updating motivational message display
- **PomodoroWidget**: Complete Pomodoro timer with visual feedback
- **Main App**: Coordinates components and handles system integration

## 🎮 Usage Guide

### Main Interface

#### Toggle Switch
- **🔒 ON (Green)**: YouTube is blocked, productivity timer is running
- **🔓 OFF (Gray)**: YouTube is accessible, timer is paused

#### Action Buttons
- **🚨 Emergency Unblock**: 5-minute temporary access (use sparingly!)
- **☕ Take a Break**: Scheduled break with session time recording

#### Statistics Panel
- **Current Session**: Real-time timer of current focus session
- **Total Productive Time**: Cumulative focused time across all sessions
- **Sessions Today**: Number of focus sessions completed today

#### System Tray
- **Right-click tray icon** for quick actions:
  - Show/Hide main window
  - Toggle blocking on/off
  - Quit application

### Best Practices

1. **🌅 Start Your Day Right**
   - Enable blocking before checking any websites
   - Set a daily productivity goal

2. **🎯 Use Emergency Unblock Wisely**
   - Only for truly urgent YouTube access
   - Automatically re-enables after 5 minutes

3. **☕ Take Regular Breaks**
   - Use the break button for scheduled rest
   - Helps maintain long-term productivity

4. **📊 Monitor Your Progress**
   - Check stats regularly for motivation
   - Celebrate productivity milestones

## ⚙️ Configuration

### Blocked Domains
The app blocks these YouTube domains by default:
- `youtube.com`
- `www.youtube.com`
- `m.youtube.com`
- `music.youtube.com`
- `youtu.be`
- `gaming.youtube.com`

### File Locations
- **Hosts File**: `C:\Windows\System32\drivers\etc\hosts`
- **Backup File**: `%USERPROFILE%\youtube_stopper_hosts_backup.txt`
- **Stats Data**: `%USERPROFILE%\youtube_stopper_data.json`

## 🛠️ Development

### Project Structure
```
youtube_stopper/
├── 📄 app.py                       # Main application entry point with admin privilege handling
├── 📄 youtube_stopper.py           # Core blocking logic and YouTubeBlocker class (343 lines)
├── 📄 motivation_widget.py         # Motivational message widget component (27 lines)
├── 📄 pomodoro_widget.py           # Pomodoro timer widget component (96 lines)
├── 📄 requirements.txt             # Python dependencies (9 packages)
├── 📄 README.md                    # This comprehensive documentation
├── 📄 LICENSE                      # Attribution-NonCommercial license
│
├── 🔧 Build System:
│   ├── 📄 build_exe.py             # Advanced Python build script with full features
│   ├── 📄 build_simple.bat         # Simple Windows batch build script
│   └── 📄 youtube_stopper.spec     # PyInstaller specification (auto-generated)
│
├── 📁 dist/                        # Distribution folder (after building)
│   ├── 📄 YouTubeStopper.exe       # Standalone executable
│   ├── 📄 launcher.bat             # Easy launcher with admin privileges
│   ├── 📄 README_DIST.md           # Distribution documentation
│   └── 📁 YouTubeStopper_Package/  # Complete distribution package
│
├── 📁 build/                       # Build artifacts (PyInstaller cache)
└── 📁 __pycache__/                 # Python bytecode cache
    ├── motivation_widget.cpython-310.pyc
    ├── motivation_widget.cpython-312.pyc
    ├── pomodoro_widget.cpython-310.pyc
    ├── pomodoro_widget.cpython-312.pyc
    ├── youtube_stopper.cpython-310.pyc
    └── youtube_stopper.cpython-312.pyc
```

### Key Classes and Components

#### `YouTubeBlocker` (youtube_stopper.py)
- **Core Functionality**: Handles hosts file modification for YouTube domain blocking
- **Admin Privileges**: Manages administrator privilege requirements and validation
- **Domain Management**: Blocks multiple YouTube domains (`youtube.com`, `www.youtube.com`, `m.youtube.com`, `music.youtube.com`, `youtu.be`, `gaming.youtube.com`)
- **Backup System**: Creates automatic backups of hosts file before modification
- **Cross-Platform**: Supports both Windows and Unix-like systems

#### `MotivationWidget` (motivation_widget.py)
- **Dynamic Messages**: Displays rotating motivational quotes to encourage productivity
- **Smart Timing**: Updates messages every 5-10 seconds randomly
- **Built-in Quotes**: 10 carefully selected motivational messages
- **Tkinter Integration**: Seamlessly integrates with the main application GUI

#### `PomodoroWidget` (pomodoro_widget.py)
- **Focus Timer**: 25-minute Pomodoro technique implementation
- **Break Management**: Automatic break detection and management
- **Timer Controls**: Start, pause, resume, and reset functionality
- **Visual Feedback**: Real-time countdown display with proper formatting
- **Session Tracking**: Tracks focus and break sessions

#### Main Application (app.py)
- **Admin Detection**: Cross-platform administrator privilege checking
- **Auto-Elevation**: Automatic privilege elevation on Windows using PowerShell
- **Component Integration**: Coordinates between all widget components
- **Error Handling**: Robust error handling for privilege and system operations

## 🔧 Troubleshooting

### Common Issues

#### "Administrator Rights Required"
**Solution**: Right-click the application and select "Run as Administrator"

#### "DNS Cache Not Flushed"
**Solution**: Run `ipconfig /flushdns` in Command Prompt as Administrator

#### "Hosts File Permission Denied"
**Solution**: Ensure you're running as Administrator and antivirus isn't blocking

#### "System Tray Icon Not Appearing"
**Solution**: Check Windows notification area settings

### Debug Mode
Run with debug output:
```bash
python run.py --debug
```

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
Edit the `MOTIVATIONAL_MESSAGES` list in `youtube_stopper.py`:
```python
MOTIVATIONAL_MESSAGES = [
    "🎯 Your custom message here!",
    "💪 Another motivational quote!",
    # Add more messages...
]
```

## 📋 Requirements

### System Requirements
- **Operating System**: Windows 10/11
- **Python Version**: 3.8 or higher
- **Privileges**: Administrator access required
- **Memory**: ~50MB RAM usage
- **Storage**: ~5MB disk space

### Python Dependencies
```
pystray>=0.19.4    # System tray functionality  
Pillow>=9.0.0      # Image processing for tray icon
psutil>=5.9.0      # System process utilities
requests>=2.28.0   # HTTP requests for future features
pyinstaller        # Executable building (development)
pygame             # Audio/multimedia capabilities
matplotlib         # Data visualization for statistics
playsound          # Sound notification system
```

## 🤝 Contributing

We welcome contributions! Here are ways you can help:

1. **🐛 Bug Reports**: Open an issue with detailed reproduction steps
2. **💡 Feature Requests**: Suggest new functionality
3. **🔧 Code Contributions**: Submit pull requests with improvements
4. **📖 Documentation**: Help improve this README and code comments

### Development Setup
```bash
git clone https://github.com/aymalkhalid/youtube_stopper.git
cd youtube_stopper
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

## 📦 **Building Executable**

### 🚀 **Quick Build (Windows)**

For easy executable creation, use the provided batch file:

```cmd
# Run the simple build script
build_simple.bat
```

This will:
- ✅ Install dependencies automatically
- 🧹 Clean old build files
- 🔧 Build executable with PyInstaller
- 📝 Create launcher batch file
- 📁 Package everything in `dist/` folder

### 🔧 **Advanced Build (Cross-Platform)**

For more control and features, use the Python build script:

```bash
# Install dependencies first
pip install -r requirements.txt

# Run the advanced build script
python build_exe.py
```

This provides:
- 🔍 Dependency checking
- 📋 Custom PyInstaller spec file creation
- 📊 Build optimization and size reporting
- 📦 Complete distribution package creation
- 🛡️ Admin privilege handling

### 📁 **Build Output**

After building, you'll find:
```
dist/
├── YouTubeStopper.exe          # Main executable (~15-25 MB)
├── launcher.bat               # Easy launcher with admin privileges
├── README_DIST.md             # Distribution documentation
└── YouTubeStopper_Package/    # Complete distribution folder
    ├── YouTubeStopper.exe
    ├── launcher.bat
    ├── README.md
    └── LICENSE.txt
```

### 🚀 **Running the Executable**

1. **Recommended**: Use `launcher.bat` for automatic admin elevation
2. **Manual**: Right-click `YouTubeStopper.exe` → "Run as Administrator"
3. **Testing**: Double-click to test (may require manual admin approval)

### ⚠️ **Build Requirements**

- **Windows**: Windows 10/11 for Windows executable
- **Python**: 3.8+ with pip
- **Dependencies**: All packages from `requirements.txt`
- **Disk Space**: ~100MB for build process
- **Admin Rights**: Required for testing the executable

## 📜 License

### 📄 **YouTube Stopper License**

**Copyright (c) 2025 - Aymal Khalid Khan**

#### ✅ **You are free to:**
- **Use** - Use this software for personal, educational, or non-commercial purposes
- **Study** - Examine the source code and learn from it
- **Modify** - Adapt, remix, and build upon the material for non-commercial purposes
- **Share** - Copy and redistribute the material in any medium or format

#### ❌ **Under the following conditions:**
- **Attribution** - You must give appropriate credit to the original author, provide a link to this repository, and indicate if changes were made
- **Non-Commercial** - You may not use the material for commercial purposes or sell this software
- **Share Alike** - If you remix, transform, or build upon the material, you must distribute your contributions under the same license

#### 🚫 **Restrictions:**
- **No Commercial Use** - This software cannot be sold, licensed for profit, or used in commercial products without explicit written permission
- **No Warranty** - This software is provided "as is" without warranty of any kind

#### 📝 **Attribution Requirements:**
When sharing or modifying this project, please include:
```
Original YouTube Stopper by [Your Name]
Repository: https://github.com/yourusername/youtube_stopper
License: Attribution-NonCommercial (CC BY-NC style)
```

#### 💼 **Commercial Licensing:**
For commercial use, enterprise licensing, or to remove these restrictions, please contact the author at [send2aymal@gmail.com].

---

**This license ensures the project remains free and open for learning and personal use while protecting the author's rights.**

## 🙏 Acknowledgments

- **Tkinter Community** for GUI inspiration
- **Productivity Experts** for behavioral insights
- **Python Community** for excellent libraries

## 🔮 Future Features

- **📱 Mobile Companion App**: Sync blocking across devices
- **🤖 Smart Break Reminders**: AI-powered break suggestions
- **📈 Advanced Analytics**: Weekly/monthly productivity reports
- **🎮 Gamification**: Achievement system and productivity streaks
- **☁️ Cloud Sync**: Backup stats across multiple computers
- **🔧 Advanced Settings**: Custom block durations, website whitelist

---

## 📞 Support

Having issues? Here's how to get help:

1. **📖 Check this README** for common solutions
2. **🐛 Open an Issue** on GitHub with detailed information
3. **💬 Discussion Forum** for general questions and tips

---

**Made with ❤️ for productivity enthusiasts who want to reclaim their time from endless YouTube scrolling!**

*Remember: The goal isn't to never use YouTube, but to use it intentionally and mindfully. This tool helps you build better digital habits!* 🧠✨

## 🤝 **Contributing & Development**

### 🚀 **Getting Started for Developers**

#### **Setting Up Development Environment**
```bash
# Clone the repository
git clone https://github.com/yourusername/youtube_stopper.git
cd youtube_stopper

# Install dependencies
pip install -r requirements.txt

# Test individual components
python youtube_stopper.py      # Core blocking functionality
python app.py                  # Main application
```

#### **Development Workflow**
1. **Test Core Components**: Start with `youtube_stopper.py` for blocking logic
2. **Test Widgets**: Use the individual widget test commands from the Usage section
3. **Test Integration**: Run `app.py` to test component integration
4. **Admin Testing**: Ensure admin privilege handling works on your system

### 🔄 **Customization Options**

#### **Adding New Blocked Domains**
Edit the `youtube_domains` list in `youtube_stopper.py`:
```python
self.youtube_domains = [
    'youtube.com',
    'www.youtube.com',
    'm.youtube.com',
    'music.youtube.com',
    'youtu.be',
    'gaming.youtube.com',
    'your-custom-domain.com'  # Add your domains here
]
```

#### **Custom Motivational Messages**
Edit the `motivation_lines` list in `motivation_widget.py`:
```python
self.motivation_lines = [
    "Stay focused, your goals are within reach!",
    "Every minute counts. Make it productive!",
    "Your custom message here!",           # Add your messages
    "Another inspirational quote!",
    # Add more messages...
]
```

#### **Pomodoro Timer Customization**
Modify timer duration in `pomodoro_widget.py`:
```python
self.pomo_seconds_left = 25 * 60  # Change 25 to your preferred minutes
```

### 👥 **Contributing Guidelines**

We welcome contributions! Here are ways you can help:

1. **🐛 Bug Reports**: Open an issue with detailed reproduction steps
2. **💡 Feature Requests**: Suggest new functionality or improvements
3. **🔧 Code Contributions**: Submit pull requests with enhancements
4. **📖 Documentation**: Help improve README and code comments
5. **🧪 Testing**: Test on different systems and report compatibility issues

### 🔐 **Security Considerations**

#### **For IT Administrators**
- **Antivirus Exceptions**: May need to whitelist due to hosts file modification
- **User Permissions**: Requires administrator privileges for full functionality
- **Network Policies**: Compatible with domain environments
- **Audit Trail**: All changes logged and reversible

#### **For End Users**
- **Safe Operation**: Always backs up hosts file before changes
- **Clean Removal**: Uninstallation removes all traces
- **No Data Collection**: All data stays on local machine
- **Open Source**: Code available for security review

## 📋 **Changelog**

### **Version 0.5.0** - *July 5, 2025* (Current Development State)
**🚧 Core Components Complete - GUI Integration In Progress**

#### **✅ Completed Features**
- **🔒 Core Blocking System**: YouTube domain blocking via hosts file modification
- **🛡️ Cross-Platform Admin Handling**: Windows and Unix administrator privilege management
- **💪 Motivation Widget**: Dynamic rotating motivational messages (10 built-in quotes)
- **🍅 Pomodoro Timer Widget**: 25-minute focus timer with full controls
- **� Modular Architecture**: Clean separation of components for easy extension
- **🔄 Safe Hosts Modification**: Automatic backup and restoration capabilities
- **🧪 Component Testing**: Individual widget testing capabilities

#### **🏗️ Technical Implementation**
- **📱 Modular Design**: Separate files for each major component
- **🔧 Cross-Platform Support**: Windows and Unix compatibility
- **🛡️ Robust Error Handling**: Comprehensive error handling for system operations
- **📊 Clean Code Structure**: Well-documented and maintainable codebase
- **🎯 Admin Privilege Automation**: PowerShell UAC integration for Windows

#### **� Current Development Focus**
- **🎨 GUI Integration**: Combining all widgets into unified interface
- **🖥️ System Tray Implementation**: Background operation capabilities
- **� Statistics Tracking**: Session and productivity data persistence
- **� Emergency Features**: Temporary unblock functionality
- **☕ Break Management**: Enhanced break system with tracking

#### **� Documentation Status**
- **� Comprehensive README**: Updated to reflect current development state
- **� Usage Instructions**: Complete setup and testing guide
- **🛠️ Developer Guide**: Component architecture and customization info

### **🔮 Next Development Milestones**
- **🎨 Complete GUI Integration**: Unified interface with all components
- **📦 Executable Distribution**: PyInstaller build system implementation
- **� System Tray**: Background operation with quick access
- **� Statistics System**: Productivity tracking and data visualization
- **🤖 Advanced Features**: Smart suggestions and enhanced user experience

## 📋 Usage

### 🚀 **Basic Usage**

1. **Start the Application**
   ```bash
   python app.py
   ```
   The application will automatically request administrator privileges if needed.

2. **Core Blocking Commands** (command line mode)
   ```bash
   python youtube_stopper.py
   ```
   - Follow the interactive prompts to enable/disable blocking
   - Type 'y' to enable blocking, 'n' to disable, 'q' to quit

3. **Widget Testing** (individual components)
   ```bash
   # Test motivation messages
   python -c "
   import tkinter as tk
   from motivation_widget import MotivationWidget
   root = tk.Tk()
   root.title('Motivation Test')
   widget = MotivationWidget(root, font=('Arial', 12))
   widget.pack(padx=20, pady=20)
   root.mainloop()
   "
   
   # Test Pomodoro timer
   python -c "
   import tkinter as tk
   from pomodoro_widget import PomodoroWidget
   root = tk.Tk()
   root.title('Pomodoro Test')
   widget = PomodoroWidget(root)
   widget.pack(padx=20, pady=20)
   root.mainloop()
   "
   ```

### 🎯 **Features in Action**

#### **Motivation Widget**
- Displays inspirational quotes that change every 5-10 seconds
- 10 built-in motivational messages focused on productivity
- Automatically randomizes timing and message selection

#### **Pomodoro Timer**
- 25-minute focus sessions with countdown display
- Start/Pause/Resume/Reset functionality
- Automatic break detection and management
- Visual feedback with time formatting (MM:SS)

#### **YouTube Blocking**
- Blocks 6 major YouTube domains at the system level
- Creates backup of hosts file before modification
- Safe removal of only YouTube Stopper entries
- Cross-platform support (Windows/Unix)
