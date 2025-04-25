"""
Python Modules Analyzer Tool
===========================

A powerful utility to inspect installed Python packages and their memory usage.

📌 Basic Usage:
1. Save this script as 'module_analyzer.py'
2. Run: python module_analyzer.py
3. View the sorted table of top 20 memory-consuming modules

✨ Features:
- Lists all installed Python packages with versions
- Calculates memory usage per module
- Identifies primary dependencies
- Sorts modules by memory consumption (descending)
- Colorful tabular output with fancy formatting
- Shows total Python process memory usage
- Lightweight and fast execution

🔧 Requirements:
✔ Python 3.8 or newer
✔ psutil package (pip install psutil)
✔ tabulate package (pip install tabulate)
✔ Standard OS permissions

🛠 How It Works:
1. Scans all loaded Python modules in memory
2. Calculates file sizes for each module
3. Collects package metadata from pip
4. Identifies primary dependencies
5. Generates a sorted memory usage report
6. Displays results in an easy-to-read table

📝 Notes:
- Only shows top 20 modules by default
- Memory values are approximate
- Some system modules may not report sizes
- Dependency shows first listed requirement
- Virtual environment modules are included

⚠️ Important:
- Requires third-party packages (psutil, tabulate)
- Memory usage includes both direct and indirect module loads
- Runtime memory may differ from file sizes

Example Output:
============ PYTHON MODULES INFORMATION ============
╒══════════════╤═══════════╤══════════╤═══════════════╕
│ Module       │ Version   │ Memory   │ Dependency    │
╞══════════════╪═══════════╪══════════╪═══════════════╡
│ numpy        │ 1.21.0    │ 15.23 MB │ packaging     │
│ pandas       │ 1.3.0     │ 12.45 MB │ numpy         │
╘══════════════╧═══════════╧══════════╧═══════════════╛

Total Python Process Memory: 145.67 MB
Estimated Modules Memory: 98.32 MB

Version: 1.0
Last Updated: 2023-11-25
"""

import sys
import os
import psutil
from tabulate import tabulate
from importlib.metadata import distributions, requires
from collections import defaultdict

def get_python_modules_info():
    # Get process memory
    process = psutil.Process(os.getpid())
    
    # Get all installed packages
    modules_info = []
    total_memory = 0
    module_sizes = defaultdict(float)
    
    # Calculate loaded modules memory
    for name, module in list(sys.modules.items()):
        try:
            if hasattr(module, '__file__') and module.__file__:
                size = os.path.getsize(module.__file__) / (1024 * 1024)
                module_sizes[name.split('.')[0]] += size
                total_memory += size
        except (TypeError, OSError, AttributeError):
            continue
    
    # Get package info
    for dist in distributions():
        try:
            pkg_name = dist.metadata['Name']
            version = dist.metadata['Version']
            deps = requires(pkg_name) or []
            primary_dep = deps[0].split(' ')[0] if deps else 'None'
            
            modules_info.append([
                pkg_name,
                version,
                f"{module_sizes.get(pkg_name.lower(), 0):.2f} MB",
                primary_dep[:20]
            ])
        except Exception as e:
            continue
    
    # Sort by memory descending
    modules_info.sort(key=lambda x: float(x[2].split()[0]), reverse=True)
    
    # Display
    if not modules_info:
        print("\nNo Python modules found!")
        return
    
    print("\n\033[1;36mPYTHON MODULES INFORMATION\033[0m")
    print(tabulate(
        modules_info[:20],
        headers=["\033[1mModule\033[0m", "\033[1mVersion\033[0m", "\033[1mMemory\033[0m", "\033[1mDependency\033[0m"],
        tablefmt="fancy_grid",
        numalign="right"
    ))
    
    mem = process.memory_info()
    print(f"\n\033[1mTotal Python Process Memory:\033[0m {mem.rss / (1024 * 1024):.2f} MB")
    print(f"\033[1mEstimated Modules Memory:\033[0m {total_memory:.2f} MB")

if __name__ == "__main__":
    get_python_modules_info()