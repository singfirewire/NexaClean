import os
import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import shutil
from datetime import datetime
import json
import logging

class NexaClean:
    def __init__(self, root):
        self.root = root
        self.root.title("NexaClean")
        self.root.geometry("800x700")
        self.root.resizable(False, False)
        
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
        self.create_widgets()
        self.search_folders()
    
    def create_widgets(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.tab1 = ttk.Frame(self.notebook)
        self.tab2 = ttk.Frame(self.notebook)
        self.tab3 = ttk.Frame(self.notebook)
        self.tab4 = ttk.Frame(self.notebook)
        self.tab5 = ttk.Frame(self.notebook)
        
        self.notebook.add(self.tab1, text="New Folder")
        self.notebook.add(self.tab2, text="Move to Folder")
        self.notebook.add(self.tab3, text="Manage Shortcuts")
        self.notebook.add(self.tab4, text="Clean Temp Files")
        self.notebook.add(self.tab5, text="Statistics")
        
        self.create_tab1_widgets()
        self.create_tab2_widgets()
        self.create_tab3_widgets()
        self.create_tab4_widgets()
        self.create_tab5_widgets()
        
        style = ttk.Style()
        style.configure("TNotebook.Tab", font=("Arial", 10, "bold"), padding=[10, 5])
    
    def create_tab1_widgets(self):
        title_label = tk.Label(self.tab1, text="Find and delete unnecessary 'New folder' on Desktop", 
                              font=("Arial", 14, "bold"))
        title_label.pack(pady=10)
        
        button_frame = tk.Frame(self.tab1)
        button_frame.pack(pady=10)
        
        self.search_btn = tk.Button(button_frame, text="Search Folders", 
                                   command=self.search_folders,
                                   bg="#4CAF50", fg="white", font=("Arial", 10, "bold"),
                                   width=15, height=2)
        self.search_btn.pack(side=tk.LEFT, padx=5)
        
        self.delete_btn = tk.Button(button_frame, text="Delete Selected", 
                                   command=self.delete_selected_folders,
                                   bg="#f44336", fg="white", font=("Arial", 10, "bold"),
                                   width=15, height=2)
        self.delete_btn.pack(side=tk.LEFT, padx=5)
        
        result_frame = tk.Frame(self.tab1)
        result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.count_label = tk.Label(result_frame, text="Found: 0 folders", 
                                   font=("Arial", 10, "bold"))
        self.count_label.pack(anchor=tk.W)
        
        self.canvas = tk.Canvas(result_frame, bg="white")
        self.scrollbar = ttk.Scrollbar(result_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        
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
        header_label = tk.Label(self.tab2, text="Organize Files by Extension", 
                               font=("Arial", 14, "bold"))
        header_label.pack(pady=10)
        
        folder_frame = tk.Frame(self.tab2)
        folder_frame.pack(pady=10, padx=20, fill=tk.X)
        
        tk.Label(folder_frame, text="Folder:", font=("Arial", 10)).pack(side=tk.LEFT)
        
        folder_entry = tk.Entry(folder_frame, textvariable=self.current_folder_path, 
                               width=50, font=("Arial", 9))
        folder_entry.pack(side=tk.LEFT, padx=5)
        
        browse_btn = tk.Button(folder_frame, text="Browse", command=self.browse_folder,
                              font=("Arial", 9))
        browse_btn.pack(side=tk.LEFT)
        
        duplicate_frame = tk.Frame(self.tab2)
        duplicate_frame.pack(pady=5, padx=20, fill=tk.X)
        
        tk.Label(duplicate_frame, text="Duplicate files:", font=("Arial", 10)).pack(side=tk.LEFT)
        
        tk.Radiobutton(duplicate_frame, text="Skip", variable=self.duplicate_handling, 
                      value="skip", font=("Arial", 9)).pack(side=tk.LEFT, padx=10)
        tk.Radiobutton(duplicate_frame, text="Overwrite", variable=self.duplicate_handling, 
                      value="overwrite", font=("Arial", 9)).pack(side=tk.LEFT, padx=10)
        tk.Radiobutton(duplicate_frame, text="Keep newest", variable=self.duplicate_handling, 
                      value="keep_newest", font=("Arial", 9)).pack(side=tk.LEFT, padx=10)
        
        button_frame = tk.Frame(self.tab2)
        button_frame.pack(pady=10)
        
        scan_btn = tk.Button(button_frame, text="Scan Extensions", 
                            command=self.scan_extensions, width=15, height=2,
                            font=("Arial", 10, "bold"), bg="#2196F3", fg="white")
        scan_btn.pack(side=tk.LEFT, padx=5)
        
        organize_btn = tk.Button(button_frame, text="Move by Extension", 
                                command=self.organize_files, width=15, height=2,
                                font=("Arial", 10, "bold"), bg="#4CAF50", fg="white")
        organize_btn.pack(side=tk.LEFT, padx=5)
        
        clear_btn = tk.Button(button_frame, text="Clear Data", 
                             command=self.clear_data, width=15, height=2,
                             font=("Arial", 10, "bold"), bg="#FF9800", fg="white")
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        self.tree_frame = tk.Frame(self.tab2)
        self.tree_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        columns = ("Extension", "File Count", "Folder Exists")
        self.tree = ttk.Treeview(self.tree_frame, columns=columns, show="headings", height=12)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        
        scrollbar = ttk.Scrollbar(self.tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def create_tab3_widgets(self):
        title_label = tk.Label(self.tab3, text="Manage and move Shortcuts (.lnk) from Desktop", 
                              font=("Arial", 14, "bold"))
        title_label.pack(pady=10)
        
        desc_label = tk.Label(self.tab3, 
                             text="Find and move Shortcuts to 'SHORTCUT' folder on Desktop",
                             font=("Arial", 10), fg="gray")
        desc_label.pack(pady=5)
        
        button_frame = tk.Frame(self.tab3)
        button_frame.pack(pady=10)
        
        self.search_shortcut_btn = tk.Button(button_frame, text="Search Shortcuts", 
                                           command=self.search_shortcuts,
                                           bg="#9C27B0", fg="white", font=("Arial", 10, "bold"),
                                           width=15, height=2)
        self.search_shortcut_btn.pack(side=tk.LEFT, padx=5)
        
        self.move_shortcut_btn = tk.Button(button_frame, text="Move Selected", 
                                         command=self.move_selected_shortcuts,
                                         bg="#4CAF50", fg="white", font=("Arial", 10, "bold"),
                                         width=15, height=2)
        self.move_shortcut_btn.pack(side=tk.LEFT, padx=5)
        
        self.move_all_shortcut_btn = tk.Button(button_frame, text="Move All", 
                                             command=self.move_all_shortcuts,
                                             bg="#2196F3", fg="white", font=("Arial", 10, "bold"),
                                             width=15, height=2)
        self.move_all_shortcut_btn.pack(side=tk.LEFT, padx=5)
        
        result_frame = tk.Frame(self.tab3)
        result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.shortcut_count_label = tk.Label(result_frame, text="Found: 0 shortcuts", 
                                           font=("Arial", 10, "bold"))
        self.shortcut_count_label.pack(anchor=tk.W)
        
        self.shortcut_canvas = tk.Canvas(result_frame, bg="white")
        self.shortcut_scrollbar = ttk.Scrollbar(result_frame, orient="vertical", command=self.shortcut_canvas.yview)
        self.shortcut_scrollable_frame = ttk.Frame(self.shortcut_canvas)
        
        self.shortcut_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.shortcut_canvas.configure(scrollregion=self.shortcut_canvas.bbox("all"))
        )
        
        self.shortcut_canvas.create_window((0, 0), window=self.shortcut_scrollable_frame, anchor="nw")
        self.shortcut_canvas.configure(yscrollcommand=self.shortcut_scrollbar.set)
        
        self.shortcut_canvas.pack(side="left", fill="both", expand=True)
        self.shortcut_scrollbar.pack(side="right", fill="y")
        
        self.shortcut_canvas.bind("<MouseWheel>", self._on_shortcut_mousewheel)
    
    def create_tab4_widgets(self):
        title_label = tk.Label(self.tab4, text="Clean Temp and Junk Files from Desktop", 
                              font=("Arial", 14, "bold"))
        title_label.pack(pady=10)
        
        desc_label = tk.Label(self.tab4, 
                             text="Find and delete temp files (.tmp, .temp, .log, .cache, ~)",
                             font=("Arial", 10), fg="gray")
        desc_label.pack(pady=5)
        
        button_frame = tk.Frame(self.tab4)
        button_frame.pack(pady=10)
        
        self.search_temp_btn = tk.Button(button_frame, text="Search Temp Files", 
                                       command=self.search_temp_files,
                                       bg="#FF9800", fg="white", font=("Arial", 10, "bold"),
                                       width=15, height=2)
        self.search_temp_btn.pack(side=tk.LEFT, padx=5)
        
        self.delete_temp_btn = tk.Button(button_frame, text="Delete Selected", 
                                       command=self.delete_selected_temp_files,
                                       bg="#f44336", fg="white", font=("Arial", 10, "bold"),
                                       width=15, height=2)
        self.delete_temp_btn.pack(side=tk.LEFT, padx=5)
        
        self.delete_all_temp_btn = tk.Button(button_frame, text="Delete All Temp", 
                                           command=self.delete_all_temp_files,
                                           bg="#E91E63", fg="white", font=("Arial", 10, "bold"),
                                           width=15, height=2)
        self.delete_all_temp_btn.pack(side=tk.LEFT, padx=5)
        
        result_frame = tk.Frame(self.tab4)
        result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.temp_count_label = tk.Label(result_frame, text="Found: 0 temp files (0 KB)", 
                                       font=("Arial", 10, "bold"))
        self.temp_count_label.pack(anchor=tk.W)
        
        self.temp_canvas = tk.Canvas(result_frame, bg="white")
        self.temp_scrollbar = ttk.Scrollbar(result_frame, orient="vertical", command=self.temp_canvas.yview)
        self.temp_scrollable_frame = ttk.Frame(self.temp_canvas)
        
        self.temp_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.temp_canvas.configure(scrollregion=self.temp_canvas.bbox("all"))
        )
        
        self.temp_canvas.create_window((0, 0), window=self.temp_scrollable_frame, anchor="nw")
        self.temp_canvas.configure(yscrollcommand=self.temp_scrollbar.set)
        
        self.temp_canvas.pack(side="left", fill="both", expand=True)
        self.temp_scrollbar.pack(side="right", fill="y")
        
        self.temp_canvas.bind("<MouseWheel>", self._on_temp_mousewheel)
    
    def create_tab5_widgets(self):
        title_label = tk.Label(self.tab5, text="Statistics and Reports", 
                              font=("Arial", 14, "bold"))
        title_label.pack(pady=10)
        
        stats_frame = tk.Frame(self.tab5)
        stats_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        cleanup_frame = tk.LabelFrame(stats_frame, text="Cleanup Statistics", 
                                    font=("Arial", 11, "bold"), padx=10, pady=10)
        cleanup_frame.pack(fill=tk.X, pady=5)
        
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
            frame = tk.Frame(cleanup_frame)
            frame.pack(fill=tk.X, pady=2)
            
            tk.Label(frame, text=label, font=("Arial", 10), width=20, anchor="w").pack(side=tk.LEFT)
            
            if key == "total_cleaned_size":
                value = self.format_file_size(self.stats[key])
            else:
                value = self.stats[key] if self.stats[key] else "Never"
                if suffix:
                    value = f"{value}{suffix}"
            
            value_label = tk.Label(frame, text=value, font=("Arial", 10, "bold"), fg="#2196F3")
            value_label.pack(side=tk.LEFT)
            self.stats_labels[key] = value_label
        
        button_frame = tk.Frame(stats_frame)
        button_frame.pack(pady=15)
        
        refresh_btn = tk.Button(button_frame, text="Refresh Stats", 
                              command=self.refresh_stats_display,
                              bg="#4CAF50", fg="white", font=("Arial", 10, "bold"),
                              width=15, height=2)
        refresh_btn.pack(side=tk.LEFT, padx=5)
        
        reset_btn = tk.Button(button_frame, text="Reset Stats", 
                            command=self.reset_stats,
                            bg="#FF9800", fg="white", font=("Arial", 10, "bold"),
                            width=15, height=2)
        reset_btn.pack(side=tk.LEFT, padx=5)
        
        export_btn = tk.Button(button_frame, text="Export Report", 
                             command=self.export_report,
                             bg="#2196F3", fg="white", font=("Arial", 10, "bold"),
                             width=15, height=2)
        export_btn.pack(side=tk.LEFT, padx=5)
        
        summary_frame = tk.LabelFrame(stats_frame, text="Cleanup Summary", 
                                    font=("Arial", 11, "bold"), padx=10, pady=10)
        summary_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.summary_text = tk.Text(summary_frame, height=6, font=("Arial", 9), wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(summary_frame, orient=tk.VERTICAL, command=self.summary_text.yview)
        self.summary_text.configure(yscrollcommand=scrollbar.set)
        
        self.summary_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.update_summary()
    
    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def _on_shortcut_mousewheel(self, event):
        self.shortcut_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def _on_temp_mousewheel(self, event):
        self.temp_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def search_folders(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        self.checkbox_vars.clear()
        self.folders_to_delete = []
        
        try:
            for item in os.listdir(self.desktop_path):
                item_path = os.path.join(self.desktop_path, item)
                if (os.path.isdir(item_path) and 
                    item.startswith("New folder") and 
                    not item.endswith(".lnk")):
                    
                    self.folders_to_delete.append(item_path)
                    
                    var = tk.BooleanVar(value=True)
                    self.checkbox_vars.append(var)
                    
                    item_frame = tk.Frame(self.scrollable_frame, bg="white")
                    item_frame.pack(fill="x", padx=5, pady=2)
                    
                    checkbox = tk.Checkbutton(item_frame, variable=var, bg="white")
                    checkbox.pack(side=tk.LEFT, padx=5)
                    
                    name_label = tk.Label(item_frame, text=item, 
                                         font=("Arial", 9), bg="white",
                                         width=30, anchor="w")
                    name_label.pack(side=tk.LEFT, padx=5)
                    
                    full_path = item_path
                    if len(full_path) > 40:
                        display_path = full_path[:37] + "..."
                    else:
                        display_path = full_path
                    
                    path_label = tk.Label(item_frame, text=display_path, 
                                         font=("Arial", 8), fg="gray", bg="white",
                                         anchor="w")
                    path_label.pack(side=tk.LEFT, fill="x", expand=True, padx=5)
        
        except Exception as e:
            messagebox.showerror("Error", f"Cannot access Desktop: {e}")
        
        self.count_label.config(text=f"Found: {len(self.folders_to_delete)} folders")
    
    def search_shortcuts(self):
        for widget in self.shortcut_scrollable_frame.winfo_children():
            widget.destroy()
        
        self.shortcut_checkbox_vars.clear()
        self.shortcuts_to_delete = []
        
        try:
            for item in os.listdir(self.desktop_path):
                item_path = os.path.join(self.desktop_path, item)
                if os.path.isfile(item_path) and item.lower().endswith('.lnk'):
                    
                    self.shortcuts_to_delete.append(item_path)
                    
                    var = tk.BooleanVar(value=True)
                    self.shortcut_checkbox_vars.append(var)
                    
                    item_frame = tk.Frame(self.shortcut_scrollable_frame, bg="white")
                    item_frame.pack(fill="x", padx=5, pady=2)
                    
                    checkbox = tk.Checkbutton(item_frame, variable=var, bg="white")
                    checkbox.pack(side=tk.LEFT, padx=5)
                    
                    name_label = tk.Label(item_frame, text=item, 
                                         font=("Arial", 9), bg="white",
                                         width=40, anchor="w")
                    name_label.pack(side=tk.LEFT, padx=5)
                    
                    file_size = os.path.getsize(item_path)
                    size_text = self.format_file_size(file_size)
                    
                    size_label = tk.Label(item_frame, text=size_text, 
                                         font=("Arial", 8), fg="gray", bg="white",
                                         width=15, anchor="w")
                    size_label.pack(side=tk.LEFT, padx=5)
                    
                    mtime = os.path.getmtime(item_path)
                    date_text = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M")
                    
                    date_label = tk.Label(item_frame, text=date_text, 
                                         font=("Arial", 8), fg="gray", bg="white",
                                         width=20, anchor="w")
                    date_label.pack(side=tk.LEFT, padx=5)
        
        except Exception as e:
            messagebox.showerror("Error", f"Cannot access Desktop: {e}")
        
        self.shortcut_count_label.config(text=f"Found: {len(self.shortcuts_to_delete)} shortcuts")
    
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
                                     f"Move {len(selected_shortcuts)} selected shortcuts to SHORTCUT folder?")
        if not confirm:
            return
        
        moved_count = 0
        errors = []
        
        for shortcut_path in selected_shortcuts:
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
    
    def move_all_shortcuts(self):
        if not self.shortcuts_to_delete:
            messagebox.showinfo("Info", "No shortcuts found on Desktop")
            return
        
        shortcut_folder = self.create_shortcut_folder()
        if not shortcut_folder:
            return
        
        confirm = messagebox.askyesno("Confirm Move", 
                                     f"Move all {len(self.shortcuts_to_delete)} shortcuts to SHORTCUT folder?")
        if not confirm:
            return
        
        moved_count = 0
        errors = []
        
        for shortcut_path in self.shortcuts_to_delete:
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
    
    def search_temp_files(self):
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
            for item in os.listdir(self.desktop_path):
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
                        
                        item_frame = tk.Frame(self.temp_scrollable_frame, bg="white")
                        item_frame.pack(fill="x", padx=5, pady=2)
                        
                        checkbox = tk.Checkbutton(item_frame, variable=var, bg="white")
                        checkbox.pack(side=tk.LEFT, padx=5)
                        
                        name_label = tk.Label(item_frame, text=item, 
                                             font=("Arial", 9), bg="white",
                                             width=35, anchor="w")
                        name_label.pack(side=tk.LEFT, padx=5)
                        
                        size_text = self.format_file_size(file_size)
                        size_label = tk.Label(item_frame, text=size_text, 
                                             font=("Arial", 8), fg="gray", bg="white",
                                             width=10, anchor="w")
                        size_label.pack(side=tk.LEFT, padx=5)
                        
                        mtime = os.path.getmtime(item_path)
                        date_text = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d")
                        date_label = tk.Label(item_frame, text=date_text, 
                                             font=("Arial", 8), fg="gray", bg="white",
                                             width=12, anchor="w")
                        date_label.pack(side=tk.LEFT, padx=5)
                        
                        type_label = tk.Label(item_frame, text="Temp file", 
                                             font=("Arial", 8), fg="red", bg="white",
                                             width=10, anchor="w")
                        type_label.pack(side=tk.LEFT, padx=5)
        
        except Exception as e:
            messagebox.showerror("Error", f"Cannot access Desktop: {e}")
        
        size_text = self.format_file_size(total_size)
        self.temp_count_label.config(text=f"Found: {len(self.temp_files_to_delete)} temp files ({size_text})")
    
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
                                     f"Delete {len(selected_folders)} selected folders?")
        if not confirm:
            return
        
        deleted_count = 0
        errors = []
        
        for folder_path in selected_folders:
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
    
    def delete_selected_temp_files(self):
        selected_files = self.get_selected_temp_files()
        
        if not selected_files:
            messagebox.showinfo("Info", "No temp files selected for deletion")
            return
        
        total_size = sum(f['size'] for f in selected_files)
        confirm = messagebox.askyesno("Confirm Delete", 
                                     f"Delete {len(selected_files)} selected temp files ({self.format_file_size(total_size)})?")
        if not confirm:
            return
        
        deleted_count = 0
        deleted_size = 0
        errors = []
        
        for file_info in selected_files:
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
    
    def delete_all_temp_files(self):
        if not self.temp_files_to_delete:
            messagebox.showinfo("Info", "No temp files found on Desktop")
            return
        
        total_size = sum(f['size'] for f in self.temp_files_to_delete)
        
        confirm = messagebox.askyesno("Confirm Delete", 
                                     f"Delete all {len(self.temp_files_to_delete)} temp files ({self.format_file_size(total_size)})?\n\nWarning: This cannot be undone!")
        if not confirm:
            return
        
        deleted_count = 0
        deleted_size = 0
        errors = []
        
        for file_info in self.temp_files_to_delete:
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
        
        self.extensions = {}
        self.clear_tree()
        
        try:
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                if os.path.isfile(file_path):
                    _, ext = os.path.splitext(filename)
                    if ext:
                        ext = ext.lower()
                        if ext in self.extensions:
                            self.extensions[ext]["count"] += 1
                        else:
                            folder_name = ext[1:].upper()
                            folder_exists = os.path.exists(os.path.join(folder_path, folder_name))
                            self.extensions[ext] = {
                                "count": 1,
                                "folder_exists": folder_exists
                            }
            
            for ext, data in self.extensions.items():
                folder_status = "Yes" if data["folder_exists"] else "No"
                self.tree.insert("", tk.END, values=(ext, data["count"], folder_status))
            
        except Exception as e:
            messagebox.showerror("Error", f"Error scanning files: {str(e)}")
    
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
        
        try:
            moved_files = 0
            skipped_files = 0
            overwritten_files = 0
            
            for ext, data in self.extensions.items():
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
                                result = self.handle_duplicate_file(file_path, target_path)
                                
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
            stats_file = "nexaclean_stats.json"
            if os.path.exists(stats_file):
                with open(stats_file, 'r', encoding='utf-8') as f:
                    saved_stats = json.load(f)
                    self.stats.update(saved_stats)
        except Exception as e:
            print(f"Cannot load stats: {e}")
    
    def save_stats(self):
        try:
            stats_file = "nexaclean_stats.json"
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
            'total_cleaned_size': self.format_file_size(self.stats['total_cleaned_size']),
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
            
            messagebox.showinfo("Success", f"Report exported successfully: {filename}")
            
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
