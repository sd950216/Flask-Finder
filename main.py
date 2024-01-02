import socket
import webbrowser
import ctypes
import winsound
import threading
import time

def get_local_ip():
    try:
        host_name = socket.gethostname()
        local_ip = socket.gethostbyname(host_name)
        return local_ip
    except:
        return "127.0.0.1"

def is_flask_app_alive(port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.1)
            s.connect((get_local_ip(), port))
        return True
    except (socket.timeout, ConnectionRefusedError):
        return False

def play_sound(sound):
    winsound.PlaySound(sound, winsound.SND_ALIAS)

def open_flask_app_in_browser():
    port = 5000

    if is_flask_app_alive(port):
        url = f"http://{get_local_ip()}:{port}/"
        webbrowser.open(url)

        # Use threading to play the sound without waiting for the MessageBox
        threading.Thread(target=play_sound, args=("SystemAsterisk",)).start()

    else:
        # Use threading to play the sound without waiting for the MessageBox
        threading.Thread(target=play_sound, args=("SystemExclamation",)).start()

        msg = "App is not running. Please start the app and try again.\n"
        ctypes.windll.user32.MessageBoxW(0, msg, "Flask App Not Found", 0)

if __name__ == "__main__":
    open_flask_app_in_browser()
