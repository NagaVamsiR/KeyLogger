# KeyLogger
A lightweight ethical keylogger written in Python for **educational** and **authorized monitoring** use cases only. It logs keyboard activity, captures periodic screenshots, encrypts logs, and optionally sends them via email.

--

## 🚀 Features

- 🔐 Logs all keyboard inputs
- 🖼️ Captures screenshots at regular intervals
- 🔒 Encrypts log data using `cryptography.Fernet`
- 📧 Sends encrypted logs to a configured email address
- 🧵 Multi-threaded: non-blocking background logging

---

## 📁 Project Structure

```bash
ethical-keylogger/
├── keylogger.py          # Main script
├── decrypt_log.py        # Decrypt logs locally
├── secret.key            # Symmetric key (auto-generated)
├── log.enc               # Encrypted keystroke log
├── screenshots/          # Saved screenshots
