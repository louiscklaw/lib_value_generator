# /usr/bin/env python

import os,sys
from string import Template
import csv


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
    pin_in_group = 0

    for i in range(0,len(l_pin_configuration)):
        pin_group=pin_balls=pin_name=pin_type=''


        # FIXME: dirty way for temporary working
        pin_group=l_pin_configuration[i][0]
        START_Y_POS = 0 - (int(IDX_PIN_GROUPING[pin_group]/2))* PIN_Y_SEP

        pin_group = IDX_PIN_GROUPING.keys().index(pin_group)+1
        if i == 0:
            last_pin_group = pin_group

        if last_pin_group != pin_group:
            pin_in_group=0
            last_pin_group= pin_group
        pin_in_group+=1
        pin_balls = l_pin_configuration[i][1:-6]
        pin_name = l_pin_configuration[i][-6]


        for key in PIN_TYPE_MAPPING.keys():
            if pin_type in key.split(','):
                pin_type = PIN_TYPE_MAPPING[key]
            else:
                pin_type = PIN_TYPE_MAPPING['A']
        # else:
        #     pin_type = DEFAULT_PIN_TYPE

        CURRENT_Y_POS = START_Y_POS + PIN_Y_SEP * (pin_in_group)
        # print(pin_in_group)
        # print(CURRENT_Y_POS)
        # print(START_Y_POS)
        # print(PIN_Y_SEP)


        if pin_name in d_multiplex.keys():
            pin_name = '/'.join([pin_name, d_multiplex[pin_name]])
            # print(pin_name)

        l_temp.append(getPinText(pin_name,pin_balls[0],PIN_X_START_LOC,CURRENT_Y_POS,200,'R',symbol_grouping=pin_group,pin_type=pin_type))


    return '\n'.join(l_temp)

def selfTest():
    testGetPinText()
    testgetDrawText()
    print(getDrawText(GetPinArray()))

with open('./allwinner_h3_multiplex.csv','r') as f1:
    multiplex_pins = f1.readlines()
    for multiplex_pin in multiplex_pins:
        multiplex_pin = multiplex_pin.strip().split(',')
        d_multiplex[multiplex_pin[0]] = multiplex_pin[1]

with open('./allwinner_h3.csv','r') as f:
    pin_grouping = ''
    l_splitted=[]
    csv_pins = f.readlines()
    for csv_pin in csv_pins:
        csv_pin = csv_pin.strip()
        if len(csv_pin) > 0:
            if csv_pin[0]=="#":
                pin_grouping=csv_pin.replace('#','')
                IDX_PIN_GROUPING[pin_grouping]=0
            else:
                csv_splitted = csv_pin.strip().split(',')
                if len(csv_splitted) > 8:
                    pin_balls = csv_splitted[1:-6]
                    pin_name = csv_splitted[-6]
                    function = csv_splitted[-5]
                    the_rest = csv_splitted[-4:]
                    for pin_ball in pin_balls:
                        # ['T17', 'SA0', 'DRAM', 'I/O', 'Z', '-', '-']


                        l_splitted.append([pin_grouping]+[pin_ball,pin_name, function]+the_rest)
                else:
                    l_splitted.append([pin_grouping]+csv_splitted)


                IDX_PIN_GROUPING[pin_grouping]+=1

    print(getDrawText(GetPinArray(l_splitted)))
