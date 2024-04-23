6 Files in each folder (Node):
1) BC.py
2) Client.py
3) Server.py
4) Node_A.py
5) RSA.py
6) Gossip.py 

Folder A --> Simulates Node A
Folder B --> Simulats Node B

Files in Node A has proper comments with clean source code. Files in Node B has comments along with different experimental source code for later user.

## RUNNING THE CODE
The code should run in any OS given that python is installed with library cryptograph, numpy, and pprint which can all be installed using pip.

No data files is needed to run the program, other than provided. 

# Running the Nodes:
python Node_A.py
    --> To add new nodes, change the Node_A.py and add the IP address in the other_nodes list. Make sure you use the same port address or if other port address is used, we need to change the server.py and client.py to communicate through new port address.

# Running the blockchain:
python BC.py

    # Change the variables in Blockchain:
    difficulty = 3 #Sets the difficutly level of computing the hash
    nonce = 0 #Initial nonce value

    # Adding data to blockchain
    --> It's fully automated. Press 1 to display the block, 2 to update the block, and 3 to insert a file.
    --> If pressed 3 -> Enter the name of the file. Enter the path if not on same working directory.
    --> Press 4 or any other key to exit the blockchain.

# Running the RSA.py
python RSA.py 
    # This creates two keys in you current directory. First is the private key, and public key is dervied from it. 
    # You can change the key size used in the program easily.
    # Make sure you use the public key of other node to encrypt and private key of own node to decrypt. i.e., share public key, but keep private key.

# Github Repo
https://github.com/Biski7/CyberPhysicalSystemProject-Blockchain

How to run??????
Step 1: Clone the project onto your local drive.
Step 2: Change the IP address, and port address of your nodes in the Node_A and Node_B file.
Step 3: Also make subsequent changes in server.py and client.py in every node. 
Step 4: Change the file path in the BC.py file, and Gossip.py file.
Step 5: Run the nodes (Node_A, Node_B, and any other nodes you added) using commands as per "Running the code" section above.
