# /usr/bin/env python

import os,sys
from string import Template

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
DEFA

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

def GetPinArray(number_of_pin=19):
    l_temp = []
    for i in range(0,number_of_pin+1):
        CURRENT_Y_POS = PIN_Y_START_LOC - PIN_Y_SEP * i
        l_temp.append(getPinText('right',i,PIN_X_START_LOC,CURRENT_Y_POS,200,'R'))

    return '\n'.join(l_temp)

if __name__=="__main__":
    testGetPinText()
    testgetDrawText()
    print(getDrawText(GetPinArray()))
