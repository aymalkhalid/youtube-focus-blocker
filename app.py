import sys
import os
import tkinter as tk
from tkinter import messagebox
from youtube_stopper import YouTubeBlocker
from motivation_widget import MotivationWidget
from pomodoro_widget import PomodoroWidget

def is_admin():
    try:
        # This is for Unix/Linux systems
        uid = os.getuid()
        print(f"Unix system detected, UID: {uid}")
        return uid == 0
    except AttributeError:
        # This is for Windows systems
        import ctypes
        try:
            admin_status = ctypes.windll.shell32.IsUserAnAdmin()
            print(f"Windows system detected, admin status: {admin_status}")
            return admin_status != 0
        except Exception as e:
            print(f"Error checking admin status: {e}")
            return False

def run_as_admin():
    print("Checking admin status...")
    if is_admin():
        print("Already running as admin")
        return True
    else:
        print("Not running as admin, attempting to relaunch...")
        import subprocess
        import time
        
        # Use the full path to the current Python executable
        python_exe = sys.executable
        script = os.path.abspath(sys.argv[0])
        
        # For the executable, we don't need to use python interpreter
        if script.endswith('.exe'):
            cmd = f'Start-Process -FilePath "{script}" -ArgumentList "--as-admin" -Verb RunAs'
        else:
            # Use a simpler approach without WindowStyle Hidden to see errors
            cmd = f'Start-Process -FilePath "{python_exe}" -ArgumentList "{script}","--as-admin" -Verb RunAs'
        
        print(f"PowerShell command: {cmd}")
        
        try:
            result = subprocess.run([
                'powershell', '-Command', cmd
            ], check=True, capture_output=True, text=True, timeout=10)
            
            print(f"PowerShell executed successfully")
            if result.stdout:
                print(f"PowerShell output: {result.stdout}")
            if result.stderr:
                print(f"PowerShell errors: {result.stderr}")
            
            # Give the new process a moment to start
            time.sleep(2)
            print("Exiting original process...")
            sys.exit(0)
            
        except subprocess.TimeoutExpired:
            print("PowerShell command timed out")
            return False
        except subprocess.CalledProcessError as e:
            print(f"PowerShell command failed: {e}")
            if e.stdout:
                print(f"Output: {e.stdout}")
            if e.stderr:
                print(f"Error: {e.stderr}")
            return False
        except Exception as e:
            print(f"Unexpected error: {e}")
            return False

class YouTubeStopperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎯 YouTube Stopper")
        self.root.geometry("520x800")  # Increased height for better layout
        self.root.minsize(450, 700)    # Increased minimum size
        self.root.resizable(True, True)  # Allow resizing for better UX
        
        # Set window icon if available and center the window
        self.center_window()
        
        self.blocker = YouTubeBlocker()
        self.create_widgets()
        self.update_status()
        
        # Add hover effects for better UX
        self.add_hover_effects()
        
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
        style = {
            "bg": "#232946",
            "fg": "#eebbc3",
            "font": ("Segoe UI", 13, "bold")
        }
        self.status_label = tk.Label(self.root, text="", **style)
        self.status_label.pack(pady=(20, 10))

        self.toggle_var = tk.IntVar(value=1 if self.blocker.is_blocked() else 0)
        self.toggle_button = tk.Checkbutton(
            self.root, text="Block YouTube", variable=self.toggle_var,
            onvalue=1, offvalue=0, command=self.toggle_block,
            font=("Segoe UI", 14, "bold"), indicatoron=False, width=18, pady=12,
            bg="#eebbc3", fg="#232946", selectcolor="#d4a5af", 
            activebackground="#d4a5af", activeforeground="#232946",
            bd=2, relief="flat", highlightthickness=0, cursor="hand2"
        )
        self.toggle_button.pack(pady=10)

        self.session_label = tk.Label(self.root, text="Session: Not started", bg="#232946", fg="#b8c1ec", font=("Segoe UI", 11))
        self.session_label.pack(pady=5)

        self.time_label = tk.Label(self.root, text="Time Blocked: 00:00:00", bg="#232946", fg="#b8c1ec", font=("Segoe UI", 11, "bold"))
        self.time_label.pack(pady=(5, 20))

        # Add a frame for a modern border effect
        border = tk.Frame(self.root, bg="#eebbc3", height=2)
        border.pack(fill="x", padx=30, pady=(0, 10))

        # Add a footer
        self.footer = tk.Label(self.root, text="Made with 💌 by Aymal Khalid Khan", bg="#232946", fg="#eebbc3", font=("Segoe UI", 9))
        self.footer.pack(side="bottom", pady=8)

        self.session_active = False
        self.session_start = None
        self.session_seconds = 0
        self.update_timer()

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

        # Custom blocklist UI with better styling
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
        
        self.update_custom_blocklist_listbox()
        
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
        
        add_btn = tk.Button(
            entry_frame, text="Add", command=self.add_custom_domain, 
            bg="#86efac", fg="#232946", font=("Segoe UI", 10, "bold"), 
            width=8, bd=0, relief="flat", cursor="hand2"
        )
        add_btn.pack(side="right")
        self.add_btn = add_btn  # Store as instance variable
        
        remove_btn = tk.Button(
            self.root, text="Remove Selected", command=self.remove_selected_custom_domain, 
            bg="#fca5a5", fg="#232946", font=("Segoe UI", 10, "bold"), 
            width=20, bd=0, relief="flat", cursor="hand2"
        )
        remove_btn.pack(pady=(5, 12))  # Reduced bottom padding
        self.remove_btn = remove_btn  # Store as instance variable
        
        # Add hover effects
        self.add_hover_effects()

    def toggle_block(self):
        if self.toggle_var.get():
            self.block_youtube()
        else:
            self.unblock_youtube()

    def block_youtube(self):
        if self.blocker.block_youtube():
            # Success feedback with better UX
            self.show_success_message("✅ YouTube Blocked Successfully", "Focus mode activated! YouTube is now blocked.")
            if not self.session_active:
                self.session_active = True
                from datetime import datetime
                self.session_start = datetime.now()
                self.session_label.config(text=f"Session: Started at {self.session_start.strftime('%H:%M:%S')}")
        else:
            self.show_error_message("❌ Blocking Failed", "Could not block YouTube. Please run as administrator.")
        self.update_status()

    def unblock_youtube(self):
        if self.blocker.unblock_youtube():
            # Success feedback with session summary
            session_summary = ""
            if self.session_active:
                self.session_active = False
                from datetime import datetime
                end_time = datetime.now()
                if self.session_start:
                    elapsed = (end_time - self.session_start).total_seconds()
                    self.session_seconds += int(elapsed)
                    hours = int(elapsed // 3600)
                    minutes = int((elapsed % 3600) // 60)
                    session_summary = f"\n\nSession Duration: {hours:02d}:{minutes:02d}:{int(elapsed % 60):02d}"
                self.session_label.config(text=f"Session: Ended at {end_time.strftime('%H:%M:%S')}")
                self.session_start = None
            
            self.show_success_message("🔓 YouTube Unblocked", f"YouTube is now accessible.{session_summary}")
        else:
            self.show_error_message("❌ Unblocking Failed", "Could not unblock YouTube. Please run as administrator.")
        self.update_status()
    
    def show_success_message(self, title, message):
        """Show a styled success message"""
        messagebox.showinfo(title, message)
    
    def show_error_message(self, title, message):
        """Show a styled error message"""
        messagebox.showerror(title, message)

    def update_status(self):
        if self.blocker.is_blocked():
            self.status_label.config(text="Status: ✅ YouTube Blocked", fg="#4ade80")  # Success green
            self.toggle_var.set(1)
            self.toggle_button.config(text="Unblock YouTube", bg="#fca5a5")  # Light red
        else:
            self.status_label.config(text="Status: ⚠️ YouTube Accessible", fg="#fb7185")  # Warning red
            self.toggle_var.set(0)
            self.toggle_button.config(text="Block YouTube", bg="#86efac")  # Light green

    def update_timer(self):
        if self.session_active and self.session_start:
            from datetime import datetime
            elapsed = (datetime.now() - self.session_start).total_seconds() + self.session_seconds
        else:
            elapsed = self.session_seconds
        h = int(elapsed // 3600)
        m = int((elapsed % 3600) // 60)
        s = int(elapsed % 60)
        self.time_label.config(text=f"Time Blocked: {h:02d}:{m:02d}:{s:02d}")
        self.root.after(1000, self.update_timer)

    def update_custom_blocklist_listbox(self):
        self.custom_blocklist_listbox.delete(0, tk.END)
        for domain in self.blocker.get_custom_domains():
            self.custom_blocklist_listbox.insert(tk.END, domain)

    def add_custom_domain(self):
        domain = self.custom_blocklist_entry.get().strip()
        if domain:
            # Basic validation
            if self.validate_domain(domain):
                # Check for duplicates
                existing_domains = self.blocker.get_custom_domains()
                if domain not in existing_domains:
                    self.blocker.add_custom_domain(domain)
                    self.update_custom_blocklist_listbox()
                    self.custom_blocklist_entry.delete(0, tk.END)
                    
                    # Enhanced feedback message
                    if self.blocker.is_blocked():
                        messagebox.showinfo("✅ Domain Added", 
                            f"Added '{domain}' to custom blocklist!\n\n"
                            f"The domain is now blocked. You may need to:\n"
                            f"• Clear your browser cache\n"
                            f"• Restart your browser\n"
                            f"• Wait a few seconds for DNS changes to take effect")
                    else:
                        messagebox.showinfo("✅ Domain Added", 
                            f"Added '{domain}' to custom blocklist!\n\n"
                            f"The domain will be blocked when you activate YouTube blocking.")
                else:
                    messagebox.showwarning("⚠️ Duplicate Domain", f"'{domain}' is already in your blocklist!")
            else:
                messagebox.showerror("❌ Invalid Domain", f"'{domain}' is not a valid domain format!\n\nExamples:\n• youtube.com\n• www.example.org\n• subdomain.site.net")
        else:
            messagebox.showwarning("⚠️ Empty Input", "Please enter a domain to block!")

    def remove_selected_custom_domain(self):
        selection = self.custom_blocklist_listbox.curselection()
        if selection:
            domain = self.custom_blocklist_listbox.get(selection[0])
            self.blocker.remove_custom_domain(domain)
            self.update_custom_blocklist_listbox()
            
            # Enhanced feedback message
            if self.blocker.is_blocked():
                messagebox.showinfo("🗑️ Domain Removed", 
                    f"Removed '{domain}' from blocklist!\n\n"
                    f"The domain has been removed from your hosts file.\n"
                    f"You should now be able to access it again.")
            else:
                messagebox.showinfo("🗑️ Domain Removed", f"Removed '{domain}' from blocklist!")
        else:
            messagebox.showwarning("⚠️ No Selection", "Please select a domain from the list to remove!")

    def validate_domain(self, domain):
        """Basic domain validation"""
        import re
        # Simple domain validation pattern
        pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9\-]*[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]*[a-zA-Z0-9])?)*$'
        return re.match(pattern, domain) and len(domain) <= 253

    def add_hover_effects(self):
        """Add hover effects to interactive elements"""
        # Hover effect for main toggle button
        def on_enter_toggle(e):
            if self.toggle_var.get():
                self.toggle_button.config(bg="#d4a5af")
            else:
                self.toggle_button.config(bg="#d4a5af")
        
        def on_leave_toggle(e):
            if self.toggle_var.get():
                self.toggle_button.config(bg="#eebbc3")
            else:
                self.toggle_button.config(bg="#eebbc3")
        
        self.toggle_button.bind("<Enter>", on_enter_toggle)
        self.toggle_button.bind("<Leave>", on_leave_toggle)
    
        # Hover effects for Add and Remove buttons
        def on_enter_add(e):
            self.add_btn.config(bg="#65a30d")
        
        def on_leave_add(e):
            self.add_btn.config(bg="#86efac")
        
        def on_enter_remove(e):
            self.remove_btn.config(bg="#991b1b")
        
        def on_leave_remove(e):
            self.remove_btn.config(bg="#fca5a5")
        
        self.add_btn.bind("<Enter>", on_enter_add)
        self.add_btn.bind("<Leave>", on_leave_add)
        self.remove_btn.bind("<Enter>", on_enter_remove)
        self.remove_btn.bind("<Leave>", on_leave_remove)

if __name__ == "__main__":
    try:
        print(f"Script started with args: {sys.argv}")
        print(f"Working directory: {os.getcwd()}")
        print(f"Python executable: {sys.executable}")
        print(f"Is admin: {is_admin()}")
        print(f"Has --as-admin flag: {'--as-admin' in sys.argv}")
        
        # If we have the --as-admin flag, we were relaunched with admin rights
        if '--as-admin' in sys.argv:
            print("Script was relaunched with admin rights")
            if is_admin():
                print("✅ Successfully running with admin privileges")
            else:
                print("❌ Still not running with admin privileges despite relaunch")
                # Continue anyway, maybe some features will work
        
        # If not admin and no --as-admin flag, try to relaunch
        elif not is_admin():
            print("Requesting admin rights...")
            if not run_as_admin():
                print("⚠️ Could not get admin rights, continuing anyway...")
                print("⚠️ Some features may not work properly")
        
        print("Launching YouTube Stopper...")
        
        # Test if all imports work
        print("Testing imports...")
        from youtube_stopper import YouTubeBlocker
        from motivation_widget import MotivationWidget
        from pomodoro_widget import PomodoroWidget
        print("✅ All imports successful")
        
        # Test if tkinter works
        print("Initializing GUI...")
        root = tk.Tk()
        print("✅ Tkinter root created")
        
        app = YouTubeStopperApp(root)
        print("✅ App instance created")
        
        print("Starting main loop...")
        root.mainloop()
        
    except ImportError as e:
        error_msg = f"Import Error: {e}\n\nMissing required modules. Please install dependencies with:\npip install -r requirements.txt"
        print(f"❌ {error_msg}")
        try:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Import Error", error_msg)
        except:
            pass
        input("Press Enter to exit...")
        sys.exit(1)
        
    except Exception as e:
        error_msg = f"Unexpected Error: {e}"
        print(f"❌ {error_msg}")
        import traceback
        traceback.print_exc()
        
        try:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Application Error", f"{error_msg}\n\nCheck the console for detailed error information.")
        except:
            pass
        
        input("Press Enter to exit...")
        sys.exit(1)