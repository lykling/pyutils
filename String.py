#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
String module, some utils of string
"""

import random


def randstr(length):
    """
    generate a random string with length $length
    """
    return ''.join([chr(random.randint(32, 127)) for i in range(length)])

def int2buf(src, length=1):
    """
    convert integer to buffer string
    """
    result = []
    while length:
        result.insert(0, chr(src & 0xff))
        src = src >> 8
        length -= 1
    return ''.join(result)


if __name__ == "__main__":
    print randstr(10);
