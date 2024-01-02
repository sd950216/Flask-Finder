import socket
import webbrowser
import ctypes
import winsound
import threading

def get_local_ips():
    local_ips = []
    try:
        host_name = socket.gethostname()
        local_ips.append(socket.gethostbyname(host_name))
    except:
        pass

    try:
        # Loop through common local IP ranges (adjust as needed)
        for i in range(1, 256):
            ip = f"192.168.1.{i}"
            local_ips.append(ip)
    except:
        pass

    return local_ips

def is_flask_app_alive(ip, port):
    try:
        with socket.create_connection((ip, port), timeout=0.1):
            return True
    except (socket.timeout, ConnectionRefusedError, OSError) as e:
        return False

def play_sound(sound):
    winsound.PlaySound(sound, winsound.SND_ALIAS)

def open_flask_app_in_browser():
    port = 5000
    local_ips = get_local_ips()

    for ip in local_ips:
        try:
            if is_flask_app_alive(ip, port):
                url = f"http://{ip}:{port}/"
                webbrowser.open(url)

                # Use threading to play the sound without waiting for the MessageBox
                threading.Thread(target=play_sound, args=("SystemAsterisk",)).start()
                break
        except Exception as e:
            print(f"Error connecting to {ip}: {e}")

    else:
        # Use threading to play the sound without waiting for the MessageBox
        threading.Thread(target=play_sound, args=("SystemExclamation",)).start()

        msg = "No running Flask app found on the local network."
        ctypes.windll.user32.MessageBoxW(0, msg, "Flask App Not Found", 0)

if __name__ == "__main__":
    open_flask_app_in_browser()
