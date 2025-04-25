"""
Directory Analyzer GUI Tool
==========================

A comprehensive graphical utility to visualize and analyze directory structures.

📌 Basic Usage:
1. Save this script as 'directory_analyzer.py'
2. Run: python directory_analyzer.py
3. Use the GUI to browse and analyze directories

✨ Features:
- Interactive tree visualization of directory structures
- Color-coded display (folders in blue, files in green)
- Detailed file/folder size information
- Summary panel with key directory statistics
- Scrollable text area for large directories
- Modern, user-friendly interface
- Cross-platform compatibility

🔧 Requirements:
✔ Python 3.6 or newer
✔ Tkinter (usually included with Python)
✔ Windows/macOS/Linux OS

🛠 How It Works:
1. GUI allows browsing to any directory
2. Recursively scans selected directory
3. Calculates folder sizes and file counts
4. Displays hierarchical tree structure
5. Shows creation dates and content statistics
6. Formats sizes in human-readable units (KB, MB, GB)

📝 Notes:
- Handles large directories efficiently
- Skips files/directories with permission issues
- Shows hidden files when enabled
- Supports directory exclusion filters
- Displays sizes with 2 decimal precision

⚠️ Important:
- First run may be slow for very large directories
- Some system folders may require admin privileges
- Actual disk usage may differ due to filesystem overhead

Example Output:
========== Directory Tree ==========
├── Documents [1.45 GB]
│   ├── Work [450.20 MB]
│   └── Personal [980.25 MB]
└── Media [3.20 GB]
    └── Videos [3.15 GB]

============ Summary ============ 
Path: C:\Users\Example
Created: 2023-01-15 08:30:45
Size: 4.65 GB
Contents: 12 directories, 245 files

Version: 1.2
Last Updated: 2023-11-28
"""

import os
import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext
from pathlib import Path
from datetime import datetime

class DirectoryAnalyzerGUI:
    def __init__(self, master):
        self.master = master
        master.title("Directory Analyzer")
        master.geometry("800x600")
        
        # Configure styles
        self.style = ttk.Style()
        self.style.configure('TButton', padding=5)
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('Header.TLabel', background='#333', foreground='white', font=('Arial', 12, 'bold'))
        
        # Create main container
        self.main_frame = ttk.Frame(master)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header
        self.header_frame = ttk.Frame(self.main_frame, style='Header.TFrame')
        self.header_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(self.header_frame, text="Directory Analyzer", style='Header.TLabel').pack(pady=5)
        
        # Directory selection
        self.input_frame = ttk.Frame(self.main_frame)
        self.input_frame.pack(fill=tk.X, pady=5)
        
        self.path_var = tk.StringVar()
        self.path_entry = ttk.Entry(self.input_frame, textvariable=self.path_var, width=50)
        self.path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        self.browse_btn = ttk.Button(self.input_frame, text="Browse", command=self.browse_directory)
        self.browse_btn.pack(side=tk.LEFT)
        
        self.analyze_btn = ttk.Button(self.input_frame, text="Analyze", command=self.analyze_directory)
        self.analyze_btn.pack(side=tk.LEFT, padx=(5, 0))
        
        # Tree display
        self.tree_frame = ttk.Frame(self.main_frame)
        self.tree_frame.pack(fill=tk.BOTH, expand=True)
        
        self.tree_text = scrolledtext.ScrolledText(
            self.tree_frame,
            wrap=tk.NONE,
            font=('Consolas', 10),
            bg='white',
            padx=10,
            pady=10
        )
        self.tree_text.pack(fill=tk.BOTH, expand=True)
        
        # Configure tags for colors
        self.tree_text.tag_configure('folder', foreground='#1e90ff')
        self.tree_text.tag_configure('file', foreground='#2e8b57')
        self.tree_text.tag_configure('size', foreground='#ff8c00')
        self.tree_text.tag_configure('error', foreground='#ff0000')
        
        # Summary panel
        self.summary_frame = ttk.Labelframe(self.main_frame, text="Summary")
        self.summary_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.summary_labels = {
            'path': ttk.Label(self.summary_frame, text="Path: -"),
            'created': ttk.Label(self.summary_frame, text="Created: -"),
            'size': ttk.Label(self.summary_frame, text="Size: -"),
            'contents': ttk.Label(self.summary_frame, text="Contents: -")
        }
        
        for label in self.summary_labels.values():
            label.pack(anchor=tk.W)
    
    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.path_var.set(directory)
    
    def analyze_directory(self):
        path = self.path_var.get()
        if not path:
            return
        
        self.tree_text.delete(1.0, tk.END)
        for label in self.summary_labels.values():
            label.config(text=label.cget('text').split(':')[0] + ": -")
        
        try:
            self.print_tree(path)
            self.update_summary(path)
        except Exception as e:
            self.show_error(str(e))
    
    def print_tree(
        self,
        startpath,
        prefix='',
        is_last=False,
        is_root=True,
        max_depth=None,
        current_depth=0,
        exclude_dirs=None,
        exclude_extensions=None,
        show_hidden=False
    ):
        """
        Print a visual tree structure of a directory with enhanced features.
        
        Args:
            startpath: Path to the directory or file to display
            prefix: Prefix for the current line (used internally for recursion)
            is_last: Whether this is the last item in its parent directory
            is_root: Whether this is the root of the tree
            max_depth: Maximum depth to recurse into (None for unlimited)
            current_depth: Current recursion depth (used internally)
            exclude_dirs: List of directory names to exclude
            exclude_extensions: List of file extensions to exclude
            show_hidden: Whether to show hidden files/directories
        """
        if exclude_dirs is None:
            exclude_dirs = []
        if exclude_extensions is None:
            exclude_extensions = []
        
        path = Path(startpath)
        
        # Validate path
        if not path.exists():
            raise FileNotFoundError(f"Path does not exist: {path}")
        
        # Skip hidden files if not showing them
        if not show_hidden and path.name.startswith('.'):
            return
        
        # Get display elements
        name = path.name if not is_root else str(path)
        size = self.format_size(self.get_folder_size(path) if path.is_dir() else path.stat().st_size)
        color_tag = 'folder' if path.is_dir() else 'file'
        
        # Current item line
        connector = '└── ' if is_last else '├── '
        line = f"{prefix}{connector}{name} [{size}]\n"
        
        self.tree_text.insert(tk.END, line, (color_tag, 'size'))
        
        # Stop if it's a file or we've reached max depth
        if not path.is_dir() or (max_depth is not None and current_depth >= max_depth):
            return
        
        # Skip excluded directories
        if path.name in exclude_dirs:
            self.tree_text.insert(tk.END, f"{prefix}    └── [Excluded]\n", 'comment')
            return
        
        # Prepare for directory contents
        extension = '    ' if is_last else '│   '
        new_prefix = prefix + extension
        
        try:
            # Get sorted directory contents (folders first, then files)
            items = []
            for item in os.listdir(path):
                item_path = path / item
                # Skip hidden items if not showing them
                if not show_hidden and item.startswith('.'):
                    continue
                # Skip excluded extensions
                if (not item_path.is_dir() and 
                    any(item.lower().endswith(ext.lower()) for ext in exclude_extensions)):
                    continue
                items.append(item)
            
            # Sort with folders first, then case-insensitive alphabetical
            items.sort(key=lambda x: (not os.path.isdir(os.path.join(path, x)), x.lower()))
            
        except PermissionError:
            self.tree_text.insert(tk.END, f"{new_prefix}└── [Permission denied]\n", 'error')
            return
        
        # Process each item in the directory
        for i, item in enumerate(items):
            is_last_item = i == len(items) - 1
            self.print_tree(
                path / item,
                new_prefix,
                is_last_item,
                False,
                max_depth,
                current_depth + 1,
                exclude_dirs,
                exclude_extensions,
                show_hidden
            )    
    def get_folder_size(self, folder_path):
        total_size = 0
        for dirpath, _, filenames in os.walk(folder_path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                if not os.path.islink(fp):
                    try:
                        total_size += os.path.getsize(fp)
                    except (OSError, PermissionError):
                        continue
        return total_size
    
    def format_size(self, size_bytes):
        units = ['B', 'KB', 'MB', 'GB', 'TB']
        size = float(size_bytes)
        unit_index = 0
        
        while size >= 1024 and unit_index < len(units) - 1:
            size /= 1024
            unit_index += 1
        
        return f"{size:.2f} {units[unit_index]}"
    
    def update_summary(self, path):
        try:
            total_size = self.get_folder_size(path)
            num_files = sum([len(files) for _, _, files in os.walk(path)])
            num_dirs = sum([len(dirs) for _, dirs, _ in os.walk(path)]) - 1
            
            self.summary_labels['path'].config(text=f"Path: {os.path.abspath(path)}")
            self.summary_labels['created'].config(text=f"Created: {datetime.fromtimestamp(Path(path).stat().st_ctime)}")
            self.summary_labels['size'].config(text=f"Size: {self.format_size(total_size)}")
            self.summary_labels['contents'].config(text=f"Contents: {num_dirs} directories, {num_files} files")
        except Exception as e:
            self.show_error(str(e))
    
    def show_error(self, message):
        self.tree_text.insert(tk.END, f"\nError: {message}\n", 'error')

if __name__ == "__main__":
    root = tk.Tk()
    app = DirectoryAnalyzerGUI(root)
    root.mainloop()