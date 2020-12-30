

import random
import ipfs_node
import consts

import os

base_dir = os.getcwd()
file_name = os.path.join(base_dir, 'result_2.txt')

global_nodes = []

network = [[1 if random.random() < consts.CONNECTION_DEGREE else 0 for i in range(consts.NODE_NUMBER)] for j in
           range(consts.NODE_NUMBER)]


def init_network():
    for i in range(consts.NODE_NUMBER):
        for j in range(consts.NODE_NUMBER):
            if i == j:
                network[j][i] = 0
            if network[i][j] == 1:
                network[j][i] = 1

def init_ledger():
    for i in range(0, consts.NODE_NUMBER):
        for j in range(0, consts.NODE_NUMBER):
            if network[i][j] == 1:
                global_nodes[i].add_peer(j)


""" download are all 600M/min, upload limit set: 500 nodes 900M/min | 2500 nodes 600M/min | 1000 300M/min | 500 60M/min | 500 0M/min """
def init_peers():

    """ Init node type A """
    for i in range(0, consts.NODE_NUMBER):
        random_value = random.randint(0, consts.NODE_NUMBER-1)
        if random_value < consts.NODE_NUMBER * consts.NODE_A_RATE:
            global_nodes.append(ipfs_node.IpfsNode(id=i, node_type=0, upload_limit=consts.LIMIT_NODE_A,
                                                   download_limit=consts.DOWNLOAD_LIMIT))
        elif random_value < consts.NODE_NUMBER * (consts.NODE_A_RATE + consts.NODE_B_RATE):
            global_nodes.append(ipfs_node.IpfsNode(id=i, node_type=1, upload_limit=consts.LIMIT_NODE_B,
                                                   download_limit=consts.DOWNLOAD_LIMIT))
        elif random_value < consts.NODE_NUMBER * (consts.NODE_A_RATE + consts.NODE_B_RATE + consts.NODE_C_RATE):
            global_nodes.append(ipfs_node.IpfsNode(id=i, node_type=2, upload_limit=consts.LIMIT_NODE_C,
                                                   download_limit=consts.DOWNLOAD_LIMIT))
        elif random_value < consts.NODE_NUMBER * (consts.NODE_A_RATE + consts.NODE_B_RATE + consts.NODE_C_RATE + consts.NODE_D_RATE):
            global_nodes.append(ipfs_node.IpfsNode(id=i, node_type=3, upload_limit=consts.LIMIT_NODE_D,
                                                   download_limit=consts.DOWNLOAD_LIMIT))
        else:
            global_nodes.append(ipfs_node.IpfsNode(id=i, node_type=4, upload_limit=consts.LIMIT_NODE_E,
                                                   download_limit=consts.DOWNLOAD_LIMIT))

def new_round():
    for node in global_nodes:
        node.current_upload = 0
        node.current_download = 0
        for peer_id in node.ledgers:
            node.ledgers[peer_id].calculate_send_ratio()


""" Find who will send block to one node, and how many blocks will be sent """
def retrieval_file(node_id):
    start_number = random.randint(0, consts.NODE_NUMBER)
    needed_blocks = consts.SESSION_TRANSFORM

    for i in range(start_number, consts.NODE_NUMBER):
        if needed_blocks <= 0:
            break
        if network[i][node_id] == 1:
            get_blocks = global_nodes[i].decision(node_id)
            if get_blocks != 0:
                if get_blocks > consts.SESSION_TRANSFORM:
                    global_nodes[i].send_blocks(node_id, consts.SESSION_TRANSFORM)
                    global_nodes[node_id].download_blocks(i, consts.SESSION_TRANSFORM)
                    needed_blocks -= consts.SESSION_TRANSFORM
                    continue
                else:
                    global_nodes[i].send_blocks(node_id, get_blocks)
                    global_nodes[node_id].download_blocks(i, get_blocks)
                    needed_blocks -= get_blocks
                    continue
            else:
                continue

    for i in range(0, start_number):
        if needed_blocks <= 0:
            break
        if network[i][node_id] == 1:
            get_blocks = global_nodes[i].decision(node_id)
            if get_blocks != 0:
                if get_blocks > consts.SESSION_TRANSFORM:
                    global_nodes[i].send_blocks(node_id, consts.SESSION_TRANSFORM)
                    global_nodes[node_id].download_blocks(i, consts.SESSION_TRANSFORM)
                    needed_blocks -= consts.SESSION_TRANSFORM
                    continue
                else:
                    global_nodes[i].send_blocks(node_id, get_blocks)
                    global_nodes[node_id].download_blocks(i, get_blocks)
                    needed_blocks -= get_blocks
                    continue
            else:
                continue

    if needed_blocks < 0:
        return 0
    else:
        return needed_blocks



def one_round(round_num):
    print("\nRound " + str(round_num))
    my_open.write("\nRound " + str(round_num) + '\n')
    needed_blocks = [ 0 for n in range(consts.NODE_NUMBER)]
    total_needed = [ 0 for n in range(5)]
    ave_needed = [ 0.0 for n in range(5)]
    type_num = [ 0 for n in range(5)]

    for s in range(consts.SESSIONS):
        li = list(range(consts.NODE_NUMBER))
        random.shuffle(li)
        for i in li:
            needed_blocks[i] += retrieval_file(i)

    for i in range(consts.NODE_NUMBER):
        type_num[global_nodes[i].node_type] += 1
        type = global_nodes[i].node_type
        total_needed[type] += needed_blocks[i]

        #if needed_blocks[i] > 2200:
            #print("Node " + str(i) + " is type " + str(type) + ", It is dead ")
            #my_open.write("Node " + str(i) + " is type " + str(type) + ", It is dead \n")

    for i in range(5):
        ave_needed[i] = total_needed[i] / type_num[i]
        print("Node " + str(i) + ', need block: ' + str(ave_needed[i]) + " \n")
        my_open.write("Node " + str(i) + ', need block: ' + str(ave_needed[i]) + " \n")


my_open = open(file_name, 'a')

init_network()
init_peers()
init_ledger()
for i in range(consts.ROUND_NUMBER):
    new_round()
    one_round(i)
