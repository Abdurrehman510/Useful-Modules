```markdown
# Python Utility Scripts 🐍

**A collection of powerful Python scripts to automate everyday tasks and boost productivity.**

[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

## 🚀 Introduction

This repository hosts a curated set of Python scripts designed to simplify common workflows. Whether you need to analyze disk usage, generate QR codes, organize cluttered directories, or automate other routine tasks, these scripts have you covered. Perfect for developers, sysadmins, and productivity enthusiasts!

## ✨ Features

### Core Scripts
- **📂 Storage Finder**  
  Recursively calculate folder size with human-readable output (MB/GB/TB).
- **🔳 QR Code Generator**  
  Generate customizable QR codes in PNG/SVG format with size and color options.
- **🗂 File Organizer**  
  Automatically sort files into category-based folders (Documents, Images, Videos, etc.).

### Additional Utilities
- **🌐 URL Shortener** _(coming soon)_  
- **📷 Image Converter** _(coming soon)_  
- **🔒 File Encryptor** _(coming soon)_

## ⚙️ Installation

### Prerequisites
- Python 3.6 or higher
- `pip` package manager

### Steps
1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/python-utility-scripts.git
   cd python-utility-scripts
   ```

2. **(Optional) Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/MacOS
   venv\Scripts\activate    # Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## 🛠 Usage

### General Syntax
```bash
python script_name.py [arguments] [options]
```

### Script Examples

#### 1. **Storage Finder**  
Calculate the size of a folder and its subdirectories:
```bash
python storage_finder.py /path/to/folder
```
**Options**:
- `--unit [B/KB/MB/GB]`: Specify output unit (default: auto-detected)
- `--exclude-hidden`: Ignore hidden files and directories

#### 2. **QR Code Generator**  
Generate a QR code for a URL and save as PNG:
```bash
python qr_code_generator.py "https://example.com" --output example_qr.png --size 10 --color blue
```
**Options**:
- `--output <filename>`: Output file name (supports .png/.svg)
- `--size <int>`: QR code pixel size per module (default: 10)
- `--color <color_name>`: QR code color (default: black)

#### 3. **File Organizer**  
Organize files in the `Downloads` folder:
```bash
python file_organizer.py ~/Downloads --dry-run
```
**Options**:
- `--dry-run`: Preview changes without moving files
- `--log`: Generate a log file of moved items

**Supported File Categories**:
| Category    | File Extensions                          |
|-------------|------------------------------------------|
| Documents   | .pdf, .docx, .txt, .md, .xlsx           |
| Images      | .jpg, .png, .gif, .svg, .bmp            |
| Videos      | .mp4, .avi, .mov, .mkv, .flv            |
| Audio       | .mp3, .wav, .ogg, .flac                 |
| Archives    | .zip, .rar, .7z, .tar.gz                |
| Code        | .py, .js, .html, .css, .json            |

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch:
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. Commit your changes:
   ```bash
   git commit -m 'Add some amazing feature'
   ```
4. Push to the branch:
   ```bash
   git push origin feature/amazing-feature
   ```
5. Open a Pull Request

## 📜 License

Distributed under the MIT License. See [LICENSE](LICENSE) for details.

## 💬 Support

Reach out for help or feedback:
- [Open an Issue](https://github.com/your-username/python-utility-scripts/issues)
- ✉️ Email: your-email@example.com

---

**Happy Coding!** 🎉
```
