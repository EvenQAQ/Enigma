#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
恩格玛机(Enigma machine)起源解释程序
"""

__author__ = 'guti'


def replace_encrypt(clear_text, password_table):
    """
    单字母替换加密
    :param clear_text: str, 明文，需要加密的内容, 假设输入为小写
    :param password_table: dict, 密码表
    :return: str, 密文, 加密后的内容
    """
    cipher_text = ''
    for char in clear_text:
        cipher_text += password_table[char]
    return cipher_text


def multi_char_encrypt(clear_text,  cipher_code, password_table):
    """
    多字母替换加密
    :param clear_text: str, 明文， 假设输入为小写
    :param cipher_code: str, 密钥
    :param password_table: list, 二维表
    :return:
    """
    cipher_text = ''
    for i in range(len(clear_text)):
        row = ord(cipher_code[i % len(cipher_code)]) - ord('a')
        col = ord(clear_text[i]) - ord('a')
        cipher_text += password_table[row][col]
    return cipher_text


def test_replace_encrypt():
    """
    单字母替换加密测试
    """
    password_table = {'a': 'C', 'b': 'O', 'c': 'M', 'd': 'P', 'e': 'U', 'f': 'T', 'g': 'E', 'h': 'R', 'i': 'S',
                      'j': 'V', 'k': 'W', 'l': 'X', 'm': 'Y', 'n': 'Z', 'o': 'A', 'p': 'B', 'q': 'D', 'r': 'F',
                      's': 'G', 't': 'H', 'u': 'I', 'v': 'J', 'w': 'K', 'x': 'L', 'y': 'N', 'z': 'Q'}
    clear_text = 'theimitationgame'
    cipher_text = replace_encrypt(clear_text, password_table)
    print 'clear text is : ' + clear_text
    print 'cipher text is : ' + cipher_text


def test_multi_char_encrypt():
    """
    多字母替换加密测试
    :return:
    """
    from string import ascii_lowercase as alpha_str
    # 生成维热纳尔方阵
    vigenere_square = list()
    for i in range(len(alpha_str)):
        forward_str = alpha_str[i:] + alpha_str[:i]
        vigenere_square.append(forward_str)
    # 加密密钥
    cipher_code = 'xjtu'
    clear_text = 'theimitationgame'
    cipher_text = multi_char_encrypt(clear_text, cipher_code, vigenere_square)
    print 'clear text is : ' + clear_text
    print 'cipher text is : ' + cipher_text


if __name__ == '__main__':
    test_multi_char_encrypt()