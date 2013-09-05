#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
Crypt model, encrypt text
"""

import base64


ORIG_MAP = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
DEFAULT_MAP_RANK = 8
DEFAULT_MAP_SCALE = 64
CRYPT_DIRECTION_HORIZONTAL = -1
CRYPT_DIRECTION_VERTICAL = 1
CRYPT_ENCRYPT = 1
CRYPT_DECRYPT = -1


def build_map(key=""):
    """
    Generate a crypt map for encrypt and decrypt.
    """
    map_set = set(ORIG_MAP)
    crypt_map = ""
    for char in list(key):
        if char in map_set:
            crypt_map += char
            map_set.discard(char)
    crypt_map += "".join(sorted(list(map_set), key=lambda x: ORIG_MAP.find(x)))
    return crypt_map


def transform(keymap, flag, src, direction=CRYPT_DIRECTION_VERTICAL):
    """
    Transform metod transform two character of original text or
    cihper text to cipher text base on keymap
    """
    if len(src) != 2:
        pass
    rank = DEFAULT_MAP_RANK
    scale = DEFAULT_MAP_SCALE
    posl_old = keymap.find(src[0])
    posr_old = keymap.find(src[1])
    deltax = (posl_old % 8) - (posr_old % 8)
    deltay = (posl_old / 8) - (posr_old / 8)
    if deltax == 0 and deltay == 0:
        posl_new = scale - posl_old - 1
        posr_new = scale - posr_old - 1
    elif deltax == 0:
        posl_new = (posl_old + rank * flag) % scale
        posr_new = (posr_old + rank * flag) % scale
    elif deltay == 0:
        posl_new = posl_old / rank * rank + (posl_old + flag) % rank
        posr_new = posr_old / rank * rank + (posr_old + flag) % rank
    else:
        if direction == CRYPT_DIRECTION_VERTICAL:
            posl_new = posl_old - deltay * rank
            posr_new = posr_old + deltay * rank
        else:
            posl_new = posl_old - deltax
            posr_new = posr_old + deltax
    des = keymap[posl_new] + keymap[posr_new]
    return des


def encrypt(original_text, key="", direction=CRYPT_DIRECTION_VERTICAL):
    """
    Encrypt text with specify key.
    """
    crypt_map = build_map(key)
    b64_text = base64.b64encode(original_text).strip()
    while b64_text[-1] == "=":
        b64_text = b64_text[:-1]
    cipher_text = ""
    for idx in range(0, len(b64_text) / 2 * 2, 2):
        cipher_text += transform(crypt_map, CRYPT_ENCRYPT,
                                 b64_text[idx: idx + 2], direction)
    if len(b64_text) % 2:
        cipher_text += b64_text[-1]
    return cipher_text


def decrypt(cipher_text, key="", direction=CRYPT_DIRECTION_VERTICAL):
    """
    Decrypt text with specify key.
    """
    crypt_map = build_map(key)
    b64_text = ""
    for idx in range(0, len(cipher_text) / 2 * 2, 2):
        b64_text += transform(crypt_map, CRYPT_DECRYPT,
                              cipher_text[idx: idx + 2], direction)
    if len(cipher_text) % 2:
        b64_text += cipher_text[-1]
    b64_text += "=" * (3 - ((len(b64_text) - 1) % 4))
    original_text = base64.b64decode(b64_text)
    return original_text


if __name__ == "__main__":
    print encrypt("lykling")
    print decrypt("DftjDetmxY")
