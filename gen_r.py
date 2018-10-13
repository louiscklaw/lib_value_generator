#!/usr/bin/env python
# coding:utf-8

import os
import sys
import logging
import traceback
from pprint import pprint

from math import log10, floor

from string import Template

LIB_FILE_PATH='/home/logic/_workspace/kicad/kicad_library/kicad-symbols/taobao-r.lib'
DCM_FILE_PATH=LIB_FILE_PATH.replace('.lib','.dcm')

R_LIB_TEMPLATE=Template("""EESchema-LIBRARY Version 2.4
#encoding utf-8
$R_CONTENT
#
#End Library""")

R_DCM_TEMPLATE=Template("""EESchema-DOCLIB  Version 2.0
$R_CONTENT
#
#End Doc Library""")

R_LIB_UNIT_TEMPLATE=Template("""#
# $R_THREE_DIGIT_VALUE
#
DEF $R_THREE_DIGIT_VALUE R 0 10 N N 1 F N
F0 "R" 30 20 50 H V L CNN
F1 "$R_THREE_DIGIT_VALUE" 30 -40 50 H V L CNN
F2 "" 0 0 50 H I C CNN
F3 "" 0 0 50 H I C CNN
$$FPLIST
 R_*
 Resistor_SMD:R_0805_*
 Resistor_SMD:R_0603_*
$$ENDFPLIST
DRAW
S -30 70 30 -70 0 1 8 N
X ~ 1 0 100 30 D 50 50 1 1 P
X ~ 2 0 -100 30 U 50 50 1 1 P
ENDDRAW
ENDDEF
""")

R_DCM_UNIT_TEMPLATE=Template("""#
$$CMP $R_THREE_DIGIT_VALUE
D Resistor
K R r res resistor $R_THREE_DIGIT_VALUE $R_TEXT_VALUE
F ~
$$ENDCMP
""")

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

    return float(number_value.replace('K','')) * factor

def getThreeDigitCode(int_r_value):
    try:
        if int_r_value == 0:
            return '0'
        else:
            str_r_value = str(int_r_value)
            no_of_zero = floor(log10(int_r_value))
            left_2_digit = str_r_value[0:2]
            last_digit = str(no_of_zero-1)
            return left_2_digit+last_digit
    except Exception as e:
        pprint(int_r_value)


def getLibFile(three_digit_codes):
    text_content=[]
    for three_digit_code in three_digit_codes:
        int_r_value = parseTextCode(three_digit_code)
        r_three_digit_code = 'R'+getThreeDigitCode(int_r_value)
        text_content.append(R_LIB_UNIT_TEMPLATE.substitute(R_THREE_DIGIT_VALUE=r_three_digit_code))

    text_to_write = R_LIB_TEMPLATE.substitute(
        R_CONTENT=''.join(text_content)
    )

    with open(LIB_FILE_PATH, 'r+') as f:
        f.write(text_to_write)


def getDcmFile(three_digit_codes):
    text_content=[]
    for three_digit_code in three_digit_codes:
        int_r_value = parseTextCode(three_digit_code)
        r_three_digit_code = 'R'+getThreeDigitCode(int_r_value)
        text_content.append(R_DCM_UNIT_TEMPLATE.substitute(R_THREE_DIGIT_VALUE=r_three_digit_code,
        R_TEXT_VALUE=three_digit_code))

    text_to_write = R_DCM_TEMPLATE.substitute(
        R_CONTENT = ''.join(text_content)
    )

    with open(DCM_FILE_PATH, 'r+') as f:
        f.write(text_to_write)

def main():
    with open('r_value_list.csv','r') as f:
        raw_lines = f.readlines()
        raw_values = []
        for test_line in raw_lines:
            test_line = test_line.strip()
            raw_values.append(test_line)

        getLibFile(raw_values)
        getDcmFile(raw_values)


        # three_digit_code = getThreeDigitCode(int_r_value)
        # # print('testline:%s,%d, %s' % (test_line, int_r_value, three_digit_code))
        # print(R_LIB_UNIT_TEMPLATE.substitute(R_VALUE='R'+three_digit_code), end='')

if __name__ == '__main__':
    main()
