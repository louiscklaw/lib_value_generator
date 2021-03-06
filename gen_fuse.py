#!/usr/bin/env python
# coding:utf-8

import os
import sys
import logging
import traceback
from pprint import pprint

from math import log10, floor

from string import Template

LIB_FILE_PATH='/home/logic/_workspace/kicad/kicad_library/kicad-symbols/taobao-fuse.lib'
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
# $fusevalue
#
DEF $fusevalue F 0 10 N N 1 F N
F0 "F" 0 -60 50 H V C CNN
F1 "$fusevalue" 0 60 50 H V C CNN
F2 "$d_footprint" 0 0 50 H I C CNN
F3 "" 0 0 50 H I C CNN
$$FPLIST
 fuse*
$$ENDFPLIST
DRAW
S -50 20 50 -20 0 1 0 N
P 2 0 1 0 -50 0 50 0 N
X ~ 1 -100 0 50 R 50 50 1 1 P
X ~ 2 100 0 50 L 50 50 1 1 P
ENDDRAW
ENDDEF
""")

R_LIB_UNIT_WITH_SIZE_TEMPLATE=Template("""#
# $fusevalue
#
DEF $fusevalue F 0 10 N N 1 F N
F0 "F" 0 -60 50 H V C CNN
F1 "$fusevalue" 0 60 50 H V C CNN
F2 "$d_footprint" 0 0 50 H I C CNN
F3 "" 0 0 50 H I C CNN
$$FPLIST
 fuse*$R_SIZE*
$$ENDFPLIST
DRAW
S -50 20 50 -20 0 1 0 N
P 2 0 1 0 -50 0 50 0 N
X ~ 1 -100 0 50 R 50 50 1 1 P
X ~ 2 100 0 50 L 50 50 1 1 P
ENDDRAW
ENDDEF
""")


R_DCM_UNIT_WITH_SIZE_TEMPLATE=Template("""#
$$CMP $fusevalue
D Fuse, small symbol
K fuse $fusevalue $R_TEXT_VALUE
F ~
$$ENDCMP
""")


R_DCM_UNIT_TEMPLATE=Template("""#
$$CMP $fusevalue
D Fuse, small symbol
K fuse $fusevalue $R_TEXT_VALUE
F ~
$$ENDCMP
""")

fp_default_fp_matcher={
    '1206':'Resistor_SMD:R_1206_3216Metric_Pad1.42x1.75mm_HandSolder',
    '0805':'Resistor_SMD:R_0805_2012Metric_Pad1.15x1.40mm_HandSolder',
    '0603': 'Resistor_SMD:R_0603_1608Metric_Pad1.05x0.95mm_HandSolder',
    '0402':'Resistor_SMD:R_0402_1005Metric',

}


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

    if number_value.find('M') == 2:
        factor = 1000000

    return float(number_value.replace('K','').replace('M','')) * factor

def getThreeDigitCode(str_r_value):
    float_r_value = float(str_r_value)
    str_r_value = str(str_r_value)
    try:
        if float_r_value == 0:
            return '0'
        if float_r_value < 10:
            # for x.y format
            return '%sR%s' % (str_r_value[0], str_r_value[2])

        else:
            str_r_value = str(float_r_value)
            no_of_zero = floor(log10(float_r_value))

            no_of_zero = int(no_of_zero)

            left_2_digit = str_r_value[0:2]
            last_digit = str(no_of_zero-1)
            return left_2_digit+last_digit
    except Exception as e:
        # pprint(float_r_value)
        # pprint(float_r_value < 10)
        pprint(type(str_r_value))
        pprint('%sR%s' % (str_r_value[0], str_r_value[2]))
        pass


def getLibFile(r_settings):
    text_content=[]

    # int_r_value='6.2'
    # r_three_digit_code = 'R'+getThreeDigitCode(int_r_value)
    # pprint(r_three_digit_code)
    # sys.exit()


    for r_name, l_r_size in r_settings:
            print(r_name)
            # sys.exit()
            # int_r_value = parseTextCode(r_name)

            # R_r_name = 'R'+getThreeDigitCode(int_r_value)

            text_content.append(R_LIB_UNIT_TEMPLATE.substitute(fusevalue=r_name,
            # default symbol done deserve a default footprint (no size specified)
            d_footprint=''
            ))

            for r_size in l_r_size:
                text_content.append(R_LIB_UNIT_WITH_SIZE_TEMPLATE.substitute(
                    fusevalue=','.join([r_name, r_size]),
                    R_SIZE=r_size,
                    d_footprint=fp_default_fp_matcher[r_size]
                ))


    text_to_write = R_LIB_TEMPLATE.substitute(
        R_CONTENT=''.join(text_content)
    )
    text_to_write = text_to_write.replace('\n\n','\n')

    with open(LIB_FILE_PATH, 'w') as f:
        f.write(text_to_write)


def getDcmFile(r_settings):
    text_content=[]
    for r_name, l_r_size in r_settings:
        # int_r_value = parseTextCode(r_name)
        # R_r_name = 'R'+getThreeDigitCode(int_r_value)
        text_content.append(R_DCM_UNIT_TEMPLATE.substitute(fusevalue=r_name,
        R_TEXT_VALUE=r_name))

        for r_size in l_r_size:
            text_content.append(R_DCM_UNIT_TEMPLATE.substitute(fusevalue=','.join([r_name,r_size]),
            R_TEXT_VALUE=r_name))

    text_to_write = R_DCM_TEMPLATE.substitute(
        R_CONTENT = ''.join(text_content)
    )

    text_to_write = text_to_write.replace('\n\n','\n')

    with open(DCM_FILE_PATH, 'w') as f:
        f.write(text_to_write)

def main():
    with open('fuse_value_list.csv','r') as f:
        raw_lines = f.readlines()
        raw_values = []
        for test_line in raw_lines:
            try:
                test_line = test_line.strip()
                test_line_split = test_line.split(',')

                r_name = test_line_split[0]
                l_r_size = test_line_split[1].split('/')
                # default_footprint = test_line_split[2]

                raw_values.append([r_name, l_r_size])
                pass
            except Exception as e:
                pprint(test_line)
                pass

        getLibFile(raw_values)
        getDcmFile(raw_values)


        # three_digit_code = getThreeDigitCode(int_r_value)
        # # print('testline:%s,%d, %s' % (test_line, int_r_value, three_digit_code))
        # print(R_LIB_UNIT_TEMPLATE.substitute(R_VALUE='R'+three_digit_code), end='')

if __name__ == '__main__':
    main()
