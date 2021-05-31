import unittest
from signatures import Signatures


class TestSignature(unittest.TestCase):
    pr, pu = Signatures.generate_keys()

    def test_verification(self):
        message = "My secret message to you <3"
        sig = Signatures.sign(message, self.pr)
        self.assertTrue(Signatures.verify(message, sig, self.pu))


if __name__ == '__main__':
    unittest.main()
