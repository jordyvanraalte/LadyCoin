import unittest
from signatures import Signatures
from blockchain.Transaction import Transaction


class TestTransaction(unittest.TestCase):
    pr1, pu1 = Signatures.generate_keys()
    pr2, pu2 = Signatures.generate_keys()
    pr3, pu3 = Signatures.generate_keys()
    pr4, pu4 = Signatures.generate_keys()

    transaction1 = Transaction()
    transaction1.add_input(pu1, 1)
    transaction1.add_output(pu2, 1)
    transaction1.sign(pr1)

    transaction2 = Transaction()
    transaction2.add_input(pu1, 2)
    transaction2.add_output(pu2, 1)
    transaction2.add_output(pu3, 1)
    transaction2.sign(pr1)

    transaction3 = Transaction()
    transaction3.add_input(pu3, 1.2)
    transaction3.add_output(pu1, 1.1)
    transaction3.add_reqd(pu4)
    transaction3.sign(pr3)
    transaction3.sign(pr4)

    # Wrong signatures
    transaction4 = Transaction()
    transaction4.add_input(pu1, 1)
    transaction4.add_output(pu2, 1)
    transaction4.sign(pr2)

    # Escrow Transaction not signed by the arbiter
    transaction5 = Transaction()
    transaction5.add_input(pu3, 1.2)
    transaction5.add_output(pu1, 1.1)
    transaction5.add_reqd(pu4)
    transaction5.sign(pr3)

    # Two input addrs, signed by one
    transaction6 = Transaction()
    transaction6.add_input(pu3, 1)
    transaction6.add_input(pu4, 0.1)
    transaction6.add_output(pu1, 1.1)
    transaction6.sign(pr3)

    # Outputs exceed inputs
    transaction7 = Transaction()
    transaction7.add_input(pu4, 1.2)
    transaction7.add_output(pu1, 1)
    transaction7.add_output(pu2, 2)
    transaction7.sign(pr4)

    # Negative values
    transaction8 = Transaction()
    transaction8.add_input(pu2, -1)
    transaction8.add_output(pu1, -1)
    transaction8.sign(pr2)

    # Modified Transaction
    transaction9 = Transaction()
    transaction9.add_input(pu1, 1)
    transaction9.add_output(pu2, 1)
    transaction9.sign(pr1)
    # outputs = [(pu2,1)]
    # change to [(pu3,1)]
    transaction9.outputs[0] = (pu3, 1)

    for t in [transaction4, transaction5, transaction6, transaction7, transaction8, transaction9]:
        if t.is_valid():
            print("ERROR! Bad Transaction is valid")
        else:
            print("Success! Bad Transaction is invalid")

    # tests if previous is correct.
    def test_valid(self):
        for t in [self.transaction1, self.transaction2, self.transaction3]:
            self.assertTrue(t.is_valid())

    def test_wrong_signature(self):
        self.assertFalse(self.transaction4.is_valid())

    def test_not_signed(self):
        self.assertFalse(self.transaction5.is_valid())

    def test_2_signed_by_1(self):
        self.assertFalse(self.transaction6.is_valid())

    # def test_outputs_exceeding_input(self):
      #  self.assertFalse(self.transaction7.is_valid())

    def test_negative_transactions(self):
        self.assertFalse(self.transaction8.is_valid())

    def test_modified_transaction(self):
        self.assertFalse(self.transaction9.is_valid())

if __name__ == '__main__':
    unittest.main()
