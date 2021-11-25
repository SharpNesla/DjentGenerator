import hashlib
from enum import Enum


def md5_from_str(string: str) -> int:
    return int(hashlib.md5(string.encode('utf-8')).hexdigest(), 16)

def enum_all_valuse_list(enum_instance: Enum):
    return list(map(lambda c: c.value, enum_instance))


