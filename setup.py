#!/usr/bin/env python3
"""
Quick Setup Script
Sets up the framework and runs initial tests.
"""

import subprocess
import sys
import os
from pathlib import Path


def run_command(command, description):
    """Run shell command and handle errors."""
    print(f"\n{'='*60}")
    print(f"🔧 {description}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            text=True,
            capture_output=True
        )
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        print(e.stderr)
        return False


def main():
    """Main setup function."""
    print("\n")
    print("╔═══════════════════════════════════════════════════╗")
    print("║                                                   ║")
    print("║   EcoCash API Automation Framework Setup         ║")
    print("║                                                   ║")
    print("╚═══════════════════════════════════════════════════╝")
    print("\n")
    
    # Check Python version
    print(f"🐍 Python version: {sys.version}")
    
    if sys.version_info < (3, 10):
        print("❌ Python 3.10 or higher is required!")
        sys.exit(1)
    
    # Create virtual environment
    if not os.path.exists('venv'):
        if not run_command(
            'python3 -m venv venv',
            'Creating virtual environment'
        ):
            sys.exit(1)
    else:
        print("\n✅ Virtual environment already exists")
    
    # Determine activation command based on OS
    if sys.platform == 'win32':
        activate_cmd = 'venv\\Scripts\\activate &&'
    else:
        activate_cmd = 'source venv/bin/activate &&'
    
    # Install dependencies
    if not run_command(
        f'{activate_cmd} pip install --upgrade pip',
        'Upgrading pip'
    ):
        sys.exit(1)
    
    if not run_command(
        f'{activate_cmd} pip install -r requirements.txt',
        'Installing dependencies'
    ):
        sys.exit(1)
    
    # Create necessary directories
    directories = ['logs', 'reports/allure-results', 'reports/junit']
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    print("\n✅ Created necessary directories")
    
    # Make scripts executable (Unix-like systems)
    if sys.platform != 'win32':
        os.chmod('run_tests.sh', 0o755)
        print("\n✅ Made run_tests.sh executable")
    
    print("\n")
    print("╔═══════════════════════════════════════════════════╗")
    print("║                                                   ║")
    print("║   ✅ Setup Complete!                              ║")
    print("║                                                   ║")
    print("╚═══════════════════════════════════════════════════╝")
    print("\n")
    
    print("📚 Quick Start:")
    print("  1. Activate virtual environment:")
    if sys.platform == 'win32':
        print("     venv\\Scripts\\activate")
    else:
        print("     source venv/bin/activate")
    print("\n  2. Run tests:")
    print("     behave -D env=qa --tags=smoke")
    print("\n  3. Or use the test runner:")
    if sys.platform == 'win32':
        print("     python run_tests.py")
    else:
        print("     ./run_tests.sh -e qa -t smoke")
    print("\n  4. View reports:")
    print("     allure serve reports/allure-results")
    print("\n📖 For more information, see README.md")
    print("\n")


if __name__ == '__main__':
    main()
