
import pickle
import json
import os

class BotDB:

    db_path = "db/db.json"

    database_dict = dict()

    def __init__(self):
        if os.path.exists(self.db_path):
            print("Loaded json db")
            with open(self.db_path, 'r') as fp:
                self.database_dict = json.load(fp)
        else:
            self.database_dict["custom_commands"] = dict()

    def add_command(self, command_name, print_string):
        self.database_dict["custom_commands"][command_name] = print_string
        with open(self.db_path, 'w') as fp:

            json.dump(self.database_dict, fp)

    def get_command(self, command_name):
        return self.database_dict["custom_commands"][command_name]

