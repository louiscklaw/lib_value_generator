#!/usr/bin/env python

R_list_0603 = """R0,0603
R102,0603
R103,0603
R104,0603
R106,0603
R113,0603
R154,0603
R202,0603
R204,0603
R220,0603
R241,0603
R473,0603
R49R9,0603
R5R1,0603
R602,0603
R682,0603
R684,0603
R822,0603
"""

C_list_0603 ="""C101,0603
C102,0603
C104,0603
C105,0603
C106,0603
C18pf,0603
C223,0603
C33pf,0603
C475,0603
"""

R_list = """R102,0805
R103,0805
R221,0805
"""

C_list = """C105,0805
C106,0805
"""



R_CHINESE_CODE = "%B5%E7%D7%E8"
C_CHINESE_CODE = '%EB%8A%C8%DD'

SEARCH_LINK_TEMPLATE="""https://shop68577010.taobao.com/search.htm?orderType=hotsell_desc&viewType=grid&keyword={com_chinese_code}+{com_value}+{com_size}&lowPrice=&highPrice="""

CMD_LINE_TEMPLATE ="""firefox %s &"""

print('# resistor')
for line in R_list.split():
    r_value, r_size = line.split(',')
    r_value = r_value.replace('R','')
    print(CMD_LINE_TEMPLATE % SEARCH_LINK_TEMPLATE.format(
        com_chinese_code = R_CHINESE_CODE,
        com_value=r_value, com_size = r_size))

print('# capacitor')
for line in C_list.split():
    C_value, r_size = line.split(',')
    C_value = C_value.replace('C','')


    print(CMD_LINE_TEMPLATE % SEARCH_LINK_TEMPLATE.format(
        com_chinese_code = C_CHINESE_CODE,
        com_value=C_value, com_size = r_size))
