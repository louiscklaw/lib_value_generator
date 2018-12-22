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

draw_template="""DRAW\n{}\nENDDRAW"""
pin_print_template='X {} {} -500 {} 200 R 50 50 1 1 I'

def readCSV(csv_file):
    with open(csv_file,'r') as f:
        pin_confs = f.readlines()

        # dilute the pins
        pin_confs = [pin_conf.strip() for pin_conf in pin_confs]

    return pin_confs

def getPins(pin_confs):
    kicad_pins = [
        pin_print_template.format(pin_confs[i],i+1, DRAW_Y_START_POS-(i*Y_SPACING)) for i in range(0,len(pin_confs))
    ]
    return kicad_pins

def writePins(kicad_pins):

    print('\n'.join(kicad_pins))

pin_confs = readCSV('/home/logic/_workspace/kicad/lib_value_generator/pinout_CSVs/HDMI_19_PLUG_TYPEA.csv')

kicad_pins = getPins(pin_confs)
writePins(kicad_pins)
