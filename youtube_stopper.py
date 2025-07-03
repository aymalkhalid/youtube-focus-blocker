#!/usr/bin/env python3
"""
YouTube Stopper - A productivity app to block YouTube distractions
Author: Learning with AI Assistant
Date: July 3, 2025

This application helps users avoid YouTube distractions by:
1. Blocking YouTube domains through hosts file modification
2. Providing a simple GUI interface
3. Running in system tray for easy access
4. Tracking productivity time
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import os
import sys
import subprocess
import json
from datetime import datetime, timedelta
from pathlib import Path
import pystray
from PIL import Image, ImageDraw
import psutil

class YouTubeBlocker:
    """
    Core class that handles the blocking functionality
    """
    
    def __init__(self):
        # Define YouTube domains to block
        self.youtube_domains = [
            'youtube.com',
            'www.youtube.com',
            'm.youtube.com',
            'music.youtube.com',
            'youtu.be',
            'gaming.youtube.com'
        ]
        
        # Windows hosts file location
        self.hosts_file = r"C:\Windows\System32\drivers\etc\hosts"
        
        # Backup file location
        self.backup_file = Path.home() / "youtube_stopper_hosts_backup.txt"
        
        # Marker comments for our entries
        self.start_marker = "# YouTube Stopper - START"
        self.end_marker = "# YouTube Stopper - END"
        
    def is_admin(self):
        """
        Check if the script is running with administrator privileges
        This is required to modify the hosts file on Windows
        """
        try:
            return os.getuid() == 0
        except AttributeError:
            # Windows specific check
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
    
    def run_as_admin(self):
        """
        Restart the script with administrator privileges
        """
        if self.is_admin():
            return True
        else:
            # Re-run the program with admin rights
            try:
                subprocess.run([
                    'powershell', '-Command', 
                    f'Start-Process python -ArgumentList "{sys.argv[0]}" -Verb RunAs'
                ], check=True)
                return False
            except subprocess.CalledProcessError:
                messagebox.showerror(
                    "Admin Rights Required", 
                    "This app needs administrator privileges to modify the hosts file.\n"
                    "Please right-click and 'Run as Administrator'."
                )
                return False
    
    def backup_hosts_file(self):
        """
        Create a backup of the original hosts file before modification
        """
        try:
            if os.path.exists(self.hosts_file):
                with open(self.hosts_file, 'r', encoding='utf-8') as original:
                    content = original.read()
                
                with open(self.backup_file, 'w', encoding='utf-8') as backup:
                    backup.write(content)
                    
                print(f"✅ Hosts file backed up to: {self.backup_file}")
                return True
        except Exception as e:
            print(f"❌ Error backing up hosts file: {e}")
            return False
    
    def is_blocked(self):
        """
        Check if YouTube is currently blocked
        """
        try:
            with open(self.hosts_file, 'r', encoding='utf-8') as f:
                content = f.read()
                return self.start_marker in content
        except Exception as e:
            print(f"❌ Error checking block status: {e}")
            return False
    
    def block_youtube(self):
        """
        Add YouTube domains to hosts file to block access
        """
        if not self.is_admin():
            return False
            
        try:
            # First, create a backup
            self.backup_hosts_file()
            
            # Read current hosts file
            with open(self.hosts_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check if already blocked
            if self.start_marker in content:
                print("🔒 YouTube is already blocked")
                return True
            
            # Prepare blocking entries
            blocking_entries = [
                "",  # Empty line for spacing
                self.start_marker,
                "# Blocking YouTube domains for productivity"
            ]
            
            for domain in self.youtube_domains:
                blocking_entries.append(f"127.0.0.1 {domain}")
            
            blocking_entries.append(self.end_marker)
            blocking_entries.append("")  # Empty line at the end
            
            # Add to hosts file
            new_content = content + "\n" + "\n".join(blocking_entries)
            
            with open(self.hosts_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            # Flush DNS cache (Windows)
            try:
                subprocess.run(['ipconfig', '/flushdns'], 
                             capture_output=True, check=True)
                print("🔄 DNS cache flushed")
            except subprocess.CalledProcessError:
                print("⚠️ Could not flush DNS cache")
            
            print("🔒 YouTube blocked successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Error blocking YouTube: {e}")
            messagebox.showerror("Error", f"Failed to block YouTube: {e}")
            return False
    
    def unblock_youtube(self):
        """
        Remove YouTube blocking entries from hosts file
        """
        if not self.is_admin():
            return False
            
        try:
            with open(self.hosts_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # Remove lines between markers
            new_lines = []
            skip = False
            
            for line in lines:
                if self.start_marker in line:
                    skip = True
                    continue
                elif self.end_marker in line:
                    skip = False
                    continue
                
                if not skip:
                    new_lines.append(line)
            
            # Write back to hosts file
            with open(self.hosts_file, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
            
            # Flush DNS cache
            try:
                subprocess.run(['ipconfig', '/flushdns'], 
                             capture_output=True, check=True)
                print("🔄 DNS cache flushed")
            except subprocess.CalledProcessError:
                print("⚠️ Could not flush DNS cache")
            
            print("🔓 YouTube unblocked successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Error unblocking YouTube: {e}")
            messagebox.showerror("Error", f"Failed to unblock YouTube: {e}")
            return False


class ProductivityTracker:
    """
    Tracks productivity time when YouTube is blocked
    """
    
    def __init__(self):
        self.data_file = Path.home() / "youtube_stopper_data.json"
        self.load_data()
        
    def load_data(self):
        """Load productivity data from file"""
        try:
            if self.data_file.exists():
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    self.total_productive_time = data.get('total_productive_time', 0)
                    self.sessions_today = data.get('sessions_today', 0)
                    self.last_date = data.get('last_date', datetime.now().strftime('%Y-%m-%d'))
            else:
                self.reset_data()
        except Exception as e:
            print(f"Error loading data: {e}")
            self.reset_data()
    
    def reset_data(self):
        """Reset productivity data"""
        self.total_productive_time = 0
        self.sessions_today = 0
        self.last_date = datetime.now().strftime('%Y-%m-%d')
        
    def save_data(self):
        """Save productivity data to file"""
        try:
            data = {
                'total_productive_time': self.total_productive_time,
                'sessions_today': self.sessions_today,
                'last_date': self.last_date
            }
            with open(self.data_file, 'w') as f:
                json.dump(data, f)
        except Exception as e:
            print(f"Error saving data: {e}")
    
    def check_new_day(self):
        """Check if it's a new day and reset daily counters"""
        today = datetime.now().strftime('%Y-%m-%d')
        if today != self.last_date:
            self.sessions_today = 0
            self.last_date = today
            self.save_data()
    
    def start_session(self):
        """Start a productivity session"""
        self.check_new_day()
        self.session_start = time.time()
        self.sessions_today += 1
        
    def end_session(self):
        """End a productivity session and update stats"""
        if hasattr(self, 'session_start'):
            session_time = time.time() - self.session_start
            self.total_productive_time += session_time
            self.save_data()
            return session_time
        return 0
    
    def get_stats(self):
        """Get formatted productivity statistics"""
        total_hours = self.total_productive_time / 3600
        return {
            'total_time': f"{total_hours:.1f} hours",
            'sessions_today': self.sessions_today,
            'current_session': self.get_current_session_time() if hasattr(self, 'session_start') else "Not active"
        }
    
    def get_current_session_time(self):
        """Get current session duration"""
        if hasattr(self, 'session_start'):
            duration = time.time() - self.session_start
            minutes = int(duration // 60)
            seconds = int(duration % 60)
            return f"{minutes:02d}:{seconds:02d}"
        return "00:00"


# Motivational messages to show when users try to access YouTube
MOTIVATIONAL_MESSAGES = [
    "🎯 Stay focused! You're building something amazing!",
    "💪 Your future self will thank you for this discipline!",
    "🚀 Productivity mode is ON! Keep going!",
    "⭐ Every minute of focus is an investment in your goals!",
    "🔥 You're stronger than your distractions!",
    "🌟 Great things happen when you stay focused!",
    "💡 Your dreams are worth more than YouTube shorts!",
    "🏆 Champions are made in moments like this!",
    "⚡ Channel this energy into your projects!",
    "🎨 Create something instead of consuming!",
    "⏳ Time is your most valuable asset—don't let it slip away!",
    "🕰️ Procrastination is the thief of time. Guard your minutes!",
    "⛔ YouTube can wait—your goals can't.",
    "📈 Every second spent focused is a step closer to success.",
    "🛡️ Protect your time from digital thieves!",
    "🧠 Feed your mind with progress, not endless scrolling.",
    "🌱 Plant seeds of discipline now, harvest success later.",
    "⏰ Don't let distractions steal your precious hours.",
    "🦉 Wisdom is knowing what to ignore. Ignore the noise!",
    "🎯 Your attention is currency—spend it wisely.",
    "🚦 Stop. Refocus. Your future is calling.",
    "🕳️ Endless videos are a rabbit hole—climb out and build!",
    "🔒 Lock away distractions, unlock your potential.",
    "📚 Invest your time in learning, not losing it.",
    "🧭 Stay on course—don't let YouTube steer you off track.",
    "🌄 The best views come after the hardest climbs—keep going!",
    "💡 Instead of watching YouTube, create your own content!"
]

if __name__ == "__main__":
    print("🎯 YouTube Stopper - Starting...")
    
    # For now, let's test the basic functionality
    blocker = YouTubeBlocker()
    tracker = ProductivityTracker()
    
    print(f"📊 Current stats: {tracker.get_stats()}")
    print(f"🔒 YouTube blocked: {blocker.is_blocked()}")
    
    # We'll add the GUI in the next step
    print("✅ Core components initialized!")
