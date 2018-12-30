#!/usr/bin/env python

#!/usr/bin/env python
# coding:utf-8

import os
import sys
CWD = os.path.dirname(os.path.abspath(__file__))

import logging
import traceback
from pprint import pprint


# GEN_STYLE
GEN_STYLE_U=0
GEN_STYLE_ODD_EVEN=1

gen_pin_style=GEN_STYLE_U


DRAW_X_START_POS=-500
DRAW_Y_START_POS=750
Y_SPACING=100
X_SPACING=800


CSV_FILENAME = 'CAMERA_OV5640.csv'
CSV_FILEPATH = '{}/{}'.format(CWD, CSV_FILENAME)


STAGING_COMPONENT_LIB_FILEPATH='/home/logic/_workspace/kicad/kicad_library/kicad-symbols/taobao-components-staging.lib'
STAGING_COMPONENT_TEMPLATE="""EESchema-LIBRARY Version 2.4
#encoding utf-8
#
# {COMPONENT_NAME}
#
DEF {COMPONENT_NAME} U 0 40 Y Y 1 F N
F0 "U" 0 -1550 50 H V C CNN
F1 "{COMPONENT_NAME}" 0 -1700 50 H V C CNN
F2 "" -500 100 50 H I C CNN
F3 "" -500 100 50 H I C CNN
{COMPONENT_BODY}
#
#End Library
"""

DEF_TEMPALTE="""{}\nENDDEF"""
DRAW_TEMPLATE="""DRAW\n{}\nENDDRAW"""
PIN_PRINT_TEMPLATE='X {pin_name} {pin_number} {pin_x_pos} {pin_y_pos} 200 R 50 50 1 1 {pin_type}'

PIN_TYPE_MAPPER={
    'DEFAULT':'I',
    'GND':'P',
    'NC':'N',
    '3.3V':'W',
    '5V':'W',
    '+3.3V':'W',
    '+5V':'W',
    }

def readCSV(csv_file):
    with open(csv_file,'r') as f:
        pin_confs = f.readlines()

        # dilute the pins
        pin_confs = [pin_conf.strip() for pin_conf in pin_confs]

    return pin_confs

def getPins(pin_confs):
    if len(pin_confs[0].split(',')) > 1:
        # TODO: tidy me, temp branch out for handle customize pin number
        kicad_pins = [
            PIN_PRINT_TEMPLATE.format(
                pin_name=pin_confs[i].split(',')[1],
                pin_number=pin_confs[i].split(',')[0],
                pin_x_pos=DRAW_X_START_POS,
                pin_y_pos=DRAW_Y_START_POS-(i*Y_SPACING),
                pin_type=PIN_TYPE_MAPPER[pin_confs[i]] if pin_confs[i] in PIN_TYPE_MAPPER.keys()  else PIN_TYPE_MAPPER['DEFAULT']
                ) for i in range(0,len(pin_confs))
        ]
    else:
        if gen_pin_style == GEN_STYLE_ODD_EVEN:
            kicad_pins = [
                PIN_PRINT_TEMPLATE.format(
                    pin_name=pin_confs[i],
                    pin_number=i+1,
                    pin_x_pos=DRAW_X_START_POS+X_SPACING if i%2==0 else 0,
                    pin_y_pos=DRAW_Y_START_POS-(Y_SPACING*i//2),
                    pin_type=PIN_TYPE_MAPPER[pin_confs[i]] if pin_confs[i] in PIN_TYPE_MAPPER.keys()  else PIN_TYPE_MAPPER['DEFAULT']
                    ) for i in range(0,len(pin_confs))
            ]

        else:
            kicad_pins = [
                PIN_PRINT_TEMPLATE.format(
                    pin_name=pin_confs[i],
                    pin_number=i+1,
                    pin_x_pos=DRAW_X_START_POS,
                    pin_y_pos=DRAW_Y_START_POS-(i*Y_SPACING),
                    pin_type=PIN_TYPE_MAPPER[pin_confs[i]] if pin_confs[i] in PIN_TYPE_MAPPER.keys()  else PIN_TYPE_MAPPER['DEFAULT']
                    ) for i in range(0,len(pin_confs))
            ]
    return kicad_pins

def getStagingComponents(kicad_pins):

    text_pins='\n'.join(kicad_pins)
    text_draw = DRAW_TEMPLATE.format(text_pins)
    text_def = DEF_TEMPALTE.format(text_draw)
    return STAGING_COMPONENT_TEMPLATE.format(
        COMPONENT_NAME=CSV_FILENAME,
        COMPONENT_BODY=text_def)


def copyToClipbaord(text_to_copy):
    import pyperclip
    pyperclip.copy(text_to_copy)
    print('output copied to clipboard')

def writeStagingComponent(component_def):
    with open(STAGING_COMPONENT_LIB_FILEPATH, 'r+') as f:
        f.writelines(component_def)

pin_confs = readCSV(CSV_FILEPATH)
kicad_pins = getPins(pin_confs)

result = getStagingComponents(kicad_pins)
print(result)
# copyToClipbaord(result)
writeStagingComponent(result)
