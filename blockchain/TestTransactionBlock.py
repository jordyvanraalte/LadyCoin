import unittest
import datetime
from blockchain.BlockChain import Block
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from signatures import Signatures
from blockchain.Transaction import Transaction
from blockchain.TransactionBlock import TxBlock
import time


class TestTransactionBlockChain(unittest.TestCase):
    pr1, pu1 = Signatures.generate_keys()
    pr2, pu2 = Signatures.generate_keys()
    pr3, pu3 = Signatures.generate_keys()

    Tx1 = Transaction()
    Tx1.add_input(pu1, 1)
    Tx1.add_output(pu2, 1)
    Tx1.sign(pr1)

    Tx2 = Transaction()
    Tx2.add_input(pu2, 1.1)
    Tx2.add_output(pu3, 1)
    Tx2.sign(pr2)

    Tx3 = Transaction()
    Tx3.add_input(pu3, 1.1)
    Tx3.add_output(pu1, 1)
    Tx3.sign(pr3)

    Tx4 = Transaction()
    Tx4.add_input(pu1, 1)
    Tx4.add_output(pu2, 1)
    Tx4.add_reqd(pu3)
    Tx4.sign(pr1)
    Tx4.sign(pr3)

    # wrong transaction
    Tx5 = Transaction()
    Tx5.add_input(pu1, 1)
    Tx5.add_output(pu2, 1)
    Tx5.add_reqd(pu3)
    Tx5.sign(pr1)

    Genesis = TxBlock(None)
    Genesis.add_transaction(Tx1)
    Genesis.add_transaction(Tx2)

    Block1 = TxBlock(Genesis)
    Block1.add_transaction(Tx3)
    Block1.add_transaction(Tx4)

    Block2 = TxBlock(Genesis)
    Block2.add_transaction(Tx5)

    def test_genesis_valid(self):
        self.assertTrue(self.Genesis.is_valid())

    def test_block_1_valid(self):
        self.assertTrue(self.Block1.is_valid())

    def test_block_2_not_valid(self):
        self.assertFalse(self.Block2.is_valid())

    def test_mining(self):
        start = time.time()
        nonce = self.Block1.find_nonce()
        print(str(time.time() - start) + " seconds")

        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update(bytes(str(self.Block1.data), 'utf8'))
        digest.update(bytes(str(self.Block1.previous_hash), 'utf8'))
        digest.update(bytes(str(self.Block1.nonce), 'utf8'))
        this_hash = digest.finalize()
        print("found hash with nonce " + str(this_hash))
        print(nonce)

        self.assertTrue(nonce)

if __name__ == '__main__':
    unittest.main()
