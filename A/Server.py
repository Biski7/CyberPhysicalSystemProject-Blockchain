########################################################
### IMPORTS
########################################################
import socket
import time
import os
import select
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes


########################################################
### Function For Hosting Server
########################################################

def server(index):
    time.sleep(0.1)

    PORT = 8888
    SIZE = 256
    DISCONNECT_MESSAGE = '!END'
    FORMAT = 'utf-8'
    SERVER = '192.168.4.25'

    ADDR = (SERVER, PORT)

########################################################
### Loading the Private Key for Decryption
########################################################
    def load_private_key():
        with open("private_key_A.pem", "rb") as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None, 
                backend=default_backend()
            )
        return private_key

    f = open(f'{index}.txt', 'wb')

    private_key_A = load_private_key()

    print("Server Starting...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"Server listening on {SERVER}...")
    conn, addr = server.accept()

########################################################
### Decrypting and Writing the received information to a file
########################################################

    try:
        with open(f'{index}.txt', 'wb') as f:
            while True:
                data = conn.recv(SIZE)
                if data == DISCONNECT_MESSAGE:
                    print("Closing connection.")
                    break
                elif data:
                    decrypted_mes = private_key_A.decrypt(
                        data,
                        padding.OAEP(
                            mgf=padding.MGF1(algorithm=hashes.SHA256()),
                            algorithm=hashes.SHA256(),
                            label=None
                        )
                    )
                    f.write(decrypted_mes)
                else:
                    break 
    finally:
        f.close()
        conn.close()
        server.close()
        print("Connection and server closed.")

