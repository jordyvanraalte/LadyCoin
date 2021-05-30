from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes


class Block:
    data = None
    previous_hash = None
    previous_block = None

    def __init__(self, data, previous_block):
        # enables genesis block
        if previous_block is not None:
            self.previous_block = previous_block
            self.previous_hash = previous_block.calc_hash()

        self.data = data

    def calc_hash(self):
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update(bytes(str(self.data), 'utf8'))
        digest.update(bytes(str(self.previous_hash), 'utf8'))
        return digest.finalize()

    def is_valid(self):
        if self.previous_block is None:
            return True
        return self.previous_block.calc_hash() == self.previous_hash
