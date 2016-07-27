import json
import os


def load_schema(name):
    current_dir = os.path.dirname(__file__)
    with open(os.path.join(current_dir, name + '.json')) as f:
        schema = json.load(f)

    return schema
