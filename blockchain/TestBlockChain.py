import unittest
import datetime
from blockchain.BlockChain import Block


class Data:
    data = ""
    time = {}

    def __init__(self, data):
        self.data = data
        self.time = datetime.datetime.now()


class TestBlockChain(unittest.TestCase):
    genesis = Block("My name is Root", None)
    block1 = Block("My name is Block1", genesis)
    block2 = Block(12345, genesis)
    block3 = Block(Data("Test"), block1)
    block4 = Block("My name is Block4", block2)
    block5 = Block("My name is Block5", block3)

    # tests if previous is correct.
    def test_previous(self):
        self.assertTrue(self.block1.previous_block.calc_hash() == self.block1.previous_hash)

    # test blockchain
    def test_chain(self):
        for b in [self.block1, self.block2, self.block3, self.block4, self.block5]:
            self.assertTrue(b.previous_block.calc_hash() == b.previous_hash)

    # test tampering
    def test_tampering(self):
        self.block3.data = "random data"
        self.assertFalse(self.block5.previous_block.calc_hash() == self.block5.previous_hash)


if __name__ == '__main__':
    unittest.main()
