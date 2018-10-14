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


LIB_FILE_PATH='/home/logic/_workspace/kicad/kicad_library/kicad-symbols/taobao-osc.lib'
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
# $O_VALUE
#
DEF $O_VALUE Y 0 40 N N 1 F N
F0 "Y" 0 100 50 H V C CNN
F1 "$O_VALUE" 0 -100 50 H V C CNN
F2 "" 0 0 50 H I C CNN
F3 "" 0 0 50 H I C CNN
$$FPLIST
 Crystal*
$$ENDFPLIST
DRAW
S -30 -60 30 60 0 1 0 N
P 2 0 1 15 -50 -30 -50 30 N
P 2 0 1 15 50 -30 50 30 N
X 1 1 -100 0 50 R 50 50 1 1 P
X 2 2 100 0 50 L 50 50 1 1 P
ENDDRAW
ENDDEF
""")

C_DCM_UNIT_TEMPLATE=Template("""#
$$CMP $O_VALUE
D Unpolarized capacitor, small symbol, $C_KEYWORD
K capacitor cap $O_VALUE $C_KEYWORD
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

def getLibFile(three_digit_codes):
    text_content=[]
    for three_digit_code, keyword in three_digit_codes:
        # int_r_value = parseTextCode(three_digit_code)
        # r_three_digit_code = 'R'+getThreeDigitCode(int_r_value)
        text_content.append(C_LIB_UNIT_TEMPLATE.substitute(O_VALUE=three_digit_code))

    text_to_write = C_LIB_TEMPLATE.substitute(O_CONTENT=''.join(text_content))
    text_to_write = text_to_write.replace('\n\n','\n')

    with open(LIB_FILE_PATH, 'w') as f:
        f.write(text_to_write)


def getDcmFile(three_digit_codes):
    text_content=[]
    for three_digit_code, keyword in three_digit_codes:
        # int_r_value = parseTextCode(three_digit_code)
        # r_three_digit_code = 'C'+getThreeDigitCode(int_r_value)
        text_content.append(C_DCM_UNIT_TEMPLATE.substitute(O_VALUE=three_digit_code, C_KEYWORD=keyword))
    o_content = ''.join(text_content)

    text_to_write = C_DCM_TEMPLATE.substitute(O_CONTENT = o_content)

    with open(DCM_FILE_PATH, 'w') as f:
        f.write(text_to_write)

def main():
    readKeywordTable()
    with open('osc_value_list.csv','r') as f:
        raw_lines = f.readlines()
        raw_values = []
        for test_line in raw_lines:
            c_keyword = ''
            test_line = test_line.strip()
            if test_line.find('(') > 0:
                test_line = test_line.split('(')[1].replace(')','')
                p_value, n_value, u_value = d_keyword_lookup[test_line]['value']
                c_keyword = ' ,'.join([p_value+'(p)', n_value+'(n)', u_value+'(u)'])
            raw_values.append(('O'+test_line,c_keyword))

        getLibFile(raw_values)
        getDcmFile(raw_values)

if __name__ == '__main__':
    main()
