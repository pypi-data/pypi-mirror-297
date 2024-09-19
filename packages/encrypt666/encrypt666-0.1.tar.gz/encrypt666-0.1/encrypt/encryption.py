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

# Example usage:
cipher = CustomCipher()

encrypted = cipher.encrypt("Hello World!")
print("Encrypted:", encrypted)

decrypted = cipher.decrypt(encrypted)
print("Decrypted:", decrypted)
