########################################################
### Gossip Protocol Node 
########################################################
from Gossip import GossipNode
# hostname = '192.168.68.84'
hostname = '192.168.4.25'
port = 8000
# IP = '192.168.68.81'
# other_nodes = ['192.168.68.81']
other_nodes = ['192.168.4.25']
node = GossipNode(port, hostname, other_nodes)



