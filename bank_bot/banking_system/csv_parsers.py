import csv
import os
from bank_bot.banking_system.user_class import User
from bank_bot.banking_system.address_record_class import AddressRecord

def mass_set_contact_csv(document, database):
    with open("mass_сontact_set.csv", "wb") as csvfile:
        csvfile.write(document)
    error_list = []
    good_result_counter = 0
    with open("mass_сontact_set.csv", "r+") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        next(reader, None)
        for row_number, row in enumerate(reader):
            owner_hash = row[0]
            target_hash = row[1]
            target_name = row[2]
            owner = User.get_user_by_user_hash(owner_hash, database)
            if owner is None:
                error_list.append(f"Row {row_number + 2}: NO SUCH USER (OWNER)")
                continue
            target = User.get_user_by_user_hash(target_hash, database)
            if target is None:
                error_list.append(f"Row {row_number + 2}: NO SUCH USER (TARGET)")
                continue
            address_records = AddressRecord.list_address_records(owner_hash, database)
            existing_records = [x.target_hash for x in address_records]
            if target_hash == owner_hash:
                error_list.append(f"Row {row_number + 2}: SELF ADRESSING")
                continue
            if target_hash in existing_records:
                error_list.append(f"Row {row_number + 2}: DUPLICATE")
                continue
            AddressRecord.create_address_record(owner_hash, target_hash, target_name, database)
            good_result_counter += 1
    total_result_counter = row_number + 1
    os.remove("mass_сontact_set.csv")
    return good_result_counter, total_result_counter, error_list 


def mass_set_character_csv(document, database):
    with open("mass_character_set.csv", "wb") as csvfile:
        csvfile.write(document)
    error_list = []
    good_result_counter = 0
    with open("mass_character_set.csv", "r+") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        next(reader, None)
        for row_number, row in enumerate(reader):
            character_hash = row[0]
            finances = row[1]
            hacker_level = row[2]
            hacker_defence = row[3]
            is_admin = row[4]
            user = User.get_user_by_user_hash(character_hash, database)
            if user is None:
                error_list.append(f"Row {row_number + 2}: NO SUCH USER")
                continue
            User.update_db_value(character_hash, "finances", finances, database)
            User.update_db_value(character_hash, "hacker_level", hacker_level, database)
            User.update_db_value(character_hash, "hacker_defence", hacker_defence, database)
            User.update_db_value(character_hash, "is_admin", is_admin, database)
            good_result_counter += 1
    total_result_counter = row_number + 1
    os.remove("mass_character_set.csv")
    return good_result_counter, total_result_counter, error_list 
