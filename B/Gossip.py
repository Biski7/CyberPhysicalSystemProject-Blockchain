# The Gossip protocol was coded using following resource
# https://codereview.stackexchange.com/questions/95671/gossip-algorithm-in-distributed-systems

########################################################
### IMPORTS
########################################################
import random
import socket
from threading import Thread
import time
from datetime import datetime
from Server import server
from Client import client
import os.path
import numpy as np

path = '/Users/bishalthapa/Desktop/2024/Cyber Physical System/Final Project/BC/Gossip Socket/2024Crypt/B/name.txt'

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
### Gossip Class for Gossip Protocol
########################################################
class GossipNode:
    def __init__(self, port, hostname, other_nodes):
        self.node = socket.socket(type=socket.SOCK_DGRAM)
        self.hostname = hostname
        self.port = port 
        self.node.bind((self.hostname, self.port))
        self.other_nodes = other_nodes

        self.file = 1

        print(f"{Colors.ITALIC}My IP is : {self.hostname},\nPort: {self.port}{Colors.RESET}")
        print("Other nodes are =>", self.other_nodes)
        self.start_threads()

    ########################################################
    ### Function to determine the latest block
    ########################################################
    def find_latest_block(self):
        path = '/Users/bishalthapa/Desktop/2024/Cyber Physical System/Final Project/BC/Gossip Socket/2024Crypt/B/name.txt'
        path1 = path.replace('name', str(self.file))
        if os.path.exists(path1):
            # filename = self.file
            self.file = self.file + 1
            self.find_latest_block()
        else:
            print(f'{self.file} doesnot exist.')
            print(f"filename is {self.file}")
            self.file = self.file
        return self.file  

    ########################################################
    ### Function to prompt user with Updation or Exit
    ########################################################
    def ask_question(self):
        while True:
            print(f'{Colors.ORANGE}#{Colors.RESET}' *50)
            input_from_node = input(f"{Colors.RED}Enter 1 to update or 2 to exit.{Colors.RESET}\n")
            if input_from_node == '1':
                latest_block_number = self.find_latest_block()
                # if latest_block_number < 0:
                #     latest_block_number == 0
                self.transmit_message(str(latest_block_number).encode('ascii')) 
            else:
                exit()

    ########################################################
    ### Function to transmit message to different nodes (Run Client)
    ########################################################
    def transmit_message(self, message):
        for address in self.other_nodes:
            print("\n")
            print(f"{Colors.MAGENTA}-"*50)
            self.file = int(message)
            self.node.sendto(message, (address, 8888))

            print("Message: '{0}' sent to [{1}].".format(message.decode('ascii'), address))
            print("-"*50)
            time.sleep(2)
            print(f"{Colors.RESET}\n")

    ########################################################
    ### Function to receive message from different nodes (Run Server)
    ########################################################
    def transmit_message_specific(self, message, address):
        print("\n")
        print(f"{Colors.MAGENTA}-"*50)
        self.node.sendto(message, (address, 8888))
        print("Message: '{0}' sent to [{1}].".format(message.decode('ascii'), address))
        print("*"*50)
        time.sleep(1)
        print(f"{Colors.RESET}\n")



    def receive_message(self):
        while True:
            message_received, address = self.node.recvfrom(1024)
            print('-'*50)
            print("\nMessage is: '{0}' which means Block {0} doesn't exist in the node at {2}.\nReceived at [{1}] from [{2}]\n".format(message_received.decode('ascii'), time.ctime(time.time()), address[0]))
            # print("\nMessage is: '{0}' which means Block {0} doesn't exist in the node at {1}".format(message_received.decode('ascii'), address[0]))

            if 'StartServer' in message_received.decode('ascii'):
                message_received = message_received.decode('ascii').split("=>")[1]
                message_received = message_received.strip('][').split(', ')
                for i in message_received:
                    time.sleep(5)
                    server(i)
                    print("Server ran SUCCESSFULLY")
                # self.ask_question()
                # input_from_node = input(f"{Colors.RED}Enter 1 to update or 2 to exit.{Colors.RESET}\n")
                # if input_from_node == '1':
                #     latest_block_number = self.find_latest_block()
                #     self.transmit_message(str(latest_block_number).encode('ascii')) 
                # else:
                #     exit()
            else:
                # Print both of these are uptodate
                # listen again
                # pass
                my_block_list = []
                # x = self.find_latest_block(1)
                # if x == 2:
                #     my_latest_block_number = self.find_latest_block(x)
                #     y = x + 1
                # else:
                #     my_latest_block_number = self.find_latest_block(y)
                #     y = y + 1
                my_latest_block_number = self.find_latest_block()
                print(f"Current Block Number in Node A : {my_latest_block_number}")
                for i in np.arange(1, my_latest_block_number ):
                    my_block_list.append(i)
                # print(f"Node A : {my_block_list}")


                node_block_list = []
                latest_block_number = int(message_received) 
                print(f"Current Block Number in Node B : {latest_block_number}")
                for i in np.arange(1, latest_block_number ):
                    node_block_list.append(i)
                # print(f"Node B : {node_block_list}")

                new_list_1 = list(set(my_block_list).difference(node_block_list))
                new_list_2 = list(set(node_block_list).difference(my_block_list))
                new_list = new_list_1 + new_list_2
                new_list.sort()
                new_list = set(new_list)
                new_list = list(new_list)
                print(new_list)

                if len(new_list) > 0:
                    self.transmit_message_specific(f'StartServer =>{new_list}'.encode('ascii'), address[0])
                    for i in new_list:
                        time.sleep(5)
                        client(address[0], i)
                        print("Client ran SUCCESSFULLY")
                    input_from_node = input(f"{Colors.RED}Enter 1 to update or 2 to exit.{Colors.RESET}\n")
                    if input_from_node == '1':
                        latest_block_number = self.find_latest_block()
                        self.transmit_message(str(latest_block_number).encode('ascii')) 
                    else:
                        exit()
                else:
                    pass
                    # Send uptodate
                    # listen again
                # my_latest_block_number = self.find_latest_block()


    def start_threads(self):
        Thread(target=self.ask_question).start()
        Thread(target=self.receive_message).start()




