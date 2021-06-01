from signatures import Signatures


class Transaction:
    inputs = None
    outputs = None
    # signatures
    sigs = None
    # for third party extra signing
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
#        total_out = 0
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
          #  total_in = total_in + amount
        for addr in self.reqd:
            found = False
            for s in self.sigs:
                if Signatures.verify(message, s, addr):
                    found = True
            if not found:
                return False
        # for addr, amount in self.outputs:
          #  if amount < 0:
           #     return False
            # total_out = total_out + amount

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