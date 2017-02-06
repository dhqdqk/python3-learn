#!/usr/bin/env python
# coding:utf-8

import base64

'''
base64编码原理：
首先，准备一个包含64个字符的数组
对二进制数据进行处理，每3个字节一组，一共是3x8=24bit，划为4组，每组正好6个bit
4个数字作为索引，然后查表，获得相应的4个字符，就是编码后的字符串。
Base64编码会把3字节的二进制数据编码为4字节的文本数据，长度增加33%，
Base64编码的长度永远是4的倍数

base64.urlsafe_b64encode()处理URL的编码

Base64是一种通过查表的编码方法，不能用于加密，即使使用自定义的编码表也不行。

Base64适用于小段内容的编码，比如数字证书签名、Cookie的内容等。
'''

b1 = b'binary\x00string'
b1_encode = base64.b64encode(b1)
print(b1_encode)
b1_decode = base64.b64decode(b1_encode)
print(b1_decode)

b2 = b'i\xb7\x1d\xfb\xef\xff'
b2_encode = base64.b64encode(b2)
print(b2_encode)
b2_sencode = base64.urlsafe_b64encode(b2)
print(b2_sencode)
print(base64.urlsafe_b64decode(b2_sencode))

def safe_base64_decode(s):
    m = len(s) % 4
    print(m)
    if m:
        s = s + b'=' * (4 - m)
    # print(s)
    return base64.b64decode(s)


print(safe_base64_decode(b'YWJjZA'))
