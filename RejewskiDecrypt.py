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
        for config_str in itertools.product(ascii_lowercase, ascii_lowercase, ascii_lowercase):
            earmark = '-'.join([calc_earmark(d) for d in calc_middle_table(position_str, config_str)])
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
    earmark_dict_list = [dict(), dict(), dict()]
    for char in ascii_lowercase:
        machine = Enigma.EnigmaMachine()
        clear_text = char * 6
        machine.config_rotorset_dynamic(position_str, config_str)
        encrypt_text = machine.encrypt_str(clear_text)
        for i in range(3):
            earmark_dict_list[i][encrypt_text[i]] = encrypt_text[i+3]
    return earmark_dict_list


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
            if end not in item_list:
                item_list.append(end)
                start = end
            else:
                earmark_list.append(item_list)
                for item in item_list:
                    del table[item]
                break
    earmark_list = [len(li) for li in earmark_list]
    earmark_list.sort()
    earmark_len = '.'.join([str(s) for s in earmark_list])
    return earmark_len


def generate_middle_table(m_list):
    """
    模拟生成前6个字符的映射表, 即中间表
    :return: dict
    """
    earmark_dict_list = [dict(), dict(), dict()]
    for msg in m_list:
        for i in range(3):
            if msg[i] not in earmark_dict_list[i]:
                earmark_dict_list[i][msg[i]] = msg[i+3]
    for i in range(3):
        assert len(earmark_dict_list[i]) == 26, 'Error: numbers of messages not enough for middle table.'
    return earmark_dict_list


def generate_msg():
    """
    模拟生成今日的德军消息通信，其中正文都用ascii字母表模拟
    生成的通信信息保证了中间表足够生成
    :return:
    """
    m_list = list()
    head_set_list = ['', '', '']
    while True:
        # 模拟生成低质量的密钥
        # random_code = ''.join(sample(list(ascii_lowercase), 3))
        random_code = ''.join(sample(list(ascii_lowercase), 1)*3)
        machine = Enigma.EnigmaMachine()
        # 使用今日配置生成信息头部len(possible_list)
        machine.config_rotorset()
        machine.config_plugboard()
        head_msg = random_code * 2
        cipher_head_msg = machine.encrypt_str(head_msg)
        # 修改转子配置到随机密钥，生成正文信息密文
        machine.config_rotorset_dynamic(machine.rotorset.position_str, head_msg)
        cipher_msg = cipher_head_msg + machine.encrypt_str(ascii_lowercase)
        m_list.append(cipher_msg)
        # 保证了可以生成中间表
        for i in range(3):
            if cipher_msg[i] not in head_set_list[i]:
                head_set_list[i] += cipher_msg[i]
        for i in range(3):
            if len(head_set_list[i]) != 26:
                break
        else:
            break
    return m_list


def is_match(middle_table, possible_config):
    """
    判断是否复合中间表特性
    :type middle_table: object
    :param middle_table: dict, 中间表
    :param possible_config: tuple, 潜在比较对象配置
    :return:
    """
    return middle_table == calc_middle_table(*possible_config)


def decrypt_rotorset_config():
    """
    解密启动入口
    :return:
    """
    print 'INFO: start to generate middle table of today'
    # 模拟生成德军密文信息
    msg_list = generate_msg()
    middle_table_list = generate_middle_table(msg_list)
    earmark = '-'.join([calc_earmark(d) for d in deepcopy(middle_table_list)])
    # 查找可能的配置表
    with open('data.pkl') as f:
        earmark_table = p.load(f)
        print 'INFO: load earmark dict'
        possible_list = earmark_table[earmark]
        del earmark_table
    # ###############################################
    # # 当没有插线板时的暴力破解
    # checked_list = list()
    # for possible_config in possible_list:
    #     if is_match(middle_table_list, possible_config):
    #         # print "The config is:", possible_config
    #         checked_list.append(possible_config)
    # for possible_config in checked_list:
    #     print possible_config
    # ################################################
    # 有插线板时的方法是对所有的可能性都做一次解码分析
    machine = Enigma.EnigmaMachine()
    print len(possible_list)
    for possible_config in possible_list:
        print 20 * '#', possible_config
        for msg in msg_list:
            machine.config_rotorset_dynamic(*possible_config)
            print msg[:6], machine.encrypt_str(msg[:6])


if __name__ == '__main__':
    # chain_classify()
    decrypt_rotorset_config()
