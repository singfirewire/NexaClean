import os
import sys
import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import shutil
from datetime import datetime
import json

def get_app_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

class NexaClean:
    def __init__(self, root):
        self.root = root
        self.root.title("NexaClean")
        self.root.geometry("900x750")
        self.root.resizable(False, False)
        
        self.app_dir = get_app_dir()
        self.desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        
        self.checkbox_vars = []
        self.folders_to_delete = []
        self.shortcuts_to_delete = []
        self.shortcut_checkbox_vars = []
        self.temp_files_to_delete = []
        self.temp_checkbox_vars = []
        self.extensions = {}
        self.current_folder_path = tk.StringVar(value=self.desktop_path)
        self.duplicate_handling = tk.StringVar(value="skip")
        self.theme_var = tk.StringVar(value="Retro Purple")
        
        self.title_bar = None
        self.window_borderless = False

        self.themes = {
            "Macrium Dark": {
                'bg_dark': '#1c1c1c',
                'bg_card': '#2d2d2d',
                'bg_input': '#3a3a3a',
                'accent': '#e8850c',
                'accent_green': '#5cb85c',
                'accent_blue': '#5bc0de',
                'accent_orange': '#e8850c',
                'text_primary': '#e0e0e0',
                'text_secondary': '#999999',
                'success': '#5cb85c',
                'danger': '#d9534f',
                'warning': '#e8850c'
            },
            "Dark Neon": {
                'bg_dark': '#1a1a2e',
                'bg_card': '#16213e',
                'bg_input': '#0f3460',
                'accent': '#e94560',
                'accent_green': '#00d4aa',
                'accent_blue': '#4361ee',
                'accent_orange': '#ff6b35',
                'text_primary': '#ffffff',
                'text_secondary': '#a0a0b0',
                'success': '#00d4aa',
                'danger': '#e94560',
                'warning': '#ff6b35'
            },
            "Light Clean": {
                'bg_dark': '#f5f5f5',
                'bg_card': '#ffffff',
                'bg_input': '#e8e8e8',
                'accent': '#3b82f6',
                'accent_green': '#22c55e',
                'accent_blue': '#3b82f6',
                'accent_orange': '#f97316',
                'text_primary': '#1f2937',
                'text_secondary': '#6b7280',
                'success': '#22c55e',
                'danger': '#ef4444',
                'warning': '#f97316'
            },
            "Ocean Blue": {
                'bg_dark': '#0a1929',
                'bg_card': '#132f4c',
                'bg_input': '#1a3a5c',
                'accent': '#0077b6',
                'accent_green': '#06d6a0',
                'accent_blue': '#0096c7',
                'accent_orange': '#fca311',
                'text_primary': '#ffffff',
                'text_secondary': '#94a3b8',
                'success': '#06d6a0',
                'danger': '#e63946',
                'warning': '#fca311'
            },
            "Forest Green": {
                'bg_dark': '#1a2f1a',
                'bg_card': '#2d4a2d',
                'bg_input': '#3d5c3d',
                'accent': '#4ade80',
                'accent_green': '#22c55e',
                'accent_blue': '#60a5fa',
                'accent_orange': '#fbbf24',
                'text_primary': '#ffffff',
                'text_secondary': '#a3be8c',
                'success': '#22c55e',
                'danger': '#f87171',
                'warning': '#fbbf24'
            },
            "Sunset Orange": {
                'bg_dark': '#2d1b1b',
                'bg_card': '#3d2525',
                'bg_input': '#4d3030',
                'accent': '#fb923c',
                'accent_green': '#4ade80',
                'accent_blue': '#60a5fa',
                'accent_orange': '#f97316',
                'text_primary': '#ffffff',
                'text_secondary': '#d4a574',
                'success': '#4ade80',
                'danger': '#f87171',
                'warning': '#fbbf24'
            },
            "Purple Haze": {
                'bg_dark': '#1e1033',
                'bg_card': '#2a1845',
                'bg_input': '#3a2555',
                'accent': '#a855f7',
                'accent_green': '#4ade80',
                'accent_blue': '#818cf8',
                'accent_orange': '#fb923c',
                'text_primary': '#ffffff',
                'text_secondary': '#c4b5fd',
                'success': '#4ade80',
                'danger': '#f87171',
                'warning': '#fb923c'
            },
            "Glitch Purple": {
                'bg_dark': '#f0e8ff',
                'bg_card': '#ffffff',
                'bg_input': '#e8dff5',
                'accent': '#8b5cf6',
                'accent_green': '#22c55e',
                'accent_blue': '#6366f1',
                'accent_orange': '#f97316',
                'text_primary': '#1e1b4b',
                'text_secondary': '#6b7280',
                'success': '#22c55e',
                'danger': '#ef4444',
                'warning': '#f97316'
            },
            "Retro Purple": {
                'bg_dark': '#1a1025',
                'bg_card': '#2a1d3d',
                'bg_input': '#3a2d52',
                'accent': '#b388ff',
                'accent_green': '#a5d6a7',
                'accent_blue': '#90caf9',
                'accent_orange': '#ffcc80',
                'text_primary': '#e8d5f5',
                'text_secondary': '#9575cd',
                'success': '#a5d6a7',
                'danger': '#ef9a9a',
                'warning': '#ffcc80',
                'retro_font': 'Consolas',
                'retro_border': 'groove',
                'retro_border_width': 3,
                'retro_card_relief': 'ridge'
            }
        }
        
        self.colors = self.themes["Retro Purple"]
        
        self.stats = {
            'folders_deleted': 0,
            'shortcuts_deleted': 0,
            'temp_files_deleted': 0,
            'files_organized': 0,
            'total_cleaned_size': 0,
            'first_use_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'last_cleanup_date': None
        }
        
        self.load_stats()
        self.apply_theme(self.theme_var.get())
        self.setup_styles()
        self.create_widgets()
        self.search_folders()
    
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        tab_font = self.get_font(11, True)
        style.configure("TNotebook", 
                       background=self.colors['bg_dark'],
                       borderwidth=0)
        style.configure("TNotebook.Tab",
                       background=self.colors['bg_card'],
                       foreground=self.colors['text_primary'],
                       padding=[20, 10],
                       font=tab_font)
        style.map("TNotebook.Tab",
                 background=[("selected", self.colors['accent'])],
                 foreground=[("selected", self.colors['text_primary'])])
        
        style.configure("Vertical.TScrollbar",
                       background=self.colors['bg_card'],
                       troughcolor=self.colors['bg_dark'],
                       borderwidth=0)
        
        tree_font = self.get_font(10)
        tree_heading_font = self.get_font(10, True)
        style.configure("Custom.Treeview",
                       background=self.colors['bg_card'],
                       foreground=self.colors['text_primary'],
                       fieldbackground=self.colors['bg_card'],
                       font=tree_font,
                       rowheight=30)
        style.configure("Custom.Treeview.Heading",
                       background=self.colors['bg_input'],
                       foreground=self.colors['text_primary'],
                       font=tree_heading_font)
        style.map("Custom.Treeview",
                 background=[("selected", self.colors['accent'])],
                 foreground=[("selected", self.colors['text_primary'])])
    
    def apply_theme(self, theme_name):
        if theme_name in self.themes:
            self.colors = self.themes[theme_name]
            self.root.configure(bg=self.colors['bg_dark'])
            
            if self.is_retro_theme() and not self.window_borderless:
                self.set_borderless(True)
            elif not self.is_retro_theme() and self.window_borderless:
                self.set_borderless(False)
            
            self.refresh_ui()
    
    def refresh_ui(self):
        self.setup_styles()
        
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.configure(bg=self.colors['bg_dark'])
                for child in widget.winfo_children():
                    self.update_widget_colors(child)
        
        self.create_widgets()
        self.search_folders()
        self.refresh_stats_display()
    
    def update_widget_colors(self, widget):
        try:
            if isinstance(widget, tk.Frame):
                widget.configure(bg=self.colors['bg_card'])
            elif isinstance(widget, tk.Label):
                current_bg = widget.cget("bg")
                if current_bg in self.themes.get("Dark Neon", {}).values():
                    widget.configure(bg=self.colors['bg_card'], 
                                   fg=self.colors['text_primary'])
            elif isinstance(widget, tk.Button):
                widget.configure(bg=self.colors['accent_blue'],
                               fg=self.colors['text_primary'])
        except:
            pass
        
        for child in widget.winfo_children():
            self.update_widget_colors(child)
    
    def create_widgets(self):
        for widget in self.root.winfo_children():
            if isinstance(widget, (ttk.Notebook, tk.Frame)):
                if widget != self.title_bar:
                    widget.destroy()
        
        top_frame = tk.Frame(self.root, bg=self.colors['bg_dark'])
        top_frame.pack(fill=tk.X, padx=15, pady=(15, 5))
        
        theme_label = tk.Label(top_frame, text="Theme:", 
                              font=("Segoe UI", 10, "bold"),
                              bg=self.colors['bg_dark'],
                              fg=self.colors['text_primary'])
        theme_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.theme_combo = ttk.Combobox(top_frame, 
                                        textvariable=self.theme_var,
                                        values=list(self.themes.keys()),
                                        state="readonly",
                                        width=15,
                                        font=("Segoe UI", 10))
        self.theme_combo.pack(side=tk.LEFT)
        self.theme_combo.bind("<<ComboboxSelected>>", self.on_theme_change)
        
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)
        
        self.tab1 = tk.Frame(self.notebook, bg=self.colors['bg_dark'])
        self.tab2 = tk.Frame(self.notebook, bg=self.colors['bg_dark'])
        self.tab3 = tk.Frame(self.notebook, bg=self.colors['bg_dark'])
        self.tab4 = tk.Frame(self.notebook, bg=self.colors['bg_dark'])
        self.tab5 = tk.Frame(self.notebook, bg=self.colors['bg_dark'])
        
        self.notebook.add(self.tab1, text="  New Folder  ")
        self.notebook.add(self.tab2, text="  Move to Folder  ")
        self.notebook.add(self.tab3, text="  Manage Shortcuts  ")
        self.notebook.add(self.tab4, text="  Clean Temp  ")
        self.notebook.add(self.tab5, text="  Statistics  ")
        
        self.progress_var = tk.DoubleVar()
        self.status_var = tk.StringVar(value="Ready")
        
        self.create_tab1_widgets()
        self.create_tab2_widgets()
        self.create_tab3_widgets()
        self.create_tab4_widgets()
        self.create_tab5_widgets()
        self.create_status_bar()
    
    def on_theme_change(self, event=None):
        selected_theme = self.theme_var.get()
        self.apply_theme(selected_theme)
        self.save_stats()
    
    def create_status_bar(self):
        status_frame = tk.Frame(self.root, bg=self.colors['bg_card'], height=40)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(status_frame, 
                                    textvariable=self.status_var,
                                    bg=self.colors['bg_card'],
                                    fg=self.colors['text_secondary'],
                                    font=("Segoe UI", 9))
        self.status_label.pack(side=tk.LEFT, padx=15, pady=8)
        
        self.progress_bar = ttk.Progressbar(status_frame, 
                                           variable=self.progress_var,
                                           maximum=100,
                                           mode='determinate',
                                           length=200)
        self.progress_bar.pack(side=tk.RIGHT, padx=15, pady=8)
    
    def update_status(self, message, progress=None):
        self.status_var.set(message)
        if progress is not None:
            self.progress_var.set(progress)
        self.root.update_idletasks()
    
    def create_card(self, parent, **kwargs):
        relief = self.colors.get('retro_card_relief', tk.FLAT)
        borderwidth = self.colors.get('retro_border_width', 1) if self.is_retro_theme() else 1
        card = tk.Frame(parent, 
                       bg=self.colors['bg_card'],
                       highlightbackground=self.colors['bg_input'],
                       highlightthickness=borderwidth,
                       relief=relief,
                       **kwargs)
        return card
    
    def create_button(self, parent, text, command, color_key='accent_blue', **kwargs):
        colors = {
            'accent_green': self.colors['accent_green'],
            'accent_blue': self.colors['accent_blue'],
            'accent': self.colors['accent'],
            'accent_orange': self.colors['accent_orange'],
            'danger': self.colors['danger']
        }
        bg_color = colors.get(color_key, self.colors['accent_blue'])
        
        if self.is_retro_theme():
            relief = tk.RAISED
            borderwidth = self.colors.get('retro_border_width', 3)
            font = self.get_font(11, True)
        else:
            relief = tk.FLAT
            borderwidth = 0
            font = ("Segoe UI", 10, "bold")
        
        btn = tk.Button(parent,
                       text=text,
                       command=command,
                       bg=bg_color,
                       fg=self.colors['text_primary'],
                       font=font,
                       relief=relief,
                       bd=borderwidth,
                       cursor="hand2",
                       activebackground=self.lighten_color(bg_color),
                       activeforeground=self.colors['text_primary'],
                       **kwargs)
        btn.bind("<Enter>", lambda e: btn.configure(bg=self.lighten_color(bg_color)))
        btn.bind("<Leave>", lambda e: btn.configure(bg=bg_color))
        return btn
    
    def lighten_color(self, color, factor=1.2):
        color = color.lstrip('#')
        r, g, b = int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16)
        r = min(255, int(r * factor))
        g = min(255, int(g * factor))
        b = min(255, int(b * factor))
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def is_retro_theme(self):
        return 'retro_font' in self.colors
    
    def get_font(self, size=10, bold=False):
        weight = "bold" if bold else "normal"
        if self.is_retro_theme():
            return (self.colors['retro_font'], size, weight)
        return ("Segoe UI", size, weight)
    
    def create_custom_title_bar(self):
        if self.title_bar:
            self.title_bar.destroy()
        
        self.title_bar = tk.Frame(self.root, bg=self.colors['bg_dark'], height=35)
        self.title_bar.pack(fill=tk.X, side=tk.TOP)
        self.title_bar.pack_propagate(False)
        
        title_font = self.get_font(11, True)
        
        title_label = tk.Label(self.title_bar, text="NexaClean",
                              font=title_font,
                              bg=self.colors['bg_dark'],
                              fg=self.colors['text_primary'])
        title_label.pack(side=tk.LEFT, padx=15, pady=5)
        
        close_btn = tk.Button(self.title_bar, text="X",
                             font=self.get_font(10, True),
                             bg=self.colors['danger'],
                             fg=self.colors['text_primary'],
                             bd=0,
                             width=3,
                             command=self.close_window)
        close_btn.pack(side=tk.RIGHT, padx=2, pady=5)
        
        minimize_btn = tk.Button(self.title_bar, text="_",
                                font=self.get_font(10, True),
                                bg=self.colors['accent_orange'],
                                fg=self.colors['text_primary'],
                                bd=0,
                                width=3,
                                command=self.minimize_window)
        minimize_btn.pack(side=tk.RIGHT, padx=2, pady=5)
        
        self.title_bar.bind("<Button-1>", self.start_drag)
        self.title_bar.bind("<B1-Motion>", self.do_drag)
        title_label.bind("<Button-1>", self.start_drag)
        title_label.bind("<B1-Motion>", self.do_drag)
    
    def start_drag(self, event):
        self._drag_x = event.x
        self._drag_y = event.y
    
    def do_drag(self, event):
        x = self.root.winfo_x() + event.x - self._drag_x
        y = self.root.winfo_y() + event.y - self._drag_y
        self.root.geometry(f"+{x}+{y}")
    
    def minimize_window(self):
        self.root.overrideredirect(False)
        self.root.iconify()
        self.root.after(100, self.restore_override)
    
    def restore_override(self):
        self.root.bind("<Map>", self.on_restore)
    
    def on_restore(self, event):
        self.root.unbind("<Map>")
        if self.window_borderless:
            self.root.overrideredirect(True)
    
    def close_window(self):
        self.root.destroy()
    
    def set_borderless(self, enabled):
        self.window_borderless = enabled
        if enabled:
            self.root.overrideredirect(True)
            self.create_custom_title_bar()
        else:
            self.root.overrideredirect(False)
            if self.title_bar:
                self.title_bar.destroy()
                self.title_bar = None
    
    def create_tab1_widgets(self):
        header = self.create_card(self.tab1)
        header.pack(fill=tk.X, padx=20, pady=(20, 10))
        
        tk.Label(header, text="New Folder Cleanup", 
                font=self.get_font(16, True),
                bg=self.colors['bg_card'],
                fg=self.colors['text_primary']).pack(pady=15)
        
        tk.Label(header, text="Find and delete unnecessary 'New folder' directories",
                font=self.get_font(10),
                bg=self.colors['bg_card'],
                fg=self.colors['text_secondary']).pack(pady=(0, 15))
        
        button_frame = tk.Frame(header, bg=self.colors['bg_card'])
        button_frame.pack(pady=10)
        
        self.create_button(button_frame, "Search Folders", 
                          self.search_folders, 'accent_green',
                          width=18, height=2).pack(side=tk.LEFT, padx=10)
        
        self.create_button(button_frame, "Delete Selected", 
                          self.delete_selected_folders, 'danger',
                          width=18, height=2).pack(side=tk.LEFT, padx=10)
        
        result_card = self.create_card(self.tab1)
        result_card.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        self.count_label = tk.Label(result_card, text="Found: 0 folders", 
                                   font=("Segoe UI", 11, "bold"),
                                   bg=self.colors['bg_card'],
                                   fg=self.colors['accent_green'])
        self.count_label.pack(anchor=tk.W, padx=15, pady=10)
        
        list_frame = tk.Frame(result_card, bg=self.colors['bg_input'])
        list_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        self.canvas = tk.Canvas(list_frame, bg=self.colors['bg_card'], 
                               highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(list_frame, orient="vertical", 
                                      command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=self.colors['bg_card'])
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
    
    def create_tab2_widgets(self):
        header = self.create_card(self.tab2)
        header.pack(fill=tk.X, padx=20, pady=(20, 10))
        
        tk.Label(header, text="File Organization", 
                font=self.get_font(16, True),
                bg=self.colors['bg_card'],
                fg=self.colors['text_primary']).pack(pady=15)
        
        folder_frame = tk.Frame(header, bg=self.colors['bg_card'])
        folder_frame.pack(fill=tk.X, padx=20, pady=5)
        
        tk.Label(folder_frame, text="Folder:", 
                font=self.get_font(10),
                bg=self.colors['bg_card'],
                fg=self.colors['text_secondary']).pack(side=tk.LEFT)
        
        self.folder_entry = tk.Entry(folder_frame, 
                                    textvariable=self.current_folder_path,
                                    font=("Segoe UI", 10),
                                    bg=self.colors['bg_input'],
                                    fg=self.colors['text_primary'],
                                    insertbackground=self.colors['text_primary'],
                                    relief=tk.FLAT)
        self.folder_entry.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
        
        self.create_button(folder_frame, "Browse", 
                          self.browse_folder, 'accent_blue',
                          width=10).pack(side=tk.LEFT, padx=5)
        
        duplicate_frame = tk.Frame(header, bg=self.colors['bg_card'])
        duplicate_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(duplicate_frame, text="Duplicate handling:", 
                font=("Segoe UI", 10),
                bg=self.colors['bg_card'],
                fg=self.colors['text_secondary']).pack(side=tk.LEFT)
        
        for text, value in [("Skip", "skip"), ("Overwrite", "overwrite"), 
                           ("Keep newest", "keep_newest")]:
            rb = tk.Radiobutton(duplicate_frame, text=text, 
                               variable=self.duplicate_handling,
                               value=value,
                               font=("Segoe UI", 10),
                               bg=self.colors['bg_card'],
                               fg=self.colors['text_primary'],
                               selectcolor=self.colors['bg_input'],
                               activebackground=self.colors['bg_card'],
                               activeforeground=self.colors['accent_green'])
            rb.pack(side=tk.LEFT, padx=15)
        
        button_frame = tk.Frame(header, bg=self.colors['bg_card'])
        button_frame.pack(pady=15)
        
        self.create_button(button_frame, "Scan Extensions", 
                          self.scan_extensions, 'accent_blue',
                          width=18, height=2).pack(side=tk.LEFT, padx=10)
        
        self.create_button(button_frame, "Move by Extension", 
                          self.organize_files, 'accent_green',
                          width=18, height=2).pack(side=tk.LEFT, padx=10)
        
        self.create_button(button_frame, "Clear Data", 
                          self.clear_data, 'accent_orange',
                          width=18, height=2).pack(side=tk.LEFT, padx=10)
        
        tree_card = self.create_card(self.tab2)
        tree_card.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        tree_frame = tk.Frame(tree_card, bg=self.colors['bg_card'])
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        columns = ("Extension", "File Count", "Folder Exists")
        self.tree = ttk.Treeview(tree_frame, columns=columns, 
                                show="headings", height=12,
                                style="Custom.Treeview")
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, 
                                 command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def create_tab3_widgets(self):
        header = self.create_card(self.tab3)
        header.pack(fill=tk.X, padx=20, pady=(20, 10))
        
        tk.Label(header, text="Shortcut Management", 
                font=self.get_font(16, True),
                bg=self.colors['bg_card'],
                fg=self.colors['text_primary']).pack(pady=15)
        
        tk.Label(header, text="Move shortcuts to a dedicated SHORTCUT folder",
                font=self.get_font(10),
                bg=self.colors['bg_card'],
                fg=self.colors['text_secondary']).pack(pady=(0, 15))
        
        button_frame = tk.Frame(header, bg=self.colors['bg_card'])
        button_frame.pack(pady=10)
        
        self.create_button(button_frame, "Search Shortcuts", 
                          self.search_shortcuts, 'accent_orange',
                          width=18, height=2).pack(side=tk.LEFT, padx=10)
        
        self.create_button(button_frame, "Move Selected", 
                          self.move_selected_shortcuts, 'accent_green',
                          width=18, height=2).pack(side=tk.LEFT, padx=10)
        
        self.create_button(button_frame, "Move All", 
                          self.move_all_shortcuts, 'accent_blue',
                          width=18, height=2).pack(side=tk.LEFT, padx=10)
        
        result_card = self.create_card(self.tab3)
        result_card.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        self.shortcut_count_label = tk.Label(result_card, text="Found: 0 shortcuts", 
                                           font=("Segoe UI", 11, "bold"),
                                           bg=self.colors['bg_card'],
                                           fg=self.colors['accent_green'])
        self.shortcut_count_label.pack(anchor=tk.W, padx=15, pady=10)
        
        list_frame = tk.Frame(result_card, bg=self.colors['bg_input'])
        list_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        self.shortcut_canvas = tk.Canvas(list_frame, bg=self.colors['bg_card'], 
                                        highlightthickness=0)
        self.shortcut_scrollbar = ttk.Scrollbar(list_frame, orient="vertical", 
                                               command=self.shortcut_canvas.yview)
        self.shortcut_scrollable_frame = tk.Frame(self.shortcut_canvas, 
                                                 bg=self.colors['bg_card'])
        
        self.shortcut_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.shortcut_canvas.configure(
                scrollregion=self.shortcut_canvas.bbox("all"))
        )
        
        self.shortcut_canvas.create_window((0, 0), 
                                          window=self.shortcut_scrollable_frame, 
                                          anchor="nw")
        self.shortcut_canvas.configure(yscrollcommand=self.shortcut_scrollbar.set)
        
        self.shortcut_canvas.pack(side="left", fill="both", expand=True)
        self.shortcut_scrollbar.pack(side="right", fill="y")
        
        self.shortcut_canvas.bind("<MouseWheel>", self._on_shortcut_mousewheel)
    
    def create_tab4_widgets(self):
        header = self.create_card(self.tab4)
        header.pack(fill=tk.X, padx=20, pady=(20, 10))
        
        tk.Label(header, text="Temp File Cleanup", 
                font=self.get_font(16, True),
                bg=self.colors['bg_card'],
                fg=self.colors['text_primary']).pack(pady=15)
        
        tk.Label(header, text="Remove temporary and junk files (.tmp, .temp, .log, .cache)",
                font=self.get_font(10),
                bg=self.colors['bg_card'],
                fg=self.colors['text_secondary']).pack(pady=(0, 15))
        
        button_frame = tk.Frame(header, bg=self.colors['bg_card'])
        button_frame.pack(pady=10)
        
        self.create_button(button_frame, "Search Temp Files", 
                          self.search_temp_files, 'accent_orange',
                          width=18, height=2).pack(side=tk.LEFT, padx=10)
        
        self.create_button(button_frame, "Delete Selected", 
                          self.delete_selected_temp_files, 'danger',
                          width=18, height=2).pack(side=tk.LEFT, padx=10)
        
        self.create_button(button_frame, "Delete All Temp", 
                          self.delete_all_temp_files, 'danger',
                          width=18, height=2).pack(side=tk.LEFT, padx=10)
        
        result_card = self.create_card(self.tab4)
        result_card.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        self.temp_count_label = tk.Label(result_card, text="Found: 0 temp files (0 KB)", 
                                       font=("Segoe UI", 11, "bold"),
                                       bg=self.colors['bg_card'],
                                       fg=self.colors['accent_green'])
        self.temp_count_label.pack(anchor=tk.W, padx=15, pady=10)
        
        list_frame = tk.Frame(result_card, bg=self.colors['bg_input'])
        list_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        self.temp_canvas = tk.Canvas(list_frame, bg=self.colors['bg_card'], 
                                    highlightthickness=0)
        self.temp_scrollbar = ttk.Scrollbar(list_frame, orient="vertical", 
                                           command=self.temp_canvas.yview)
        self.temp_scrollable_frame = tk.Frame(self.temp_canvas, 
                                            bg=self.colors['bg_card'])
        
        self.temp_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.temp_canvas.configure(
                scrollregion=self.temp_canvas.bbox("all"))
        )
        
        self.temp_canvas.create_window((0, 0), window=self.temp_scrollable_frame, 
                                      anchor="nw")
        self.temp_canvas.configure(yscrollcommand=self.temp_scrollbar.set)
        
        self.temp_canvas.pack(side="left", fill="both", expand=True)
        self.temp_scrollbar.pack(side="right", fill="y")
        
        self.temp_canvas.bind("<MouseWheel>", self._on_temp_mousewheel)
    
    def create_tab5_widgets(self):
        header = self.create_card(self.tab5)
        header.pack(fill=tk.X, padx=20, pady=(20, 10))
        
        tk.Label(header, text="Statistics & Reports", 
                font=self.get_font(16, True),
                bg=self.colors['bg_card'],
                fg=self.colors['text_primary']).pack(pady=15)
        
        stats_card = self.create_card(self.tab5)
        stats_card.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 10))
        
        stats_frame = tk.Frame(stats_card, bg=self.colors['bg_card'])
        stats_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        stats_data = [
            ("Folders deleted:", "folders_deleted", " items"),
            ("Shortcuts managed:", "shortcuts_deleted", " items"),
            ("Temp files deleted:", "temp_files_deleted", " items"),
            ("Files organized:", "files_organized", " items"),
            ("Space recovered:", "total_cleaned_size", ""),
            ("First use:", "first_use_date", ""),
            ("Last cleanup:", "last_cleanup_date", "")
        ]
        
        self.stats_labels = {}
        
        for i, (label, key, suffix) in enumerate(stats_data):
            frame = tk.Frame(stats_frame, bg=self.colors['bg_card'])
            frame.pack(fill=tk.X, pady=5)
            
            tk.Label(frame, text=label, font=("Segoe UI", 11),
                    bg=self.colors['bg_card'],
                    fg=self.colors['text_secondary'],
                    width=20, anchor="w").pack(side=tk.LEFT)
            
            if key == "total_cleaned_size":
                value = self.format_file_size(self.stats[key])
            else:
                value = self.stats[key] if self.stats[key] else "Never"
                if suffix:
                    value = f"{value}{suffix}"
            
            value_label = tk.Label(frame, text=value, 
                                  font=("Segoe UI", 11, "bold"),
                                  bg=self.colors['bg_card'],
                                  fg=self.colors['accent_green'])
            value_label.pack(side=tk.LEFT)
            self.stats_labels[key] = value_label
        
        button_frame = tk.Frame(stats_card, bg=self.colors['bg_card'])
        button_frame.pack(pady=15)
        
        self.create_button(button_frame, "Refresh Stats", 
                          self.refresh_stats_display, 'accent_green',
                          width=18, height=2).pack(side=tk.LEFT, padx=10)
        
        self.create_button(button_frame, "Reset Stats", 
                          self.reset_stats, 'accent_orange',
                          width=18, height=2).pack(side=tk.LEFT, padx=10)
        
        self.create_button(button_frame, "Export Report", 
                          self.export_report, 'accent_blue',
                          width=18, height=2).pack(side=tk.LEFT, padx=10)
        
        summary_card = self.create_card(self.tab5)
        summary_card.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        tk.Label(summary_card, text="Cleanup Summary", 
                font=("Segoe UI", 12, "bold"),
                bg=self.colors['bg_card'],
                fg=self.colors['text_primary']).pack(anchor=tk.W, padx=15, pady=10)
        
        self.summary_text = tk.Text(summary_card, height=6, 
                                   font=("Segoe UI", 10),
                                   bg=self.colors['bg_input'],
                                   fg=self.colors['text_primary'],
                                   insertbackground=self.colors['text_primary'],
                                   relief=tk.FLAT,
                                   wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(summary_card, orient=tk.VERTICAL, 
                                 command=self.summary_text.yview)
        self.summary_text.configure(yscrollcommand=scrollbar.set)
        
        self.summary_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, 
                              padx=15, pady=(0, 15))
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=(0, 15))
        
        self.update_summary()
    
    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def _on_shortcut_mousewheel(self, event):
        self.shortcut_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def _on_temp_mousewheel(self, event):
        self.temp_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def search_folders(self):
        self.update_status("Searching for folders...", 0)
        
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        self.checkbox_vars.clear()
        self.folders_to_delete = []
        
        try:
            items = os.listdir(self.desktop_path)
            total = len(items)
            
            for idx, item in enumerate(items):
                if idx % 10 == 0:
                    self.update_status(f"Scanning: {idx}/{total}", 
                                      (idx/total) * 100)
                
                item_path = os.path.join(self.desktop_path, item)
                if (os.path.isdir(item_path) and 
                    item.startswith("New folder") and 
                    not item.endswith(".lnk")):
                    
                    self.folders_to_delete.append(item_path)
                    
                    var = tk.BooleanVar(value=True)
                    self.checkbox_vars.append(var)
                    
                    item_frame = tk.Frame(self.scrollable_frame, 
                                         bg=self.colors['bg_card'])
                    item_frame.pack(fill="x", padx=5, pady=3)
                    
                    checkbox = tk.Checkbutton(item_frame, variable=var,
                                            bg=self.colors['bg_card'],
                                            fg=self.colors['accent_green'],
                                            selectcolor=self.colors['bg_input'],
                                            activebackground=self.colors['bg_card'])
                    checkbox.pack(side=tk.LEFT, padx=10)
                    
                    name_label = tk.Label(item_frame, text=item, 
                                         font=("Segoe UI", 10),
                                         bg=self.colors['bg_card'],
                                         fg=self.colors['text_primary'],
                                         width=30, anchor="w")
                    name_label.pack(side=tk.LEFT, padx=5)
                    
                    full_path = item_path
                    if len(full_path) > 45:
                        display_path = full_path[:42] + "..."
                    else:
                        display_path = full_path
                    
                    path_label = tk.Label(item_frame, text=display_path, 
                                         font=("Segoe UI", 9),
                                         fg=self.colors['text_secondary'],
                                         bg=self.colors['bg_card'],
                                         anchor="w")
                    path_label.pack(side=tk.LEFT, fill="x", expand=True, padx=5)
        
        except Exception as e:
            messagebox.showerror("Error", f"Cannot access Desktop: {e}")
        
        self.count_label.config(text=f"Found: {len(self.folders_to_delete)} folders")
        self.update_status("Ready", 100)
    
    def search_shortcuts(self):
        self.update_status("Searching for shortcuts...", 0)
        
        for widget in self.shortcut_scrollable_frame.winfo_children():
            widget.destroy()
        
        self.shortcut_checkbox_vars.clear()
        self.shortcuts_to_delete = []
        
        try:
            items = os.listdir(self.desktop_path)
            total = len(items)
            
            for idx, item in enumerate(items):
                if idx % 10 == 0:
                    self.update_status(f"Scanning: {idx}/{total}", 
                                      (idx/total) * 100)
                
                item_path = os.path.join(self.desktop_path, item)
                if os.path.isfile(item_path) and item.lower().endswith('.lnk'):
                    
                    self.shortcuts_to_delete.append(item_path)
                    
                    var = tk.BooleanVar(value=True)
                    self.shortcut_checkbox_vars.append(var)
                    
                    item_frame = tk.Frame(self.shortcut_scrollable_frame, 
                                         bg=self.colors['bg_card'])
                    item_frame.pack(fill="x", padx=5, pady=3)
                    
                    checkbox = tk.Checkbutton(item_frame, variable=var,
                                            bg=self.colors['bg_card'],
                                            fg=self.colors['accent_green'],
                                            selectcolor=self.colors['bg_input'],
                                            activebackground=self.colors['bg_card'])
                    checkbox.pack(side=tk.LEFT, padx=10)
                    
                    name_label = tk.Label(item_frame, text=item, 
                                         font=("Segoe UI", 10),
                                         bg=self.colors['bg_card'],
                                         fg=self.colors['text_primary'],
                                         width=40, anchor="w")
                    name_label.pack(side=tk.LEFT, padx=5)
                    
                    file_size = os.path.getsize(item_path)
                    size_text = self.format_file_size(file_size)
                    
                    size_label = tk.Label(item_frame, text=size_text, 
                                         font=("Segoe UI", 9),
                                         fg=self.colors['text_secondary'],
                                         bg=self.colors['bg_card'],
                                         width=15, anchor="w")
                    size_label.pack(side=tk.LEFT, padx=5)
                    
                    mtime = os.path.getmtime(item_path)
                    date_text = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M")
                    
                    date_label = tk.Label(item_frame, text=date_text, 
                                         font=("Segoe UI", 9),
                                         fg=self.colors['text_secondary'],
                                         bg=self.colors['bg_card'],
                                         width=20, anchor="w")
                    date_label.pack(side=tk.LEFT, padx=5)
        
        except Exception as e:
            messagebox.showerror("Error", f"Cannot access Desktop: {e}")
        
        self.shortcut_count_label.config(
            text=f"Found: {len(self.shortcuts_to_delete)} shortcuts")
        self.update_status("Ready", 100)
    
    def create_shortcut_folder(self):
        shortcut_folder = os.path.join(self.desktop_path, "SHORTCUT")
        if not os.path.exists(shortcut_folder):
            try:
                os.makedirs(shortcut_folder)
            except Exception as e:
                messagebox.showerror("Error", f"Cannot create SHORTCUT folder: {e}")
                return None
        return shortcut_folder
    
    def move_selected_shortcuts(self):
        selected_shortcuts = self.get_selected_shortcuts()
        
        if not selected_shortcuts:
            messagebox.showinfo("Info", "No shortcuts selected for moving")
            return
        
        shortcut_folder = self.create_shortcut_folder()
        if not shortcut_folder:
            return
        
        confirm = messagebox.askyesno("Confirm Move", 
                                     f"Move {len(selected_shortcuts)} shortcuts to SHORTCUT folder?")
        if not confirm:
            return
        
        self.update_status("Moving shortcuts...", 0)
        moved_count = 0
        errors = []
        total = len(selected_shortcuts)
        
        for idx, shortcut_path in enumerate(selected_shortcuts):
            self.update_status(f"Moving: {idx+1}/{total}", 
                              ((idx+1)/total) * 100)
            
            try:
                filename = os.path.basename(shortcut_path)
                target_path = os.path.join(shortcut_folder, filename)
                
                if os.path.exists(target_path):
                    name, ext = os.path.splitext(filename)
                    counter = 1
                    while os.path.exists(target_path):
                        new_filename = f"{name}_{counter}{ext}"
                        target_path = os.path.join(shortcut_folder, new_filename)
                        counter += 1
                
                shutil.move(shortcut_path, target_path)
                moved_count += 1
                
            except Exception as e:
                errors.append(f"{os.path.basename(shortcut_path)}: {e}")
        
        self.stats['shortcuts_deleted'] += moved_count
        self.stats['last_cleanup_date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.save_stats()
        
        self.search_shortcuts()
        self.refresh_stats_display()
        self.update_status("Ready", 100)
    
    def move_all_shortcuts(self):
        if not self.shortcuts_to_delete:
            messagebox.showinfo("Info", "No shortcuts found on Desktop")
            return
        
        shortcut_folder = self.create_shortcut_folder()
        if not shortcut_folder:
            return
        
        confirm = messagebox.askyesno("Confirm Move", 
                                     f"Move all {len(self.shortcuts_to_delete)} shortcuts?")
        if not confirm:
            return
        
        self.update_status("Moving all shortcuts...", 0)
        moved_count = 0
        errors = []
        total = len(self.shortcuts_to_delete)
        
        for idx, shortcut_path in enumerate(self.shortcuts_to_delete):
            self.update_status(f"Moving: {idx+1}/{total}", 
                              ((idx+1)/total) * 100)
            
            try:
                filename = os.path.basename(shortcut_path)
                target_path = os.path.join(shortcut_folder, filename)
                
                if os.path.exists(target_path):
                    name, ext = os.path.splitext(filename)
                    counter = 1
                    while os.path.exists(target_path):
                        new_filename = f"{name}_{counter}{ext}"
                        target_path = os.path.join(shortcut_folder, new_filename)
                        counter += 1
                
                shutil.move(shortcut_path, target_path)
                moved_count += 1
                
            except Exception as e:
                errors.append(f"{os.path.basename(shortcut_path)}: {e}")
        
        self.stats['shortcuts_deleted'] += moved_count
        self.stats['last_cleanup_date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.save_stats()
        
        self.search_shortcuts()
        self.refresh_stats_display()
        self.update_status("Ready", 100)
    
    def search_temp_files(self):
        self.update_status("Searching for temp files...", 0)
        
        for widget in self.temp_scrollable_frame.winfo_children():
            widget.destroy()
        
        self.temp_checkbox_vars.clear()
        self.temp_files_to_delete = []
        
        temp_extensions = [
            '.tmp', '.temp', '.log', '.cache', '.dmp', '.crash',
            '.chk', '.gid', '.old', '.bak', '~'
        ]
        
        total_size = 0
        
        try:
            items = os.listdir(self.desktop_path)
            total = len(items)
            
            for idx, item in enumerate(items):
                if idx % 10 == 0:
                    self.update_status(f"Scanning: {idx}/{total}", 
                                      (idx/total) * 100)
                
                item_path = os.path.join(self.desktop_path, item)
                if os.path.isfile(item_path):
                    _, ext = os.path.splitext(item)
                    is_temp_file = (
                        ext.lower() in temp_extensions or 
                        item.startswith('~') or
                        'temp' in item.lower() or
                        'cache' in item.lower()
                    )
                    
                    if is_temp_file:
                        file_size = os.path.getsize(item_path)
                        total_size += file_size
                        
                        self.temp_files_to_delete.append({
                            'path': item_path,
                            'size': file_size
                        })
                        
                        var = tk.BooleanVar(value=True)
                        self.temp_checkbox_vars.append(var)
                        
                        item_frame = tk.Frame(self.temp_scrollable_frame, 
                                             bg=self.colors['bg_card'])
                        item_frame.pack(fill="x", padx=5, pady=3)
                        
                        checkbox = tk.Checkbutton(item_frame, variable=var,
                                                bg=self.colors['bg_card'],
                                                fg=self.colors['danger'],
                                                selectcolor=self.colors['bg_input'],
                                                activebackground=self.colors['bg_card'])
                        checkbox.pack(side=tk.LEFT, padx=10)
                        
                        name_label = tk.Label(item_frame, text=item, 
                                             font=("Segoe UI", 10),
                                             bg=self.colors['bg_card'],
                                             fg=self.colors['text_primary'],
                                             width=35, anchor="w")
                        name_label.pack(side=tk.LEFT, padx=5)
                        
                        size_text = self.format_file_size(file_size)
                        size_label = tk.Label(item_frame, text=size_text, 
                                             font=("Segoe UI", 9),
                                             fg=self.colors['text_secondary'],
                                             bg=self.colors['bg_card'],
                                             width=10, anchor="w")
                        size_label.pack(side=tk.LEFT, padx=5)
                        
                        mtime = os.path.getmtime(item_path)
                        date_text = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d")
                        date_label = tk.Label(item_frame, text=date_text, 
                                             font=("Segoe UI", 9),
                                             fg=self.colors['text_secondary'],
                                             bg=self.colors['bg_card'],
                                             width=12, anchor="w")
                        date_label.pack(side=tk.LEFT, padx=5)
                        
                        type_label = tk.Label(item_frame, text="Temp file", 
                                             font=("Segoe UI", 9),
                                             fg=self.colors['danger'],
                                             bg=self.colors['bg_card'],
                                             width=10, anchor="w")
                        type_label.pack(side=tk.LEFT, padx=5)
        
        except Exception as e:
            messagebox.showerror("Error", f"Cannot access Desktop: {e}")
        
        size_text = self.format_file_size(total_size)
        self.temp_count_label.config(
            text=f"Found: {len(self.temp_files_to_delete)} temp files ({size_text})")
        self.update_status("Ready", 100)
    
    def get_selected_folders(self):
        selected_folders = []
        for i, var in enumerate(self.checkbox_vars):
            if var.get() and i < len(self.folders_to_delete):
                selected_folders.append(self.folders_to_delete[i])
        return selected_folders
    
    def get_selected_shortcuts(self):
        selected_shortcuts = []
        for i, var in enumerate(self.shortcut_checkbox_vars):
            if var.get() and i < len(self.shortcuts_to_delete):
                selected_shortcuts.append(self.shortcuts_to_delete[i])
        return selected_shortcuts
    
    def get_selected_temp_files(self):
        selected_files = []
        for i, var in enumerate(self.temp_checkbox_vars):
            if var.get() and i < len(self.temp_files_to_delete):
                selected_files.append(self.temp_files_to_delete[i])
        return selected_files
    
    def delete_selected_folders(self):
        selected_folders = self.get_selected_folders()
        
        if not selected_folders:
            messagebox.showinfo("Info", "No folders selected for deletion")
            return
        
        confirm = messagebox.askyesno("Confirm Delete", 
                                     f"Delete {len(selected_folders)} folders?")
        if not confirm:
            return
        
        self.update_status("Deleting folders...", 0)
        deleted_count = 0
        errors = []
        total = len(selected_folders)
        
        for idx, folder_path in enumerate(selected_folders):
            self.update_status(f"Deleting: {idx+1}/{total}", 
                              ((idx+1)/total) * 100)
            
            try:
                shutil.rmtree(folder_path)
                deleted_count += 1
            except Exception as e:
                errors.append(f"{os.path.basename(folder_path)}: {e}")
        
        self.stats['folders_deleted'] += deleted_count
        self.stats['last_cleanup_date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.save_stats()
        
        self.search_folders()
        self.refresh_stats_display()
        self.update_status("Ready", 100)
    
    def delete_selected_temp_files(self):
        selected_files = self.get_selected_temp_files()
        
        if not selected_files:
            messagebox.showinfo("Info", "No temp files selected for deletion")
            return
        
        total_size = sum(f['size'] for f in selected_files)
        confirm = messagebox.askyesno("Confirm Delete", 
                                     f"Delete {len(selected_files)} files ({self.format_file_size(total_size)})?")
        if not confirm:
            return
        
        self.update_status("Deleting temp files...", 0)
        deleted_count = 0
        deleted_size = 0
        errors = []
        total = len(selected_files)
        
        for idx, file_info in enumerate(selected_files):
            self.update_status(f"Deleting: {idx+1}/{total}", 
                              ((idx+1)/total) * 100)
            
            try:
                os.remove(file_info['path'])
                deleted_count += 1
                deleted_size += file_info['size']
            except Exception as e:
                errors.append(f"{os.path.basename(file_info['path'])}: {e}")
        
        self.stats['temp_files_deleted'] += deleted_count
        self.stats['total_cleaned_size'] += deleted_size
        self.stats['last_cleanup_date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.save_stats()
        
        self.search_temp_files()
        self.refresh_stats_display()
        self.update_status("Ready", 100)
    
    def delete_all_temp_files(self):
        if not self.temp_files_to_delete:
            messagebox.showinfo("Info", "No temp files found on Desktop")
            return
        
        total_size = sum(f['size'] for f in self.temp_files_to_delete)
        
        confirm = messagebox.askyesno("Confirm Delete", 
                                     f"Delete all {len(self.temp_files_to_delete)} temp files?\n\nWarning: This cannot be undone!")
        if not confirm:
            return
        
        self.update_status("Deleting all temp files...", 0)
        deleted_count = 0
        deleted_size = 0
        errors = []
        total = len(self.temp_files_to_delete)
        
        for idx, file_info in enumerate(self.temp_files_to_delete):
            self.update_status(f"Deleting: {idx+1}/{total}", 
                              ((idx+1)/total) * 100)
            
            try:
                os.remove(file_info['path'])
                deleted_count += 1
                deleted_size += file_info['size']
            except Exception as e:
                errors.append(f"{os.path.basename(file_info['path'])}: {e}")
        
        self.stats['temp_files_deleted'] += deleted_count
        self.stats['total_cleaned_size'] += deleted_size
        self.stats['last_cleanup_date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.save_stats()
        
        self.search_temp_files()
        self.refresh_stats_display()
        self.update_status("Ready", 100)
    
    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.current_folder_path.set(folder_selected)
            self.clear_tree()
    
    def scan_extensions(self):
        folder_path = self.current_folder_path.get()
        
        if not folder_path:
            messagebox.showwarning("Warning", "Please select a folder first")
            return
        
        if not os.path.exists(folder_path):
            messagebox.showerror("Error", "Selected folder does not exist")
            return
        
        self.update_status("Scanning extensions...", 0)
        self.extensions = {}
        self.clear_tree()
        
        try:
            items = os.listdir(folder_path)
            total = len(items)
            
            for idx, filename in enumerate(items):
                if idx % 10 == 0:
                    self.update_status(f"Scanning: {idx}/{total}", 
                                      (idx/total) * 100)
                
                file_path = os.path.join(folder_path, filename)
                if os.path.isfile(file_path):
                    _, ext = os.path.splitext(filename)
                    if ext:
                        ext = ext.lower()
                        if ext in self.extensions:
                            self.extensions[ext]["count"] += 1
                        else:
                            folder_name = ext[1:].upper()
                            folder_exists = os.path.exists(
                                os.path.join(folder_path, folder_name))
                            self.extensions[ext] = {
                                "count": 1,
                                "folder_exists": folder_exists
                            }
            
            for ext, data in self.extensions.items():
                folder_status = "Yes" if data["folder_exists"] else "No"
                self.tree.insert("", tk.END, values=(ext, data["count"], 
                                                     folder_status))
            
        except Exception as e:
            messagebox.showerror("Error", f"Error scanning files: {str(e)}")
        
        self.update_status("Ready", 100)
    
    def handle_duplicate_file(self, source_path, target_path):
        handling_method = self.duplicate_handling.get()
        
        if handling_method == "skip":
            return "skipped"
        
        elif handling_method == "overwrite":
            shutil.move(source_path, target_path)
            return "overwritten"
        
        elif handling_method == "keep_newest":
            source_mtime = os.path.getmtime(source_path)
            target_mtime = os.path.getmtime(target_path)
            
            if source_mtime > target_mtime:
                shutil.move(source_path, target_path)
                return "overwritten_newer"
            else:
                os.remove(source_path)
                return "deleted_older"
        
        return "unknown"
    
    def organize_files(self):
        if not self.extensions:
            messagebox.showwarning("Warning", "Please scan extensions first")
            return
        
        folder_path = self.current_folder_path.get()
        if not folder_path:
            messagebox.showwarning("Warning", "Please select a folder first")
            return
        
        confirm = messagebox.askyesno("Confirm Operation", 
                                     "Move all files to folders by extension?")
        if not confirm:
            return
        
        self.update_status("Organizing files...", 0)
        
        try:
            moved_files = 0
            skipped_files = 0
            overwritten_files = 0
            
            ext_list = list(self.extensions.items())
            total_exts = len(ext_list)
            
            for ext_idx, (ext, data) in enumerate(ext_list):
                self.update_status(f"Processing {ext}: {ext_idx+1}/{total_exts}", 
                                  ((ext_idx+1)/total_exts) * 100)
                
                folder_name = ext[1:].upper()
                target_folder = os.path.join(folder_path, folder_name)
                
                if not data["folder_exists"]:
                    os.makedirs(target_folder)
                
                for filename in os.listdir(folder_path):
                    file_path = os.path.join(folder_path, filename)
                    if os.path.isfile(file_path):
                        _, file_ext = os.path.splitext(filename)
                        if file_ext.lower() == ext:
                            target_path = os.path.join(target_folder, filename)
                            
                            if os.path.exists(target_path):
                                result = self.handle_duplicate_file(file_path, 
                                                                   target_path)
                                
                                if result == "skipped":
                                    skipped_files += 1
                                elif result in ["overwritten", "overwritten_newer"]:
                                    overwritten_files += 1
                                    moved_files += 1
                                elif result == "deleted_older":
                                    moved_files += 1
                            else:
                                try:
                                    shutil.move(file_path, target_folder)
                                    moved_files += 1
                                except Exception as e:
                                    print(f"Cannot move {filename}: {str(e)}")
            
            self.stats['files_organized'] += moved_files
            self.stats['last_cleanup_date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.save_stats()
            
            self.scan_extensions()
            self.refresh_stats_display()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error moving files: {str(e)}")
        
        self.update_status("Ready", 100)
    
    def clear_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
    
    def clear_data(self):
        self.current_folder_path.set(self.desktop_path)
        self.extensions = {}
        self.clear_tree()
    
    def format_file_size(self, size_bytes):
        if size_bytes == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        
        return f"{size_bytes:.1f} {size_names[i]}"
    
    def load_stats(self):
        try:
            stats_file = os.path.join(self.app_dir, "nexaclean_stats.json")
            if os.path.exists(stats_file):
                with open(stats_file, 'r', encoding='utf-8') as f:
                    saved_stats = json.load(f)
                    self.stats.update(saved_stats)
                    if 'theme' in saved_stats and saved_stats['theme'] in self.themes:
                        self.theme_var.set(saved_stats['theme'])
                        self.colors = self.themes[saved_stats['theme']]
        except Exception as e:
            print(f"Cannot load stats: {e}")
    
    def save_stats(self):
        try:
            stats_file = os.path.join(self.app_dir, "nexaclean_stats.json")
            self.stats['theme'] = self.theme_var.get()
            with open(stats_file, 'w', encoding='utf-8') as f:
                json.dump(self.stats, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Cannot save stats: {e}")
    
    def refresh_stats_display(self):
        stats_data = {
            'folders_deleted': f"{self.stats['folders_deleted']} items",
            'shortcuts_deleted': f"{self.stats['shortcuts_deleted']} items",
            'temp_files_deleted': f"{self.stats['temp_files_deleted']} items",
            'files_organized': f"{self.stats['files_organized']} items",
            'total_cleaned_size': self.format_file_size(
                self.stats['total_cleaned_size']),
            'first_use_date': self.stats['first_use_date'],
            'last_cleanup_date': self.stats['last_cleanup_date'] or "Never"
        }
        
        for key, value in stats_data.items():
            if key in self.stats_labels:
                self.stats_labels[key].config(text=value)
        
        self.update_summary()
    
    def reset_stats(self):
        confirm = messagebox.askyesno("Confirm Reset", 
                                     "Reset all statistics to defaults?")
        if not confirm:
            return
        
        self.stats = {
            'folders_deleted': 0,
            'shortcuts_deleted': 0,
            'temp_files_deleted': 0,
            'files_organized': 0,
            'total_cleaned_size': 0,
            'first_use_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'last_cleanup_date': None
        }
        
        self.save_stats()
        self.refresh_stats_display()
        messagebox.showinfo("Success", "Statistics reset successfully")
    
    def export_report(self):
        try:
            filename = f"NexaClean_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("=" * 50 + "\n")
                f.write("          NexaClean Report\n")
                f.write("=" * 50 + "\n\n")
                
                f.write(f"Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"First use: {self.stats['first_use_date']}\n")
                f.write(f"Last cleanup: {self.stats['last_cleanup_date'] or 'Never'}\n\n")
                
                f.write("Cleanup Statistics:\n")
                f.write("-" * 30 + "\n")
                f.write(f"Folders deleted: {self.stats['folders_deleted']} items\n")
                f.write(f"Shortcuts managed: {self.stats['shortcuts_deleted']} items\n")
                f.write(f"Temp files deleted: {self.stats['temp_files_deleted']} items\n")
                f.write(f"Files organized: {self.stats['files_organized']} items\n")
                f.write(f"Space recovered: {self.format_file_size(self.stats['total_cleaned_size'])}\n\n")
                
                f.write("Summary:\n")
                f.write("-" * 30 + "\n")
                f.write(self.generate_summary_text())
            
            messagebox.showinfo("Success", f"Report exported: {filename}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Cannot export report: {e}")
    
    def update_summary(self):
        summary_text = self.generate_summary_text()
        self.summary_text.delete(1.0, tk.END)
        self.summary_text.insert(1.0, summary_text)
    
    def generate_summary_text(self):
        total_items = (self.stats['folders_deleted'] + 
                      self.stats['shortcuts_deleted'] + 
                      self.stats['temp_files_deleted'])
        
        summary = f"Overall Cleanup Summary\n\n"
        summary += f"- Total items removed: {total_items}\n"
        summary += f"- Space recovered: {self.format_file_size(self.stats['total_cleaned_size'])}\n"
        summary += f"- Files organized: {self.stats['files_organized']}\n\n"
        
        if total_items == 0:
            summary += "Tip: Start cleaning using the tabs above"
        elif total_items < 10:
            summary += "Good job! Your Desktop is fairly clean"
        elif total_items < 50:
            summary += "Excellent! You've cleaned up a lot"
        else:
            summary += "Outstanding! You're a Desktop management pro"
        
        summary += f"\n\nLast updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        
        return summary

if __name__ == "__main__":
    root = tk.Tk()
    app = NexaClean(root)
    root.mainloop()
