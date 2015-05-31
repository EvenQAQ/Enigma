# -*- coding: utf-8 -*-
__author__ = 'guti'


import itertools
import cPickle as p
import Enigma
from string import ascii_lowercase
from copy import deepcopy
from random import sample


def chain_classify():
    """
    模拟对每一种组合所产生的字母链条数量和长度进行了分类(波兰人花了一年的时间)
    真实场景下波兰人应该简化了运算
    :return:
    """
    earmark_table = dict()
    for position_str in itertools.permutations('012', 3):
        for config_str in itertools.permutations(ascii_lowercase, 3):
            c_dict = calc_middle_table(position_str, config_str)
            earmark = calc_earmark(c_dict)
            if earmark in earmark_table:
                earmark_table[earmark].append((position_str, config_str))
                pass
            else:
                earmark_table[earmark] = [(position_str, config_str)]
    with open('data.pkl', 'w') as f:
        p.dump(earmark_table, f)


def calc_middle_table(position_str, config_str):
    """
    计算一个映射表的中间表
    :param position_str:
    :param config_str:
    :return:
    """
    c_dict = dict()
    for char in ascii_lowercase:
        machine = Enigma.EnigmaMachine()
        clear_text = char * 6
        machine.config_rotorset_dynamic(position_str, config_str)
        encrypt_text = machine.encrypt_str(clear_text)
        c_dict[encrypt_text[0]] = encrypt_text[3]
    return c_dict


def calc_earmark(table):
    """
    计算链条的数量和长度
    :param table: dict, 字符映射表, 单次计算不需要太多时间
    :return: str
    """
    earmark_list = list()
    while True:
        if len(table) == 0:
            break
        start = table.keys()[0]
        item_list = [start]
        while True:
            end = table[start]
            if end != table.keys()[0]:
                item_list.append(end)
                start = end
            else:
                earmark_list.append(item_list)
                for item in item_list:
                    del table[item]
                break
    earmark_len = '.'.join([str(len(li)) for li in earmark_list])
    return earmark_len


def generate_middle_table():
    """
    模拟生成前6个字符的映射表, 即中间表
    :return: dict
    """
    c_dict = dict()
    while True:
        random_code = sample(list(ascii_lowercase), 3)
        machine = Enigma.EnigmaMachine()
        machine.config_rotorset()
        random_code *= 2
        encrypt_text = machine.encrypt_str(random_code)
        if encrypt_text[0] not in c_dict:
            c_dict[encrypt_text[0]] = encrypt_text[3]
        if len(c_dict) == 26:
            break
    return c_dict


def is_match(middle_table, possible_config):
    """
    判断是否复合中间表特性
    :type middle_table: object
    :param middle_table: dict, 中间表
    :param possible_config: tuple, 潜在比较对象配置
    :return:
    """
    for char in ascii_lowercase:
        machine = Enigma.EnigmaMachine()
        clear_text = char * 6
        machine.config_rotorset_dynamic(*possible_config)
        encrypt_text = machine.encrypt_str(clear_text)
        if middle_table[encrypt_text[0]] != encrypt_text[3]:
            return False
    else:
        return True


def decrypt_rotorset_config():
    print 'INFO: start to generate middle table of today'
    # middle_table = {'a': 'u', 'c': 'n', 'b': 'r', 'e': 'g', 'd': 'm', 'g': 'a', 'f': 'o', 'i': 'w', 'h': 't',
    #                 'k': 's', 'j': 'e', 'm': 'p', 'l': 'v', 'o': 'z', 'n': 'd', 'q': 'k', 'p': 'b', 's': 'q',
    #                 'r': 'l', 'u': 'i', 't': 'x', 'w': 'f', 'v': 'y', 'y': 'c', 'x': 'h', 'z': 'j'}
    middle_table = generate_middle_table()
    middle_table_copy = deepcopy(middle_table)
    earmark = calc_earmark(middle_table_copy)
    with open('data.pkl') as f:
        earmark_table = p.load(f)
        print 'INFO: load earmark dict'
        possible_list = earmark_table[earmark]
        # print len(earmark_table)
        del earmark_table
        # print len(possible_list)
        for possible_config in possible_list:
            if is_match(middle_table, possible_config):
                print "The config is:", possible_config
                break


if __name__ == '__main__':
    # chain_classify()
    decrypt_rotorset_config()
