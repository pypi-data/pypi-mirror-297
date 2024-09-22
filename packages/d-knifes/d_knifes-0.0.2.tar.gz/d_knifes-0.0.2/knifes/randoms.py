import random
import string
from knifes import times
import uuid

id_alphabet = string.ascii_uppercase + string.digits


def random_str(length=4):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))


# 32位唯一的字符串
def make_unique_str():
    return str(uuid.uuid4()).replace('-', '')


# 碰撞概率极小的(唯一的)随机ID
# 长度 >= 10
def random_str_id(length=10):
    id_ = get_short_code_from_num(times.current_milli_time())
    if len(id_) < length:
        return ''.join(random.choices(id_alphabet, k=length - len(id_))) + id_
    elif len(id_) > length:
        return id_[0:length]
    else:
        return id_


def get_short_code_from_num(num):
    code = ''
    while num > 0:
        index = num % 36
        num = (num - index) // 36
        code = id_alphabet[index] + code
    return code
