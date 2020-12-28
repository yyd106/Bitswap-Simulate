
import math


class Ledger:
    """Bitswap Node's Ledger"""


    def __init__(self, debtor):
        self.debtor = debtor
        self.sent_byte = 0.0
        self.receive_byte = 0.0
        self.send_ratio = 0.998

    def set_sent(self, sent_byte):
        self.sent_byte += sent_byte

    def set_receive(self, receive):
        self.receive_byte += receive

    def get_send_ratio(self):
        return self.send_ratio

    def calculate_send_ratio(self):
        r = self.sent_byte / (self.receive_byte + 1)
        self.send_ratio = 1 - 1/(1+math.exp(6-3*r))

