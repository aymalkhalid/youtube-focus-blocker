#!/usr/bin/env python3
"""
YouTube Stopper - A productivity app to block YouTube distractions
Author: Learning with AI Assistant
Date: July 3, 2025

This application helps users avoid YouTube distractions by:
1. Blocking YouTube domains through hosts file modification
2. Providing a simple command-line interface
"""

import os
import sys
import subprocess
from pathlib import Path


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
                sys.exit(0)
            except subprocess.CalledProcessError:
                print("Error: Could not restart with admin rights. Please run as administrator.")
                sys.exit(1)

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

    def get_custom_domains(self):
        custom_file = Path.home() / "youtube_stopper_custom_blocklist.txt"
        if custom_file.exists():
            with open(custom_file, 'r', encoding='utf-8') as f:
                return [line.strip() for line in f if line.strip() and not line.startswith('#')]
        return []

    def add_custom_domain(self, domain):
        """Add a custom domain to the blocklist"""
        custom_file = Path.home() / "youtube_stopper_custom_blocklist.txt"
        domains = set(self.get_custom_domains())
        domains.add(domain)
        with open(custom_file, 'w', encoding='utf-8') as f:
            for d in sorted(domains):
                f.write(d + '\n')
        
        # If blocking is currently active, update the hosts file immediately
        if self.is_blocked():
            print(f"🔄 Updating hosts file to include {domain}...")
            self.update_blocked_domains()

    def remove_custom_domain(self, domain):
        """Remove a custom domain from the blocklist"""
        custom_file = Path.home() / "youtube_stopper_custom_blocklist.txt"
        domains = set(self.get_custom_domains())
        if domain in domains:
            domains.remove(domain)
            with open(custom_file, 'w', encoding='utf-8') as f:
                for d in sorted(domains):
                    f.write(d + '\n')
            
            # If blocking is currently active, update the hosts file immediately
            if self.is_blocked():
                print(f"🔄 Removing {domain} from hosts file...")
                self.update_blocked_domains()

    def get_all_blocked_domains(self):
        """Get all domains to block, including variations of custom domains"""
        all_domains = self.youtube_domains.copy()
        
        # Add custom domains with common variations
        for domain in self.get_custom_domains():
            all_domains.append(domain)
            # Add www prefix if not already present
            if not domain.startswith('www.'):
                all_domains.append(f'www.{domain}')
            # Add mobile prefix for social media sites
            if any(social in domain for social in ['facebook', 'instagram', 'twitter', 'tiktok']):
                all_domains.append(f'm.{domain}')
        
        return all_domains

    def block_youtube(self):
        """
        Add YouTube domains to hosts file to block access
        """
        if not self.is_admin():
            print("Requesting admin rights...")
            self.run_as_admin()
            return

        try:
            # First, create a backup
            if not self.backup_file.exists():
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

            for domain in self.get_all_blocked_domains():
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
            return False

    def unblock_youtube(self):
        """
        Remove YouTube blocking entries from hosts file
        """
        if not self.is_admin():
            print("Requesting admin rights...")
            self.run_as_admin()
            return

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
            return False

    def update_blocked_domains(self):
        """Update the hosts file with current domain list (when blocking is active)"""
        if not self.is_admin():
            print("Admin rights required to update blocked domains")
            return False
            
        try:
            # First unblock (remove old entries)
            with open(self.hosts_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()

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

            # Add updated blocking entries
            blocking_entries = [
                "",  # Empty line for spacing
                self.start_marker,
                "# Blocking domains for productivity"
            ]

            for domain in self.get_all_blocked_domains():
                blocking_entries.append(f"127.0.0.1 {domain}")

            blocking_entries.append(self.end_marker)
            blocking_entries.append("")  # Empty line at the end

            # Write updated content
            new_content = "".join(new_lines) + "\n".join(blocking_entries)
            
            with open(self.hosts_file, 'w', encoding='utf-8') as f:
                f.write(new_content)

            # Flush DNS cache
            try:
                subprocess.run(['ipconfig', '/flushdns'],
                             capture_output=True, check=True)
                print("🔄 DNS cache flushed - changes should take effect immediately")
            except subprocess.CalledProcessError:
                print("⚠️ Could not flush DNS cache - you may need to restart your browser")

            return True

        except Exception as e:
            print(f"❌ Error updating blocked domains: {e}")
            return False


if __name__ == "__main__":
    blocker = YouTubeBlocker()

    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        if command == "block":
            blocker.block_youtube()
        elif command == "unblock":
            blocker.unblock_youtube()
        elif command == "status":
            if blocker.is_blocked():
                print("🔒 YouTube is currently blocked.")
            else:
                print("🔓 YouTube is currently accessible.")
        else:
            print(f"Unknown command: {command}")
            print("Usage: python youtube_stopper.py [block|unblock|status]")
    else:
        print("🎯 YouTube Stopper")
        print("Usage: python youtube_stopper.py [block|unblock|status]")
        if blocker.is_blocked():
            print("Current status: 🔒 Blocked")
        else:
            print("Current status: 🔓 Accessible")
