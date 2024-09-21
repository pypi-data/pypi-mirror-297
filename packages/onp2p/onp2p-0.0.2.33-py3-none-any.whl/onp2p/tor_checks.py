import os
import subprocess
import socket
import platform

def check_tor_installed():
    """Controlla se Tor è installato."""
    try:
        subprocess.run(["tor", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Tor è installato.")
        return True
    except FileNotFoundError:
        print("Tor non è installato.")
        return False