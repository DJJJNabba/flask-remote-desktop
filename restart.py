import os
import sys
import time
import psutil  # Ensure psutil is installed with `pip install psutil`
import subprocess

def kill_existing_app():
    # Kill any running instances of app.py
    for process in psutil.process_iter(['pid', 'cmdline']):
        cmdline = process.info['cmdline']
        if cmdline and 'app.py' in cmdline:
            try:
                process.kill()
                print(f"Killed process with PID: {process.info['pid']}")
            except Exception as e:
                print(f"Could not kill process {process.info['pid']}: {e}")

def restart_app():
    # Kill the existing app
    kill_existing_app()
    
    # Wait briefly to ensure the process is completely terminated
    time.sleep(1)

    # Start a new instance of app.py
    python = sys.executable
    script = os.path.abspath("app.py")
    
    try:
        subprocess.Popen([python, script])
        print("Restarted app.py")
    except Exception as e:
        print(f"Failed to restart app.py: {e}")

if __name__ == "__main__":
    restart_app()
