"""
Test script to verify encryption functionality.
"""

from crypto_utils import SecureMessenger


def test_encryption():
    """Test basic encryption and decryption."""
    print("Testing Better IP Messenger Encryption...")
    print("-" * 50)
    
    # Create two users
    print("\n1. Creating two users (Alice and Bob)...")
    alice = SecureMessenger()
    bob = SecureMessenger()
    print("   ✓ Alice and Bob created with RSA key pairs")
    
    # Exchange public keys
    print("\n2. Exchanging public keys...")
    alice_pub = alice.get_public_key_pem()
    bob_pub = bob.get_public_key_pem()
    
    alice.add_peer_public_key("bob", bob_pub)
    bob.add_peer_public_key("alice", alice_pub)
    print("   ✓ Public keys exchanged")
    
    # Test message encryption
    print("\n3. Testing message encryption...")
    original_message = "Hello Bob! This is a secret message. 🔐"
    print(f"   Original message: '{original_message}'")
    
    encrypted_data = alice.encrypt_message("bob", original_message)
    print(f"   ✓ Message encrypted")
    print(f"   Encrypted message length: {len(encrypted_data['encrypted_message'])} chars")
    
    # Test message decryption
    print("\n4. Testing message decryption...")
    decrypted_message = bob.decrypt_message(encrypted_data)
    print(f"   Decrypted message: '{decrypted_message}'")
    
    # Verify
    if original_message == decrypted_message:
        print("   ✓ Encryption/Decryption successful!")
    else:
        print("   ✗ Encryption/Decryption failed!")
        return False
    
    # Test signature
    print("\n5. Testing message signatures...")
    signature = alice.sign_message(original_message)
    print(f"   ✓ Message signed")
    print(f"   Signature length: {len(signature)} chars")
    
    # Verify signature
    print("\n6. Verifying signature...")
    is_valid = bob.verify_signature("alice", original_message, signature)
    if is_valid:
        print("   ✓ Signature verified successfully!")
    else:
        print("   ✗ Signature verification failed!")
        return False
    
    # Test tampered message
    print("\n7. Testing tampered message detection...")
    tampered_message = "Hello Bob! This is a TAMPERED message."
    is_valid_tampered = bob.verify_signature("alice", tampered_message, signature)
    if not is_valid_tampered:
        print("   ✓ Tampered message detected correctly!")
    else:
        print("   ✗ Failed to detect tampered message!")
        return False
    
    print("\n" + "=" * 50)
    print("✓ All encryption tests passed!")
    print("=" * 50)
    return True


if __name__ == "__main__":
    success = test_encryption()
    exit(0 if success else 1)
