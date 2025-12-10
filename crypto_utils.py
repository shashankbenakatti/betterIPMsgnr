"""
Encryption utilities for secure IP Messenger.
Provides end-to-end encryption using RSA for key exchange and AES for message encryption.
"""

import os
import json
import base64
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend


class SecureMessenger:
    """Handles encryption and decryption of messages."""
    
    def __init__(self):
        """Initialize with a new RSA key pair."""
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        self.public_key = self.private_key.public_key()
        self.peer_public_keys = {}  # Store public keys of peers
    
    def get_public_key_pem(self):
        """Export public key in PEM format for sharing."""
        return self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode('utf-8')
    
    def add_peer_public_key(self, peer_id, public_key_pem):
        """Add a peer's public key."""
        public_key = serialization.load_pem_public_key(
            public_key_pem.encode('utf-8'),
            backend=default_backend()
        )
        self.peer_public_keys[peer_id] = public_key
    
    def encrypt_message(self, peer_id, message):
        """
        Encrypt a message for a specific peer using AES with RSA-encrypted key.
        Returns a dictionary with encrypted message and encrypted AES key.
        """
        if peer_id not in self.peer_public_keys:
            raise ValueError(f"No public key found for peer {peer_id}")
        
        # Generate random AES key for this message
        aes_key = os.urandom(32)  # 256-bit key
        iv = os.urandom(16)  # 128-bit IV
        
        # Encrypt message with AES
        cipher = Cipher(
            algorithms.AES(aes_key),
            modes.CBC(iv),
            backend=default_backend()
        )
        encryptor = cipher.encryptor()
        
        # Pad message to multiple of 16 bytes
        message_bytes = message.encode('utf-8')
        padding_length = 16 - (len(message_bytes) % 16)
        padded_message = message_bytes + bytes([padding_length] * padding_length)
        
        encrypted_message = encryptor.update(padded_message) + encryptor.finalize()
        
        # Encrypt AES key with peer's RSA public key
        peer_public_key = self.peer_public_keys[peer_id]
        encrypted_key = peer_public_key.encrypt(
            aes_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        
        return {
            'encrypted_message': base64.b64encode(encrypted_message).decode('utf-8'),
            'encrypted_key': base64.b64encode(encrypted_key).decode('utf-8'),
            'iv': base64.b64encode(iv).decode('utf-8')
        }
    
    def decrypt_message(self, encrypted_data):
        """
        Decrypt a message using RSA private key to decrypt AES key.
        encrypted_data should be a dictionary with encrypted_message, encrypted_key, and iv.
        """
        # Decrypt AES key with our private key
        encrypted_key = base64.b64decode(encrypted_data['encrypted_key'])
        aes_key = self.private_key.decrypt(
            encrypted_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        
        # Decrypt message with AES
        iv = base64.b64decode(encrypted_data['iv'])
        encrypted_message = base64.b64decode(encrypted_data['encrypted_message'])
        
        cipher = Cipher(
            algorithms.AES(aes_key),
            modes.CBC(iv),
            backend=default_backend()
        )
        decryptor = cipher.decryptor()
        padded_message = decryptor.update(encrypted_message) + decryptor.finalize()
        
        # Remove padding
        padding_length = padded_message[-1]
        message = padded_message[:-padding_length]
        
        return message.decode('utf-8')
    
    def sign_message(self, message):
        """Create a digital signature for message authentication."""
        message_bytes = message.encode('utf-8')
        signature = self.private_key.sign(
            message_bytes,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return base64.b64encode(signature).decode('utf-8')
    
    def verify_signature(self, peer_id, message, signature):
        """Verify a message signature from a peer."""
        if peer_id not in self.peer_public_keys:
            return False
        
        try:
            peer_public_key = self.peer_public_keys[peer_id]
            signature_bytes = base64.b64decode(signature)
            message_bytes = message.encode('utf-8')
            
            peer_public_key.verify(
                signature_bytes,
                message_bytes,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except Exception:
            return False
