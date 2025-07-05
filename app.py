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
        self.root.title("YouTube Stopper")
        self.root.geometry("500x650")  # Increased height to accommodate new UI elements
        self.root.minsize(350, 500)     # Set a reasonable minimum size
        self.blocker = YouTubeBlocker()
        self.create_widgets()
        self.update_status()

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
            font=("Segoe UI", 12, "bold"), indicatoron=False, width=18, pady=10,
            bg="#eebbc3", fg="#232946", selectcolor="#eebbc3", activebackground="#eebbc3", activeforeground="#232946",
            bd=0, relief="flat", highlightthickness=0, cursor="hand2"
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

        # Motivation widget
        self.motivation_label = MotivationWidget(self.root, bg="#232946", fg="#fffffe", font=("Segoe UI", 11, "italic"), wraplength=340, justify="center")
        self.motivation_label.pack(pady=(0, 15))

        # Pomodoro widget
        self.pomodoro_widget = PomodoroWidget(self.root)
        self.pomodoro_widget.pack(pady=(0, 10))

        # Custom blocklist UI
        self.custom_blocklist_label = tk.Label(self.root, text="Custom Blocked Links:", bg="#232946", fg="#eebbc3", font=("Segoe UI", 11, "bold"))
        self.custom_blocklist_label.pack(pady=(10, 0))
        self.custom_blocklist_listbox = tk.Listbox(self.root, bg="#232946", fg="#fffffe", selectbackground="#eebbc3", selectforeground="#232946", font=("Segoe UI", 10), width=40, height=4)
        self.custom_blocklist_listbox.pack(pady=(0, 5))
        self.update_custom_blocklist_listbox()
        entry_frame = tk.Frame(self.root, bg="#232946")
        entry_frame.pack(pady=(0, 5))
        self.custom_blocklist_entry = tk.Entry(entry_frame, font=("Segoe UI", 10), width=25)
        self.custom_blocklist_entry.pack(side="left", padx=(0, 5))
        add_btn = tk.Button(entry_frame, text="Add", command=self.add_custom_domain, bg="#eebbc3", fg="#232946", font=("Segoe UI", 10, "bold"), width=7)
        add_btn.pack(side="left")
        remove_btn = tk.Button(self.root, text="Remove Selected", command=self.remove_selected_custom_domain, bg="#eebbc3", fg="#232946", font=("Segoe UI", 10), width=18)
        remove_btn.pack(pady=(0, 10))

    def toggle_block(self):
        if self.toggle_var.get():
            self.block_youtube()
        else:
            self.unblock_youtube()

    def block_youtube(self):
        if self.blocker.block_youtube():
            messagebox.showinfo("Success", "YouTube has been blocked.")
            if not self.session_active:
                self.session_active = True
                from datetime import datetime
                self.session_start = datetime.now()
                self.session_label.config(text=f"Session: Started at {self.session_start.strftime('%H:%M:%S')}")
        else:
            messagebox.showerror("Error", "Could not block YouTube. Please run as administrator.")
        self.update_status()

    def unblock_youtube(self):
        if self.blocker.unblock_youtube():
            messagebox.showinfo("Success", "YouTube has been unblocked.")
            if self.session_active:
                self.session_active = False
                from datetime import datetime
                end_time = datetime.now()
                if self.session_start:
                    elapsed = (end_time - self.session_start).total_seconds()
                    self.session_seconds += int(elapsed)
                self.session_label.config(text=f"Session: Ended at {end_time.strftime('%H:%M:%S')}")
                self.session_start = None
        else:
            messagebox.showerror("Error", "Could not unblock YouTube. Please run as administrator.")
        self.update_status()

    def update_status(self):
        if self.blocker.is_blocked():
            self.status_label.config(text="Status: Blocked", fg="red")
            self.toggle_var.set(1)
            self.toggle_button.config(text="Unblock YouTube")
        else:
            self.status_label.config(text="Status: Unblocked", fg="green")
            self.toggle_var.set(0)
            self.toggle_button.config(text="Block YouTube")

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
            self.blocker.add_custom_domain(domain)
            self.update_custom_blocklist_listbox()
            self.custom_blocklist_entry.delete(0, tk.END)
            
            # Enhanced feedback message
            if self.blocker.is_blocked():
                messagebox.showinfo("Custom Blocklist", 
                    f"Added: {domain}\n\n"
                    f"The domain has been added to your hosts file.\n"
                    f"You may need to:\n"
                    f"• Clear your browser cache\n"
                    f"• Restart your browser\n"
                    f"• Wait a few seconds for DNS changes to take effect")
            else:
                messagebox.showinfo("Custom Blocklist", 
                    f"Added: {domain}\n\n"
                    f"The domain will be blocked when you activate YouTube blocking.")
        else:
            messagebox.showwarning("Input Error", "Please enter a domain to block.")

    def remove_selected_custom_domain(self):
        selection = self.custom_blocklist_listbox.curselection()
        if selection:
            domain = self.custom_blocklist_listbox.get(selection[0])
            self.blocker.remove_custom_domain(domain)
            self.update_custom_blocklist_listbox()
            
            # Enhanced feedback message
            if self.blocker.is_blocked():
                messagebox.showinfo("Custom Blocklist", 
                    f"Removed: {domain}\n\n"
                    f"The domain has been removed from your hosts file.\n"
                    f"You should now be able to access it again.")
            else:
                messagebox.showinfo("Custom Blocklist", f"Removed: {domain}")
        else:
            messagebox.showwarning("Selection Error", "Please select a domain to remove.")

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