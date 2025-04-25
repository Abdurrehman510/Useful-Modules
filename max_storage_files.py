"""
File Size Analyzer Tool
=======================

A lightweight Python utility to identify largest files on your storage drives.

📌 Basic Usage:
1. Save this script as 'file_size_analyzer.py'
2. Run: python file_size_analyzer.py
3. For custom directory: Modify the path in search_directory() call

✨ Features:
- Scans entire directory trees recursively
- Identifies top 25 largest files by default
- Efficient memory usage with min-heap algorithm
- Handles permission errors gracefully
- Displays results in clean MB format
- Outputs top 15 files by default in ranked order

🔧 Requirements:
✔ Windows/macOS/Linux
✔ Python 3.6 or newer
✔ Standard OS permissions (admin not required)

🛠 How It Works:
1. Walks through all files in specified directory
2. Tracks file sizes using efficient heap structure
3. Maintains only top files in memory
4. Sorts final results by size (descending)
5. Presents clean formatted output

📝 Notes:
- Default scans D:\ drive (modify as needed)
- Files with access restrictions are skipped
- Actual disk space may differ due to allocation units
- Network drives supported but may be slow

⚠️ Important:
Scanning large directories may take time - be patient!

Example Output:
============ TOP LARGE FILES (D:\) ============
 1. 2458 MB
    D:\Videos\vacation_4k.mp4
 2. 1872 MB
    D:\Backups\system_image.bak
===============================================

Version: 1.0
Last Updated: 2023-11-20
"""

import os
import heapq

MAX_TOP_FILES = 25

# Min-heap to store top files by size
top_files = []

def update_top_files(path, size):
    if len(top_files) < MAX_TOP_FILES:
        heapq.heappush(top_files, (size, path))
    else:
        if size > top_files[0][0]:  # Replace the smallest
            heapq.heappushpop(top_files, (size, path))

def search_directory(directory):
    try:
        for root, dirs, files in os.walk(directory):
            for file in files:
                full_path = os.path.join(root, file)
                try:
                    size = os.path.getsize(full_path)
                    update_top_files(full_path, size)
                except Exception:
                    pass  # Skip unreadable files
    except Exception:
        pass  # Skip directories with permission issues

if __name__ == "__main__":
    search_directory("C:\\")

    # Sort files in descending order by size
    top_files_sorted = sorted(top_files, reverse=True)

    print("Top 15 Largest Files in C:\\ Drive:")
    print("===================================")
    for i, (size, path) in enumerate(top_files_sorted, 1):
        print(f"{i:2d}. {size // (1024 * 1024)} MB\n    {path}\n")
