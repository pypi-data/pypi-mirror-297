import sys
import os

class CustomCipher:
    def __init__(self):
        self.encryption_table = {
            'a': '*', 'b': '@', 'c': '#', 'd': '$', 'e': '%', 'f': '^',
            'g': '&', 'h': '(', 'i': ')', 'j': '-', 'k': '=', 'l': '+',
            'm': '[', 'n': ']', 'o': '{', 'p': '}', 'q': ':', 'r': ';',
            's': '<', 't': '>', 'u': '?', 'v': '/', 'w': '|', 'x': '1',
            'y': '2', 'z': '3', 'A': '4', 'B': '5', 'C': '6', 'D': '7',
            'E': '8', 'F': '9', 'G': '0', 'H': '!', 'I': '~', 'J': '`',
            'K': '_', 'L': '.', 'M': ',', 'N': '€', 'O': '¥', 'P': '£',
            'Q': '©', 'R': '®', 'S': '±', 'T': '§', 'U': 'µ', 'V': '¶',
            'W': '•', 'X': '×', 'Y': '÷', 'Z': '¤', ' ': '_', '.': '…',
            ',': '–', '?': '¿', '!': '¡', '0': 'ß', '1': 'æ', '2': 'ø',
            '3': 'å', '4': 'þ', '5': 'ð', '6': 'Ω', '7': 'ψ', '8': 'ε',
            '9': 'π'
        }
        self.decryption_table = {v: k for k, v in self.encryption_table.items()}

    def encrypt(self, text):
        return ''.join([self.encryption_table.get(char, char) for char in text])

    def decrypt(self, encrypted_text):
        return ''.join([self.decryption_table.get(char, char) for char in encrypted_text])

    def encrypt_file(self, input_file, output_file):
        with open(input_file, 'r') as file:
            code = file.read()
        encrypted_code = self.encrypt(code)
        with open(output_file, 'w') as file:
            file.write(encrypted_code)
        print(f"File encrypted and saved to '{output_file}'")

    def decrypt_and_run_file(self, encrypted_file):
        with open(encrypted_file, 'r') as file:
            encrypted_code = file.read()
        decrypted_code = self.decrypt(encrypted_code)
        exec(decrypted_code)

def main():
    if len(sys.argv) != 2:
        print("Usage: encrypt666 <path_to_python_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    if not os.path.isfile(input_file):
        print(f"File not found: {input_file}")
        sys.exit(1)

    base_name, ext = os.path.splitext(input_file)
    encrypted_file = f"{base_name}_666{ext}"

    cipher = CustomCipher()
    cipher.encrypt_file(input_file, encrypted_file)

    # Create a runnable script that will decrypt and execute the encrypted file
    with open(base_name + "_runner.py", 'w') as runner_file:
        runner_file.write(f"""
import os
from encryption import CustomCipher

cipher = CustomCipher()
cipher.decrypt_and_run_file('{encrypted_file}')
""")
    print(f"Runner script created: '{base_name}_runner.py'")

if __name__ == "__main__":
    main()
