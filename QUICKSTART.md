# Quick Start Guide - Better IP Messenger

Get started with Better IP Messenger in 3 easy steps!

## Prerequisites

- Python 3.7 or higher
- pip (Python package manager)
- Local Area Network (LAN) connection

## Installation

### Step 1: Clone or Download

```bash
git clone https://github.com/shashankbenakatti/betterIPMsgnr.git
cd betterIPMsgnr
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

That's it! The application is ready to use.

## Quick Test

### Test Encryption (No Network Required)

```bash
python demo.py
```

This will showcase all security features without requiring a network connection.

### Test Encryption Unit Tests

```bash
python test_encryption.py
```

## Usage

### Option 1: Graphical Interface (Recommended)

```bash
python messenger_gui.py
```

1. Enter your username
2. Wait for peers to be discovered (automatically)
3. Select a user from the left panel
4. Type a message and press Ctrl+Enter or click Send

### Option 2: Command Line Interface

```bash
python messenger_cli.py Alice
```

Commands:
- `list` - Show connected users
- `send 0 Hello!` - Send message to first user in list
- `quit` - Exit

## Testing with Multiple Users

### Same Computer

Open multiple terminals:

**Terminal 1:**
```bash
python messenger_cli.py Alice
```

**Terminal 2:**
```bash
python messenger_cli.py Bob
```

Now you can send messages between Alice and Bob!

### Different Computers

Make sure both computers are on the same LAN, then:

**Computer 1:**
```bash
python messenger_gui.py
```

**Computer 2:**
```bash
python messenger_gui.py
```

They will automatically discover each other!

## Firewall Configuration

If you're using a firewall, allow these ports:

```bash
# Linux (ufw)
sudo ufw allow 5000/udp
sudo ufw allow 5001/udp

# Windows Firewall
# Add inbound rules for UDP ports 5000 and 5001
```

## Troubleshooting

### "No peers found"

**Solutions:**
- Ensure both instances are on the same subnet
- Check firewall settings (ports 5000-5001 UDP)
- Wait 5-10 seconds for discovery
- Verify network connectivity with `ping`

### "Failed to send message"

**Solutions:**
- Check that peer is still online (`list` command in CLI)
- Verify firewall isn't blocking traffic
- Ensure recipient is running the application

### "Import Error: No module named cryptography"

**Solution:**
```bash
pip install -r requirements.txt
```

### Connection across subnets doesn't work

**Explanation:**
- The app uses UDP broadcast for discovery
- Broadcasts don't cross subnet boundaries by default
- Use on the same subnet/VLAN

## Security Checklist

Before using for sensitive communications:

- [ ] Verify you're on a trusted network
- [ ] Confirm peer identities through another channel
- [ ] Check that firewall rules are appropriate
- [ ] Ensure your system is up-to-date and secure
- [ ] Read SECURITY.md for detailed security information

## What's Happening Under the Hood?

1. **Startup**: Generate RSA-2048 key pair
2. **Discovery**: Broadcast presence with public key every 5 seconds
3. **Connection**: Store peer's public key when discovered
4. **Sending**: 
   - Generate fresh AES-256 key
   - Encrypt message with AES
   - Encrypt AES key with peer's RSA public key
   - Sign message with your RSA private key
   - Send encrypted package via UDP
5. **Receiving**:
   - Decrypt AES key with your RSA private key
   - Decrypt message with AES key
   - Verify signature with sender's RSA public key
   - Display message

## Features Demo

### See Encryption in Action

```bash
python demo.py
```

Output shows:
- Key generation
- Message encryption
- Signature creation
- Decryption
- Tampering detection

### Test Network Features

```bash
# Terminal 1
python messenger_cli.py TestUser1

# Terminal 2 (new terminal)
python messenger_cli.py TestUser2

# In Terminal 1
> list
Active Peers:
  0. TestUser2 (192.168.1.100)

> send 0 Hello from Terminal 1!
```

## Next Steps

- Read [README.md](README.md) for detailed documentation
- Review [SECURITY.md](SECURITY.md) for security considerations
- Explore the source code to understand the implementation
- Try different network configurations
- Test with friends on your LAN!

## Common Use Cases

### 1. Office Communication
```bash
python messenger_gui.py
```
Select colleagues from the list and chat securely.

### 2. Temporary Secure Channel
```bash
python messenger_cli.py ProjectAlpha
```
Quick setup for confidential discussions during meetings.

### 3. Home Network Chat
```bash
python messenger_gui.py
```
Communicate with family members on the same home network.

## Getting Help

- Check [README.md](README.md) for detailed documentation
- Review [SECURITY.md](SECURITY.md) for security information
- Open an issue on GitHub for bugs or questions

## Tips for Best Experience

1. **Username Choice**: Use recognizable usernames
2. **Network**: Ensure stable LAN connection
3. **Verification**: Verify peer IP addresses match expected values
4. **Updates**: Keep dependencies updated for security
5. **Backups**: The app doesn't store messages (by design)

---

**Ready to start secure messaging? Run:**

```bash
python messenger_gui.py
```

**Enjoy secure, private communication! 🔐**
