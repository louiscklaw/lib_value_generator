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


conn_row = range(1,3+1)
conn_column = range(1,30)

row_matrix = ['%dx%02d,2.54,1.27,1.00\n' % (row, column) for row in conn_row for column in conn_column]

with open('./pinhead_value_list.csv','w') as f:
    f.writelines(row_matrix)

LIB_FILE_PATH='/home/logic/_workspace/kicad/kicad_library/kicad-symbols/taobao-pinhead.lib'
DCM_FILE_PATH=LIB_FILE_PATH.replace('.lib','.dcm')

COMPONENT_DRAW_TEXT="""DRAW
S -50 -195 0 -205 1 1 6 N
S -50 -95 0 -105 1 1 6 N
S -50 5 0 -5 1 1 6 N
S -50 105 0 95 1 1 6 N
S -50 205 0 195 1 1 6 N
S -50 250 50 -250 1 1 10 f
X Pin_1 1 -200 200 150 R 50 50 1 1 P
X Pin_2 2 -200 100 150 R 50 50 1 1 P
X Pin_3 3 -200 0 150 R 50 50 1 1 P
X Pin_4 4 -200 -100 150 R 50 50 1 1 P
X Pin_5 5 -200 -200 150 R 50 50 1 1 P
ENDDRAW"""

COMPONENT_F_TEXT=Template("""F0 "J" 0 300 50 H V C CNN
F1 "$component_name" 0 -300 50 H V C CNN
F2 "" 0 0 50 H I C CNN
F3 "" 0 0 50 H I C CNN""")

# COMPONENT_FP_TEXT="""Connector*:*_1x??_*
# """

LIB_TEMPLATE=Template("""EESchema-LIBRARY Version 2.4
#encoding utf-8
$LIB_CONTENT
#
#End Library""")

DCM_TEMPLATE=Template("""EESchema-DOCLIB  Version 2.0
$LED_CONTENT#
#End Doc Library""")

PINHEAD_LIB_UNIT_TEMPLATE=Template("""#
# $component_name
#
DEF $component_name J 0 40 Y N 1 F N
$F_TEXT
$$FPLIST
$FP_TEXT
$$ENDFPLIST
$DRAW_TEXT
ENDDEF
""")

PINHEAD_DCM_UNIT_TEMPLATE=Template("""#
$$CMP $component_name
D Generic connector, single row, https://detail.tmall.com/item.htm?spm=a230r.1.14.30.2ab6682fV9I30u&id=14570712634&ns=1&abbucket=19
K connector pinhead
F ~
$$ENDCMP
""")

PINHEAD_SIZE_TEMPLATE=Template('*PinHeader*$PINHEAD_SPACE*$PIN_NUMBER*')

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

def getLibFile(components):
    pinhead_units=[]
    for pinhead_name, pin_number, pin_space_sizes in components:
        pin_footprint_texts = (PINHEAD_SIZE_TEMPLATE.substitute(
            PINHEAD_SPACE=pin_space, PIN_NUMBER='%02d' % int(pin_number[2:])
            ) for pin_space in pin_space_sizes)
        FP_TEXT = '\n '.join(pin_footprint_texts)
        F_TEXT = COMPONENT_F_TEXT.substitute(
            component_name=pinhead_name
        )
        DRAW_TEXT = COMPONENT_DRAW_TEXT

        pinhead_units.append(PINHEAD_LIB_UNIT_TEMPLATE.substitute(
            component_name= pinhead_name,
            F_TEXT = F_TEXT,
            FP_TEXT = FP_TEXT,
            DRAW_TEXT = DRAW_TEXT
            ))

    lib_text = LIB_TEMPLATE.substitute(LIB_CONTENT=''.join(pinhead_units))

    with open(LIB_FILE_PATH,'w') as f:
        f.write(lib_text)

def getDcmFile(components):
    text_content=[]
    for pinhead_name, pin_number, pin_space_sizes in components:

        text_content.append(PINHEAD_DCM_UNIT_TEMPLATE.substitute(component_name=pinhead_name))
    led_content = ''.join(text_content)

    text_to_write = DCM_TEMPLATE.substitute(LED_CONTENT = led_content)

    text_to_write = text_to_write.replace('\n\n','\n')

    with open(DCM_FILE_PATH, 'w') as f:
        f.write(text_to_write)

def main():
    readKeywordTable()
    with open('pinhead_value_list.csv','r') as f:
        raw_lines = f.readlines()
        raw_values = []
        for test_line in raw_lines:
            try:
                test_line = test_line.strip()
                splitted = test_line.split(',')
                pin_number = splitted[0]
                pin_space_size = splitted[1:]

                raw_values.append(('PIN_HEAD_'+ pin_number, pin_number,pin_space_size))
            except Exception as e:
                pprint(test_line)
                raise e
                pass



        getLibFile(raw_values)
        getDcmFile(raw_values)

if __name__ == '__main__':
    main()
