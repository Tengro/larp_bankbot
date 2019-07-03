from .banking_system_class_based import BankingClient

class BankingClientFactory(object):
    def __init__(self, database):
        self.database = database

    def create_client(self, message):
        return BankingClient(message=message, database=self.database)
