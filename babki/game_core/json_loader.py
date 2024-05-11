import json

class JsonLoader:
    @staticmethod
    def load(file_name):
        with open(file_name, 'r') as file:
            return json.load(file)