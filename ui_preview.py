#!/usr/bin/env python3
"""
Test script to preview the YouTube Stopper GUI without admin privileges.
This allows testing UI/UX improvements without system modifications.
"""

import tkinter as tk
from tkinter import messagebox
import os
import sys

# Add the current directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from motivation_widget import MotivationWidget
from pomodoro_widget import PomodoroWidget

class YouTubeStopperPreview:
    def __init__(self, root):
        self.root = root
        self.root.title("🎯 YouTube Stopper - UI Preview")
        self.root.geometry("520x800")  # Increased height to fit all content
        self.root.minsize(450, 700)    # Increased minimum size
        self.root.resizable(True, True)
        
        # Center the window
        self.center_window()
        
        # Mock blocker for preview
        self.blocked_status = False
        self.create_widgets()
        self.update_status()
        
    def center_window(self):
        """Center the window on the screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def create_widgets(self):
        self.root.configure(bg="#232946")
        
        # Status section with better visual emphasis
        status_frame = tk.Frame(self.root, bg="#232946")
        status_frame.pack(pady=(20, 15))
        
        style = {
            "bg": "#232946",
            "fg": "#eebbc3",
            "font": ("Segoe UI", 13, "bold")
        }
        self.status_label = tk.Label(status_frame, text="Status: Preview Mode", **style)
        self.status_label.pack()

        # Main action button with better styling
        self.toggle_var = tk.IntVar(value=0)
        self.toggle_button = tk.Checkbutton(
            self.root, text="Block YouTube (Preview)", variable=self.toggle_var,
            onvalue=1, offvalue=0, command=self.toggle_block,
            font=("Segoe UI", 14, "bold"), indicatoron=False, width=18, pady=12,
            bg="#eebbc3", fg="#232946", selectcolor="#d4a5af", 
            activebackground="#d4a5af", activeforeground="#232946",
            bd=2, relief="flat", highlightthickness=0, cursor="hand2"
        )
        self.toggle_button.pack(pady=15)

        # Session info section with card-like appearance
        session_frame = tk.Frame(self.root, bg="#2c3454", relief="flat", bd=1)
        session_frame.pack(pady=(10, 20), padx=30, fill="x")
        
        tk.Label(session_frame, text="📊 Session Info", bg="#2c3454", fg="#eebbc3", font=("Segoe UI", 11, "bold")).pack(pady=(10, 5))
        
        self.session_label = tk.Label(session_frame, text="Session: Preview Mode", bg="#2c3454", fg="#b8c1ec", font=("Segoe UI", 10))
        self.session_label.pack(pady=2)

        self.time_label = tk.Label(session_frame, text="Time Blocked: 00:15:42", bg="#2c3454", fg="#b8c1ec", font=("Segoe UI", 10, "bold"))
        self.time_label.pack(pady=(2, 10))

        # Motivation widget with visual separator
        separator1 = tk.Frame(self.root, bg="#3d4465", height=1)
        separator1.pack(fill="x", padx=40, pady=(20, 15))
        
        motivation_header = tk.Label(self.root, text="💪 Daily Motivation", bg="#232946", fg="#eebbc3", font=("Segoe UI", 11, "bold"))
        motivation_header.pack(pady=(0, 10))
        
        self.motivation_label = MotivationWidget(self.root, bg="#232946", fg="#fffffe", font=("Segoe UI", 11, "italic"), wraplength=340, justify="center")
        self.motivation_label.pack(pady=(0, 20))

        # Pomodoro widget with visual separator
        separator2 = tk.Frame(self.root, bg="#3d4465", height=1)
        separator2.pack(fill="x", padx=40, pady=(0, 15))
        
        self.pomodoro_widget = PomodoroWidget(self.root)
        self.pomodoro_widget.pack(pady=(0, 20))

        # Custom blocklist UI with better styling and improved layout
        separator3 = tk.Frame(self.root, bg="#3d4465", height=1)
        separator3.pack(fill="x", padx=40, pady=(0, 15))
        
        self.custom_blocklist_label = tk.Label(self.root, text="🚫 Custom Blocked Sites", bg="#232946", fg="#eebbc3", font=("Segoe UI", 11, "bold"))
        self.custom_blocklist_label.pack(pady=(0, 10))
        
        # Create a frame for the listbox with padding - reduced height for better fit
        listbox_frame = tk.Frame(self.root, bg="#2c3454", relief="flat", bd=1)
        listbox_frame.pack(pady=(0, 8), padx=30, fill="x")
        
        self.custom_blocklist_listbox = tk.Listbox(
            listbox_frame, bg="#2c3454", fg="#fffffe", 
            selectbackground="#eebbc3", selectforeground="#232946", 
            font=("Segoe UI", 10), height=3, bd=0, highlightthickness=0  # Reduced height from 4 to 3
        )
        self.custom_blocklist_listbox.pack(pady=6, padx=6, fill="x")  # Reduced padding
        
        # Add some sample items
        self.custom_blocklist_listbox.insert(tk.END, "facebook.com")
        self.custom_blocklist_listbox.insert(tk.END, "twitter.com")
        self.custom_blocklist_listbox.insert(tk.END, "instagram.com")
        
        # Input section with better styling and more prominent appearance
        entry_container = tk.Frame(self.root, bg="#2c3454", relief="flat", bd=1)
        entry_container.pack(pady=(5, 8), padx=30, fill="x")
        
        # Add a label for the input
        input_label = tk.Label(entry_container, text="Add new site to block:", bg="#2c3454", fg="#eebbc3", font=("Segoe UI", 9))
        input_label.pack(pady=(8, 4))
        
        entry_frame = tk.Frame(entry_container, bg="#2c3454")
        entry_frame.pack(pady=(0, 8), padx=8)
        
        self.custom_blocklist_entry = tk.Entry(
            entry_frame, font=("Segoe UI", 11), width=22,  # Slightly larger font and adjusted width
            bg="#232946", fg="#fffffe", insertbackground="#fffffe",
            bd=2, relief="flat", highlightthickness=2, highlightcolor="#eebbc3"
        )
        self.custom_blocklist_entry.pack(side="left", padx=(0, 8), pady=2, fill="x", expand=True)
        
        # Bind Enter key to add domain
        self.custom_blocklist_entry.bind("<Return>", lambda e: self.add_custom_domain())
        
        self.add_btn = tk.Button(
            entry_frame, text="Add", command=self.add_custom_domain, 
            bg="#86efac", fg="#232946", font=("Segoe UI", 10, "bold"), 
            width=8, bd=0, relief="flat", cursor="hand2"
        )
        self.add_btn.pack(side="right")
        
        self.remove_btn = tk.Button(
            self.root, text="Remove Selected", command=self.remove_selected_custom_domain, 
            bg="#fca5a5", fg="#232946", font=("Segoe UI", 10, "bold"), 
            width=20, bd=0, relief="flat", cursor="hand2"
        )
        self.remove_btn.pack(pady=(5, 12))  # Reduced bottom padding

        # Add a frame for a modern border effect
        border = tk.Frame(self.root, bg="#eebbc3", height=2)
        border.pack(fill="x", padx=30, pady=(10, 10))

        # Add a footer
        self.footer = tk.Label(self.root, text="Made with 💌 by Aymal Khalid Khan", bg="#232946", fg="#eebbc3", font=("Segoe UI", 9))
        self.footer.pack(side="bottom", pady=8)

        # Add hover effects
        self.add_hover_effects()

    def add_hover_effects(self):
        """Add hover effects to interactive elements"""
        # Hover effect for main toggle button
        def on_enter_toggle(e):
            self.toggle_button.config(bg="#d4a5af")
        
        def on_leave_toggle(e):
            self.toggle_button.config(bg="#eebbc3")
        
        self.toggle_button.bind("<Enter>", on_enter_toggle)
        self.toggle_button.bind("<Leave>", on_leave_toggle)
        
        # Hover effects for add button
        def on_enter_add(e):
            self.add_btn.config(bg="#65a30d")
        
        def on_leave_add(e):
            self.add_btn.config(bg="#86efac")
        
        # Hover effects for remove button
        def on_enter_remove(e):
            self.remove_btn.config(bg="#991b1b")
        
        def on_leave_remove(e):
            self.remove_btn.config(bg="#fca5a5")
        
        self.add_btn.bind("<Enter>", on_enter_add)
        self.add_btn.bind("<Leave>", on_leave_add)
        self.remove_btn.bind("<Enter>", on_enter_remove)
        self.remove_btn.bind("<Leave>", on_leave_remove)

    def toggle_block(self):
        self.blocked_status = not self.blocked_status
        if self.blocked_status:
            messagebox.showinfo("✅ Preview Mode", "This is a preview - YouTube blocking would be activated in the real app!")
        else:
            messagebox.showinfo("🔓 Preview Mode", "This is a preview - YouTube would be unblocked in the real app!")
        self.update_status()

    def update_status(self):
        if self.blocked_status:
            self.status_label.config(text="Status: ✅ YouTube Blocked (Preview)", fg="#4ade80")
            self.toggle_var.set(1)
            self.toggle_button.config(text="Unblock YouTube", bg="#fca5a5")
        else:
            self.status_label.config(text="Status: ⚠️ YouTube Accessible (Preview)", fg="#fb7185")
            self.toggle_var.set(0)
            self.toggle_button.config(text="Block YouTube", bg="#86efac")

    def add_custom_domain(self):
        domain = self.custom_blocklist_entry.get().strip()
        if domain:
            # Basic validation
            if self.validate_domain(domain):
                # Check for duplicates
                existing_domains = [self.custom_blocklist_listbox.get(i) for i in range(self.custom_blocklist_listbox.size())]
                if domain not in existing_domains:
                    self.custom_blocklist_listbox.insert(tk.END, domain)
                    self.custom_blocklist_entry.delete(0, tk.END)
                    messagebox.showinfo("✅ Preview", f"Added '{domain}' to preview list!")
                else:
                    messagebox.showwarning("⚠️ Duplicate", f"'{domain}' is already in the list!")
            else:
                messagebox.showerror("❌ Invalid Domain", f"'{domain}' is not a valid domain format!\n\nExample: youtube.com or www.example.org")
        else:
            messagebox.showwarning("⚠️ Empty Input", "Please enter a domain to block!")
    
    def validate_domain(self, domain):
        """Basic domain validation"""
        import re
        # Simple domain validation pattern
        pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9\-]*[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]*[a-zA-Z0-9])?)*$'
        return re.match(pattern, domain) and len(domain) <= 253

    def remove_selected_custom_domain(self):
        selection = self.custom_blocklist_listbox.curselection()
        if selection:
            domain = self.custom_blocklist_listbox.get(selection[0])
            self.custom_blocklist_listbox.delete(selection[0])
            messagebox.showinfo("🗑️ Preview", f"Removed '{domain}' from preview list!")
        else:
            messagebox.showwarning("⚠️ No Selection", "Please select a domain from the list to remove!")

if __name__ == "__main__":
    print("🎨 Starting YouTube Stopper UI Preview...")
    print("This preview shows the improved UI without requiring admin privileges.")
    
    root = tk.Tk()
    app = YouTubeStopperPreview(root)
    root.mainloop()
    
    print("UI Preview closed.")
