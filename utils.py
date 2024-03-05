import json

def is_json(content):
    try:
        json.loads(content)
        return True
    except ValueError:
        return False