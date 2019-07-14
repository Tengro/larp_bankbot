import sqlite3
from bank_bot.settings import ADDRESS_RECORD_DATA

class AddressRecord(object):
    def __init__(
        self, owner_hash, target_hash, target_name,
    ):
        self.owner_hash = owner_hash
        self.target_hash = target_hash
        self.target_name = target_name

    def __str__(self):
        return ADDRESS_RECORD_DATA.substitute(
            owner_hash=self.owner_hash, target_hash=self.target_hash, 
            target_name=self.target_name,
        )
        
    @classmethod
    def create_address_record(cls, owner_hash, target_hash, target_name, database):
        return database.create_address_record(owner_hash, target_hash, target_name)

    @classmethod
    def list_address_records(cls, owner_hash, database):
        return database.inspect_address_records(owner_hash, cls)

    @classmethod
    def delete_address_record(cls, owner_hash, target_hash, database):
        database.delete_address_record(owner_hash, target_hash)
