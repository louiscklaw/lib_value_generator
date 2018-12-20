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
    'PWR,P':'W',
    '':'w',
    '':'N',
    'I/O':'B',
    'A':'P',
    'GND':'P',
}

IDX_PIN_GROUPING={}

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
    last_pin_group = j=0

    for i in range(0,len(l_pin_configuration)):
        pin_group=pin_balls=pin_name=pin_type=''

        pin_group=l_pin_configuration[i][0]
        pin_group = IDX_PIN_GROUPING.keys().index(pin_group)+1
        if i == 0:
            last_pin_group = pin_group

        pin_balls = l_pin_configuration[i][1:-6]
        pin_name = l_pin_configuration[i][-6]
        for key in PIN_TYPE_MAPPING.keys():
            if pin_type in key.split(','):
                pin_type = PIN_TYPE_MAPPING[key]
            else:
                pin_type = PIN_TYPE_MAPPING['A']
        # else:
        #     pin_type = DEFAULT_PIN_TYPE
        for pin_ball in pin_balls:
            if pin_group != last_pin_group:
                j=0
                last_pin_group = pin_group
            else:
                j+=1

            CURRENT_Y_POS = PIN_Y_START_LOC - PIN_Y_SEP * j

            l_temp.append(getPinText(pin_name,pin_ball,PIN_X_START_LOC,CURRENT_Y_POS,200,'R',symbol_grouping=pin_group,pin_type=pin_type))

    return '\n'.join(l_temp)

def selfTest():
    testGetPinText()
    testgetDrawText()
    print(getDrawText(GetPinArray()))

with open('./allwinner_H3.csv','r') as f:
    pin_grouping = ''
    l_splitted=[]
    csv_pins = f.readlines()
    for csv_pin in csv_pins:
        csv_pin = csv_pin.strip()
        if len(csv_pin) > 0:
            if csv_pin[0]=="#":
                pin_grouping=csv_pin.replace('#','')
                IDX_PIN_GROUPING[pin_grouping]=''
            else:
                l_splitted.append([pin_grouping]+csv_pin.strip().split(','))


    print(getDrawText(GetPinArray(l_splitted)))
