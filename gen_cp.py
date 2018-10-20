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


LIB_FILE_PATH='/home/logic/_workspace/kicad/kicad_library/kicad-symbols/taobao-cp.lib'
DCM_FILE_PATH=LIB_FILE_PATH.replace('.lib','.dcm')

C_LIB_TEMPLATE=Template("""EESchema-LIBRARY Version 2.4
#encoding utf-8
$C_CONTENT
#
#End Library""")

C_DCM_TEMPLATE=Template("""EESchema-DOCLIB  Version 2.0
$C_CONTENT#
#End Doc Library""")

C_LIB_UNIT_TEMPLATE=Template("""#
# $component_name
#
DEF $component_name C 0 10 N N 1 F N
F0 "C" 10 70 50 H V L CNN
F1 "$component_name" 10 -80 50 H V L CNN
F2 "" 0 0 50 H I C CNN
F3 "" 0 0 50 H I C CNN
$$FPLIST
 CP_Elec*$C_SIZE
$$ENDFPLIST
DRAW
S -60 -12 60 -27 0 1 0 F
S -60 27 60 12 0 1 0 N
P 2 0 1 0 -50 60 -30 60 N
P 2 0 1 0 -40 50 -40 70 N
X ~ 1 0 100 73 D 50 50 1 1 P
X ~ 2 0 -100 73 U 50 50 1 1 P
ENDDRAW
ENDDEF
""")

C_DCM_UNIT_TEMPLATE=Template("""#
$$CMP $component_name
D Polarized capacitor, small symbol
K cap capacitor 铝电解电容 https://item.taobao.com/item.htm?spm=2013.1.0.0.372d47d1RDfViZ&id=571150150979
F ~
$$ENDCMP
""")

translate_size={
    '6*7MM':'6.3x7.7',
    '6*5MM':'6.3x5.2',
    '5*5MM':'5x5.3',
    '4*5MM':'4x5.3',
    '10.5*10MM':'10x10.5'
}

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
        cp_voltage, cp_size = keyword.split(',')
        c_size = translate_size[cp_size]+'*'
        text_content.append(C_LIB_UNIT_TEMPLATE.substitute(component_name=','.join([three_digit_code, cp_voltage]),C_SIZE=c_size))

    text_to_write = C_LIB_TEMPLATE.substitute(C_CONTENT=''.join(text_content)).strip()

    with open(LIB_FILE_PATH, 'w') as f:
        f.write(text_to_write)


def getDcmFile(three_digit_codes):
    text_content=[]
    for three_digit_code, keyword in three_digit_codes:
        # int_r_value = parseTextCode(three_digit_code)
        # r_three_digit_code = 'C'+getThreeDigitCode(int_r_value)
        cp_voltage, cp_size = keyword.split(',')
        text_content.append(C_DCM_UNIT_TEMPLATE.substitute(component_name=','.join([three_digit_code, cp_voltage]), C_KEYWORD=keyword))
    c_content = ''.join(text_content)

    text_to_write = C_DCM_TEMPLATE.substitute(C_CONTENT = c_content)
    text_to_write = text_to_write.replace('\n\n','\n')

    with open(DCM_FILE_PATH, 'w') as f:
        f.write(text_to_write)

def main():
    readKeywordTable()
    with open('cp_value_list.csv','r') as f:
        raw_lines = f.readlines()
        raw_values = []
        for test_line in raw_lines:
            c_keyword = ''
            test_line = test_line.strip()
            cp_value, cp_voltage, cp_size = test_line.split(',')

            c_keyword = ','.join([cp_voltage, cp_size])

            raw_values.append(('CP'+cp_value,c_keyword))

        getLibFile(raw_values)
        getDcmFile(raw_values)

if __name__ == '__main__':
    main()
