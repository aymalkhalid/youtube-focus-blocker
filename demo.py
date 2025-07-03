#!/usr/bin/env python3
"""
YouTube Stopper - Demo Script
This demonstrates the core functionality without requiring admin privileges
"""

import time
import json
from pathlib import Path
from datetime import datetime

# Simulate the core classes for demo purposes
class DemoYouTubeBlocker:
    """Demo version that simulates blocking without actually modifying hosts file"""
    
    def __init__(self):
        self.is_blocked_state = False
        self.demo_mode = True
        
    def is_admin(self):
        return False  # Demo mode - no admin needed
        
    def is_blocked(self):
        return self.is_blocked_state
        
    def block_youtube(self):
        print("🔒 DEMO: Simulating YouTube blocking...")
        print("   In real mode, this would add entries to hosts file:")
        print("   127.0.0.1 youtube.com")
        print("   127.0.0.1 www.youtube.com")
        print("   127.0.0.1 m.youtube.com")
        print("   ...")
        self.is_blocked_state = True
        return True
        
    def unblock_youtube(self):
        print("🔓 DEMO: Simulating YouTube unblocking...")
        print("   In real mode, this would remove entries from hosts file")
        self.is_blocked_state = False
        return True

class DemoProductivityTracker:
    """Demo version of productivity tracker"""
    
    def __init__(self):
        self.session_start = None
        self.total_time = 0
        self.sessions_today = 0
        
    def start_session(self):
        self.session_start = time.time()
        self.sessions_today += 1
        print(f"⏱️  DEMO: Starting productivity session #{self.sessions_today}")
        
    def end_session(self):
        if self.session_start:
            session_duration = time.time() - self.session_start
            self.total_time += session_duration
            print(f"✅ DEMO: Session completed! Duration: {session_duration:.1f} seconds")
            self.session_start = None
            return session_duration
        return 0
        
    def get_current_session_time(self):
        if self.session_start:
            duration = time.time() - self.session_start
            return f"{int(duration)}s"
        return "Not active"
        
    def get_stats(self):
        return {
            'total_time': f"{self.total_time:.1f} seconds",
            'sessions_today': self.sessions_today,
            'current_session': self.get_current_session_time()
        }

def demo_app():
    """Demonstrate the YouTube Stopper functionality"""
    print("=" * 60)
    print("🎯 YOUTUBE STOPPER - DEMO MODE")
    print("=" * 60)
    print()
    
    # Initialize components
    blocker = DemoYouTubeBlocker()
    tracker = DemoProductivityTracker()
    
    print("🔧 Components initialized!")
    print(f"📊 Current stats: {tracker.get_stats()}")
    print(f"🔒 YouTube blocked: {blocker.is_blocked()}")
    print()
    
    # Demo workflow
    print("--- DEMO WORKFLOW ---")
    print()
    
    # Step 1: Block YouTube
    print("1️⃣ BLOCKING YOUTUBE:")
    blocker.block_youtube()
    tracker.start_session()
    print()
    
    # Step 2: Show active session
    print("2️⃣ PRODUCTIVITY SESSION ACTIVE:")
    print(f"   Status: YouTube blocked = {blocker.is_blocked()}")
    print(f"   Stats: {tracker.get_stats()}")
    print("   Simulating 5 seconds of focused work...")
    
    for i in range(5):
        time.sleep(1)
        print(f"   ⏰ Working... {tracker.get_current_session_time()}")
    
    print()
    
    # Step 3: Unblock YouTube
    print("3️⃣ ENDING SESSION:")
    session_time = tracker.end_session()
    blocker.unblock_youtube()
    print(f"   Final session duration: {session_time:.1f} seconds")
    print(f"   Updated stats: {tracker.get_stats()}")
    print()
    
    # Step 4: Show motivational message
    motivational_messages = [
        "🎯 Stay focused! You're building something amazing!",
        "💪 Your future self will thank you for this discipline!",
        "🚀 Productivity mode is ON! Keep going!",
        "⭐ Every minute of focus is an investment in your goals!"
    ]
    
    import random
    print("4️⃣ MOTIVATIONAL MESSAGE:")
    print(f"   {random.choice(motivational_messages)}")
    print()
    
    print("=" * 60)
    print("✅ DEMO COMPLETED!")
    print("🚀 To use the real app with GUI:")
    print("   1. Run as Administrator")
    print("   2. Execute: python run.py")
    print("   3. Or double-click: start_youtube_stopper.bat")
    print("=" * 60)

if __name__ == "__main__":
    demo_app()
