Python Utility Scripts 🐍
A collection of powerful Python scripts to automate everyday tasks and boost productivity.

Python Version
License: MIT
PRs Welcome

🚀 Introduction
This repository hosts a curated set of Python scripts designed to simplify common workflows. Whether you need to analyze disk usage, generate QR codes, organize cluttered directories, or automate other routine tasks, these scripts have you covered. Perfect for developers, sysadmins, and productivity enthusiasts!

✨ Features
Core Scripts
📂 Storage Finder
Recursively calculate folder size with human-readable output (MB/GB/TB).

🔳 QR Code Generator
Generate customizable QR codes in PNG/SVG format with size and color options.

🗂 File Organizer
Automatically sort files into category-based folders (Documents, Images, Videos, etc.).

Additional Utilities
🌐 URL Shortener (coming soon)

📷 Image Converter (coming soon)

🔒 File Encryptor (coming soon)

⚙️ Installation
Prerequisites
Python 3.6 or higher

pip package manager

Steps
Clone the repository:

bash
git clone https://github.com/your-username/python-utility-scripts.git
cd python-utility-scripts
(Optional) Create a virtual environment:

bash
python -m venv venv
source venv/bin/activate  # Linux/MacOS
venv\Scripts\activate    # Windows
Install dependencies:

bash
pip install -r requirements.txt
🛠 Usage
General Syntax
bash
python script_name.py [arguments] [options]
Script Examples
1. Storage Finder
Calculate the size of a folder and its subdirectories:

bash
python storage_finder.py /path/to/folder
Options:

--unit [B/KB/MB/GB]: Specify output unit (default: auto-detected).

--exclude-hidden: Ignore hidden files and directories.

2. QR Code Generator
Generate a QR code for a URL and save as PNG:

bash
python qr_code_generator.py "https://example.com" --output example_qr.png --size 10 --color blue
Options:

--output <filename>: Output file name (supports .png/.svg).

--size <int>: QR code pixel size per module (default: 10).

--color <color_name>: QR code color (default: black).

3. File Organizer
Organize files in the Downloads folder:

bash
python file_organizer.py ~/Downloads --dry-run
Options:

--dry-run: Preview changes without moving files.

--log: Generate a log file of moved items.

📚 Scripts Overview
storage_finder.py
Description: Recursively scans directories to calculate total storage usage.

Dependencies: os, sys, humanize

qr_code_generator.py
Description: Generates QR codes with customizable size, color, and format.

Dependencies: qrcode, Pillow

file_organizer.py
Description: Organizes files into predefined categories (e.g., .pdf → Documents).
Supported Categories:

📁 Documents: PDF, DOCX, TXT

🖼 Images: JPG, PNG, GIF

🎥 Videos: MP4, AVI, MOV

🎵 Audio: MP3, WAV

📦 Archives: ZIP, RAR

🤝 Contributing
We welcome contributions! Please follow these steps:

Read our Contributing Guidelines.

Fork the repository and create a feature branch.

Ensure your code passes all tests (add tests if applicable).

Submit a Pull Request with a detailed description of changes.

Got an idea for a script?
Open an issue using the Feature Request Template.

📜 License
Distributed under the MIT License. See LICENSE for details.

💬 Support
Reach out for help or feedback:

Open an Issue

✉️ Email: your-email@example.com

Happy Coding! 🎉

