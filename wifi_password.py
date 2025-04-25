"""
Wi-Fi Password Retrieval Tool
============================

A user-friendly Python utility that helps you recover saved Wi-Fi credentials on Windows systems.

📌 Basic Usage:
1. Save this script as 'wifi_passwords.py'
2. Right-click Command Prompt -> "Run as administrator"
3. Run: python wifi_passwords.py

✨ Features:
- Retrieves all saved Wi-Fi network names and passwords
- Displays network security type (WPA2, WEP, Open, etc.)
- Color-coded output for easy reading
- Checks for required admin privileges
- Presents results in a clean, numbered table

🔧 Requirements:
✔ Windows 7/8/10/11
✔ Python 3.6 or newer
✔ Administrator privileges (for full access)
✔ colorama package (install with: pip install colorama)

🛠 How It Works:
1. Uses Windows' built-in 'netsh wlan' commands
2. Extracts:
   - Network names (SSIDs)
   - Saved passwords (when available)
   - Security protocols
3. Formats everything in an easy-to-read report

📝 Notes:
- Passwords marked "Not Available" either:
  - Are enterprise networks (work/school)
  - Weren't saved by Windows
  - Require admin rights to access
- Some public networks may show no password

⚠️ Important:
Only use this on computers you own or have permission to access!

Example Output:
=============== SAVED WI-FI PASSWORDS ===============
[1] HomeWiFi       : MyPassword123 (WPA2-Personal)
[2] CoffeeShop      : No password (Open)
[3] OfficeNetwork   : (Requires admin privileges)
====================================================

Version: 1.1
Last Updated: 2023-11-15
"""

import subprocess
import sys
from datetime import datetime

from colorama import Fore

def get_wifi_profiles():
    """
    Retrieve all saved Wi-Fi profiles from Windows system using netsh command
    Returns: List of profile names or empty list if error occurs
    """
    try:
        meta_data = subprocess.check_output(
            ['netsh', 'wlan', 'show', 'profiles'], 
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        return [line.split(":")[1].strip() 
               for line in meta_data.split('\n') 
               if "All User Profile" in line]
    except subprocess.CalledProcessError as e:
        print(f"[!] Error retrieving profiles: {e.stderr}")
        return []

def get_wifi_details(profile):
    """
    Get password and security details for a specific Wi-Fi profile
    Returns: Tuple of (password, security_type)
    """
    try:
        # Get password
        results = subprocess.check_output(
            ['netsh', 'wlan', 'show', 'profile', profile, 'key=clear'],
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        
        password_lines = [line.split(":")[1].strip() 
                         for line in results.split('\n') 
                         if "Key Content" in line]
        password = password_lines[0] if password_lines else "Not Available"
        
        # Get security type
        security_lines = [line.split(":")[1].strip() 
                         for line in results.split('\n') 
                         if "Authentication" in line]
        security = security_lines[0] if security_lines else "Unknown"
        
        return password, security
        
    except subprocess.CalledProcessError as e:
        print(f"[!] Error retrieving details for {profile}: {e.stderr}")
        return "Error", "Unknown"

def print_results(profiles):
    """
    Display results in a formatted table with colored output
    """
    from colorama import init, Fore
    
    init()  # Initialize colorama
    
    # Header with timestamp
    print(f"\n{Fore.CYAN}{' SAVED WI-FI PASSWORDS ':=^60}{Fore.RESET}")
    print(f"{Fore.YELLOW}Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Fore.RESET}\n")
    
    # Table header
    print(f"{Fore.GREEN}{'No.':<5}{Fore.RESET} | {Fore.GREEN}{'Wi-Fi Name':<25}{Fore.RESET} | {Fore.GREEN}{'Password':<20}{Fore.RESET} | {Fore.GREEN}{'Security Type'}{Fore.RESET}")
    print(f"{'-'*5} | {'-'*25} | {'-'*20} | {'-'*15}")
    
    # Print each profile
    for idx, profile in enumerate(profiles, 1):
        password, security = get_wifi_details(profile)
        
        # Color coding for password availability
        password_color = Fore.RED if password == "Not Available" else Fore.GREEN
        
        print(f"{Fore.CYAN}{idx:<5}{Fore.RESET} | {Fore.BLUE}{profile:<25}{Fore.RESET} | "
              f"{password_color}{password:<20}{Fore.RESET} | {Fore.MAGENTA}{security}{Fore.RESET}")

def check_admin():
    """Check if script is running with admin privileges"""
    try:
        if sys.platform == 'win32':
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin()
        return True  # For non-Windows systems
    except:
        return False

def main():
    """
    MAIN EXECUTION
    ==============
    How to Run:
    1. Save this script as 'wifi_passwords.py'
    2. Open Command Prompt as Administrator
    3. Run: python wifi_passwords.py
    
    Note: Administrator privileges are required to retrieve passwords
    """
    if not check_admin():
        print(f"{Fore.RED}[!] Warning: Run as Administrator for full functionality{Fore.RESET}")
        print("Some passwords may not be retrievable without admin rights.\n")
    
    profiles = get_wifi_profiles()
    
    if not profiles:
        print(f"{Fore.RED}[!] No Wi-Fi profiles found or access denied{Fore.RESET}")
        return
    
    print_results(profiles)
    
    # Footer
    print(f"\n{Fore.YELLOW}Total networks found: {len(profiles)}{Fore.RESET}")
    print(f"{Fore.CYAN}{'='*60}{Fore.RESET}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}[!] Operation cancelled by user{Fore.RESET}")
    except Exception as e:
        print(f"{Fore.RED}[!] An unexpected error occurred: {str(e)}{Fore.RESET}")