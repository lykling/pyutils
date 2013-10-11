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


if __name__ == "__main__":
    print randstr(10);
