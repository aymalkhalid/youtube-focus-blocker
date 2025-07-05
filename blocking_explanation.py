#!/usr/bin/env python3
"""
Demo script to show how custom domain blocking works.
This explains the persistent nature of hosts file blocking.
"""

def explain_blocking_mechanism():
    print("🔐 YouTube Stopper - Custom Domain Blocking Explanation")
    print("=" * 60)
    print()
    
    print("📋 HOW IT WORKS:")
    print("1. Modifies your system's hosts file")
    print("2. Redirects blocked domains to 127.0.0.1 (localhost)")
    print("3. Operating system blocks requests BEFORE they reach the internet")
    print()
    
    print("✅ PERSISTENT BLOCKING (24/7):")
    print("• Works even when YouTube Stopper app is closed")
    print("• Blocks domains across ALL browsers and applications")
    print("• No background processes or memory usage")
    print("• System-level blocking that can't be bypassed easily")
    print()
    
    print("🔄 WHEN DOMAINS ARE BLOCKED:")
    print("• Immediately when added (if blocking is active)")
    print("• When you activate blocking (if domains were added while inactive)")
    print("• Remains active until you manually remove domains or deactivate blocking")
    print()
    
    print("📁 FILE LOCATIONS:")
    print("• Hosts file: C:\\Windows\\System32\\drivers\\etc\\hosts")
    print("• Custom domains: %USERPROFILE%\\youtube_stopper_custom_blocklist.txt")
    print("• Backup: %USERPROFILE%\\youtube_stopper_hosts_backup.txt")
    print()
    
    print("⚠️ IMPORTANT NOTES:")
    print("• Requires administrator privileges to modify hosts file")
    print("• Changes persist through reboots")
    print("• You can manually edit hosts file to remove entries if needed")
    print("• App automatically backs up your original hosts file")
    print()
    
    print("🌐 WHAT HAPPENS WHEN YOU TRY TO ACCESS BLOCKED SITE:")
    print("1. You type 'facebook.com' in browser")
    print("2. Operating system checks hosts file first")
    print("3. Finds '127.0.0.1 facebook.com' entry")
    print("4. Redirects request to your own computer (localhost)")
    print("5. Browser shows 'This site can't be reached' or similar error")
    print()

if __name__ == "__main__":
    explain_blocking_mechanism()
    
    input("\nPress Enter to close...")
