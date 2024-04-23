########################################################
### Imports
########################################################
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

########################################################
### Generating RSA Keys of size 2048 (Can use other variants)
########################################################
def generate_rsa_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,  
        backend=default_backend()
    )

    pem_private = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption() 
    )

########################################################
### Saving the Private key
########################################################
    with open("private_key_A.pem", "wb") as f:
        f.write(pem_private)

    public_key = private_key.public_key()

    pem_public = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

########################################################
### Saving the Public key
########################################################
    with open("public_key_A.pem", "wb") as f:
        f.write(pem_public)

if __name__ == "__main__":
    generate_rsa_keys()
