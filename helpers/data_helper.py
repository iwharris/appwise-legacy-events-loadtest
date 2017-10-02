import random
import string
import json


# Utility functions

def random_string(length=10):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))


def random_url():
    return 'https://fake-url.com/{}'.format(random_string())


def object_to_json(obj):
    return json.dumps(obj, default=lambda o: o.__dict__)
