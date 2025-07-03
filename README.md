# 🎯 YouTube Stopper - Productivity App

A modern Python desktop application that helps you break the YouTube addiction cycle and stay focused on your goals. **Now available as a standalone Windows executable!**

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Executable](https://img.shields.io/badge/Executable-Ready-brightgreen.svg)
![Size](https://img.shields.io/badge/Size-20.5MB-informational.svg)

## 📦 **Ready-to-Use Executable Available!**

**Don't want to install Python?** Download the standalone executable from the [Releases](../../releases) section:

- 🚀 **No Python installation required**
- 🔒 **Complete functionality included**
- 📁 **Single download with all dependencies**
- ⚡ **Instant setup - just run and go!**

**Quick Download**: Get the `YouTubeStopper_Package.zip` from releases and run `launcher.bat`

## 🌟 Features

### Core Functionality
- **🔒 Smart Website Blocking**: Blocks YouTube domains at the system level using hosts file modification
- **⏱️ Productivity Tracking**: Tracks your focused time and daily sessions
- **🎨 Modern GUI**: Beautiful, user-friendly interface with custom toggle switches
- **🖥️ System Tray Integration**: Runs quietly in the background
- **💪 Motivational Messages**: Encourages you when you try to access YouTube

### Advanced Features
- **🚨 Emergency Unblock**: 5-minute emergency access when absolutely necessary
- **☕ Break Management**: Healthy break system with session tracking
- **📊 Detailed Statistics**: Total productive time, daily sessions, current session timer
- **🔄 Auto DNS Flush**: Ensures blocking takes effect immediately
- **🛡️ Safe Hosts Modification**: Backs up your hosts file before any changes

## 🚀 Quick Start

### 🎯 **Option 1: Download Executable (Recommended)**
**Perfect for end users - no technical setup required!**

1. **Download** the latest `YouTubeStopper_Package.zip` from [Releases](../../releases)
2. **Extract** the zip file to any folder on your computer
3. **Run** `launcher.bat` (will automatically request admin privileges)
4. **Start focusing!** Toggle blocking on/off as needed

### 🐍 **Option 2: Run from Source Code**
**Perfect for developers who want to modify or learn from the code**

#### Prerequisites
- **Windows 10/11** (Administrator privileges required)
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
   - **Option A**: Double-click `start_youtube_stopper.bat`
   - **Option B**: Run `python run.py`
   - **Option C**: Right-click `start_youtube_stopper.bat` → "Run as Administrator"

### 🔧 **Option 3: Build Your Own Executable**
**Want to create your own customized version?**

```bash
# Install build dependencies
pip install -r requirements.txt

# Create the executable
python build_exe.py

# Find your executable in dist/YouTubeStopper_Package/
```

## 💻 **Executable Distribution**

### 📁 **What's Included in the Executable Package:**

```
YouTubeStopper_Package/
├── 📄 YouTubeStopper.exe        (20.5 MB) - Complete standalone application
├── 📄 launcher.bat              (3.2 KB)  - Easy launcher with admin privileges
├── 📄 README.md                 (8.9 KB)  - Complete documentation
├── 📄 LEARNING_SUMMARY.md       (8.2 KB)  - Developer learning guide
└── 📄 QUICK_START.txt           (0.7 KB)  - Quick user instructions
```

### ⚡ **Executable Features:**

- **🔐 No Python Required**: Completely self-contained with all dependencies
- **🛡️ Admin Privilege Handling**: Automatic UAC prompt for required permissions
- **📱 Professional UI**: Custom icon and Windows version information
- **💾 Optimized Size**: PyInstaller with UPX compression (20.5 MB total)
- **🚀 Instant Startup**: No installation required - just download and run
- **🔧 Easy Distribution**: Single package ready for sharing

### 🏗️ **Build Process:**

The executable is created using our custom build system:

```bash
# Automated build with comprehensive optimizations
python build_exe.py
```

**Build Features:**
- ✅ **Dependency Verification**: Ensures all required files are present
- ✅ **Clean Builds**: Removes old artifacts for fresh compilation
- ✅ **Optimization Passes**: Size reduction and performance improvements
- ✅ **Package Creation**: Complete distribution folder with documentation
- ✅ **Error Handling**: Robust build process with detailed feedback

### 📊 **Technical Specifications:**

| Component | Details |
|-----------|---------|
| **File Size** | 20.5 MB (optimized with UPX compression) |
| **Dependencies** | All bundled: tkinter, PIL, pystray, psutil, requests |
| **Platform** | Windows 10/11 (64-bit) |
| **Privileges** | Administrator required for hosts file modification |
| **Startup Time** | ~2-3 seconds on modern systems |
| **Memory Usage** | ~50-80 MB RAM during operation |

### 🔧 **For Developers: Building from Source**

#### Build Requirements:
```bash
pip install pyinstaller  # Added to requirements.txt
```

#### Custom PyInstaller Configuration:
- **Spec File**: `youtube_stopper.spec` with advanced optimizations
- **Icon Integration**: Custom YouTube stopper icon (`icon.ico`)
- **Version Info**: Professional Windows file properties
- **UAC Manifest**: Automatic administrator privilege requests
- **Hidden Imports**: All dependencies properly configured

#### Build Process Overview:
1. **Clean Phase**: Remove previous build artifacts
2. **Verification Phase**: Check all required files exist
3. **Compilation Phase**: PyInstaller with custom spec file
4. **Optimization Phase**: Size reduction and performance tuning
5. **Packaging Phase**: Create distribution folder with documentation
```

## 📖 How It Works

### Technical Implementation

#### 1. **Hosts File Blocking**
```python
# When blocking is enabled, these entries are added to C:\Windows\System32\drivers\etc\hosts:
127.0.0.1 youtube.com
127.0.0.1 www.youtube.com
127.0.0.1 m.youtube.com
127.0.0.1 music.youtube.com
127.0.0.1 youtu.be
127.0.0.1 gaming.youtube.com
```

#### 2. **Safe Modification Process**
1. **Backup Creation**: Original hosts file is backed up
2. **Marker System**: Uses comments to identify our entries
3. **DNS Cache Flush**: Clears Windows DNS cache for immediate effect
4. **Rollback Capability**: Can safely remove only our entries

#### 3. **Productivity Tracking**
- **Session Timer**: Tracks active focus time
- **Daily Reset**: Counters reset each day
- **Persistent Storage**: Data saved in JSON format
- **Statistics**: Total time, sessions, current session duration

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
├── 📄 youtube_stopper.py           # Core blocking and tracking logic (348 lines)
├── 📄 gui.py                       # Modern GUI interface (580+ lines)
├── 📄 run.py                       # Main startup script
├── 📄 demo.py                      # Interactive demo without admin requirements
├── 📄 build_exe.py                 # Comprehensive build system for executables
├── 📄 create_icon.py               # Icon generation script
├── 📄 start_youtube_stopper.bat    # Windows batch file for easy startup
├── 📄 requirements.txt             # Python dependencies (including PyInstaller)
├── 📄 README.md                    # This comprehensive documentation
├── 📄 LEARNING_SUMMARY.md          # Educational summary for developers
├── 📄 DISTRIBUTION_GUIDE.md        # Complete distribution guide
│
├── 🔧 Build Configuration Files:
│   ├── 📄 youtube_stopper.spec     # PyInstaller specification file
│   ├── 📄 version_info.txt         # Windows version information
│   └── 📄 icon.ico                 # Application icon
│
├── 📁 dist/                        # Distribution folder (after building)
│   ├── 📄 YouTubeStopper.exe       # Standalone executable (20.5 MB)
│   └── 📁 YouTubeStopper_Package/  # Complete distribution package
│       ├── 📄 YouTubeStopper.exe
│       ├── 📄 launcher.bat
│       ├── 📄 README.md
│       ├── 📄 LEARNING_SUMMARY.md
│       └── 📄 QUICK_START.txt
│
└── 📁 build/                       # Build artifacts (PyInstaller cache)
```
└── README.md              # This file
```

### Key Classes

#### `YouTubeBlocker`
- Handles hosts file modification
- Manages administrator privileges
- Provides blocking/unblocking functionality

#### `ProductivityTracker`
- Tracks focus sessions and statistics
- Handles data persistence
- Manages daily resets

#### `YouTubeStopperGUI`
- Modern tkinter interface
- System tray integration
- User interaction handling

#### `ModernToggleButton`
- Custom animated toggle switch
- Built with tkinter Canvas
- Smooth visual feedback

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
requests>=2.28.0   # HTTP requests (future features)
```

## 🤝 Contributing

We welcome contributions! Here are ways you can help:

1. **🐛 Bug Reports**: Open an issue with detailed reproduction steps
2. **💡 Feature Requests**: Suggest new functionality
3. **🔧 Code Contributions**: Submit pull requests with improvements
4. **📖 Documentation**: Help improve this README and code comments

### Development Setup
```bash
git clone https://github.com/yourusername/youtube_stopper.git
cd youtube_stopper
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

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

## 📦 **Distribution & Sharing**

### 🚀 **For End Users

#### **Option 1: GitHub Releases (Recommended)**
1. Visit the [Releases](../../releases) page
2. Download the latest `YouTubeStopper_Package.zip`
3. Extract and run `launcher.bat`

#### **Option 2: Direct Download**
1. Download this entire repository as ZIP
2. Follow the Python installation instructions above
3. Run from source code

### 🔄 **For Developers & Distributors**

#### **Creating Custom Builds**
```bash
# Clone the repository
git clone https://github.com/yourusername/youtube_stopper.git
cd youtube_stopper

# Install dependencies
pip install -r requirements.txt

# Build executable
python build_exe.py

# Your custom executable will be in dist/YouTubeStopper_Package/
```

#### **Customization Options**
- **Add Websites**: Edit `youtube_domains` list in `youtube_stopper.py`
- **Custom Messages**: Modify `MOTIVATIONAL_MESSAGES` array
- **UI Themes**: Adjust colors in `gui.py` color dictionary
- **Build Settings**: Modify `youtube_stopper.spec` for advanced options

#### **Enterprise Distribution**
- **Network Deployment**: Deploy via Group Policy or software distribution tools
- **Configuration Management**: Pre-configure settings via JSON config files
- **Centralized Logging**: Add network logging for organizational monitoring
- **Custom Branding**: Replace icons and messages with company branding

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

### **Version 1.0.0** - *July 3, 2025*
**🎉 Initial Release - Complete Production Version**

#### **✨ New Features**
- **🔒 Core Blocking System**: YouTube domain blocking via hosts file modification
- **🎨 Modern GUI Interface**: Custom toggle switches and card-based design
- **⏱️ Productivity Tracking**: Session timers and daily statistics
- **🖥️ System Tray Integration**: Background operation with quick access
- **🚨 Emergency Features**: 5-minute emergency unblock functionality
- **☕ Break Management**: Healthy break system with session recording
- **💪 Motivational System**: Encouraging messages and positive reinforcement

#### **🏗️ Technical Implementation**
- **📱 Professional Executable**: 20.5 MB standalone Windows executable
- **🔧 Advanced Build System**: PyInstaller with custom optimizations
- **🛡️ Security Features**: Safe hosts file modification with backups
- **📊 Data Persistence**: JSON-based statistics storage
- **🎯 Admin Privilege Handling**: Automatic UAC integration
- **🔄 DNS Cache Management**: Automatic cache flushing for immediate effects

#### **📚 Documentation**
- **📖 Comprehensive README**: Complete user and developer documentation
- **🎓 Learning Guide**: Educational summary for developers
- **📦 Distribution Guide**: Professional distribution instructions
- **🚀 Quick Start Guide**: Simple setup instructions for end users

#### **🛠️ Developer Tools**
- **🔨 Build Scripts**: Automated executable creation
- **🎨 Icon Generation**: Professional icon creation tools
- **🧪 Demo Mode**: Non-admin testing capabilities
- **📝 Multiple Launchers**: Batch files for various use cases

### **🔮 Planned Features**
- **📱 Mobile Companion**: Browser extension integration
- **☁️ Cloud Sync**: Settings and statistics synchronization
- **🤖 Smart Suggestions**: AI-powered productivity recommendations
- **📈 Advanced Analytics**: Weekly and monthly productivity reports
- **👥 Team Features**: Family and organizational monitoring
- **🎮 Gamification**: Achievement system and productivity streaks
