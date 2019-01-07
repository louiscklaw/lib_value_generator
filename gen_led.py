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


LIB_FILE_PATH='/home/logic/_workspace/kicad/kicad_library/kicad-symbols/taobao-led.lib'
DCM_FILE_PATH=LIB_FILE_PATH.replace('.lib','.dcm')


LED_SIZE_TEXT_TEMPLATE=Template('*LED_$SIZE*')

LED_LIB_TEMPLATE=Template("""EESchema-LIBRARY Version 2.4
#encoding utf-8
$LED_CONTENT
#
#End Library""")

LED_DCM_TEMPLATE=Template("""EESchema-DOCLIB  Version 2.0
$LED_CONTENT#
#End Doc Library""")

LED_LIB_UNIT_TEMPLATE=Template("""#
# $component_name
#
DEF $component_name D 0 10 N N 1 F N
F0 "D" -50 125 50 H V L CNN
F1 "$component_name" -175 -100 50 H V L CNN
F2 "$DEFAULT_LED_FOOTPRINT" 0 0 50 V I C CNN
F3 "" 0 0 50 V I C CNN
$$FPLIST
 $LED_SIZE
$$ENDFPLIST
DRAW
P 2 0 1 0 -30 -40 -30 40 N
P 2 0 1 0 40 0 -30 0 N
P 4 0 1 0 30 -40 -30 0 30 40 30 -40 N
P 5 0 1 0 0 30 -20 50 -10 50 -20 50 -20 40 N
P 5 0 1 0 20 50 0 70 10 70 0 70 0 60 N
X K 1 -100 0 70 R 50 50 1 1 P
X A 2 100 0 70 L 50 50 1 1 P
ENDDRAW
ENDDEF
""")

LED_DCM_UNIT_TEMPLATE=Template("""#
$$CMP $component_name
D Light emitting diode, small symbol
K LED diode light-emitting-diode https://item.taobao.com/item.htm?spm=2013.1.0.0.16691961RUKr3e&id=41375954474
F ~
$$ENDCMP
""")

TRANSLATE_DEFAULT_LED_FOOTPRINT={
    '0402':'LED_SMD:LED_0402_1005Metric',
    '0603':'LED_SMD:LED_0603_1608Metric_Pad1.05x0.95mm_HandSolder',
    '0805':'LED_SMD:LED_0805_2012Metric_Pad1.15x1.40mm_HandSolder',
    '1206':'LED_SMD:LED_1206_3216Metric_Pad1.42x1.75mm_HandSolder',
    '1210':'LED_SMD:LED_1210_3225Metric_Pad1.42x2.65mm_HandSolder'
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

def getLibFile(components):
    led_units=[]


    for led_color, led_sizes in components:
        led_size_texts = (LED_SIZE_TEXT_TEMPLATE.substitute(SIZE=led_size) for led_size in led_sizes)
        led_size_texts = '\n '.join(led_size_texts)
        led_units.append(LED_LIB_UNIT_TEMPLATE.substitute(
            component_name= led_color,
            DEFAULT_LED_FOOTPRINT='',
            LED_SIZE=led_size_texts))


        for led_size in led_sizes:
            # led_size_texts = (LED_SIZE_TEXT_TEMPLATE.substitute(SIZE=led_size) for led_size in led_sizes)
            # led_size_texts = '\n '.join(led_size_texts)
            led_units.append(LED_LIB_UNIT_TEMPLATE.substitute(
                component_name= ','.join([led_color, led_size]),
                DEFAULT_LED_FOOTPRINT=TRANSLATE_DEFAULT_LED_FOOTPRINT[led_size],
                LED_SIZE="*"+led_size+"*"))

    led_lib = LED_LIB_TEMPLATE.substitute(LED_CONTENT=''.join(led_units))

    with open(LIB_FILE_PATH,'w') as f:
        f.write(led_lib)

def getDcmFile(components):
    text_content=[]
    for led_color, led_sizes in components:

        text_content.append(LED_DCM_UNIT_TEMPLATE.substitute(component_name=led_color))
    led_content = ''.join(text_content)

    text_to_write = LED_DCM_TEMPLATE.substitute(LED_CONTENT = led_content)

    text_to_write = text_to_write.replace('\n\n','\n')

    with open(DCM_FILE_PATH, 'w') as f:
        f.write(text_to_write)

def main():
    readKeywordTable()
    with open('led_value_list.csv','r') as f:
        raw_lines = f.readlines()
        raw_values = []
        for test_line in raw_lines:
            try:
                test_line = test_line.strip()
                splitted = test_line.split(',')
                led_color = splitted[0]
                led_sizes = splitted[1].split('/')

                raw_values.append(('LED_'+led_color, led_sizes))
            except Exception as e:
                pprint(test_line)
                raise e

        getLibFile(raw_values)
        getDcmFile(raw_values)

if __name__ == '__main__':
    main()
