from signatures import Signatures


class Transaction:
    inputs = None
    outputs = None
    sigs = None
    reqd = None

    def __init__(self):
        self.inputs = []
        self.outputs = []
        self.sigs = []
        self.reqd = []

    def add_input(self, from_addr, amount):
        self.inputs.append((from_addr, amount))

    def add_output(self, to_addr, amount):
        self.outputs.append((to_addr, amount))

    def add_reqd(self, addr):
        self.reqd.append(addr)

    def sign(self, private):
        message = self.__gather()
        newsig = Signatures.sign(message, private)
        self.sigs.append(newsig)

    def is_valid(self):
        total_in = 0
        total_out = 0
        message = self.__gather()
        for addr, amount in self.inputs:
            found = False
            for s in self.sigs:
                if Signatures.verify(message, s, addr):
                    found = True
            if not found:
                # print ("No good sig found for " + str(message))
                return False
            if amount < 0:
                return False
            total_in = total_in + amount
        for addr in self.reqd:
            found = False
            for s in self.sigs:
                if Signatures.verify(message, s, addr):
                    found = True
            if not found:
                return False
        for addr, amount in self.outputs:
            if amount < 0:
                return False
            total_out = total_out + amount

        # if total_out > total_in:
        # print("Outputs exceed inputs")
        #    return False

        return True

    def __gather(self):
        data = [self.inputs, self.outputs, self.reqd]
        return data

    def __repr__(self):
        reprstr = "INPUTS:\n"
        for addr, amt in self.inputs:
            reprstr = reprstr + str(amt) + " from " + str(addr) + "\n"
        reprstr = reprstr + "OUTPUTS:\n"
        for addr, amt in self.outputs:
            reprstr = reprstr + str(amt) + " to " + str(addr) + "\n"
        reprstr = reprstr + "REQD:\n"
        for r in self.reqd:
            reprstr = reprstr + str(r) + "\n"
        reprstr = reprstr + "SIGS:\n"
        for s in self.sigs:
            reprstr = reprstr + str(s) + "\n"
        reprstr = reprstr + "END\n"
        return reprstr


if __name__ == "__main__":
    pr1, pu1 = Signatures.generate_keys()
    pr2, pu2 = Signatures.generate_keys()
    pr3, pu3 = Signatures.generate_keys()
    pr4, pu4 = Signatures.generate_keys()

    transaction1 = Transaction()
    transaction1.add_input(pu1, 1)
    transaction1.add_output(pu2, 1)
    transaction1.sign(pr1)
    if transaction1.is_valid():
        print("Success! Transaction is valid")
    else:
        print("ERROR! Transaction is invalid")

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

    for t in [transaction1, transaction2, transaction3]:
        if t.is_valid():
            print("Success! Transaction is valid")
        else:
            print("ERROR! Transaction is invalid")

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
