#!/usr/bin/env python
# coding:utf-8

import os
import sys
import logging
import traceback
from pprint import pprint
from math import log10, floor
from string import Template
import csv

FILE_VALUE_LIST='mounting_value_list.csv'
LIB_FILE_PATH='/home/logic/_workspace/kicad/kicad_library/kicad-symbols/taobao-mounting-hole.lib'
DCM_FILE_PATH=LIB_FILE_PATH.replace('.lib','.dcm')

C_LIB_TEMPLATE=Template("""EESchema-LIBRARY Version 2.4
#encoding utf-8
$O_CONTENT
#
#End Library""")

C_DCM_TEMPLATE=Template("""EESchema-DOCLIB  Version 2.0
$O_CONTENT#
#End Doc Library""")

C_LIB_UNIT_TEMPLATE=Template("""#
# $M_VALUE
#
DEF $M_VALUE H 0 40 Y Y 1 F N
F0 "H" 0 200 50 H V C CNN
F1 "$M_VALUE" 0 125 50 H V C CNN
F2 "" 0 0 50 H I C CNN
F3 "" 0 0 50 H I C CNN
$$FPLIST
 $M_FOOTPRINT
$$ENDFPLIST
DRAW
C 0 0 50 0 1 50 N
ENDDRAW
ENDDEF
""")

C_DCM_UNIT_TEMPLATE=Template("""#
$$CMP $M_VALUE
D Mounting Hole
K mounting hole $M_VALUE
F ~
$$ENDCMP
""")

d_keyword_lookup = {}
def readKeywordTable():
    for row in csv.reader(open('./c_code_mapping_table.csv','r').readlines()):
        p_value, n_value, u_value, code=row
        d_keyword_lookup[code]={'value':[p_value, n_value, u_value]}


def parseTextCode(number_value):
    factor = 1
    if number_value.find('K') ==1:
        if len(number_value) == 3:
            factor = 100
        if len(number_value) == 2:
            factor = 1000

    if number_value.find('K') == 2:
        factor = 1000
    if number_value.find('K') == 3:
        factor = 1000

    return int(number_value.replace('K','')) * factor

def getThreeDigitCode(int_r_value):
    str_r_value = str(int_r_value)
    no_of_zero = floor(log10(int_r_value))
    left_2_digit = str_r_value[0:2]
    last_digit = str(no_of_zero-1)
    return left_2_digit+last_digit

def getLibFile(raw_values):
    text_content=[]
    for mounting_value, mounting_footprint in raw_values:
        # int_r_value = parseTextCode(three_digit_code)
        # r_three_digit_code = 'R'+getThreeDigitCode(int_r_value)
        text_content.append(C_LIB_UNIT_TEMPLATE.substitute(
            M_VALUE=mounting_value,
            M_FOOTPRINT='*%s*' % mounting_footprint
            ))

    text_to_write = C_LIB_TEMPLATE.substitute(O_CONTENT=''.join(text_content))
    text_to_write = text_to_write.replace('\n\n','\n')

    with open(LIB_FILE_PATH, 'w') as f:
        f.write(text_to_write)


def getDcmFile(three_digit_codes):
    text_content=[]
    for three_digit_code, keyword in three_digit_codes:
        # int_r_value = parseTextCode(three_digit_code)
        # r_three_digit_code = 'C'+getThreeDigitCode(int_r_value)
        text_content.append(C_DCM_UNIT_TEMPLATE.substitute(M_VALUE=three_digit_code, C_KEYWORD=keyword))
    o_content = ''.join(text_content)

    text_to_write = C_DCM_TEMPLATE.substitute(O_CONTENT = o_content)

    with open(DCM_FILE_PATH, 'w') as f:
        f.write(text_to_write)

def main():
    readKeywordTable()
    with open(FILE_VALUE_LIST,'r') as f:
        raw_lines = f.readlines()
        raw_values = []
        for test_line in raw_lines:
            c_keyword = ''
            test_line = test_line.strip()
            # if test_line.find('(') > 0:
            #     test_line = test_line.split('(')[1].replace(')','')
            #     p_value, n_value, u_value = d_keyword_lookup[test_line]['value']
            #     c_keyword = ' ,'.join([p_value+'(p)', n_value+'(n)', u_value+'(u)'])

            mounting_value = test_line.split(',')[0]
            mounting_footprint = "MountingHole*%s*" % mounting_value
            raw_values.append(('MOUNT_'+mounting_value, mounting_footprint))

        getLibFile(raw_values)
        getDcmFile(raw_values)

if __name__ == '__main__':
    main()
