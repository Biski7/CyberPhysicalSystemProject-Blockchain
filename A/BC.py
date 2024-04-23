########################################################
### IMPORTS
########################################################
import hashlib
import time
from datetime import datetime 
from pprint import pprint
import sys 
import csv
import psutil
import os 
import os.path
import json
import subprocess

########################################################
### ANSI escape codes for some colors
########################################################
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    ORANGE = '\033[48;5;208m'
    ITALIC = '\033[3m'



########################################################
### Generate the hash of any given input
########################################################
def hashGenerator(data):
    return hashlib.sha256(data.encode()).hexdigest()

########################################################
### Generate the hash of a file
########################################################
def hashGeneratorfile(data):
    with open(data, 'rb') as f: 
        fb = f.read() 
        file_hash = hashlib.sha256(fb)
    return [file_hash.hexdigest(), fb]

global path
path = '/Users/bishalthapa/Desktop/2024/Cyber Physical System/Final Project/BC/Gossip Socket/2024Crypt/A/1.txt'

########################################################
### Blockchain Code
########################################################
class Blockchain(object):
    def __init__(self):
        self.difficulty = 3
        self.nonce = 0
        def exists(filename):
            with open(f"{filename}.txt", "r") as fp:
                block_value = json.load(fp)
                index = block_value.get('index')
                data = block_value.get('data')
                timestamp = block_value.get("timestamp")
                hash_of_current_block = block_value.get('hash_of_current_block')
                hash_of_previous_block = block_value.get('hash_of_previous_block')

            block = {
                'index': index,
                'data': data,
                'timestamp': timestamp,
                'hash_of_current_block': hash_of_current_block,
                'hash_of_previous_block': hash_of_previous_block
            }

            self.chain.append(block) 

            new_index = str(index + 2)
            path1 = path 
            path1 = path1.replace('1', new_index)
            if os.path.exists(path1):
                exists(new_index)
            else:
                pass

        if os.path.exists(path):
            self.chain = []
            filename = '1'
            exists(filename)
        else:
            self.chain = []
            index = 0
            hashLast = None
            timestamp = datetime.now()
            hashStart = hashGenerator( hashGenerator('gen_hash') + hashGenerator(str(index)) + hashGenerator(str(timestamp) + str(self.nonce)))
            while not hashStart.startswith('0' * self.difficulty):
                self.nonce +=1 
                hashStart = hashGenerator(hashGenerator('gen_hash') + hashGenerator(str(index)) + hashGenerator(str(timestamp) + str(self.nonce)))

            genesis_block = {
                'index': index,
                'data': 'gen_hash',
                'timestamp': timestamp,
                'hash_of_current_block': hashStart,
                'hash_of_previous_block': hashLast,
            }
            self.chain = [genesis_block]
            
            message ={"index": index, "data":"gen_hash", "timestamp": str(timestamp), "hash_of_current_block": hashStart, "hash_of_previous_block":hashLast}
            filename = '1'
            with open(f"{filename}.txt", "w") as fp:
                json.dump(message, fp)
                print('dictionary saved successfully to file')

########################################################
### Function for proof of work
########################################################
    def proof_of_work(self, hashString, index, timestamp):
        hashStart = hashGenerator( hashGenerator(hashString) + hashGenerator(str(index)) + hashGenerator(str(timestamp) + str(self.nonce)))
        while not hashStart.startswith('0' * self.difficulty):
            self.nonce +=1 
            hashStart = hashGenerator( hashGenerator(hashString) + hashGenerator(str(index)) + hashGenerator(str(timestamp) + str(self.nonce)))
        return hashStart

########################################################
### Function to add a block
########################################################
    def add_block(self, file_name):
        starttime = time.time_ns()
        index = len(self.chain)
        timestamp = datetime.now()
        hash_of_previous_block = self.chain[-1]['hash_of_current_block']
        nonce = 0
        hash_of_current_block = 0
        data_hash, data = hashGeneratorfile(file_name)
        hash_string = str(timestamp).join([str(index), hash_of_previous_block,data_hash,str(nonce)])
        # hash_of_current_block = hashGenerator(hash_string)
        hash_of_current_block = self.proof_of_work(hash_string,index, timestamp)
        block = {
            'index': index,
            'data': data,
            'timestamp': timestamp,
            'hash_of_current_block': hash_of_current_block,
            'hash_of_previous_block': hash_of_previous_block
        }

        if self.valid_chain(self.chain) == False:
            return False
        self.chain.append(block) 

        endtime = time.time_ns()
        size = sys.getsizeof(block)
        elapsed_time = endtime - starttime
        message ={"index": index, "data": str(data), "timestamp": str(timestamp), "hash_of_current_block": hash_of_current_block, "hash_of_previous_block":hash_of_previous_block}
        filename = index + 1
        with open(f"{filename}.txt", "w") as fp:
            json.dump(message, fp)
            print('dictionary saved successfully to individual file')
        return block

########################################################
### Checking if chain is valid
########################################################
    def valid_chain(self, chain):
        current_index = 1 
        previous_index = 0
        
        while current_index < len(chain):
            block = chain[current_index]
            block_previous = chain[previous_index]
            if block['hash_of_previous_block'] != block_previous['hash_of_current_block']:
                return False
            current_index += 1
            previous_index += 1
        return True
    

########################################################
### Creating an instance of Blockchain
########################################################
bc = Blockchain()
while True:   
    print(f"{Colors.BLUE}")
    decision = input("Press 1 to display the block, 2 to update, 3 to add new block, or 4 to quit.\n")
    print(f"{Colors.RESET}")
    if decision == str('1'):
        for block in bc.chain:
            index = block['index']
            data = block['data']
            timestamp = block['timestamp']
            current_hash = block['hash_of_current_block']
            previous_hash = block['hash_of_previous_block']
            print(f"Block {index}")
            print("-------------------------------------------------------------------------------------")
            print(f"{Colors.RED}")
            print(f'Index: {index}')
            print(f'Data: {data}')
            print(f'Timestamp: {timestamp}')
            print(f'Current Hash: {current_hash}')
            print(f'Previous Hash: {previous_hash}')
            print("-------------------------------------------------------------------------------------")
            print(f"\n{Colors.RESET}")

    elif decision == str('2'):
        bc = Blockchain()

    elif decision == str('3'):
        file = str(input("Enter the file to add: "))
        bc.add_block(file)

    elif decision == str('4'):
        exit()

    else:
        exit()


