import random
import string


def generate_secure_code() -> str:
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))


def control_required_keys(data: dict, required_keys: list) -> str:
    for key in required_keys:
        if key not in data:
            return key
    return 'ok'
