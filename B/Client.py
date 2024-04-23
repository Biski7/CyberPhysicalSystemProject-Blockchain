########################################################
### IMPORTS
########################################################
import socket
import time
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

########################################################
### Loading the Private Key for Decryption
########################################################
def load_public_key():
    with open("public_key_A.pem", "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )
    return public_key



########################################################
### Function For Creating Client
########################################################

def client(IP, index):
    IP = '192.168.4.25'
    PORT = 8888
    DISCONNECT_MESSAGE = '!END'
    ADDR = (IP, PORT)
    FORMAT = "utf-8"
    SIZE = 100
    time.sleep(2)

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    f = open(f'{index}.txt', 'rb')

    public_key_A = load_public_key()
########################################################
### Encrypting and sending the information through socket connection
########################################################

    while True:
        fb = f.read(SIZE)
        if not fb:
            break
        encrypted_fb = public_key_A.encrypt(
            fb,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        client.sendall(encrypted_fb)

    print("Data Sent by Client")
    client.shutdown(socket.SHUT_RDWR)
    client.close()
    print('Client closed')
    f.close()