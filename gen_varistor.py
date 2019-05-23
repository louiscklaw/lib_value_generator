#!/usr/bin/env python
# coding:utf-8

import os
import sys
import logging
import traceback
from pprint import pprint

from math import log10, floor

from string import Template

LIB_FILE_PATH='/home/logic/_workspace/kicad/kicad_library/kicad-symbols/taobao-varistor.lib'
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
F2 "$d_footprint" 0 0 50 H I C CNN
F3 "" 0 0 50 H I C CNN
$$FPLIST
 footprint-lib:VAR_*
$$ENDFPLIST
DRAW
T 0 -70 -80 50 0 0 0 U Normal 0 C C
S -40 -100 40 100 0 1 10 N
P 3 0 1 0 -75 100 -75 50 75 -50 N
X ~ 1 0 150 50 D 50 50 1 1 P
X ~ 2 0 -150 50 U 50 50 1 1 P
ENDDRAW
ENDDEF
""")

R_LIB_UNIT_WITH_SIZE_TEMPLATE=Template("""#
# $R_THREE_DIGIT_VALUE_SIZE
#
DEF $R_THREE_DIGIT_VALUE_SIZE R 0 10 N N 1 F N
F0 "R" 30 20 50 H V L CNN
F1 "$R_THREE_DIGIT_VALUE_SIZE" 30 -40 50 H V L CNN
F2 "$d_footprint" 0 0 50 H I C CNN
F3 "" 0 0 50 H I C CNN
$$FPLIST
 Resistor_SMD:R_$R_SIZE*
$$ENDFPLIST
DRAW
T 0 -70 -80 50 0 0 0 U Normal 0 C C
S -40 -100 40 100 0 1 10 N
P 3 0 1 0 -75 100 -75 50 75 -50 N
X ~ 1 0 150 50 D 50 50 1 1 P
X ~ 2 0 -150 50 U 50 50 1 1 P
ENDDRAW
ENDDEF
""")


R_DCM_UNIT_WITH_SIZE_TEMPLATE=Template("""#
$$CMP $R_THREE_DIGIT_VALUE_SIZE
D Resistor
K R r res resistor $R_THREE_DIGIT_VALUE_SIZE $R_TEXT_VALUE
F $LINK
$$ENDCMP
""")


R_DCM_UNIT_TEMPLATE=Template("""#
$$CMP $R_THREE_DIGIT_VALUE
D Resistor
K R r res resistor $R_THREE_DIGIT_VALUE $R_TEXT_VALUE
F ~
$$ENDCMP
""")

fp_default_fp_matcher={
    '1206':'footprint-lib:VAR_1206',
    '0805':'footprint-lib:VAR_0805',
    '0603': 'footprint-lib:VAR_0603',
    '0402':'footprint-lib:VAR_0402',

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


    for r_name, l_r_size, link in r_settings:
        try:
            # int_r_value = parseTextCode(r_name)
            # R_r_name = 'R'+getThreeDigitCode(int_r_value)

            R_r_name = r_name
            text_content.append(R_LIB_UNIT_TEMPLATE.substitute(R_THREE_DIGIT_VALUE=R_r_name,
            # default symbol done deserve a default footprint (no size specified)
            d_footprint=''
            ))

            for r_size in l_r_size:
                text_content.append(R_LIB_UNIT_WITH_SIZE_TEMPLATE.substitute(
                    R_THREE_DIGIT_VALUE_SIZE=','.join([R_r_name, r_size]),
                    R_SIZE=r_size,
                    d_footprint=fp_default_fp_matcher[r_size]
                ))

        except Exception as e:
            pprint(int_r_value)
            raise e

    text_to_write = R_LIB_TEMPLATE.substitute(
        R_CONTENT=''.join(text_content)
    )
    text_to_write = text_to_write.replace('\n\n','\n')

    with open(LIB_FILE_PATH, 'w') as f:
        f.write(text_to_write)


def getDcmFile(r_settings):
    text_content=[]
    for r_name, l_r_size, link in r_settings:
        # int_r_value = parseTextCode(r_name)
        # R_r_name = 'R'+getThreeDigitCode(int_r_value)

        R_r_name = r_name
        text_content.append(R_DCM_UNIT_TEMPLATE.substitute(R_THREE_DIGIT_VALUE=R_r_name,
        R_TEXT_VALUE=r_name,
        LINK=link
        ))

        for r_size in l_r_size:
            text_content.append(R_DCM_UNIT_TEMPLATE.substitute(R_THREE_DIGIT_VALUE=','.join([R_r_name,r_size]),
            R_TEXT_VALUE=r_name,
            LINK=link
            ))

    text_to_write = R_DCM_TEMPLATE.substitute(
        R_CONTENT = ''.join(text_content)
    )

    text_to_write = text_to_write.replace('\n\n','\n')

    with open(DCM_FILE_PATH, 'w') as f:
        f.write(text_to_write)

def main():
    with open('varistor_value_list.csv','r') as f:
        raw_lines = f.readlines()
        raw_values = []
        for test_line in raw_lines:
            try:
                test_line = test_line.strip()
                test_line_split = test_line.split(',')

                r_name = test_line_split[0]
                l_r_size = test_line_split[1].split('/')
                link = test_line_split[2]
                # default_footprint = test_line_split[2]

                raw_values.append([r_name, l_r_size, link])
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
