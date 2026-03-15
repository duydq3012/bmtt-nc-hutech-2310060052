import os

import rsa


class RSACipher:
    def __init__(self, keys_dir=None):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.keys_dir = keys_dir or os.path.join(base_dir, "keys")
        os.makedirs(self.keys_dir, exist_ok=True)
        self.private_key_path = os.path.join(self.keys_dir, "private.pem")
        self.public_key_path = os.path.join(self.keys_dir, "public.pem")

    def generate_keys(self, key_size=1024):
        public_key, private_key = rsa.newkeys(key_size)
        with open(self.private_key_path, "wb") as private_file:
            private_file.write(private_key.save_pkcs1("PEM"))
        with open(self.public_key_path, "wb") as public_file:
            public_file.write(public_key.save_pkcs1("PEM"))

    def load_keys(self):
        if not os.path.exists(self.private_key_path) or not os.path.exists(self.public_key_path):
            self.generate_keys()

        with open(self.private_key_path, "rb") as private_file:
            private_key = rsa.PrivateKey.load_pkcs1(private_file.read())
        with open(self.public_key_path, "rb") as public_file:
            public_key = rsa.PublicKey.load_pkcs1(public_file.read())
        return private_key, public_key

    def encrypt(self, message, key):
        if isinstance(message, str):
            message = message.encode("utf-8")
        return rsa.encrypt(message, key)

    def decrypt(self, ciphertext, key):
        decrypted = rsa.decrypt(ciphertext, key)
        return decrypted.decode("utf-8")

    def sign(self, message, private_key):
        if isinstance(message, str):
            message = message.encode("utf-8")
        return rsa.sign(message, private_key, "SHA-256")

    def verify(self, message, signature, public_key):
        if isinstance(message, str):
            message = message.encode("utf-8")
        try:
            rsa.verify(message, signature, public_key)
            return True
        except rsa.VerificationError:
            return False
