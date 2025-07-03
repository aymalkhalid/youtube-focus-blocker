#!/usr/bin/env python3
"""
YouTube Stopper GUI - Modern interface for the productivity app
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
from datetime import datetime
import random
import pystray
from PIL import Image, ImageDraw
import webbrowser

from youtube_stopper import YouTubeBlocker, ProductivityTracker, MOTIVATIONAL_MESSAGES


class ModernToggleButton(tk.Canvas):
    """
    A modern, animated toggle switch widget
    """
    
    def __init__(self, parent, width=80, height=40, command=None):
        super().__init__(parent, width=width, height=height, highlightthickness=0)
        
        self.command = command
        self.width = width
        self.height = height
        self.is_on = False
        
        # Colors
        self.bg_color_off = "#e0e0e0"
        self.bg_color_on = "#4CAF50"
        self.circle_color = "#ffffff"
        self.circle_color_hover = "#f5f5f5"
        
        self.bind("<Button-1>", self.toggle)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        
        self.draw()
    
    def draw(self):
        """Draw the toggle switch"""
        self.delete("all")
        
        # Background
        bg_color = self.bg_color_on if self.is_on else self.bg_color_off
        self.create_oval(0, 0, self.height, self.height, fill=bg_color, outline="")
        self.create_oval(self.width-self.height, 0, self.width, self.height, fill=bg_color, outline="")
        self.create_rectangle(self.height//2, 0, self.width-self.height//2, self.height, fill=bg_color, outline="")
        
        # Circle
        circle_x = self.width - self.height + 5 if self.is_on else 5
        circle_y = 5
        circle_size = self.height - 10
        
        self.create_oval(circle_x, circle_y, circle_x + circle_size, circle_y + circle_size, 
                        fill=self.circle_color, outline="", width=0)
    
    def toggle(self, event=None):
        """Toggle the switch state"""
        self.is_on = not self.is_on
        self.draw()
        if self.command:
            self.command(self.is_on)
    
    def set_state(self, state):
        """Set the switch state programmatically"""
        self.is_on = state
        self.draw()
    
    def on_enter(self, event):
        """Mouse hover effect"""
        self.configure(cursor="hand2")
    
    def on_leave(self, event):
        """Mouse leave effect"""
        self.configure(cursor="")


class YouTubeStopperGUI:
    """
    Main GUI application for YouTube Stopper
    """
    
    def __init__(self):
        self.blocker = YouTubeBlocker()
        self.tracker = ProductivityTracker()
        
        # Check admin rights first
        if not self.blocker.is_admin():
            result = messagebox.askyesno(
                "Administrator Rights Required",
                "This app needs administrator privileges to work properly.\n\n"
                "Would you like to restart with admin rights?"
            )
            if result:
                if not self.blocker.run_as_admin():
                    return
            else:
                messagebox.showinfo(
                    "Limited Functionality",
                    "The app will run in demo mode. Blocking features will not work."
                )
        
        self.setup_gui()
        self.setup_system_tray()
        self.update_timer()
        
        # Update GUI with current state
        self.update_status()
        
    def setup_gui(self):
        """Setup the main GUI window"""
        self.root = tk.Tk()
        self.root.title("YouTube Stopper - Stay Focused! 🎯")
        self.root.geometry("500x600")
        self.root.resizable(False, False)
        
        # Modern color scheme
        self.colors = {
            'bg': '#f8f9fa',
            'card': '#ffffff',
            'primary': '#007bff',
            'success': '#28a745',
            'danger': '#dc3545',
            'warning': '#ffc107',
            'text_primary': '#212529',
            'text_secondary': '#6c757d'
        }
        
        self.root.configure(bg=self.colors['bg'])
        
        # Configure styles
        style = ttk.Style()
        style.theme_use('clam')
        
        # Main container
        self.main_frame = tk.Frame(self.root, bg=self.colors['bg'], padx=20, pady=20)
        self.main_frame.pack(fill='both', expand=True)
        
        self.create_header()
        self.create_toggle_section()
        self.create_stats_section()
        self.create_motivation_section()
        self.create_footer()
        
        # Window close handling
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        
    def create_header(self):
        """Create the header section"""
        header_frame = tk.Frame(self.main_frame, bg=self.colors['bg'])
        header_frame.pack(fill='x', pady=(0, 20))
        
        # App title
        title_label = tk.Label(
            header_frame,
            text="🎯 YouTube Stopper",
            font=('Segoe UI', 24, 'bold'),
            fg=self.colors['primary'],
            bg=self.colors['bg']
        )
        title_label.pack()
        
        # Subtitle
        subtitle_label = tk.Label(
            header_frame,
            text="Take control of your digital habits",
            font=('Segoe UI', 12),
            fg=self.colors['text_secondary'],
            bg=self.colors['bg']
        )
        subtitle_label.pack()
        
    def create_toggle_section(self):
        """Create the main toggle section"""
        # Card frame
        card_frame = tk.Frame(
            self.main_frame,
            bg=self.colors['card'],
            relief='solid',
            bd=1
        )
        card_frame.pack(fill='x', pady=(0, 20))
        
        # Card content
        content_frame = tk.Frame(card_frame, bg=self.colors['card'], padx=30, pady=25)
        content_frame.pack(fill='both', expand=True)
        
        # Status text
        self.status_label = tk.Label(
            content_frame,
            text="YouTube is accessible",
            font=('Segoe UI', 16, 'bold'),
            fg=self.colors['text_primary'],
            bg=self.colors['card']
        )
        self.status_label.pack(pady=(0, 15))
        
        # Toggle button
        toggle_frame = tk.Frame(content_frame, bg=self.colors['card'])
        toggle_frame.pack(pady=(0, 15))
        
        tk.Label(
            toggle_frame,
            text="Block YouTube:",
            font=('Segoe UI', 12),
            fg=self.colors['text_primary'],
            bg=self.colors['card']
        ).pack(side='left', padx=(0, 15))
        
        self.toggle_button = ModernToggleButton(
            toggle_frame,
            width=80,
            height=40,
            command=self.toggle_blocking
        )
        self.toggle_button.pack(side='left')
        
        # Action buttons
        button_frame = tk.Frame(content_frame, bg=self.colors['card'])
        button_frame.pack(fill='x', pady=(15, 0))
        
        self.emergency_btn = tk.Button(
            button_frame,
            text="🚨 Emergency Unblock (5 min)",
            font=('Segoe UI', 10),
            bg=self.colors['warning'],
            fg='white',
            relief='flat',
            padx=15,
            pady=8,
            command=self.emergency_unblock
        )
        self.emergency_btn.pack(side='left', padx=(0, 10))
        
        self.break_btn = tk.Button(
            button_frame,
            text="☕ Take a Break",
            font=('Segoe UI', 10),
            bg=self.colors['primary'],
            fg='white',
            relief='flat',
            padx=15,
            pady=8,
            command=self.take_break
        )
        self.break_btn.pack(side='left')
        
    def create_stats_section(self):
        """Create the productivity stats section"""
        # Stats card
        stats_frame = tk.Frame(
            self.main_frame,
            bg=self.colors['card'],
            relief='solid',
            bd=1
        )
        stats_frame.pack(fill='x', pady=(0, 20))
        
        content_frame = tk.Frame(stats_frame, bg=self.colors['card'], padx=30, pady=25)
        content_frame.pack(fill='both', expand=True)
        
        # Stats title
        tk.Label(
            content_frame,
            text="📊 Productivity Stats",
            font=('Segoe UI', 16, 'bold'),
            fg=self.colors['text_primary'],
            bg=self.colors['card']
        ).pack(anchor='w', pady=(0, 15))
        
        # Stats grid
        stats_grid = tk.Frame(content_frame, bg=self.colors['card'])
        stats_grid.pack(fill='x')
        
        # Current session
        session_frame = tk.Frame(stats_grid, bg=self.colors['card'])
        session_frame.pack(fill='x', pady=(0, 10))
        
        tk.Label(
            session_frame,
            text="Current Session:",
            font=('Segoe UI', 11, 'bold'),
            fg=self.colors['text_primary'],
            bg=self.colors['card']
        ).pack(side='left')
        
        self.session_time_label = tk.Label(
            session_frame,
            text="00:00",
            font=('Segoe UI', 11),
            fg=self.colors['success'],
            bg=self.colors['card']
        )
        self.session_time_label.pack(side='right')
        
        # Total time
        total_frame = tk.Frame(stats_grid, bg=self.colors['card'])
        total_frame.pack(fill='x', pady=(0, 10))
        
        tk.Label(
            total_frame,
            text="Total Productive Time:",
            font=('Segoe UI', 11, 'bold'),
            fg=self.colors['text_primary'],
            bg=self.colors['card']
        ).pack(side='left')
        
        self.total_time_label = tk.Label(
            total_frame,
            text="0.0 hours",
            font=('Segoe UI', 11),
            fg=self.colors['primary'],
            bg=self.colors['card']
        )
        self.total_time_label.pack(side='right')
        
        # Sessions today
        sessions_frame = tk.Frame(stats_grid, bg=self.colors['card'])
        sessions_frame.pack(fill='x')
        
        tk.Label(
            sessions_frame,
            text="Sessions Today:",
            font=('Segoe UI', 11, 'bold'),
            fg=self.colors['text_primary'],
            bg=self.colors['card']
        ).pack(side='left')
        
        self.sessions_today_label = tk.Label(
            sessions_frame,
            text="0",
            font=('Segoe UI', 11),
            fg=self.colors['primary'],
            bg=self.colors['card']
        )
        self.sessions_today_label.pack(side='right')
        
    def create_motivation_section(self):
        """Create the motivation section"""
        # Motivation card
        motivation_frame = tk.Frame(
            self.main_frame,
            bg=self.colors['card'],
            relief='solid',
            bd=1
        )
        motivation_frame.pack(fill='x', pady=(0, 20))
        
        content_frame = tk.Frame(motivation_frame, bg=self.colors['card'], padx=30, pady=25)
        content_frame.pack(fill='both', expand=True)
        
        # Motivation title
        tk.Label(
            content_frame,
            text="💡 Stay Motivated",
            font=('Segoe UI', 16, 'bold'),
            fg=self.colors['text_primary'],
            bg=self.colors['card']
        ).pack(anchor='w', pady=(0, 15))
        
        # Motivation message
        self.motivation_label = tk.Label(
            content_frame,
            text=random.choice(MOTIVATIONAL_MESSAGES),
            font=('Segoe UI', 12),
            fg=self.colors['text_secondary'],
            bg=self.colors['card'],
            wraplength=400,
            justify='center'
        )
        self.motivation_label.pack(pady=(0, 15))
        
        # New message button
        tk.Button(
            content_frame,
            text="🔄 New Message",
            font=('Segoe UI', 10),
            bg=self.colors['primary'],
            fg='white',
            relief='flat',
            padx=15,
            pady=5,
            command=self.new_motivation_message
        ).pack()
        
    def create_footer(self):
        """Create the footer section"""
        footer_frame = tk.Frame(self.main_frame, bg=self.colors['bg'])
        footer_frame.pack(fill='x', side='bottom')
        
        # Settings and help buttons
        button_frame = tk.Frame(footer_frame, bg=self.colors['bg'])
        button_frame.pack(fill='x')
        
        tk.Button(
            button_frame,
            text="⚙️ Settings",
            font=('Segoe UI', 10),
            bg=self.colors['text_secondary'],
            fg='white',
            relief='flat',
            padx=15,
            pady=5,
            command=self.show_settings
        ).pack(side='left')
        
        tk.Button(
            button_frame,
            text="❓ Help",
            font=('Segoe UI', 10),
            bg=self.colors['text_secondary'],
            fg='white',
            relief='flat',
            padx=15,
            pady=5,
            command=self.show_help
        ).pack(side='left', padx=(10, 0))
        
        tk.Button(
            button_frame,
            text="🎯 Hide to Tray",
            font=('Segoe UI', 10),
            bg=self.colors['success'],
            fg='white',
            relief='flat',
            padx=15,
            pady=5,
            command=self.hide_to_tray
        ).pack(side='right')
        
    def toggle_blocking(self, is_on):
        """Handle toggle button click"""
        if is_on:
            if self.blocker.block_youtube():
                self.tracker.start_session()
                messagebox.showinfo(
                    "Blocking Activated! 🔒",
                    "YouTube is now blocked. Stay focused and productive!\n\n"
                    f"💡 {random.choice(MOTIVATIONAL_MESSAGES)}"
                )
            else:
                self.toggle_button.set_state(False)
        else:
            if self.blocker.unblock_youtube():
                session_time = self.tracker.end_session()
                minutes = int(session_time // 60)
                messagebox.showinfo(
                    "Blocking Deactivated 🔓",
                    f"Great work! You stayed focused for {minutes} minutes.\n\n"
                    "Remember: use YouTube mindfully! 🧠"
                )
            else:
                self.toggle_button.set_state(True)
        
        self.update_status()
    
    def emergency_unblock(self):
        """Emergency unblock for 5 minutes"""
        result = messagebox.askyesno(
            "Emergency Unblock",
            "Are you sure you need emergency access to YouTube?\n\n"
            "This will unblock YouTube for 5 minutes only.\n"
            "Use this time wisely! ⏰"
        )
        
        if result:
            self.blocker.unblock_youtube()
            self.toggle_button.set_state(False)
            
            # Schedule re-blocking after 5 minutes
            def reblock():
                time.sleep(300)  # 5 minutes
                if not self.toggle_button.is_on:  # Only if user didn't manually enable
                    self.blocker.block_youtube()
                    self.toggle_button.set_state(True)
                    self.tracker.start_session()
                    self.update_status()
            
            threading.Thread(target=reblock, daemon=True).start()
            
            messagebox.showinfo(
                "Emergency Access Granted",
                "YouTube is temporarily unblocked for 5 minutes.\n\n"
                "The app will automatically re-enable blocking after this time."
            )
            
        self.update_status()
    
    def take_break(self):
        """Take a scheduled break"""
        result = messagebox.askyesno(
            "Take a Break",
            "Taking a break is healthy! 😊\n\n"
            "This will temporarily disable blocking.\n"
            "Remember to re-enable it when you're ready to focus again."
        )
        
        if result:
            self.blocker.unblock_youtube()
            self.toggle_button.set_state(False)
            session_time = self.tracker.end_session()
            
            messagebox.showinfo(
                "Break Time! ☕",
                f"Enjoy your break! You worked for {int(session_time//60)} minutes.\n\n"
                "Don't forget to re-enable blocking when you're ready!"
            )
            
        self.update_status()
    
    def new_motivation_message(self):
        """Show a new motivational message"""
        self.motivation_label.config(text=random.choice(MOTIVATIONAL_MESSAGES))
    
    def update_status(self):
        """Update the GUI with current blocking status"""
        is_blocked = self.blocker.is_blocked()
        
        if is_blocked:
            self.status_label.config(
                text="🔒 YouTube is BLOCKED - Stay focused!",
                fg=self.colors['success']
            )
            self.toggle_button.set_state(True)
        else:
            self.status_label.config(
                text="🔓 YouTube is accessible",
                fg=self.colors['text_primary']
            )
            self.toggle_button.set_state(False)
        
        # Update stats
        stats = self.tracker.get_stats()
        self.total_time_label.config(text=stats['total_time'])
        self.sessions_today_label.config(text=str(stats['sessions_today']))
        
        if hasattr(self.tracker, 'session_start'):
            self.session_time_label.config(text=stats['current_session'])
        else:
            self.session_time_label.config(text="Not active")
    
    def update_timer(self):
        """Update the timer display every second"""
        self.update_status()
        self.root.after(1000, self.update_timer)
    
    def setup_system_tray(self):
        """Setup system tray functionality"""
        try:
            # Create a simple icon
            image = Image.new('RGB', (16, 16), color='red' if self.blocker.is_blocked() else 'gray')
            draw = ImageDraw.Draw(image)
            draw.ellipse([2, 2, 14, 14], fill='white')
            
            menu = pystray.Menu(
                pystray.MenuItem("Show", self.show_window),
                pystray.MenuItem("Toggle Blocking", self.tray_toggle_blocking),
                pystray.MenuItem("Quit", self.quit_app)
            )
            
            self.tray_icon = pystray.Icon("YouTube Stopper", image, menu=menu)
            
        except Exception as e:
            print(f"System tray setup failed: {e}")
            self.tray_icon = None
    
    def show_window(self, icon=None, item=None):
        """Show the main window"""
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()
    
    def hide_to_tray(self):
        """Hide window to system tray"""
        if self.tray_icon:
            self.root.withdraw()
            if not self.tray_icon.visible:
                threading.Thread(target=self.tray_icon.run, daemon=True).start()
        else:
            messagebox.showinfo("System Tray", "System tray not available. Window will minimize.")
            self.root.iconify()
    
    def tray_toggle_blocking(self, icon=None, item=None):
        """Toggle blocking from system tray"""
        current_state = self.blocker.is_blocked()
        self.toggle_blocking(not current_state)
    
    def on_close(self):
        """Handle window close event"""
        result = messagebox.askyesno(
            "Exit YouTube Stopper",
            "Do you want to exit YouTube Stopper?\n\n"
            "Choose 'No' to minimize to system tray instead."
        )
        
        if result:
            self.quit_app()
        else:
            self.hide_to_tray()
    
    def quit_app(self, icon=None, item=None):
        """Quit the application"""
        if hasattr(self.tracker, 'session_start'):
            self.tracker.end_session()
        
        if self.tray_icon and self.tray_icon.visible:
            self.tray_icon.stop()
        
        self.root.quit()
        self.root.destroy()
    
    def show_settings(self):
        """Show settings window"""
        messagebox.showinfo(
            "Settings",
            "Settings panel coming soon! 🛠️\n\n"
            "Future features:\n"
            "• Custom block duration\n"
            "• Website whitelist\n"
            "• Break reminders\n"
            "• Productivity goals"
        )
    
    def show_help(self):
        """Show help information"""
        messagebox.showinfo(
            "Help - YouTube Stopper",
            "🎯 How to use YouTube Stopper:\n\n"
            "1. Toggle 'Block YouTube' to start focusing\n"
            "2. Use 'Emergency Unblock' only when absolutely necessary\n"
            "3. Take breaks when you need them\n"
            "4. Monitor your productivity stats\n\n"
            "💡 Tips:\n"
            "• Run the app at startup for best results\n"
            "• Use the system tray to keep it running\n"
            "• Set daily productivity goals\n\n"
            "⚠️ Requires administrator privileges to work properly."
        )
    
    def run(self):
        """Start the GUI application"""
        self.root.mainloop()


if __name__ == "__main__":
    app = YouTubeStopperGUI()
    app.run()
