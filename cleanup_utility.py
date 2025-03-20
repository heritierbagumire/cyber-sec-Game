# cleanup_utility.py
import platform
import winreg
import os
import sys
import tkinter as tk
from tkinter import messagebox

def remove_from_startup():
    """Remove the educational demonstration from startup."""
    if platform.system() != "Windows":
        return "Not implemented for this platform", False
    
    try:
        # Open the run registry key
        registry_key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, 
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run", 
            0, 
            winreg.KEY_ALL_ACCESS
        )
        
        # Delete the registry value
        try:
            winreg.DeleteValue(registry_key, "EducationalTetris")
            status = "Successfully removed startup entry", True
        except FileNotFoundError:
            status = "No startup entry found", False
        
        # Close the registry key
        winreg.CloseKey(registry_key)
        return status
    except Exception as e:
        return f"Error: {str(e)}", False

class CleanupUtility:
    def __init__(self, root):
        self.root = root
        self.root.title("Tetris Game Cleanup Utility")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        
        # Set up the UI
        self.setup_ui()
    
    def setup_ui(self):
        # Title
        tk.Label(
            self.root, 
            text="Tetris Game Cleanup Utility", 
            font=("Arial", 16, "bold")
        ).pack(pady=20)
        
        # Description
        tk.Label(
            self.root,
            text="This utility will remove all changes made by the\n"
                 "Tetris game for cybersecurity education.",
            justify="center"
        ).pack(pady=10)
        
        # Cleanup button
        tk.Button(
            self.root,
            text="Remove All Changes",
            command=self.cleanup,
            width=20,
            height=2,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10, "bold")
        ).pack(pady=20)
        
        # Exit button
        tk.Button(
            self.root,
            text="Exit",
            command=self.root.destroy,
            width=20,
            height=1
        ).pack(pady=10)
        
        # Status label
        self.status_label = tk.Label(
            self.root,
            text="Ready to clean up",
            font=("Arial", 9, "italic")
        )
        self.status_label.pack(pady=10)
    
    def cleanup(self):
        """Perform the cleanup operations."""
        results = []
        
        # Remove from startup
        message, success = remove_from_startup()
        results.append(("Startup entry", message, success))
        
        # Display results
        success_count = sum(1 for _, _, success in results if success)
        
        if success_count > 0:
            self.status_label.config(
                text=f"Cleanup completed: {success_count} item(s) removed",
                fg="green"
            )
            messagebox.showinfo(
                "Cleanup Completed",
                f"Successfully removed {success_count} item(s).\n\n"
                "Your system has been restored to its original state."
            )
        else:
            self.status_label.config(
                text="No changes were found to remove",
                fg="blue"
            )
            messagebox.showinfo(
                "No Changes Found",
                "No changes were found that needed to be removed."
            )

if __name__ == "__main__":
    root = tk.Tk()
    app = CleanupUtility(root)
    root.mainloop()