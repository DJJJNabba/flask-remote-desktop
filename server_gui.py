import tkinter as tk
from tkinter import ttk, messagebox, PhotoImage
import threading
import json
import os
import subprocess
import sys
import psutil
from pathlib import Path
import socket

class ServerGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Screen Stream Server Control")
        self.root.geometry("500x600")

        # Set the window icon
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'favicon.png')
        if os.path.exists(icon_path):
            icon = PhotoImage(file=icon_path)
            self.root.iconphoto(True, icon)

        # Default config
        self.config = {
            "port": 5000,
            "password": "your_password",
            "secret_key": "your_secret_key"
        }
        
        self.server_process = None
        self.create_widgets()
        self.load_config()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def create_widgets(self):
        # Main container
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title = ttk.Label(main_frame, text="Screen Stream Server Control", font=('Helvetica', 16, 'bold'))
        title.pack(pady=(0, 20))
        
        # Server Status
        self.status_label = ttk.Label(main_frame, text="Server Status: Stopped", font=('Helvetica', 12))
        self.status_label.pack(pady=(0, 20))
        
        # Settings Frame
        settings_frame = ttk.LabelFrame(main_frame, text="Server Settings", padding="10")
        settings_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Port
        ttk.Label(settings_frame, text="Port:").pack(anchor='w')
        self.port_entry = ttk.Entry(settings_frame)
        self.port_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Password
        ttk.Label(settings_frame, text="Password:").pack(anchor='w')
        self.password_entry = ttk.Entry(settings_frame)
        self.password_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Save Config Button
        ttk.Button(settings_frame, text="Save Configuration", command=self.save_config).pack(pady=10)
        
        # Server Control Buttons
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=20)
        
        self.start_button = ttk.Button(control_frame, text="Start Server", command=self.start_server)
        self.start_button.pack(side=tk.LEFT, expand=True, padx=5)
        
        self.stop_button = ttk.Button(control_frame, text="Stop Server", command=self.stop_server, state='disabled')
        self.stop_button.pack(side=tk.RIGHT, expand=True, padx=5)
        
        # Connection Info
        self.info_text = tk.Text(main_frame, height=12, wrap=tk.WORD)
        self.info_text.pack(fill=tk.X, pady=10)
        self.info_text.insert('1.0', "Server not running")
        self.info_text.config(state='disabled')
        
    def load_config(self):
        config_path = Path("server_config.json")
        if config_path.exists():
            with open(config_path, 'r') as f:
                self.config = json.load(f)
        
        # Set values in entries
        self.port_entry.insert(0, str(self.config["port"]))
        self.password_entry.insert(0, self.config["password"])
        
    def save_config(self):
        try:
            self.config["port"] = int(self.port_entry.get())
            self.config["password"] = self.password_entry.get()
            
            # Validate values
            if not (1024 <= self.config["port"] <= 65535):
                raise ValueError("Port must be between 1024 and 65535")
            
            # Save to JSON
            with open("server_config.json", 'w') as f:
                json.dump(self.config, f, indent=4)
            
            # Update config.py
            self.update_config_py()
            
            messagebox.showinfo("Success", "Configuration saved successfully!")
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
    
    def update_config_py(self):
        config_content = f"""import os

class Config:
    SECRET_KEY = '{self.config["secret_key"]}'
    SESSION_TYPE = 'filesystem'
    PASSWORD = "{self.config["password"]}"
"""
        with open('config.py', 'w') as f:
            f.write(config_content)
    
    def start_server(self):
        if self.server_process is None:
            try:
                # Determine the correct path to AppServer.exe
                if getattr(sys, 'frozen', False):
                    # If running as a PyInstaller bundle
                    application_path = os.path.dirname(sys.executable)
                else:
                    # If running as a normal Python script
                    application_path = os.path.dirname(os.path.abspath(__file__))

                app_executable = os.path.join(application_path, 'AppServer.exe')
                
                if not os.path.exists(app_executable):
                    messagebox.showerror("Error", f"AppServer.exe not found at {app_executable}")
                    return

                # Start the AppServer executable
                self.server_process = subprocess.Popen(
                    [app_executable],
                    cwd=application_path,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    shell=False,
                    text=True,
                    bufsize=1,
                    universal_newlines=True
                )
                
                # Start output monitoring threads
                threading.Thread(target=self.monitor_output, args=(self.server_process.stdout, "stdout"), daemon=True).start()
                threading.Thread(target=self.monitor_output, args=(self.server_process.stderr, "stderr"), daemon=True).start()
                
                self.status_label.config(text="Server Status: Running")
                self.start_button.config(state='disabled')
                self.stop_button.config(state='normal')
                
                # Update info text
                self.info_text.config(state='normal')
                self.info_text.delete('1.0', tk.END)
                # Get the local IP address
                hostname = socket.gethostname()
                local_ip = socket.gethostbyname(hostname)
                self.info_text.insert('1.0', f"Server is running!\n\n"
                                        f"Connect using:\n"
                                        f"http://localhost:{self.config['port']}\n"
                                        f"or http://{local_ip}:{self.config['port']}")
                self.info_text.config(state='disabled')
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to start server: {str(e)}")
    
    def monitor_output(self, pipe, pipe_name):
        """Monitor the subprocess output pipes and update the GUI."""
        try:
            while True:
                line = pipe.readline()
                if not line:
                    break
                self.update_server_output(f"{line.strip()}\n")
        except Exception as e:
            print(f"Error monitoring {pipe_name}: {e}")

    def update_server_output(self, text):
        """Update the info text with server output."""
        self.info_text.config(state='normal')
        self.info_text.insert(tk.END, text)
        self.info_text.see(tk.END)  # Auto-scroll to the bottom
        self.info_text.config(state='disabled')
    
    def stop_server(self):
        if self.server_process:
            try:
                parent = psutil.Process(self.server_process.pid)
                for child in parent.children(recursive=True):
                    child.kill()
                parent.kill()
                
                self.server_process = None
                self.status_label.config(text="Server Status: Stopped")
                self.start_button.config(state='normal')
                self.stop_button.config(state='disabled')
                
                self.info_text.config(state='normal')
                self.info_text.delete('1.0', tk.END)
                self.info_text.insert('1.0', "Server not running")
                self.info_text.config(state='disabled')
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to stop server: {str(e)}")
    
    def on_closing(self):
        """Handle the window close event."""
        if self.server_process:
            self.stop_server()
        self.root.destroy()
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ServerGUI()
    app.run()