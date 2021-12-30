#!/usr/bin/python3

import xml.etree.ElementTree as ET
import sys
import os
import argparse
import ipmctl.py

ap = argparse.ArgumentParser()
ap.add_argument("--input", required=True, help="input file")

args = vars(ap.parse_args())
if args['input']:  file_name = args['input']

if not file_name:
    sys.exit(1)

tree = ET.parse(file_name)
root = tree.getroot()

dimms = {}

# structure of values we care about
# white_list = {}
# white_list['Capacity'] = 1 # 'Capacity': '252.454 GiB'
# white_list['DimmUID'] = 1 # 'DimmUID': '8089-a2-1836-00002c4b'
# white_list['NmemID'] = 1 # 'NmemID': 'nmem0'
# white_list['DimmID'] = 1 # 'DimmID': '0x0001'
# white_list['FWVersion'] = 1 # 'FWVersion': '01.02.00.5446'
# white_list['PhysicalID'] = 1 # 'PhysicalID': '0x0026'
# white_list['DimmHandle'] = 1 # 'DimmHandle': '0x0001'
# white_list['SocketID'] = 1 # 'SocketID': '0x0000'
# white_list['MemControllerID'] = 1 # 'MemControllerID': '0x0000'
# white_list['ChannelID'] = 1 # 'ChannelID': '0x0000'
# white_list['ChannelPos'] = 1 # 'ChannelPos': '1'
# white_list['DeviceLocator'] = 1 # 'DeviceLocator': 'CPU1_DIMM_A2'
# white_list['ManufacturingLocation'] = 1 # 'ManufacturingLocation': '0xa2'
# white_list['ManufacturingDate'] = 1 # 'ManufacturingDate': '18-36'
# white_list['SerialNumber'] = 1 # 'SerialNumber': '0x00002c4b'
# white_list['PartNumber'] = 1 # 'PartNumber': 'NMA1XBD256GQS'


# Question: can we depend on these being in order?
# python 3.7: officially, yes
for dimm in range( len(root)):

    tmp = {}
    for dimm_attr in range(len(root[dimm])):

        tmp[root[dimm][dimm_attr].tag] = root[dimm][dimm_attr].text

        # generates white list
        print("white_list['", root[dimm][dimm_attr].tag, "'] = 0 #  ", root[dimm][dimm_attr].tag, ': ', root[dimm][dimm_attr].text)

    '''
       creating multiple indexes for accessing different ways
       expicitly indexing for clarity
    '''
    dimm_number = 'DimmNumber_{}'.format(dimm)
    dimm_id = tmp['DimmID']
    dimm_uuid = tmp['DimmUID']
    dimm_locator = tmp['DeviceLocator']

    dimms[dimm_number] = tmp     # search by .startswith('DimmNumber_')
    dimms[dimm_id] = tmp         # search by .startswith('0x')
    dimms[dimm_uuid] = tmp       # search by .startswith('8089')
    dimms[dimm_locator] = tmp    # OEM specific on naming, but provides physical & logical correlation 

print(dimms.keys())
