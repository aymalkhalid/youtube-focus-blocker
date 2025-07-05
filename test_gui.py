#!/usr/bin/env python3
"""
Simple test version of YouTube Stopper without admin requirements
This helps debug GUI and widget issues without admin privilege complications
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os

# Simple test versions of the components
class TestMotivationWidget(tk.Label):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, text="🎯 Stay focused! You've got this!", *args, **kwargs)

class TestPomodoroWidget(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, bg="#232946", *args, **kwargs)
        self.label = tk.Label(self, text="Pomodoro Timer (Test)", bg="#232946", fg="#eebbc3", font=("Segoe UI", 11, "bold"))
        self.label.pack()
        self.time_label = tk.Label(self, text="25:00", bg="#232946", fg="#fffffe", font=("Segoe UI", 16, "bold"))
        self.time_label.pack()

class TestYouTubeBlocker:
    def is_blocked(self):
        return False
    
    def block_youtube(self):
        return True
    
    def unblock_youtube(self):
        return True
    
    def get_custom_domains(self):
        return ["example.com", "test.com"]
    
    def add_custom_domain(self, domain):
        return True
    
    def remove_custom_domain(self, domain):
        return True

class TestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Stopper - Test Mode")
        self.root.geometry("500x650")
        self.root.configure(bg="#232946")
        
        # Use test components
        self.blocker = TestYouTubeBlocker()
        self.create_widgets()

    def create_widgets(self):
        # Title
        title = tk.Label(self.root, text="🎯 YouTube Stopper - Test Mode", 
                        bg="#232946", fg="#eebbc3", font=("Segoe UI", 16, "bold"))
        title.pack(pady=20)
        
        # Status
        status = tk.Label(self.root, text="✅ GUI is working correctly!", 
                         bg="#232946", fg="#b8c1ec", font=("Segoe UI", 12))
        status.pack(pady=10)
        
        # Test motivation widget
        motivation = TestMotivationWidget(self.root, bg="#232946", fg="#fffffe", 
                                        font=("Segoe UI", 11, "italic"))
        motivation.pack(pady=10)
        
        # Test pomodoro widget
        pomodoro = TestPomodoroWidget(self.root)
        pomodoro.pack(pady=10)
        
        # Test button
        test_btn = tk.Button(self.root, text="Test Button", 
                            command=self.test_function,
                            bg="#eebbc3", fg="#232946", 
                            font=("Segoe UI", 12, "bold"))
        test_btn.pack(pady=10)
        
        # Footer
        footer = tk.Label(self.root, text="If you see this, the GUI is working properly!", 
                         bg="#232946", fg="#eebbc3", font=("Segoe UI", 9))
        footer.pack(side="bottom", pady=20)

    def test_function(self):
        messagebox.showinfo("Test", "✅ Button clicks are working!\n\nThe GUI components are functioning correctly.")

def main():
    print("🧪 YouTube Stopper - Test Mode")
    print("=" * 40)
    
    try:
        print("Testing tkinter...")
        root = tk.Tk()
        print("✅ Tkinter imported and root created")
        
        print("Creating test app...")
        app = TestApp(root)
        print("✅ Test app created successfully")
        
        print("Starting GUI...")
        root.mainloop()
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("Make sure all required packages are installed")
        input("Press Enter to exit...")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
