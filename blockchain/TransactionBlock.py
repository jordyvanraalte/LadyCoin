from blockchain.BlockChain import Block
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import random


REWARD = 25
LEADING_ZEROS = 2
NEXT_CHAR_LIMIT = 100


class TxBlock(Block):
    nonce = ""

    def __init__(self, previousBlock):
        super(TxBlock, self).__init__([], previousBlock)

    def add_transaction(self, tx_in):
        self.data.append(tx_in)

    def is_valid(self):
        if not super(TxBlock, self).is_valid():
            return False
        for tx in self.data:
            if not tx.is_valid():
                return False
        total_in, total_out = self.__count_totals()
        # floating point error, so not 0 but 0.000001
        # total out shouldn't be higher than 0.
        if total_out - total_in - REWARD > 0.000000000001:
            return False
        return True

    def good_nonce(self):
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update(bytes(str(self.data), 'utf8'))
        digest.update(bytes(str(self.previous_hash), 'utf8'))
        digest.update(bytes(str(self.nonce), 'utf8'))
        this_hash = digest.finalize()
        # looks if nonce got amount of leading zero's
        if this_hash[:LEADING_ZEROS] != bytes(''.join(['\x4f' for i in range(LEADING_ZEROS)]), 'utf8'):
            return False
        return int(this_hash[LEADING_ZEROS]) < NEXT_CHAR_LIMIT

    def find_nonce(self):
        for i in range(1000000):
            self.nonce = ''.join([
                chr(random.randint(0, 255)) for i in range(10 * LEADING_ZEROS)])
            if self.good_nonce():
                return self.nonce
        return None

    # calculates the toal input and output of the transactionblock.
    def __count_totals(self):
        total_in = 0
        total_out = 0
        for tx in self.data:
            for addr, amt in tx.inputs:
                total_in = total_in + amt
            for addr, amt in tx.outputs:
                total_out = total_out + amt
        return total_in, total_out


