import os

import yaml


class QTConfig:
    instance = None

    def __init__(self):
        self.__read_yaml()

    def __read_yaml(self):
        if not os.path.exists("./config.yml"):
            QTConfig.create_default_config()

        with open(r'./config.yml') as file:
            # The FullLoader parameter handles the conversion from YAML
            # scalar values to Python the dictionary format
            config = yaml.load(file, Loader=yaml.FullLoader)

            self.auto_csv = config["auto-csv"]
            self.env = config["env"]
            self.db_path = config["db.path"]
            self.items = config["items"]
            self.locations = config["locations"]

    def __persist_changes(self, obj):
        obj["env"] = self.env
        with open('./config.yml', "w+") as file:
            yaml.dump(obj, file)

        self.auto_csv = obj["auto-csv"]
        self.db_path = obj["db.path"]
        self.items = obj["items"]
        self.locations = obj["locations"]

    @staticmethod
    def get_config():
        if QTConfig.instance is None:
            QTConfig.instance = QTConfig()

        return QTConfig.instance

    @staticmethod
    def set_config(obj):
        QTConfig.get_config().__persist_changes(obj)

    @staticmethod
    def clear_config():
        QTConfig.create_default_config()

    @staticmethod
    def create_default_config():
        obj = {
            "db.path": "./db.json",
            "auto-csv": True,
            "env": "prod",
            "items": None,
            "locations": None,
        }
        with open('./config.yml', "w+") as file:
            yaml.dump(obj, file)
