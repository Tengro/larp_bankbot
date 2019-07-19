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
    def __init__(self, message, low_level=False, victim_chat_id=None):
        self.message = message
        self.low_level = low_level
        self.victim_chat_id = victim_chat_id
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
