import os
import subprocess
import platform
import time

PERSISTENCE_PATH = os.path.join(os.getenv('APPDATA'), 'WindowsUpdate') if platform.system() == 'Windows' else os.path.expanduser('~/.config/autostart')
LOCK_FILE = os.path.join(PERSISTENCE_PATH, 'tetris.lock')

def remove_persistence():
    try:
        if platform.system() == 'Windows':
            key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
            subprocess.run(f'reg delete "HKCU\{key_path}" /v WindowsUpdate /f', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            subprocess.run(f'reg delete "HKCU\{key_path}" /v TetrisGame /f', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            vbs_path = os.path.join(PERSISTENCE_PATH, 'update.vbs')
            if os.path.exists(vbs_path):
                os.remove(vbs_path)
            if os.path.exists(LOCK_FILE):
                os.remove(LOCK_FILE)
            if os.path.exists(PERSISTENCE_PATH) and not os.listdir(PERSISTENCE_PATH):
                os.rmdir(PERSISTENCE_PATH)
        else:
            desktop_path = os.path.join(PERSISTENCE_PATH, 'system-update.desktop')
            if os.path.exists(desktop_path):
                os.remove(desktop_path)
        print("All startup entries and persistence files removed successfully!")
    except Exception as e:
        print(f"Cleanup failed: {e}")

if __name__ == "__main__":
    remove_persistence()
    print("Exiting in 5 seconds...")
    time.sleep(5)  # Wait 5 seconds before closing, avoiding input()