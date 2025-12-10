"""
Command-line interface for Better IP Messenger.
Useful for testing and headless environments.
"""

import sys
import threading
import time
from crypto_utils import SecureMessenger
from network import NetworkManager


class MessengerCLI:
    """Command-line interface for the messenger."""
    
    def __init__(self, username):
        """Initialize the CLI."""
        self.username = username
        self.crypto = SecureMessenger()
        self.network = NetworkManager(
            username,
            self.crypto,
            message_callback=self.on_message_received
        )
        self.running = False
    
    def on_message_received(self, message_data):
        """Handle received messages."""
        print(f"\n[{message_data['sender']}]: {message_data['message']}")
        print("> ", end="", flush=True)
    
    def start(self):
        """Start the messenger."""
        print(f"\n=== Better IP Messenger - CLI ===")
        print(f"Logged in as: {self.username}")
        print(f"Local IP: {self.network.local_ip}")
        print(f"\nDiscovering peers on LAN...")
        print(f"Commands:")
        print(f"  list - List active peers")
        print(f"  send <number> <message> - Send message to peer")
        print(f"  quit - Exit\n")
        
        self.network.start()
        self.running = True
        
        # Give network time to discover peers
        time.sleep(3)
        
        # Command loop
        while self.running:
            try:
                command = input("> ").strip()
                
                if not command:
                    continue
                
                if command.lower() == "quit":
                    self.stop()
                    break
                
                elif command.lower() == "list":
                    self.list_peers()
                
                elif command.lower().startswith("send "):
                    parts = command.split(None, 2)
                    if len(parts) < 3:
                        print("Usage: send <number> <message>")
                        continue
                    
                    try:
                        peer_num = int(parts[1])
                        message = parts[2]
                        self.send_message(peer_num, message)
                    except ValueError:
                        print("Invalid peer number")
                
                else:
                    print(f"Unknown command: {command}")
            
            except KeyboardInterrupt:
                print("\nShutting down...")
                self.stop()
                break
            except Exception as e:
                print(f"Error: {e}")
    
    def list_peers(self):
        """List active peers."""
        peers = self.network.get_peers()
        
        if not peers:
            print("No peers found. Make sure other instances are running on the same LAN.")
            return
        
        print("\nActive Peers:")
        for i, (peer_id, peer_info) in enumerate(peers):
            print(f"  {i}. {peer_info['username']} ({peer_info['ip']})")
        print()
    
    def send_message(self, peer_num, message):
        """Send a message to a peer."""
        peers = self.network.get_peers()
        
        if peer_num < 0 or peer_num >= len(peers):
            print("Invalid peer number")
            return
        
        peer_id, peer_info = peers[peer_num]
        
        try:
            if self.network.send_message(peer_id, message):
                print(f"Message sent to {peer_info['username']}")
            else:
                print("Failed to send message")
        except Exception as e:
            print(f"Error sending message: {e}")
    
    def stop(self):
        """Stop the messenger."""
        self.running = False
        self.network.stop()


def main():
    """Main entry point."""
    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        username = input("Enter your username: ").strip()
        if not username:
            print("Username is required")
            sys.exit(1)
    
    cli = MessengerCLI(username)
    cli.start()


if __name__ == "__main__":
    main()
