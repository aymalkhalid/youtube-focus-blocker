#!/usr/bin/env python3
"""
YouTube Stopper - Build Script
Comprehensive script to build the executable with all optimizations
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path
import time

class BuildManager:
    """Manages the build process for YouTube Stopper"""
    
    def __init__(self):
        self.project_dir = Path(__file__).parent
        self.build_dir = self.project_dir / "build"
        self.dist_dir = self.project_dir / "dist"
        self.spec_file = self.project_dir / "youtube_stopper.spec"
        
    def clean_previous_builds(self):
        """Clean up previous build artifacts"""
        print("🧹 Cleaning previous builds...")
        
        dirs_to_clean = [self.build_dir, self.dist_dir]
        for dir_path in dirs_to_clean:
            if dir_path.exists():
                shutil.rmtree(dir_path)
                print(f"   Removed: {dir_path}")
        
        # Remove __pycache__ directories
        for pycache in self.project_dir.rglob("__pycache__"):
            shutil.rmtree(pycache)
            print(f"   Removed: {pycache}")
        
        print("✅ Cleanup completed!")
    
    def verify_dependencies(self):
        """Verify all required files exist"""
        print("🔍 Verifying build dependencies...")
        
        required_files = [
            "run.py",
            "gui.py", 
            "youtube_stopper.py",
            "requirements.txt",
            "icon.ico",
            "version_info.txt",
            "youtube_stopper.spec"
        ]
        
        missing_files = []
        for file_name in required_files:
            file_path = self.project_dir / file_name
            if not file_path.exists():
                missing_files.append(file_name)
            else:
                print(f"   ✅ {file_name}")
        
        if missing_files:
            print(f"❌ Missing files: {', '.join(missing_files)}")
            return False
        
        print("✅ All dependencies verified!")
        return True
    
    def build_executable(self):
        """Build the executable using PyInstaller"""
        print("🔨 Building executable with PyInstaller...")
        
        # PyInstaller command
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--clean",  # Clean cache and temporary files
            "--noconfirm",  # Replace output directory without confirmation
            str(self.spec_file)  # Use our custom spec file
        ]
        
        print(f"   Command: {' '.join(cmd)}")
        
        try:
            # Run PyInstaller
            result = subprocess.run(
                cmd,
                cwd=self.project_dir,
                capture_output=True,
                text=True,
                check=True
            )
            
            print("✅ PyInstaller completed successfully!")
            
            # Show any warnings
            if result.stderr:
                print("⚠️ Warnings:")
                print(result.stderr)
            
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ PyInstaller failed with error code {e.returncode}")
            print("Error output:")
            print(e.stderr)
            return False
    
    def optimize_executable(self):
        """Apply additional optimizations to the executable"""
        print("⚡ Optimizing executable...")
        
        exe_path = self.dist_dir / "YouTubeStopper.exe"
        
        if not exe_path.exists():
            print("❌ Executable not found for optimization")
            return False
        
        # Get file size
        file_size = exe_path.stat().st_size
        size_mb = file_size / (1024 * 1024)
        
        print(f"   Executable size: {size_mb:.1f} MB")
        
        # TODO: Add UPX compression if available
        # This would further reduce file size
        
        print("✅ Optimization completed!")
        return True
    
    def create_distribution_package(self):
        """Create a distribution package with additional files"""
        print("📦 Creating distribution package...")
        
        # Create distribution directory
        package_dir = self.dist_dir / "YouTubeStopper_Package"
        package_dir.mkdir(exist_ok=True)
        
        # Copy executable
        exe_src = self.dist_dir / "YouTubeStopper.exe"
        exe_dst = package_dir / "YouTubeStopper.exe"
        
        if exe_src.exists():
            shutil.copy2(exe_src, exe_dst)
            print(f"   ✅ Copied: {exe_dst.name}")
        
        # Copy documentation
        docs_to_copy = [
            "README.md",
            "LEARNING_SUMMARY.md",
        ]
        
        for doc in docs_to_copy:
            src = self.project_dir / doc
            if src.exists():
                dst = package_dir / doc
                shutil.copy2(src, dst)
                print(f"   ✅ Copied: {doc}")
        
        # Create a quick start guide
        quick_start = package_dir / "QUICK_START.txt"
        with open(quick_start, 'w', encoding='utf-8') as f:
            f.write("""🎯 YouTube Stopper - Quick Start Guide

IMPORTANT: This app requires ADMINISTRATOR PRIVILEGES to work properly!

HOW TO RUN:
1. Right-click on "YouTubeStopper.exe"
2. Select "Run as administrator"
3. Click "Yes" when Windows asks for permission

FEATURES:
- Toggle YouTube blocking on/off
- Track your productivity time
- Emergency unblock (5 minutes)
- System tray integration

TROUBLESHOOTING:
- If blocking doesn't work: Make sure you're running as administrator
- If you see "Access Denied": Run as administrator
- If DNS cache issues: Run "ipconfig /flushdns" in Command Prompt

SUPPORT:
Check the README.md file for detailed documentation.

Happy focusing! 🎯
""")
        print(f"   ✅ Created: QUICK_START.txt")
        
        print("✅ Distribution package created!")
        return package_dir
    
    def show_build_summary(self, package_dir):
        """Show build summary and next steps"""
        print("\n" + "="*60)
        print("🎉 BUILD COMPLETED SUCCESSFULLY!")
        print("="*60)
        
        exe_path = self.dist_dir / "YouTubeStopper.exe"
        if exe_path.exists():
            file_size = exe_path.stat().st_size / (1024 * 1024)
            print(f"📁 Executable: {exe_path}")
            print(f"📊 Size: {file_size:.1f} MB")
        
        if package_dir and package_dir.exists():
            print(f"📦 Package: {package_dir}")
            
            # List package contents
            print("\n📋 Package Contents:")
            for item in sorted(package_dir.iterdir()):
                if item.is_file():
                    size = item.stat().st_size
                    if item.suffix == '.exe':
                        size_str = f"{size / (1024*1024):.1f} MB"
                    else:
                        size_str = f"{size / 1024:.1f} KB"
                    print(f"   📄 {item.name} ({size_str})")
        
        print("\n🚀 NEXT STEPS:")
        print("1. Test the executable by running as administrator")
        print("2. Distribute the package folder to users")
        print("3. Include the QUICK_START.txt for user guidance")
        
        print("\n💡 TIPS:")
        print("- Always run as administrator for full functionality")
        print("- The exe includes all dependencies - no Python needed!")
        print("- Consider code signing for production distribution")
        
        print("\n✨ Your YouTube Stopper is ready to help people stay focused!")
    
    def build(self):
        """Main build process"""
        print("🎯 YouTube Stopper - Build Process Starting...")
        print("="*60)
        
        start_time = time.time()
        
        # Step 1: Clean previous builds
        self.clean_previous_builds()
        print()
        
        # Step 2: Verify dependencies
        if not self.verify_dependencies():
            print("❌ Build failed: Missing dependencies")
            return False
        print()
        
        # Step 3: Build executable
        if not self.build_executable():
            print("❌ Build failed: PyInstaller error")
            return False
        print()
        
        # Step 4: Optimize
        if not self.optimize_executable():
            print("⚠️ Optimization failed, but build continues...")
        print()
        
        # Step 5: Create package
        package_dir = self.create_distribution_package()
        print()
        
        # Step 6: Show summary
        build_time = time.time() - start_time
        print(f"⏱️ Build completed in {build_time:.1f} seconds")
        self.show_build_summary(package_dir)
        
        return True

def main():
    """Main entry point"""
    builder = BuildManager()
    
    try:
        success = builder.build()
        if success:
            print("\n🎉 Build process completed successfully!")
            return 0
        else:
            print("\n❌ Build process failed!")
            return 1
            
    except KeyboardInterrupt:
        print("\n⚠️ Build process interrupted by user")
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    input("\nPress Enter to exit...")
    sys.exit(exit_code)
