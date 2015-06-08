# -*- coding: utf-8 -*-
__author__ = 'guti'

import itertools
import Enigma
from copy import deepcopy
from string import ascii_lowercase


def generate_encrypt(clear_text):
    machine = Enigma.EnigmaMachine()
    machine.config_rotorset()
    machine.config_plugboard()
    return machine.encrypt_str(clear_text)


def decrypt_rotorset_config():
    possible_list = []
    for position_str in itertools.permutations('012', 3):
        for config_str in itertools.product(ascii_lowercase, ascii_lowercase, ascii_lowercase):
            if is_match(position_str, config_str):
                possible_list.append((position_str, config_str))
    return possible_list


def decrypt_possible_config(possible_list):
    checked_list = list()
    for item in possible_list:
        if is_match(item[0], item[1]):
            checked_list.append(item)
    return checked_list


def is_match(position_str, config_str):
    rotor_set_0 = Enigma.RotorSet()
    rotor_set_0.config(position_str, config_str)
    rotor_set_i = deepcopy(rotor_set_0)
    rotor_set_j = deepcopy(rotor_set_0)
    rotor_set_k = deepcopy(rotor_set_0)
    for i in range(7):
        rotor_set_0.change_status()
    for i in range(14):
        rotor_set_i.change_status()
    for i in range(16):
        rotor_set_j.change_status()
    for i in range(22):
        rotor_set_k.change_status()
    for char in ascii_lowercase:
        out_put = rotor_set_k.output1(rotor_set_j.output1(rotor_set_i.output1(rotor_set_0.output1(char))))
        if out_put == char:
            return True
    else:
        return False




if __name__ == '__main__':
    # print decrypt_rotorset_config()
    clear_text = 'keinebesonderenereignisse'
    print clear_text
    print generate_encrypt(clear_text)
    p_list = decrypt_rotorset_config()
    print len(p_list)


