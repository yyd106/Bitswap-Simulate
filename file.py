
DEFAULT_SIZE = 1000

class File:
    """A File"""

    """ by default, each file 256M, means 1000 IPFS blocks"""

    def __init__(self, id, size):
        self.id = id
        self.size = DEFAULT_SIZE

