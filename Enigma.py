#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
恩格玛机(Enigma machine)
"""

from string import ascii_lowercase
import ConfigParser
import json


class Rotor():
    """
    转子，进行加密的部件
    """

    def __init__(self, rotor_type, password_table):
        """
        初始化
        :param rotor_type: 转子的类型，中速，低速，高速
        """
        self.password_table = password_table
        self.rotor_type = rotor_type
        self.rotor_times = 0

    @property
    def get_current_table(self):
        """
        获取当前的正向映射表
        :return: dict
        """
        current_table = dict()
        current_table_str = self.password_table[self.rotor_times:] + \
            self.password_table[:self.rotor_times]
        for i in range(26):
            current_table[ascii_lowercase[i]] = current_table_str[i]
        return current_table

    def get_back_table(self):
        """
        获取当前反向映射表
        :return: dict
        """
        current_table = self.get_current_table
        back_table = dict()
        for k, v in current_table.items():
            back_table[v] = k
        return back_table

    def change(self, need_change):
        """
        改变转子状态
        :param need_change: 是否需要改变
        :return: boolean 是否进位
        """
        if need_change:
            self.rotor_times += 1
            if self.rotor_times >= 25:
                self.rotor_times %= 25
                return True
            else:
                return False
        else:
            return False

    def __cmp__(self, other):
        return cmp(self.rotor_type, other.rotor_type)

    def __repr__(self):
        return '<Rotor %r>' % self.rotor_type


class Keyboard():
    """
    键盘，输入使用
    """

    def __init__(self):
        self.char = ''

    def input(self):
        """
        键盘输入一个字母
        """
        while True:
            s = raw_input('Keyboard >>>').lower()
            if s in ascii_lowercase+'?' and len(s) == 1:
                self.char = s
                break
            else:
                print 'ERROR: illegal keybord input.'


class Lampboard():
    """
    灯盘,输出一个字母,代表经过加密之后的字母
    """

    def __init__(self):
        self.char = ''

    def output(self, char):
        """
        输出一个字母，模拟灯盘亮起
        :param char: 需要输出的字母
        """
        self.char = char
        print 'Lampboard: ' + char


class Plugboard():
    """
    插线板, 转子进行加密后, 为了进一步提高安全性而增加的装置
    """

    def __init__(self):
        self.table = dict()
        for i in range(26):
            self.table[ascii_lowercase[i]] = ascii_lowercase[i]

    def config(self, table):
        for k, v in table.items():
            self.table[k] = v
            self.table[v] = k


class RotorSet():
    """
    三个转子组成的转子簇
    """

    def __init__(self):
        self.rotorA = Rotor(0, 'computersvwxyzabdfghijklnq')
        self.rotorB = Rotor(1, 'hijklnqcomputersvwxyzabdfg')
        self.rotorC = Rotor(2, 'puteabdfgrsvimwxyjhklnqcoz')
        self.rotorList = self.rotorListSort = [self.rotorA, self.rotorB, self.rotorC]
        self.reflect_table = self._reflect_table()

    def config(self, position_str, config_str):
        """
        配置转子簇顺序
        :param position_str: str, 转子顺序的字符串表示，如'102'
        :param config_str: str, 转子的配置字符串表示, 如'abc'
        """
        for r in self.rotorList:
            r.rotor_type = int(position_str[self.rotorList.index(r)])
            r.rotor_times = ord(config_str[self.rotorList.index(r)]) - ord('a')
        self.rotorListSort.sort()

    def output(self, char):
        """
        转子簇输出
        :param char: 输入字符
        :return: 加密后的输出字符
        """
        c_dict = self.total_table()
        cipher_char = c_dict[char]
        self.change_status()
        return cipher_char

    def change_status(self):
        """
        改变转子簇状态
        :return: dict
        """
        need_change = True
        for r in self.rotorListSort:
            need_change = r.change(need_change)

    def _forward_table(self):
        """
        获取前向字符映射列表
        :return: dict
        """
        forward_list = list()
        for r in self.rotorListSort:
            forward_list.append(r.get_current_table)
        return forward_list

    def _backward_table(self):
        """
        获取反向字符映射列表
        :return: dict
        """
        backward_list = list()
        for r in self.rotorListSort:
            backward_list.append(r.get_back_table())
        backward_list.reverse()
        return backward_list

    def total_table(self):
        total_dict = dict()
        forward = self._forward_table()
        backward = self._backward_table()
        for c in ascii_lowercase:
            char = c
            for table in forward:
                char = table[char]
            char = self.reflect_table[char]
            for table in backward:
                char = table[char]
            total_dict[c] = char
        return total_dict

    @staticmethod
    def _reflect_table():
        """
        获取反射器的映射表
        :return: dict
        """
        r_dict = dict()
        reflect_str = ascii_lowercase[::-1]
        for i in range(26):
            r_dict[ascii_lowercase[i]] = reflect_str[i]
        return r_dict


class EnigmaMachine():
    """
    恩格玛机
    """
    def __init__(self):
        self.keybord = Keyboard()
        self.lampboard = Lampboard()
        self.plugboard = Plugboard()
        self.rotorset = RotorSet()

    def config_rotorset(self):
        """
        转子静态文件读取配置输入接口
        :return:
        """
        config = ConfigParser.ConfigParser()
        config.readfp(open('config.txt'))
        position_str = config.get('rotorset', 'position')
        config_str = config.get('rotorset', 'config')
        self.rotorset.config(position_str, config_str)

    def config_rotorset_dynamic(self, position_str, config_str):
        """
        转子动态设置配置输入接口
        :param position_str: str, 转子顺序的字符串表示，如'102'
        :param config_str: str, 转子的配置字符串表示, 如'abc'
        """
        self.rotorset.config(position_str, config_str)


    def config_plugboard(self):
        """
        插线板配置输入接口
        :return:
        """
        config = ConfigParser.ConfigParser()
        config.readfp(open('config.txt'))
        config_str = config.get('plugboard', 'config')
        self.plugboard.config(json.loads(config_str))

    def start(self):
        """
        机器启动接口
        :return:
        """
        print 'Enigma machine start'
        while True:
            self.keybord.input()
            clear_char = self.keybord.char
            if clear_char == '?':
                self.config_rotorset()
                self.config_plugboard()
            else:
                cipher_char = self.rotorset.output(clear_char)
                self.lampboard.output(cipher_char)

    def encrypt_str(self, clear_text):
        """
        加密字符串接口
        :param clear_text: str, 明文
        :return: str, 密文
        """
        cipher_text = ''
        for char in clear_text:
            cipher_text += self.rotorset.output(char)
        return cipher_text


if __name__ == '__main__':
    machine = EnigmaMachine()
    # machine.start()
    # print machine.encrypt_str('abcabc')
    machine.config_rotorset()
    machine.start()