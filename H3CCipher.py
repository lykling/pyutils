#!/usr/bin/env python
#-*- coding: utf-8 -*-
import os
import sys
from Crypto.Cipher import DES
from optparse import OptionParser

__version__ = '1.0'

KEY = '\x01\x02\x03\x04\x05\x06\x07\x08'


def filltext(text='', det=8):
    if len(text) <= det:
        text += '\x00' * det
    return text + '\x00' * (((len(text) - 1) / det + 1) * det - len(text))


def ascii2binary(text=None):
    textlen = len(text)
    result = ''
    chtag = ord('a')
    for cnt in range(0, textlen, 4):
        ch1 = ord(text[cnt])
        if ch1 == chtag:
            ch1 = ord('?')
        ch2 = ch1 - 33

        ch1 = ord(text[cnt+1])
        if ch1 != chtag:
            ch2 = ch2 << 6
        else:
            ch1 = ord('?')
        ch1 = ch1 - 33
        ch2 = ch2 | ch1

        ch1 = ord(text[cnt+2])
        if ch1 != chtag:
            ch2 = ch2 << 6
        else:
            ch1 = ord('?')
        ch1 = ch1 - 33
        ch2 = ch2 | ch1

        ch1 = ord(text[cnt+3])
        if ch1 != chtag:
            ch2 = ch2 << 6
        else:
            ch1 = ord('?')
        ch1 = ch1 - 33
        ch2 = ch2 | ch1
        result += chr((ch2 >> 0x10) & 0xff)
        result += chr((ch2 >> 0x08) & 0xff)
        result += chr(ch2 & 0xff)

    return result


def binary2ascii(text=None):
    textlen = len(text)
    result = ''
    for cnt in range(0, textlen, 3):
        tmp = (ord(text[cnt]) << 0x10) +\
              (ord(text[cnt+1]) << 0x08) + ord(text[cnt+2])
        or1 = (tmp & 0x3f) + 33
        or2 = ((tmp >> 0x06) & 0x3f) + 33
        or3 = ((tmp >> 0x0c) & 0x3f) + 33
        or4 = ((tmp >> 0x12) & 0x3f) + 33
        result += chr(or4) + chr(or3) + chr(or2) + chr(or1)

    return result


def encrypt(text=None):
    binarytext = DES.new(KEY, DES.MODE_ECB).encrypt(filltext(text))
    return binary2ascii(filltext(binarytext, 6)).rstrip('\x00')


def decrypt(cipher=None):
    binarytext = filltext(ascii2binary(cipher))
    res = DES.new(KEY, DES.MODE_ECB).decrypt(binarytext)
    return res[:res.find('\x00')]


def main(argv=None):
    prog = os.path.basename(sys.argv[0])
    optparser = OptionParser(version='%s: %s' % (prog, __version__))
    optparser.add_option('-e', '--encrypt', dest='text', action='store',
                         help='encrypt text')
    optparser.add_option('-d', '--decrypt', dest='cipher', action='store',
                         help='decrypt text')
    optparser.add_option('-t', '--test', dest='test', action='store_true',
                         help='test case')
    opts, params = optparser.parse_args()

    if opts.text:
        print 'encrypt:'
        print opts.text, '-->', encrypt(opts.text)
    elif opts.cipher:
        print 'decrypt:'
        print opts.cipher, '-->', decrypt(opts.cipher)
    elif opts.test:
        test()


def test():
    cipher = '@BKE3/7]F<1BZ@@`]\'"C3Q!!'
    print 'decrypt:'
    print cipher, '-->', decrypt(cipher)

    text = 'z9gaimimalo'
    print 'encrypt:'
    print text, '-->', encrypt(text)

    text = '20051001'
    print 'encrypt:'
    print text, '-->', encrypt(text)

    text = 'since2004'
    print 'encrypt:'
    print text, '-->', encrypt(text)

    text = 'since2004.'
    print 'encrypt:'
    print text, '-->', encrypt(text)


if __name__ == '__h3c_cipher__':
    pass


if __name__ == '__main__':
    main()
