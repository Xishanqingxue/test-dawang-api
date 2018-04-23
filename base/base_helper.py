# -*- coding: UTF-8 -*-
import hashlib
import random


def md5(string):
    """
    创建md5加密字符串
    :param string:
    :return:
    """
    m = hashlib.md5()
    m.update(string.encode(encoding='UTF-8'))
    return m.hexdigest()


def generate_random_nickname(words=5):
    """
    生成一个随机昵称，以“测试”开头，words参数指定昵称字数
    :param words:
    :return:
    """
    name = '测试'
    for x in range(words-2):
        head = random.randint(0xb0, 0xf7)
        body = random.randint(0xa1, 0xf9)
        val = f'{head:x}{body:x}'
        str = bytes.fromhex(val).decode('gb2312')
        name += str
    return name

