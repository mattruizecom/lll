import miniupnpc
import socket
import tkinter as tk
from tkinter import messagebox
import threading
import subprocess

# Function to discover and forward port using UPnP
def forward_port(port):
    upnp = miniupnpc.UPnP()
    upnp.discoverdelay = 200
    found = upnp.discover()

    if found > 0:
        upnp.selectigd()
        print(f"Router found: {upnp.routername}")

        try:
            external_port = port
            internal_port = port
            internal_ip = upnp.lanaddr
            upnp.addportmapping(external_port, 'TCP', internal_ip, internal_port, 'Minecraft Server', '')
            messagebox.showinfo("Success", f"Port {external_port} forwarded to {internal_ip}:{internal_port}")
            print(f"Port {external_port} forwarded to {internal_ip}:{internal_port}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to forward port: {e}")
    else:
        messagebox.showerror("Error", "No UPnP router found.")

# Function to start the tunneling server
def start_tunneling_server():
    # Change the command according to your environment; this assumes you have Python installed
    subprocess.Popen(["python", "tunnel_server.py"])

# Setup GUI
def start_program():
    port = int(port_entry.get())
    forward_port(port)
    start_tunneling_server()

# Create the main window
root = tk.Tk()
root.title("Minecraft Server Port Forwarding")

tk.Label(root, text="Enter Minecraft Server Port:").pack(pady=10)
port_entry = tk.Entry(root)
port_entry.insert(0, "25565")  # Default port
port_entry.pack(pady=10)

start_button = tk.Button(root, text="Start Port Forwarding", command=start_program)
start_button.pack(pady=20)

root.mainloop()
