"""
GUI for Better IP Messenger.
Provides a simple and intuitive interface for secure messaging.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
from datetime import datetime
from crypto_utils import SecureMessenger
from network import NetworkManager


class MessengerGUI:
    """Main GUI application for Better IP Messenger."""
    
    def __init__(self):
        """Initialize the GUI."""
        self.root = tk.Tk()
        self.root.title("Better IP Messenger - Secure LAN Chat")
        self.root.geometry("900x600")
        
        # Set up encryption and network
        self.username = None
        self.crypto = None
        self.network = None
        self.current_peer = None
        
        # Show login dialog first
        self.show_login_dialog()
    
    def show_login_dialog(self):
        """Show login dialog to get username."""
        login_window = tk.Toplevel(self.root)
        login_window.title("Login")
        login_window.geometry("300x120")
        login_window.transient(self.root)
        login_window.grab_set()
        
        # Center the login window
        login_window.update_idletasks()
        x = (login_window.winfo_screenwidth() // 2) - (300 // 2)
        y = (login_window.winfo_screenheight() // 2) - (120 // 2)
        login_window.geometry(f"300x120+{x}+{y}")
        
        tk.Label(login_window, text="Enter your username:", font=("Arial", 10)).pack(pady=10)
        
        username_entry = tk.Entry(login_window, font=("Arial", 10))
        username_entry.pack(pady=5)
        username_entry.focus()
        
        def on_login():
            username = username_entry.get().strip()
            if username:
                self.username = username
                login_window.destroy()
                self.initialize_messenger()
            else:
                messagebox.showerror("Error", "Please enter a username")
        
        def on_enter(event):
            on_login()
        
        username_entry.bind('<Return>', on_enter)
        
        tk.Button(login_window, text="Login", command=on_login, font=("Arial", 10)).pack(pady=10)
    
    def initialize_messenger(self):
        """Initialize the messenger after login."""
        # Set up encryption
        self.crypto = SecureMessenger()
        
        # Set up network
        self.network = NetworkManager(
            self.username,
            self.crypto,
            message_callback=self.on_message_received
        )
        
        # Build GUI
        self.build_gui()
        
        # Start network services
        self.network.start()
        
        # Update peer list periodically
        self.update_peer_list()
    
    def build_gui(self):
        """Build the main GUI."""
        # Configure root window
        self.root.title(f"Better IP Messenger - {self.username}")
        
        # Create main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Left panel - User list
        left_frame = ttk.LabelFrame(main_frame, text="Active Users", padding="5")
        left_frame.grid(row=0, column=0, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        
        # User listbox
        self.user_listbox = tk.Listbox(left_frame, width=25, font=("Arial", 10))
        self.user_listbox.pack(fill=tk.BOTH, expand=True)
        self.user_listbox.bind('<<ListboxSelect>>', self.on_user_select)
        
        # Right panel - Chat area
        right_frame = ttk.Frame(main_frame)
        right_frame.grid(row=0, column=1, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(0, weight=1)
        
        # Chat display
        chat_frame = ttk.LabelFrame(right_frame, text="Chat", padding="5")
        chat_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 5))
        chat_frame.columnconfigure(0, weight=1)
        chat_frame.rowconfigure(0, weight=1)
        
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD,
            font=("Arial", 10),
            state=tk.DISABLED
        )
        self.chat_display.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure text tags for styling
        self.chat_display.tag_config("sender", foreground="blue", font=("Arial", 10, "bold"))
        self.chat_display.tag_config("timestamp", foreground="gray", font=("Arial", 8))
        self.chat_display.tag_config("system", foreground="green", font=("Arial", 9, "italic"))
        
        # Message input area
        input_frame = ttk.Frame(right_frame)
        input_frame.grid(row=1, column=0, sticky=(tk.W, tk.E))
        input_frame.columnconfigure(0, weight=1)
        
        self.message_entry = scrolledtext.ScrolledText(
            input_frame,
            wrap=tk.WORD,
            height=4,
            font=("Arial", 10)
        )
        self.message_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        self.message_entry.bind('<Control-Return>', self.send_message)
        
        send_button = ttk.Button(input_frame, text="Send\n(Ctrl+Enter)", command=self.send_message)
        send_button.grid(row=0, column=1)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set(f"Logged in as {self.username} | IP: {self.network.local_ip} | Waiting for peers...")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Add welcome message
        self.add_system_message(
            "Welcome to Better IP Messenger!\n"
            "This is a secure LAN messaging application with end-to-end encryption.\n"
            "Select a user from the left panel to start chatting."
        )
    
    def update_peer_list(self):
        """Update the list of active peers."""
        if not self.network:
            return
        
        peers = self.network.get_peers()
        
        # Save current selection
        current_selection = None
        if self.user_listbox.curselection():
            current_selection = self.user_listbox.get(self.user_listbox.curselection()[0])
        
        # Clear and repopulate list
        self.user_listbox.delete(0, tk.END)
        for peer_id, peer_info in peers:
            display_name = f"{peer_info['username']} ({peer_info['ip']})"
            self.user_listbox.insert(tk.END, display_name)
            
            # Restore selection if peer is still available
            if current_selection and display_name == current_selection:
                self.user_listbox.select_set(tk.END)
        
        # Update status
        peer_count = len(peers)
        self.status_var.set(
            f"Logged in as {self.username} | IP: {self.network.local_ip} | "
            f"{peer_count} peer(s) online"
        )
        
        # Schedule next update
        self.root.after(2000, self.update_peer_list)
    
    def on_user_select(self, event):
        """Handle user selection."""
        if self.user_listbox.curselection():
            selected_index = self.user_listbox.curselection()[0]
            selected_text = self.user_listbox.get(selected_index)
            
            # Extract IP from the display name
            ip = selected_text.split('(')[1].split(')')[0]
            
            # Find the peer_id
            peers = self.network.get_peers()
            for peer_id, peer_info in peers:
                if peer_info['ip'] == ip:
                    self.current_peer = (peer_id, peer_info)
                    self.add_system_message(f"Chatting with {peer_info['username']}")
                    break
    
    def send_message(self, event=None):
        """Send a message to the selected peer."""
        if not self.current_peer:
            messagebox.showwarning("No Recipient", "Please select a user to send a message to.")
            return
        
        message = self.message_entry.get("1.0", tk.END).strip()
        if not message:
            return
        
        peer_id, peer_info = self.current_peer
        
        try:
            # Send message
            if self.network.send_message(peer_id, message):
                # Display sent message
                self.add_chat_message("You", message, sent=True)
                
                # Clear input
                self.message_entry.delete("1.0", tk.END)
            else:
                messagebox.showerror("Error", "Failed to send message.")
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send message: {str(e)}")
        
        return "break"  # Prevent default behavior
    
    def on_message_received(self, message_data):
        """Handle received message."""
        # Schedule GUI update in main thread
        self.root.after(0, self._display_received_message, message_data)
    
    def _display_received_message(self, message_data):
        """Display received message in chat area."""
        sender = message_data['sender']
        message = message_data['message']
        self.add_chat_message(sender, message, sent=False)
    
    def add_chat_message(self, sender, message, sent=False):
        """Add a message to the chat display."""
        self.chat_display.config(state=tk.NORMAL)
        
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Add timestamp
        self.chat_display.insert(tk.END, f"[{timestamp}] ", "timestamp")
        
        # Add sender
        self.chat_display.insert(tk.END, f"{sender}: ", "sender")
        
        # Add message
        self.chat_display.insert(tk.END, f"{message}\n")
        
        # Auto-scroll to bottom
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)
    
    def add_system_message(self, message):
        """Add a system message to the chat display."""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"[SYSTEM] {message}\n", "system")
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)
    
    def run(self):
        """Run the GUI application."""
        # Handle window close
        def on_closing():
            if self.network:
                self.network.stop()
            self.root.destroy()
        
        self.root.protocol("WM_DELETE_WINDOW", on_closing)
        self.root.mainloop()


def main():
    """Main entry point."""
    app = MessengerGUI()
    app.run()


if __name__ == "__main__":
    main()
