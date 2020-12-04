import itertools
import operator
import functools
from collections import namedtuple
import re
import sys

sys.path.append('../..')

import utils

test_data_invalid = """
eyr:1972 cid:100
hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

iyr:2019
hcl:#602927 eyr:1967 hgt:170cm
ecl:grn pid:012533040 byr:1946

hcl:dab227 iyr:2012
ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

hgt:59cm ecl:zzz
eyr:2038 hcl:74454a iyr:2023
pid:3556412378 byr:2007
"""

test_data_valid = """
pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
hcl:#623a2f

eyr:2029 ecl:blu cid:129 byr:1989
iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

hcl:#888785
hgt:164cm byr:2001 iyr:2015 cid:88
pid:545766238 ecl:hzl
eyr:2022

iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719
"""

keys_required = [ 'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']

def valid_passport(passport, validate):
    all_found = all(key in passport for key in keys_required)
    if validate == False or all_found == False:
        return all_found

    # must validate all inputs.  Just use RE to match all keys
    key_dict = dict(x.groups() for x in re.finditer(r"\s*(\w+)\:(\#*\w+)\s*", passport))

    try:
        length, metric = re.match(r'(\d+)(cm|in)', key_dict['hgt']).groups()
        hair_color = re.match(r'\#([0-9a-f]{6})', key_dict['hcl']).groups()
        eye_color = re.match(r'(amb|blu|brn|gry|grn|hzl|oth)', key_dict['ecl']).groups()
        pid = re.match(r'(\d{9})\b', key_dict['pid']).groups()
    except AttributeError:
        return False

    l = int(length)
    if metric == 'cm' and (l < 150 or l > 193):
        return False
    if metric == 'in' and (l < 59 or l > 76):
        return False

    if (1920 <= int(key_dict['byr']) <= 2002) and (2010 <= int(key_dict['iyr']) <= 2020) and (2020 <= int(key_dict['eyr']) <= 2030):
        if (key_dict['pid'] == '9833212692'):
            print (key_dict)
        return True

    return False



def count_valid_passports(passports, validate):
    num_valid = sum(1 if valid_passport(p, validate) else 0 for p in passports)
    return num_valid


if __name__ == '__main__':
    with open('input.txt') as f:
        data = f.read()

    passports = data.split('\n\n')
    num_valid = count_valid_passports(passports, False)
    print(num_valid)

    num_accurate = count_valid_passports(passports, True)
    print(num_accurate)
