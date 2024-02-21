import json


def get_config():
    with open("app_config.json", 'r') as file:
        _ = json.load(file)
    return _
