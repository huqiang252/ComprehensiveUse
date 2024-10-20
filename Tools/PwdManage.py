#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : qiang.hu
# @Time: 2024-10-20

from ComDecorator.ComDeco import getRunTime
from Crypto.Cipher import AES
from binascii import b2a_hex,a2b_hex
import base64
import hashlib

class Md5Help():
    def _file_as_bytes(self,file):
        with file:
            return file.read()

    @getRunTime
    def md5_file(self,file):
        '''一般文件Md5签名'''
        return hashlib.md5(self._file_as_bytes(open(file,'rb'))).hexdigest()


    @getRunTime
    def md5_string(self,str):
        '''对字符串进行Md5签名'''
        h1 = hashlib.md5()
        h1.update(str.encode(encoding='utf-8'))
        return h1.hexdigest()


class AESHelp():
    def add_to_16(self,text):
        count = len(text.encode('utf-8'))
        length = 16
        if count<length:
            add = length-count
        elif count>length:
            add = (length-(count%length))
        text = text + ('\0'*add)
        return text.encode('utf-8')


    #加密函数
    def encrypt(self,text):
        key = '3ad3fda8deadfaf'.encode('utf-8')
        mode = AES.MODE_CBC
        iv = b'1213213123124'
        text = self.add_to_16(text)
        cryptos = AES.new(key,mode,iv)
        cipher_text = cryptos.encrypt(text)
        return b2a_hex(cipher_text)

    #解密函数
    def decrypt(self,text):
        key = '3ad3fda8deadfaf'.encode('utf-8')
        iv = b'1213213123124'
        mode = AES.MODE_CBC
        cryptos = AES.new( key, mode, iv )
        plain_text = cryptos.decrypt(a2b_hex(text))
        return bytes.decode(plain_text).rstrip('\0')
