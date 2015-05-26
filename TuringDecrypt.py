# -*- coding: utf-8 -*-
__author__ = 'guti'

import itertools
import Enigma
from copy import deepcopy
from string import ascii_lowercase


def generate_encrypt():
    clear_text = 'keinebesonderenereignisse'
    machine = Enigma.EnigmaMachine()
    machine.config_rotorset()
    return machine.encrypt_str(clear_text)


def decrypt_rotorset_config():
    possible_list = []
    for position_str in itertools.permutations('012', 3):
        for config_str in itertools.permutations(ascii_lowercase, 3):
            if is_match(position_str, config_str):
                possible_list.append((position_str, config_str))
        break
    return possible_list


def is_match(position_str, config_str):
    rotor_set0 = Enigma.RotorSet()
    rotor_set0.config(position_str, config_str)
    rotor_set1 = deepcopy(rotor_set0)
    rotor_set5 = deepcopy(rotor_set0)
    rotor_set1.change_status()
    for i in range(5):
        rotor_set5.change_status()
    for char in ascii_lowercase:
        out_put = rotor_set5.output(rotor_set1.output(rotor_set1.output(char)))
        if out_put != char:
            return False
    else:
        return True


if __name__ == '__main__':
    # print decrypt_rotorset_config()
    print generate_encrypt()


