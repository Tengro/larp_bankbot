class TransactionError(Exception):
    def __init__(self, message):
        self.message = message
        # Call the base class constructor with the parameters it needs
        super().__init__(message)

class UserError(Exception):
    def __init__(self, message):
        self.message = message
        # Call the base class constructor with the parameters it needs
        super().__init__(message)

class HackerError(Exception):
    def __init__(self, message):
        self.message = message
        # Call the base class constructor with the parameters it needs
        super().__init__(message)

class AddressRecordError(Exception):
    def __init__(self, message):
        self.message = message
        # Call the base class constructor with the parameters it needs
        super().__init__(message)

class MessageError(Exception):
    def __init__(self, message):
        self.message = message
        # Call the base class constructor with the parameters it needs
        super().__init__(message)
