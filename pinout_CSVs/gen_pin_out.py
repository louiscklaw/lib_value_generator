#!/usr/bin/env python

#!/usr/bin/env python
# coding:utf-8

import os
import sys
import logging
import traceback
from pprint import pprint

DRAW_Y_START_POS=750
Y_SPACING=100

CWD = os.path.dirname(os.path.abspath(__file__))
sys.path.append(CWD)
sys.path.append(CWD+'/_lib')


STAGING_COMPONENT_TEMPLATE="""EESchema-LIBRARY Version 2.4
#encoding utf-8
#
# STAGING_COMPONENT
#
DEF STAGING_COMPONENT U 0 40 Y Y 1 F N
F0 "U" 0 -1550 50 H V C CNN
F1 "STAGING_COMPONENT" 0 -1700 50 H V C CNN
F2 "" -500 100 50 H I C CNN
F3 "" -500 100 50 H I C CNN
{}
#
#End Library
"""

DEF_TEMPALTE="""{}\nENDDEF"""
DRAW_TEMPLATE="""DRAW\n{}\nENDDRAW"""
PIN_PRINT_TEMPLATE='X {} {} -500 {} 200 R 50 50 1 1 I'

def readCSV(csv_file):
    with open(csv_file,'r') as f:
        pin_confs = f.readlines()

        # dilute the pins
        pin_confs = [pin_conf.strip() for pin_conf in pin_confs]

    return pin_confs

def getPins(pin_confs):
    kicad_pins = [
        PIN_PRINT_TEMPLATE.format(pin_confs[i],i+1, DRAW_Y_START_POS-(i*Y_SPACING)) for i in range(0,len(pin_confs))
    ]
    return kicad_pins

def writePins(kicad_pins):

    text_pins='\n'.join(kicad_pins)
    text_draw = DRAW_TEMPLATE.format(text_pins)
    text_def = DEF_TEMPALTE.format(text_draw)
    print(STAGING_COMPONENT_TEMPLATE.format(text_def))

pin_confs = readCSV('{}/RClamp0524PA.csv'.format(CWD))

kicad_pins = getPins(pin_confs)
writePins(kicad_pins)
