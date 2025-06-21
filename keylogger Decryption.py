from cryptography.fernet import Fernet

# Load the encryption key from secret.key
def load_key():
    with open("secret.key", "rb") as key_file:
        return key_file.read()

# Load and decrypt the encrypted log file
def decrypt_log():
    key = load_key()
    fernet = Fernet(key)

    with open("log.enc", "rb") as enc_file:
        encrypted_data = enc_file.read()

    decrypted_data = fernet.decrypt(encrypted_data)
    print(" Decrypted Log:\n")
    print(decrypted_data.decode("utf-8"))

if __name__ == "__main__":
    decrypt_log()
