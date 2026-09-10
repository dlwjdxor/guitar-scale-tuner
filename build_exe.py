import os
import sys
import subprocess

def build():
    print("===================================================")
    print("  Building Guitar Scale Tuner Executable Package  ")
    print("===================================================")

    cmd = [
        "pyinstaller",
        "--noconfirm",
        "--onedir",
        "--windowed",
        "--name", "GuitarScaleTuner",
        "--icon", "favicon.ico",
        "--add-data", "index.html;.",
        "--add-data", "src;src",
        "--add-data", "favicon.ico;.",
        "--add-data", "favicon.png;.",
        "GuitarScaleTuner.py"
    ]

    print("Running command:", " ".join(cmd))
    subprocess.check_call(cmd)
    print("\n✅ Build complete! Executable generated at: dist/GuitarScaleTuner/GuitarScaleTuner.exe")

if __name__ == "__main__":
    build()
