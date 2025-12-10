"""
Network layer for secure IP Messenger.
Handles peer discovery, message sending/receiving, and network communication.
"""

import socket
import threading
import json
import time
from datetime import datetime


class NetworkManager:
    """Manages network communication for the messenger."""
    
    def __init__(self, username, crypto_manager, message_callback=None):
        """
        Initialize network manager.
        
        Args:
            username: Display name for this user
            crypto_manager: Instance of SecureMessenger for encryption
            message_callback: Function to call when message is received
        """
        self.username = username
        self.crypto = crypto_manager
        self.message_callback = message_callback
        
        # Network configuration
        self.broadcast_port = 5000
        self.message_port = 5001
        self.buffer_size = 65536
        
        # Peer management
        self.peers = {}  # {peer_id: {'username': str, 'ip': str, 'last_seen': timestamp}}
        self.running = False
        
        # Get local IP
        self.local_ip = self._get_local_ip()
        self.peer_id = f"{self.username}@{self.local_ip}"
        
    def _get_local_ip(self):
        """Get the local IP address."""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except Exception:
            return "127.0.0.1"
    
    def start(self):
        """Start network services."""
        self.running = True
        
        # Start discovery broadcast thread
        self.broadcast_thread = threading.Thread(target=self._broadcast_presence, daemon=True)
        self.broadcast_thread.start()
        
        # Start discovery listener thread
        self.discovery_thread = threading.Thread(target=self._listen_for_peers, daemon=True)
        self.discovery_thread.start()
        
        # Start message listener thread
        self.message_thread = threading.Thread(target=self._listen_for_messages, daemon=True)
        self.message_thread.start()
        
        # Start peer cleanup thread
        self.cleanup_thread = threading.Thread(target=self._cleanup_peers, daemon=True)
        self.cleanup_thread.start()
    
    def stop(self):
        """Stop network services."""
        self.running = False
    
    def _broadcast_presence(self):
        """Broadcast presence to discover peers on LAN."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        
        broadcast_data = {
            'type': 'presence',
            'peer_id': self.peer_id,
            'username': self.username,
            'ip': self.local_ip,
            'public_key': self.crypto.get_public_key_pem()
        }
        
        while self.running:
            try:
                message = json.dumps(broadcast_data).encode('utf-8')
                sock.sendto(message, ('<broadcast>', self.broadcast_port))
                time.sleep(5)  # Broadcast every 5 seconds
            except Exception as e:
                print(f"Broadcast error: {e}")
                time.sleep(5)
        
        sock.close()
    
    def _listen_for_peers(self):
        """Listen for peer discovery broadcasts."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Bind to all interfaces to receive broadcasts on LAN
        # This is intentional for peer discovery functionality
        sock.bind(('', self.broadcast_port))
        sock.settimeout(1.0)
        
        while self.running:
            try:
                data, addr = sock.recvfrom(self.buffer_size)
                message = json.loads(data.decode('utf-8'))
                
                if message['type'] == 'presence' and message['peer_id'] != self.peer_id:
                    peer_id = message['peer_id']
                    
                    # Add or update peer
                    if peer_id not in self.peers:
                        print(f"New peer discovered: {message['username']} ({message['ip']})")
                    
                    self.peers[peer_id] = {
                        'username': message['username'],
                        'ip': message['ip'],
                        'last_seen': time.time()
                    }
                    
                    # Add peer's public key
                    self.crypto.add_peer_public_key(peer_id, message['public_key'])
                    
            except socket.timeout:
                continue
            except Exception as e:
                if self.running:
                    print(f"Discovery listener error: {e}")
        
        sock.close()
    
    def _listen_for_messages(self):
        """Listen for incoming messages."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Bind to all interfaces to receive messages on LAN
        # This is intentional for the messenger functionality
        sock.bind(('', self.message_port))
        sock.settimeout(1.0)
        
        while self.running:
            try:
                data, addr = sock.recvfrom(self.buffer_size)
                message_data = json.loads(data.decode('utf-8'))
                
                if message_data['type'] == 'message':
                    sender_id = message_data['sender_id']
                    
                    # Decrypt message
                    try:
                        encrypted_data = message_data['encrypted_data']
                        decrypted_message = self.crypto.decrypt_message(encrypted_data)
                        
                        # Verify signature if present
                        if 'signature' in message_data:
                            if not self.crypto.verify_signature(
                                sender_id,
                                decrypted_message,
                                message_data['signature']
                            ):
                                print(f"Warning: Signature verification failed for message from {sender_id}")
                                continue
                        
                        # Call message callback
                        if self.message_callback:
                            self.message_callback({
                                'sender_id': sender_id,
                                'sender': self.peers.get(sender_id, {}).get('username', 'Unknown'),
                                'message': decrypted_message,
                                'timestamp': message_data.get('timestamp', time.time())
                            })
                    
                    except Exception as e:
                        print(f"Error decrypting message from {sender_id}: {e}")
                
            except socket.timeout:
                continue
            except Exception as e:
                if self.running:
                    print(f"Message listener error: {e}")
        
        sock.close()
    
    def send_message(self, peer_id, message):
        """Send an encrypted message to a peer."""
        if peer_id not in self.peers:
            raise ValueError(f"Peer {peer_id} not found")
        
        peer_info = self.peers[peer_id]
        
        try:
            # Encrypt message
            encrypted_data = self.crypto.encrypt_message(peer_id, message)
            
            # Create signature
            signature = self.crypto.sign_message(message)
            
            # Prepare message packet
            message_packet = {
                'type': 'message',
                'sender_id': self.peer_id,
                'encrypted_data': encrypted_data,
                'signature': signature,
                'timestamp': time.time()
            }
            
            # Send message
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            message_bytes = json.dumps(message_packet).encode('utf-8')
            sock.sendto(message_bytes, (peer_info['ip'], self.message_port))
            sock.close()
            
            return True
        
        except Exception as e:
            print(f"Error sending message to {peer_id}: {e}")
            return False
    
    def _cleanup_peers(self):
        """Remove peers that haven't been seen recently."""
        while self.running:
            try:
                current_time = time.time()
                timeout = 15  # Remove peers not seen for 15 seconds
                
                peers_to_remove = []
                for peer_id, peer_info in self.peers.items():
                    if current_time - peer_info['last_seen'] > timeout:
                        peers_to_remove.append(peer_id)
                
                for peer_id in peers_to_remove:
                    print(f"Peer disconnected: {self.peers[peer_id]['username']}")
                    del self.peers[peer_id]
                
                time.sleep(5)
            except Exception as e:
                print(f"Cleanup error: {e}")
                time.sleep(5)
    
    def get_peers(self):
        """Get list of active peers."""
        return list(self.peers.items())
