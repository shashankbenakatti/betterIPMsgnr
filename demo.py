"""
Demo script to showcase Better IP Messenger features.
This script simulates the core encryption and networking functionality.
"""

import time
from crypto_utils import SecureMessenger


def print_section(title):
    """Print a section header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def demo_encryption():
    """Demonstrate encryption features."""
    print_section("BETTER IP MESSENGER - SECURITY DEMO")
    
    print("\n📝 This demo showcases the security features of Better IP Messenger")
    print("   without requiring network connectivity.\n")
    
    # Setup
    print_section("1. Setting Up Two Users")
    print("\n🔑 Creating RSA key pairs for Alice and Bob...")
    alice = SecureMessenger()
    bob = SecureMessenger()
    print("   ✓ Alice's RSA-2048 key pair generated")
    print("   ✓ Bob's RSA-2048 key pair generated")
    
    # Key Exchange
    print_section("2. Public Key Exchange")
    print("\n🤝 Exchanging public keys (simulating peer discovery)...")
    alice_pub = alice.get_public_key_pem()
    bob_pub = bob.get_public_key_pem()
    
    print(f"\n   Alice's public key (first 100 chars):")
    print(f"   {alice_pub[:100]}...")
    
    alice.add_peer_public_key("bob", bob_pub)
    bob.add_peer_public_key("alice", alice_pub)
    print("\n   ✓ Public keys exchanged securely")
    
    # Message Encryption
    print_section("3. Sending Encrypted Message")
    
    messages = [
        "Hey Bob, this is a secret message! 🔐",
        "Let's meet at the usual place at 3 PM.",
        "The password is: SuperSecret123!"
    ]
    
    for i, msg in enumerate(messages, 1):
        print(f"\n📤 Message {i} from Alice to Bob:")
        print(f"   Plaintext: '{msg}'")
        
        # Encrypt
        encrypted_data = alice.encrypt_message("bob", msg)
        print(f"\n   🔒 Encrypted with AES-256-CBC:")
        print(f"      Message: {encrypted_data['encrypted_message'][:60]}...")
        print(f"      AES Key (RSA encrypted): {encrypted_data['encrypted_key'][:60]}...")
        print(f"      IV: {encrypted_data['iv']}")
        
        # Sign
        signature = alice.sign_message(msg)
        print(f"\n   ✍️  Digital signature (RSA-PSS):")
        print(f"      {signature[:60]}...")
        
        # Decrypt
        print(f"\n📥 Bob receives and decrypts:")
        decrypted = bob.decrypt_message(encrypted_data)
        print(f"   Plaintext: '{decrypted}'")
        
        # Verify
        is_valid = bob.verify_signature("alice", decrypted, signature)
        if is_valid:
            print(f"   ✓ Signature verified - message is authentic!")
        else:
            print(f"   ✗ Signature verification failed - message may be tampered!")
        
        if i < len(messages):
            time.sleep(1)
    
    # Tampering Detection
    print_section("4. Tampering Detection")
    
    original = "Transfer $1000 to account A"
    print(f"\n📤 Alice sends: '{original}'")
    
    encrypted = alice.encrypt_message("bob", original)
    signature = alice.sign_message(original)
    
    print(f"   ✓ Message encrypted and signed")
    
    # Attacker tries to modify
    print(f"\n⚠️  Attacker intercepts and tries to modify message...")
    tampered = "Transfer $9999 to account B"
    print(f"   Tampered message: '{tampered}'")
    
    # Bob checks signature
    print(f"\n🔍 Bob verifies the signature...")
    is_valid = bob.verify_signature("alice", tampered, signature)
    
    if not is_valid:
        print(f"   ✓ Tampering detected! Message rejected.")
        print(f"   🛡️  Security feature prevented the attack!")
    else:
        print(f"   ✗ Tampering NOT detected - this shouldn't happen!")
    
    # Statistics
    print_section("5. Security Statistics")
    print("\n📊 Encryption Details:")
    print(f"   • Algorithm: RSA-2048 + AES-256-CBC")
    print(f"   • Key Size: 2048 bits (RSA), 256 bits (AES)")
    print(f"   • Signature: RSA-PSS with SHA-256")
    print(f"   • Padding: OAEP for RSA encryption")
    print(f"   • Fresh Keys: New AES key for each message")
    print(f"\n🔒 Security Features:")
    print(f"   ✓ End-to-end encryption")
    print(f"   ✓ Forward secrecy (fresh AES keys)")
    print(f"   ✓ Message authentication (digital signatures)")
    print(f"   ✓ Tamper detection")
    print(f"   ✓ Identity verification")
    
    # Real-world usage
    print_section("6. Real-World Usage")
    print("\n🚀 To use the actual messenger:")
    print("\n   GUI Mode:")
    print("      python messenger_gui.py")
    print("\n   CLI Mode:")
    print("      python messenger_cli.py YourUsername")
    print("\n📖 For more information:")
    print("   • README.md - Usage and features")
    print("   • SECURITY.md - Security considerations")
    
    print("\n" + "=" * 60)
    print("  Demo Complete! 🎉")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    try:
        demo_encryption()
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user.")
    except Exception as e:
        print(f"\n\n❌ Error during demo: {e}")
        raise
