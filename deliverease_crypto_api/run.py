#!/usr/bin/env python
"""
Quick start script for running the Deliverease Crypto API.

This script sets up and runs the API with hot reload for development.
"""

import os
import sys
import subprocess
from pathlib import Path


def main():
    """Main entry point for the startup script."""
    # Get project root
    project_root = Path(__file__).parent
    
    # Check if virtual environment exists
    venv_path = project_root / "venv"
    
    if not venv_path.exists():
        print("Virtual environment not found. Creating...")
        subprocess.run([sys.executable, "-m", "venv", str(venv_path)], check=True)
        print("Virtual environment created at:", venv_path)
    
    # Activate venv and install requirements
    if sys.platform == "win32":
        activate_script = venv_path / "Scripts" / "activate.bat"
        python_exe = venv_path / "Scripts" / "python.exe"
        pip_exe = venv_path / "Scripts" / "pip.exe"
    else:
        activate_script = venv_path / "bin" / "activate"
        python_exe = venv_path / "bin" / "python"
        pip_exe = venv_path / "bin" / "pip"
    
    # Install requirements
    print("Installing requirements...")
    subprocess.run([str(pip_exe), "install", "-r", str(project_root / "requirements.txt")], check=True)
    
    # Check and create .env file
    env_file = project_root / ".env"
    if not env_file.exists():
        print("Creating .env file from template...")
        env_example = project_root / ".env.example"
        if env_example.exists():
            with open(env_example) as f:
                env_content = f.read()
            with open(env_file, "w") as f:
                f.write(env_content)
            print(".env file created. Please update with your settings.")
    
    # Run the application
    print("\nStarting Deliverease Crypto API...")
    print("API will be available at http://localhost:8000")
    print("API Docs at http://localhost:8000/docs\n")
    
    os.chdir(str(project_root))
    
    if sys.platform == "win32":
        os.system(f"{python_exe} -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
    else:
        subprocess.run([
            str(python_exe), "-m", "uvicorn",
            "app.main:app",
            "--reload",
            "--host", "0.0.0.0",
            "--port", "8000"
        ])


if __name__ == "__main__":
    main()
