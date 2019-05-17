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

INPUT_TABLE='sd_value_list.csv'
LIB_FILE_PATH='/home/logic/_workspace/kicad/kicad_library/kicad-symbols/taobao-sd.lib'
DCM_FILE_PATH=LIB_FILE_PATH.replace('.lib','.dcm')


LIB_TEMPLATE=Template("""EESchema-LIBRARY Version 2.4
#encoding utf-8
$LIB_CONTENT
#
#End Library""")

DCM_TEMPLATE=Template("""EESchema-DOCLIB  Version 2.0
$LED_CONTENT#
#End Doc Library""")


COMPONENT_DRAW_TEXT="""DRAW
P 2 0 1 0 -30 -40 -30 40 N
P 2 0 1 0 -30 0 30 0 N
P 3 0 1 0 -30 -40 -20 -40 -20 -30 N
P 3 0 1 0 -30 40 -40 40 -40 30 N
P 4 0 1 0 30 -40 -30 0 30 40 30 -40 N
X K 1 -100 0 70 R 50 50 1 1 P
X A 2 100 0 70 L 50 50 1 1 P
ENDDRAW"""

COMPONENT_F_TEXT=Template("""F0 "D" -50 80 50 H V L CNN
F1 "$component_name" -280 -80 50 H V L CNN
F2 "$DEFAULT_SD_FOOTPRINT" 0 0 50 V I C CNN
F3 "" 0 0 50 V I C CNN""")

# COMPONENT_FP_TEXT="""Connector*:*_1x??_*
# """

COMPONENT_ALIAS_TEXT=Template("""ALIAS $ALIAS""")

ZD_LIB_UNIT_TEMPLATE=Template("""#
# $component_name
#
DEF $component_name D 0 10 N N 1 F N
$F_TEXT
$$FPLIST
$ALIAS_TEXT
$FP_TEXT
$$ENDFPLIST
$DRAW_TEXT
ENDDEF
""")

ZD_DCM_UNIT_TEMPLATE=Template("""#
$$CMP $component_name
D $SD_DESCRIPTION, Schottky diode, small symbol, 肖特基二极管 ,
K $SD_KEYWORD diode
F ~
$$ENDCMP
""")

ZENER_DIODE_SIZE_TEMPLATE=Template('*D*$SIZE*')

TRANSLATE_DEFAULT_FOOTPRINT={
    'do214ac':'w_smd_diode:do214ac',
    'do214aa':'w_smd_diode:do214aa',
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
    try:
        zd_units=[]
        for zd_lib_name, zd_name, zd_footprint, zd_description, zd_keyword in components:

            zd_size_texts = (ZENER_DIODE_SIZE_TEMPLATE.substitute(SIZE=zd_size) for zd_size in zd_footprint.split('/'))
            zd_size_texts = '\n '.join(zd_size_texts)

            # get the original name and the screen name
            zd_name_screen = zd_name
            zd_name_original = ''
            if zd_name.find('_') > -1:
                zd_name_original = zd_name.split('_')[0]
                zd_name_screen = zd_name.split('_')[1]

            default_footprint = zd_footprint.split('/')[0]
            zd_units.append(ZD_LIB_UNIT_TEMPLATE.substitute(
                component_name= zd_lib_name,
                FP_TEXT=zd_size_texts,
                DRAW_TEXT=COMPONENT_DRAW_TEXT,
                F_TEXT = COMPONENT_F_TEXT.substitute(
                    component_name=zd_lib_name,
                    DEFAULT_SD_FOOTPRINT='' if default_footprint not in TRANSLATE_DEFAULT_FOOTPRINT.keys() else TRANSLATE_DEFAULT_FOOTPRINT[default_footprint]),
                ALIAS_TEXT=COMPONENT_ALIAS_TEXT.substitute(ALIAS=' '.join([zd_name_original, zd_name_screen ]))
                ))

        zd_lib = LIB_TEMPLATE.substitute(LIB_CONTENT=''.join(zd_units))
        zd_lib = zd_lib.replace('\n\n','\n')

        with open(LIB_FILE_PATH,'w') as f:
            f.write(zd_lib)
        pass
    except Exception as e:
        print(zd_name)
        raise e


def getDcmFile(components):
    text_content=[]
    for zd_lib_name, zd_name, zd_footprint, zd_description, zd_keyword in components:

        text_content.append(ZD_DCM_UNIT_TEMPLATE.substitute(
            component_name=zd_lib_name,
            SD_DESCRIPTION = zd_description.replace('_',', '),
            SD_KEYWORD = zd_keyword.replace('_',' ')
            ))

    zd_content = ''.join(text_content)

    text_to_write = DCM_TEMPLATE.substitute(LED_CONTENT = zd_content)

    text_to_write = text_to_write.replace('\n\n','\n')

    with open(DCM_FILE_PATH, 'w') as f:
        f.write(text_to_write)

def main():
    readKeywordTable()
    with open(INPUT_TABLE,'r') as f:
        raw_lines = f.readlines()
        raw_values = []
        for test_line in raw_lines:
            try:
                test_line = test_line.strip()
                splitted = test_line.split(',')
                zd_name = splitted[0]
                zd_footprint = splitted[1]
                zd_description = splitted[2]
                zd_keyword = splitted[3]

                raw_values.append(('SD_'+zd_name,zd_name, zd_footprint, zd_description, zd_keyword))
            except Exception as e:
                pprint(test_line)
                raise e
                pass

        getLibFile(raw_values)
        getDcmFile(raw_values)

if __name__ == '__main__':
    main()
