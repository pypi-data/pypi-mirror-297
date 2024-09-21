class NoFlopError(Exception):
    def __init__(self, message):
        self.message = "No flop was found in the hand history."
        super().__init__(self.message)


class NoCardError(Exception):
    def __init__(self, message):
        self.message = "No card has been found in the hand history."
        super().__init__(self.message)