"""
Build script to create a Windows .exe using PyInstaller
"""
import os
import sys
import subprocess

def build_exe():
    """Build the executable using PyInstaller"""
    print("=" * 60)
    print("Building Deskling .exe")
    print("=" * 60)
    
    # PyInstaller command with options
    # Use python -m PyInstaller to avoid PATH issues
    command = [
        sys.executable,                 # Python executable
        "-m",                           # Run as module
        "PyInstaller",
        "--onefile",                    # Create a single .exe file
        "--windowed",                   # No console window
        "--name=Deskling",              # Name of the .exe
        "--icon=NONE",                  # No icon (add --icon=path/to/icon.ico if you have one)
        "--clean",                      # Clean cache before building
        
        # Hidden imports for Supabase and dependencies
        "--hidden-import=supabase",
        "--hidden-import=gotrue",
        "--hidden-import=postgrest",
        "--hidden-import=realtime",
        "--hidden-import=storage3",
        "--hidden-import=supafunc",
        "--hidden-import=websockets",
        "--hidden-import=websockets.legacy",
        "--hidden-import=websockets.legacy.client",
        "--hidden-import=httpx",
        "--hidden-import=PyQt5",
        "--hidden-import=PyQt5.QtCore",
        "--hidden-import=PyQt5.QtGui",
        "--hidden-import=PyQt5.QtWidgets",
        "--hidden-import=PyQt5.QtNetwork",
        "--hidden-import=dotenv",
        
        # Collect all submodules
        "--collect-all=supabase",
        "--collect-all=websockets",
        
        "main.py"
    ]
    
    print("\nRunning PyInstaller...")
    print(f"Command: {' '.join(command)}\n")
    
    try:
        # Run PyInstaller as a Python module
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        
        print("\n" + "=" * 60)
        print("✓ Build successful!")
        print("=" * 60)
        print(f"\nYour executable is located at:")
        print(f"  {os.path.abspath('dist/Deskling.exe')}")
        print("\n" + "⚠" + " IMPORTANT FOR DISTRIBUTION:")
        print("=" * 60)
        print("Your Supabase credentials are hardcoded in the .exe!")
        print("To share this app:")
        print("  1. Just send Deskling.exe - that's it!")
        print("  2. Users run it and it works instantly")
        print("  3. Everyone uses YOUR Supabase backend")
        print("\n⚠️ Make sure Row Level Security is enabled!")
        print("See SUPABASE_SECURITY.md for instructions.")
        print("\n✓ You can now run Deskling.exe without Python installed!")
        
    except subprocess.CalledProcessError as e:
        print("\n" + "=" * 60)
        print("✗ Build failed!")
        print("=" * 60)
        print(f"\nError output:")
        print(e.stderr if e.stderr else str(e))
        print("\nMake sure PyInstaller is installed:")
        print("  pip install pyinstaller")
        sys.exit(1)
    except FileNotFoundError as e:
        print("\n" + "=" * 60)
        print("✗ PyInstaller not found!")
        print("=" * 60)
        print(f"\nError: {e}")
        print("\nPlease install PyInstaller:")
        print("  pip install pyinstaller")
        sys.exit(1)
    except Exception as e:
        print("\n" + "=" * 60)
        print("✗ Unexpected error!")
        print("=" * 60)
        print(f"\nError: {e}")
        sys.exit(1)

if __name__ == "__main__":
    build_exe()

