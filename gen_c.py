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


LIB_FILE_PATH='/home/logic/_workspace/kicad/kicad_library/kicad-symbols/taobao-c.lib'
DCM_FILE_PATH=LIB_FILE_PATH.replace('.lib','.dcm')

C_LIB_TEMPLATE=Template("""EESchema-LIBRARY Version 2.4
#encoding utf-8
$C_CONTENT
#
#End Library""")

C_DCM_TEMPLATE=Template("""EESchema-DOCLIB  Version 2.0
$C_CONTENT#
#End Doc Library""")

FP_TEMPLATE="""C_0805*
 C_0603*
 C_1206*
 C_1210*
"""

C_LIB_UNIT_TEMPLATE=Template("""#
# $C_VALUE
#
DEF $C_VALUE C 0 10 N N 1 F N
F0 "C" 10 70 50 H V L CNN
F1 "$C_VALUE" 10 -80 50 H V L CNN
F2 "" 0 0 50 H I C CNN
F3 "" 0 0 50 H I C CNN
$$FPLIST
 $C_FOOTPRINT
$$ENDFPLIST
DRAW
P 2 0 1 13 -60 -20 60 -20 N
P 2 0 1 12 -60 20 60 20 N
X ~ 1 0 100 80 D 50 50 1 1 P
X ~ 2 0 -100 80 U 50 50 1 1 P
ENDDRAW
ENDDEF
""")

C_DCM_UNIT_TEMPLATE=Template("""#
$$CMP $C_VALUE
D Unpolarized capacitor, small symbol, $C_KEYWORD
K capacitor cap $C_VALUE $C_KEYWORD
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
    for three_digit_code, keyword, cap_sizes,cap_voltage in three_digit_codes:
        # int_r_value = parseTextCode(three_digit_code)
        # r_three_digit_code = 'R'+getThreeDigitCode(int_r_value)
        cap_footprint = FP_TEMPLATE
        if len(cap_sizes) > 0:
            cap_footprint = '\n'.join([ "C"+"*"+cap_size+"*"  for cap_size in cap_sizes.split('/')])
        text_content.append(C_LIB_UNIT_TEMPLATE.substitute(
            C_VALUE=three_digit_code,
            C_FOOTPRINT=cap_footprint
        ))

    text_to_write = C_LIB_TEMPLATE.substitute(C_CONTENT=''.join(text_content)).strip()

    with open(LIB_FILE_PATH, 'w') as f:
        f.write(text_to_write)


def getDcmFile(three_digit_codes):
    text_content=[]
    for three_digit_code, keyword, cap_size,cap_voltage in three_digit_codes:
        # int_r_value = parseTextCode(three_digit_code)
        # r_three_digit_code = 'C'+getThreeDigitCode(int_r_value)
        text_content.append(C_DCM_UNIT_TEMPLATE.substitute(C_VALUE=three_digit_code, C_KEYWORD=keyword))
    c_content = ''.join(text_content)

    text_to_write = C_DCM_TEMPLATE.substitute(C_CONTENT = c_content)

    text_to_write = text_to_write.replace('\n\n','\n')

    with open(DCM_FILE_PATH, 'w') as f:
        f.write(text_to_write)

def main():
    readKeywordTable()
    with open('c_value_list.csv','r') as f:
        raw_lines = f.readlines()
        raw_values = []
        for test_line in raw_lines:
            c_keyword = ''
            test_line = test_line.strip()

            try:
                cap_name, cap_size, cap_voltage = test_line.split(',')
            except Exception as e:
                print(test_line.split(','))
                print(cap_size)

            if cap_name.find('(') > 0:
                cap_name = cap_name.split('(')[1].replace(')','')
                p_value, n_value, u_value = d_keyword_lookup[cap_name]['value']
                c_keyword = ' ,'.join([p_value+'(p)', n_value+'(n)', u_value+'(u)'])

            cap_name = '-'.join([cap_name, cap_voltage]) if len(cap_voltage) > 0 else cap_name

            raw_values.append(('C'+cap_name.lower(),c_keyword, cap_size, cap_voltage))

        getLibFile(raw_values)
        getDcmFile(raw_values)

if __name__ == '__main__':
    main()
