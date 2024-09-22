import json
import os

class Config:
    @staticmethod
    def load(path):
        path = os.path.expanduser(path)
        if not os.path.exists(path):
            default_config = {"projects": []}
            with open(path, 'w') as file:
                json.dump(default_config, file)
        with open(path, 'r') as file:
            return json.load(file)

