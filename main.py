import boto3
from credit_card_encryptor import CreditCardEncryptor
from tokenization_service import TokenizationService
import os

def main():
    kms_key_id = 'your-kms-key-id'
    s3_bucket_name = 'your-bucket-name'
    s3_client = boto3.client('s3')

    encryptor = CreditCardEncryptor(kms_key_id)
    token_service = TokenizationService()

    # Sample credit card data
    credit_card_number = "4111111111111111"

    # Encrypt the credit card data
    encrypted_key, encrypted_data = encryptor.encrypt(credit_card_number)
    print(f"Encrypted Data: {encrypted_data}")

    # Save encrypted data to S3
    s3_client.put_object(Bucket=s3_bucket_name, Key='encrypted_data', Body=encrypted_data)

    # Tokenize the encrypted key
    token = token_service.tokenize(encrypted_key)
    print(f"Token: {token}")

    # Retrieve encrypted data from S3
    encrypted_data_retrieved = s3_client.get_object(Bucket=s3_bucket_name, Key='encrypted_data')['Body'].read()
    print(f"Retrieved Encrypted Data: {encrypted_data_retrieved}")

    # Detokenize to get the encrypted key back
    encrypted_key_retrieved = token_service.detokenize(token)
    print(f"Retrieved Encrypted Key: {encrypted_key_retrieved}")

    # Decrypt the data to get the original credit card number
    decrypted_data = encryptor.decrypt(encrypted_key_retrieved, encrypted_data_retrieved)
    print(f"Decrypted Data: {decrypted_data}")

if __name__ == "__main__":
    main()
