# Better IP Messenger 🔐

A secure, end-to-end encrypted LAN messaging application for private and confidential communication. Perfect for areas that require high security and privacy.

## 🌟 Features

- **End-to-End Encryption**: All messages are encrypted using RSA + AES hybrid encryption
- **Peer-to-Peer Communication**: Direct communication over LAN without central servers
- **Automatic Peer Discovery**: Automatically finds other users on the local network
- **Digital Signatures**: Message authentication to verify sender identity
- **User-Friendly GUI**: Simple and intuitive Tkinter-based interface
- **CLI Mode**: Command-line interface for headless environments
- **No Data Storage**: Messages are not stored on disk for maximum privacy
- **Secure Key Exchange**: Automatic secure key exchange using RSA public key cryptography

## 🔒 Security Features

- **RSA 2048-bit** encryption for key exchange
- **AES 256-bit** encryption for message content
- **Digital signatures** using RSA-PSS for message authentication
- **Fresh encryption keys** for each message
- **No plaintext transmission** - all data encrypted before sending
- **Automatic peer verification** through public key infrastructure

## 📋 Requirements

- Python 3.7 or higher
- Network access (LAN)
- Dependencies listed in `requirements.txt`

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/shashankbenakatti/betterIPMsgnr.git
cd betterIPMsgnr
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## 💻 Usage

### GUI Mode (Recommended)

Run the graphical interface:
```bash
python messenger_gui.py
```

1. Enter your username when prompted
2. The application will automatically discover peers on your LAN
3. Select a user from the left panel
4. Type your message and press `Ctrl+Enter` or click "Send"

### CLI Mode

Run the command-line interface:
```bash
python messenger_cli.py YourUsername
```

Commands:
- `list` - Show active peers
- `send <number> <message>` - Send message to peer (use number from list)
- `quit` - Exit application

Example:
```bash
> list
Active Peers:
  0. Alice (192.168.1.100)
  1. Bob (192.168.1.101)

> send 0 Hello Alice!
Message sent to Alice
```

## 🔧 How It Works

### Architecture

```
┌─────────────────┐
│   Application   │
│   (GUI/CLI)     │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
┌───▼──┐  ┌──▼────┐
│Crypto│  │Network│
│Utils │  │Manager│
└──────┘  └───────┘
```

### Encryption Process

1. **Key Generation**: Each user generates an RSA key pair on startup
2. **Peer Discovery**: Users broadcast their public keys via UDP
3. **Message Encryption**:
   - Generate random AES-256 key for the message
   - Encrypt message content with AES-CBC
   - Encrypt AES key with recipient's RSA public key
   - Sign message with sender's RSA private key
4. **Message Transmission**: Send encrypted package via UDP
5. **Message Decryption**:
   - Decrypt AES key using recipient's RSA private key
   - Decrypt message content using AES key
   - Verify signature using sender's public key

### Network Protocol

- **Discovery Port**: 5000 (UDP broadcast)
- **Message Port**: 5001 (UDP unicast)
- **Peer Timeout**: 15 seconds
- **Broadcast Interval**: 5 seconds

## 🔐 Security Considerations

### What This Application Protects Against

✅ Eavesdropping on the network
✅ Message tampering
✅ Identity spoofing
✅ Man-in-the-middle attacks (within trusted LAN)

### Limitations

⚠️ This application is designed for trusted LANs. It does not protect against:
- Compromised endpoints
- Malicious peers on the network
- Advanced persistent threats
- Physical access to machines

### Best Practices

1. **Use on trusted networks**: Only use on networks you control
2. **Verify users**: Confirm user identities through other means
3. **Keep updated**: Regularly update dependencies for security patches
4. **Secure your endpoint**: Ensure your computer is secure and malware-free
5. **Physical security**: Protect devices from unauthorized access

## 📁 Project Structure

```
betterIPMsgnr/
├── crypto_utils.py      # Encryption and decryption utilities
├── network.py           # Network communication and peer discovery
├── messenger_gui.py     # Graphical user interface
├── messenger_cli.py     # Command-line interface
├── requirements.txt     # Python dependencies
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## 🛠️ Development

### Running Tests

```bash
# Install dependencies
pip install -r requirements.txt

# Test CLI mode
python messenger_cli.py TestUser1

# Test GUI mode (in another terminal)
python messenger_gui.py
```

### Testing on the Same Machine

You can run multiple instances on the same machine for testing:

```bash
# Terminal 1
python messenger_cli.py Alice

# Terminal 2
python messenger_cli.py Bob
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## 📝 License

This project is open source and available for educational and personal use.

## ⚠️ Disclaimer

This software is provided as-is for educational and personal use. While it implements strong encryption, it has not undergone professional security auditing. Use at your own risk for sensitive communications.

## 🎯 Use Cases

- **Private team communication** in secure environments
- **Confidential business discussions** within offices
- **Educational purposes** for learning cryptography
- **Air-gapped networks** requiring secure communication
- **Privacy-conscious users** wanting control over their data

## 📚 Technical Details

### Encryption Algorithms

- **RSA-2048**: Asymmetric encryption for key exchange and signatures
- **AES-256-CBC**: Symmetric encryption for message content
- **PKCS#1 OAEP**: Padding scheme for RSA encryption
- **PSS**: Probabilistic signature scheme for digital signatures
- **SHA-256**: Hash function for signatures and key derivation

### Dependencies

- `cryptography`: Industry-standard cryptographic library
- `tkinter`: Built-in Python GUI framework (no installation needed)

## 🔄 Future Enhancements

- [ ] File transfer support
- [ ] Group chat functionality
- [ ] Message history encryption
- [ ] Mobile application
- [ ] Cross-platform compatibility improvements
- [ ] Audio/video call support

## 👥 Authors

- Shashank Benakatti

## 📧 Support

For questions or support, please open an issue on GitHub.

---

**Remember**: Security is only as strong as its weakest link. Stay vigilant!