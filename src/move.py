
class Move:

    def __init__(self, initial, final):
        # inital and final are squares
        self.initial = initial
        self.final = final

    def __eq__(self, other):
        if other == None: return False
        return self.initial == other.initial and self.final == other.final