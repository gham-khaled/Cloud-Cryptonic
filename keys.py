import glob
import os
from cryptography.fernet import Fernet


# Generate a symmetric key
def generate_symmetric_key():
    key = Fernet.generate_key()
    return key


# Save the symmetric key
def save_key_to_ssh_folder(key, key_name):
    ssh_folder = os.path.expanduser("~/.ssh")
    key_file_path = os.path.join(ssh_folder, key_name)

    with open(key_file_path, "wb") as key_file:
        key_file.write(key)

    print(f"Key saved to {key_file_path}")


# Load a symmetric key from a file
def load_key_from_file(key_name):
    ssh_folder = os.path.expanduser("~/.ssh")
    key_file_path = os.path.join(ssh_folder, key_name)

    with open(key_file_path, "rb") as key_file:
        key = key_file.read()

    return key


# Encrypt a file using a symmetric key
def encrypt_file(input_file, output_file, key):
    fernet = Fernet(key)

    with open(input_file, "rb") as file:
        file_data = file.read()

    encrypted_data = fernet.encrypt(file_data)

    with open(output_file, "wb") as encrypted_file:
        encrypted_file.write(encrypted_data)


# Decrypt a file using a symmetric key
def decrypt_file(input_file, output_file, key):
    fernet = Fernet(key)

    with open(input_file, "rb") as file:
        encrypted_data = file.read()

    decrypted_data = fernet.decrypt(encrypted_data)

    with open(output_file, "wb") as decrypted_file:
        decrypted_file.write(decrypted_data)


def list_keys():
    ssh_folder = os.path.expanduser("~/.ssh")
    return glob.glob(os.path.join(ssh_folder, "*"))

