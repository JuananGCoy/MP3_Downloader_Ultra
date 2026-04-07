import os
import subprocess
import sys
import shutil

def get_custom_tkinter_path():
    try:
        import customtkinter
        return os.path.dirname(customtkinter.__file__)
    except ImportError:
        print("Error: customtkinter not found in Python path. Please 'pip install customtkinter'.")
        sys.exit(1)

def build():
    # 1. Clean previous build folders
    for folder in ['build', 'dist']:
        if os.path.exists(folder):
            try:
                shutil.rmtree(folder)
                print(f"Cleaned {folder}")
            except Exception as e:
                print(f"Warning: Could not clean {folder} ({e}). Ensure no executables are running.")

    # 2. Get CustomTkinter path
    ctk_path = get_custom_tkinter_path()
    print(f"Found CustomTkinter at: {ctk_path}")

    # 3. Check for FFmpeg binaries
    ff_binaries = ['ffmpeg.exe', 'ffprobe.exe']
    for b in ff_binaries:
        if not os.path.exists(b):
            print(f"Error: {b} not found in current directory. Please place it here before building.")
            sys.exit(1)

    # 4. Create PyInstaller command
    # --onefile: Bundles everything into a single .exe
    # --windowed: No console window
    # --add-data: Bundle external files
    # Syntax for --add-data: "source;destination" (Windows uses semicolon)
    
    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconfirm",
        "--onefile",
        "--windowed",
        f"--add-data={ctk_path};customtkinter/",
        "--add-data=ffmpeg.exe;.",
        "--add-data=ffprobe.exe;.",
        "--name=MP3_Downloader_Ultra",
        "main.py"
    ]

    print("Running command:", " ".join(cmd))
    
    try:
        subprocess.check_call(cmd)
        print("\nSUCCESS! Your portable .exe is in the 'dist' folder.")
    except Exception as e:
        print(f"\nBUILD FAILED: {e}")

if __name__ == "__main__":
    build()
