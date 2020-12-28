

import ledger
import consts
import random

class IpfsNode:
    """Bitswap Node"""

    def __init__(self, id, node_type, upload_limit, download_limit):
        self.id = id
        self.node_type = node_type
        self.upload_limit= upload_limit
        self.download_limit = download_limit
        self.current_upload = 0
        self.current_download = 0
        self.ledgers = {}
        self.files = []

    def add_peer(self, peer_id):
        if peer_id in self.ledgers:
            return
        new_ledger = ledger.Ledger(debtor=peer_id)
        self.ledgers[peer_id] = new_ledger

    def download_blocks(self, peer_id, size):
        if self.current_download + size > self.download_limit:
            return
        self.current_download += size
        recv_bytes = size * consts.BLOCK_SIZE
        self.ledgers[peer_id].set_receive(recv_bytes)

    def send_blocks(self, peer_id, size):
        if self.current_upload + size > self.upload_limit:
            return
        self.current_upload += size
        send_byte = size * consts.BLOCK_SIZE
        self.ledgers[peer_id].set_sent(send_byte)

    def decision(self, peer_id):
        ratio = self.ledgers[peer_id].send_ratio
        if random.random() < ratio:
            return self.upload_limit - self.current_upload
        else:
            return 0




