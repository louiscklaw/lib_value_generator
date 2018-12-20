# /usr/bin/env python

import os,sys
from string import Template
import csv


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

PIN_Y_SEP=100
PIN_Y_START_LOC=1000
PIN_X_START_LOC = -1000
DEFAULT_PIN_TYPE='I'


PIN_TYPE_MAPPING={
    'I':'I',
    'O':'O',
    'PWR':'W',
    '':'w',
    '':'N',
    'I/O':'B',
    'A':'P',
    'GND':'P',
}

def getPinText(pin_name, pin_number, pin_x_loc, pin_y_loc, pin_length, pin_orientation,pin_unknown1=50,   pin_unknown2=50, pin_unknown3=1, pin_unknown4=1, pin_type='I'):
    return "X {name} {number} {x_pos} {y_pos} {length} {ori} {u1} {u2} {u3} {u4} {type}".format(
        name=pin_name,
        number=str(pin_number),
        x_pos=str(pin_x_loc),
        y_pos=str(pin_y_loc),
        length=str(pin_length),
        ori=pin_orientation,
        u1=pin_unknown1,
        u2=pin_unknown2,
        u3=pin_unknown3,
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
    for i in range(0,len(l_pin_configuration)):
        CURRENT_Y_POS = PIN_Y_START_LOC - PIN_Y_SEP * i
        pin_name = l_pin_configuration[i][1]
        if len(l_pin_configuration[i]) > 2:
            pin_type = l_pin_configuration[i][2]
            if pin_type in PIN_TYPE_MAPPING.keys():
                pin_type = PIN_TYPE_MAPPING[pin_type]
            else:
                print(pin_type)
                raise pin_type

        else:
            pin_type = DEFAULT_PIN_TYPE


        l_temp.append(getPinText(pin_name,i+1,PIN_X_START_LOC,CURRENT_Y_POS,200,'R',pin_type=pin_type))

    return '\n'.join(l_temp)

def selfTest():
    testGetPinText()
    testgetDrawText()
    print(getDrawText(GetPinArray()))

with open('./allwinner_A13.csv','r') as f:
    l_splitted=[]
    csv_pins = f.readlines()
    for csv_pin in csv_pins:
        l_splitted.append(csv_pin.strip().split(','))


    print(GetPinArray(l_splitted))
