import boto3
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os

class CreditCardEncryptor:
    def __init__(self, kms_key_id):
        self.kms_client = boto3.client('kms')
        self.kms_key_id = kms_key_id
        self.backend = default_backend()
        self.block_size = algorithms.AES.block_size

    def encrypt(self, plaintext):
        # Generate a data key from KMS
        response = self.kms_client.generate_data_key(KeyId=self.kms_key_id, KeySpec='AES_256')
        key = response['Plaintext']
        encrypted_key = response['CiphertextBlob']
        
        # Encrypt the plaintext using the data key
        iv = os.urandom(self.block_size // 8)
        padder = padding.PKCS7(self.block_size).padder()
        padded_data = padder.update(plaintext.encode()) + padder.finalize()
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=self.backend)
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()
        
        return encrypted_key, iv + ciphertext

    def decrypt(self, encrypted_key, ciphertext):
        # Decrypt the data key using KMS
        response = self.kms_client.decrypt(CiphertextBlob=encrypted_key)
        key = response['Plaintext']
        
        # Extract the IV and encrypted data
        iv = ciphertext[:self.block_size // 8]
        actual_ciphertext = ciphertext[self.block_size // 8:]
        
        # Decrypt the ciphertext using the data key
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=self.backend)
        decryptor = cipher.decryptor()
        padded_plaintext = decryptor.update(actual_ciphertext) + decryptor.finalize()
        unpadder = padding.PKCS7(self.block_size).unpadder()
        plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
        
        return plaintext.decode()

if __name__ == "__main__":
    kms_key_id = 'your-kms-key-id'
    encryptor = CreditCardEncryptor(kms_key_id)
    encrypted_key, ciphertext = encryptor.encrypt("4111111111111111")
    print(f"Encrypted Key: {encrypted_key}")
    print(f"Ciphertext: {ciphertext}")
    plaintext = encryptor.decrypt(encrypted_key, ciphertext)
    print(f"Decrypted: {plaintext}")
