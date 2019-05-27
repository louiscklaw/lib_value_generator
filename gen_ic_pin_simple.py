# /usr/bin/env python

import os,sys
from string import Template
import csv

csv_filename = "./pinout_CSVs/fe1_1.csv"

d_multiplex={}

"""
DRAW
X right 1 -500 750 200 R 50 50 1 1 I
X left 2 2050 750 200 L 50 50 1 1 I
X right_output 3 -500 650 200 R 50 50 1 1 O
X up 3 1000 -400 200 U 50 50 1 1 I
X down 4 -200 1600 200 D 50 50 1 1 I
X right_power_input 4 -500 550 200 R 50 50 1 1 W
X right_power_output 5 -500 450 200 R 50 50 1 1 w
X right_not_connected 6 -500 350 200 R 50 50 1 1 N
X right_test 7 -400 250 200 R 50 50 1 1 W
ENDDRAW
"""

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

PIN_Y_SEP=100
PIN_Y_START_LOC=1000
PIN_X_START_LOC = -1000
DEFAULT_PIN_TYPE='I'


PIN_TYPE_MAPPING={
    'I':'I',
    'O':'O',
    'PWR,P':'W',
    '':'w',
    '':'N',
    'I/O':'B',
    'A':'P',
    'GND':'P',
}

IDX_PIN_GROUPING={}

START_Y_POS = PIN_Y_START_LOC

def getPinText(pin_name, pin_number, pin_x_loc, pin_y_loc, pin_length, pin_orientation,pin_unknown1=50,   pin_unknown2=50, symbol_grouping=1, pin_unknown4=1, pin_type='I'):
    return "X {name} {number} {x_pos} {y_pos} {length} {ori} {u1} {u2} {u3} {u4} {type}".format(
        name=pin_name,
        number=str(pin_number),
        x_pos=str(pin_x_loc),
        y_pos=str(pin_y_loc),
        length=str(pin_length),
        ori=pin_orientation,
        u1=pin_unknown1,
        u2=pin_unknown2,
        u3=symbol_grouping,
        u4=pin_unknown4,
        type=pin_type
    )

def getDrawText(pin_text):
    return """DRAW\n{}\nENDDRAW""".format(pin_text)

def testGetPinText():
    print(getPinText('right',1,'-500','750','200','R'))

def testgetDrawText():
    print(getDrawText(getPinText('right',1,'-500','750','200','R')))

def GetPinArray(l_pin_configuration):
    l_temp = []
    # last_pin_group = j=0
    pin_in_group = 0
    pin_num=1

    for i in range(0,len(l_pin_configuration)):
        pin_group=pin_balls=pin_name=pin_type=''

        pin_name = l_pin_configuration[i]


        for key in PIN_TYPE_MAPPING.keys():
            if pin_type in key.split(','):
                pin_type = PIN_TYPE_MAPPING[key]
            else:
                pin_type = PIN_TYPE_MAPPING['A']
        # else:
        #     pin_type = DEFAULT_PIN_TYPE

        CURRENT_Y_POS = START_Y_POS + PIN_Y_SEP * i
        # print(pin_in_group)
        # print(CURRENT_Y_POS)
        # print(START_Y_POS)
        # print(PIN_Y_SEP)


        if pin_name in d_multiplex.keys():
            pin_name = '/'.join([pin_name, d_multiplex[pin_name]])
            # print(pin_name)

        l_temp.append(getPinText(pin_name,pin_num,PIN_X_START_LOC,CURRENT_Y_POS,200,'R'))
        pin_num+=1


    return '\n'.join(l_temp)

def writeToStagingSymbolLibrary(text_to_write):
    with open(STAGING_COMPONENT_LIB_FILEPATH, 'r+') as f:
        f.writelines(text_to_write)

def getComponentName(file_path):
    return os.path.basename(file_path).replace('.','_')

def selfTest():
    testGetPinText()
    testgetDrawText()
    print(getDrawText(GetPinArray()))

with open(csv_filename,'r') as f:
    pin_grouping = ''
    l_splitted=[]
    csv_pins = f.readlines()
    for csv_pin in csv_pins:
        csv_pin = csv_pin.strip()
        if csv_pin.find(' ') > 0:
            print('not allowed space for pin name >> %s' % csv_pin)

            sys.exit()
        if len(csv_pin) > 0:

            l_splitted.append(csv_pin)

    # from pprint import pprint
    # pprint(l_splitted)
    # import sys
    # sys.exit()

    test = GetPinArray(l_splitted)
    draw_text = DRAW_TEMPLATE.format(test)
    text_def = DEF_TEMPALTE.format(draw_text)
    component_text = STAGING_COMPONENT_TEMPLATE.format(
            COMPONENT_NAME=getComponentName(csv_filename),
            COMPONENT_BODY=text_def)
    writeToStagingSymbolLibrary(component_text)
