#!/usr/bin/python3

import xml.etree.ElementTree as ET
import sys
import os
from common import message, get_linenumber, pretty_print
from common import V0, V1, V2, V3, V4, V5, D0, D1, D2, D3, D4, D5
import common as c
import time

VERBOSE = c.VERBOSE

tmp_dir = '/tmp'

timers = []

# If working in a test sandbox, change paths
# to start with path to sandbox
#
if not os.getenv('SANDBOX'):
    SANDBOX = ''
else:
    SANDBOX = os.environ['SANDBOX']
    print('Enabling Sandbox at:', SANDBOX)

DEVDIR = SANDBOX + '/dev'
DEV_UUID = DEVDIR + '/disk/by-uuid/'
NDCTL_FILE = SANDBOX + "/tmp/ndctl_list_NDRH.txt"

'''ipmctl commands to use'''
show_dimm_cmd = 'ipmctl show -o nvmxml -a -dimm'
show_region_cmd = 'ipmctl show -o nvmxml -a -region'
show_socket_cmd = 'ipmctl show -o nvmxml -a -socket'
show_sensor_cmd = 'ipmctl_show -o nvmxml -a -sensor'
show_topology_cmd = 'ipmctl show -o nvmxml -a -topology'
'''Files to send XML to'''
dimm_xml_file = SANDBOX + tmp_dir + '/ipmctl_show_-o_nvmxml_-a_-dimm.xml'
region_xml_file = SANDBOX + tmp_dir + '/ipmctl_show_-o_nvmxml_-a_-region.xml'
socket_xml_file = SANDBOX + tmp_dir + '/ipmctl_show_-o_nvmxml_-a_-socket.xml'
sensor_xml_file = SANDBOX + tmp_dir + '/ipmctl_show_-o_nvmxml_-a_-sensor.xml'
topology_xml_file = SANDBOX + tmp_dir + '/ipmctl_show_-o_nvmxml_-a_-topology.xml'

'''
this is the current list of fields available from Optane PMEM 100 series
They are included here for completeness
'''
# TODO
# do we really need the whitelist for those things we don't care about?
# I don't think we do, and it would clean up any errors from unknown keys
#
white_list = {}
white_list['DimmID'] = 0 #   DimmID :  0x0001
white_list['Capacity'] = 0 #   Capacity :  252.454 GiB
white_list['LockState'] = 0 #   LockState :  Disabled
white_list['SVNDowngrade'] = 0 #   SVNDowngrade :  Unknown
white_list['SecureErasePolicy'] = 0 #   SecureErasePolicy :  Unknown
white_list['S3ResumeOptIn'] = 0 #   S3ResumeOptIn :  Unknown
white_list['FwActivateOptIn'] = 0 #   FwActivateOptIn :  Unknown
white_list['HealthState'] = 0 #   HealthState :  Healthy
white_list['HealthStateReason'] = 0 #   HealthStateReason :  None
white_list['FWVersion'] = 0 #   FWVersion :  01.02.00.5446
white_list['FWAPIVersion'] = 0 #   FWAPIVersion :  01.15
white_list['InterfaceFormatCode'] = 0 #   InterfaceFormatCode :  0x0301 (Non-Energy Backed Byte Addressable)
white_list['ManageabilityState'] = 0 #   ManageabilityState :  Manageable
white_list['PopulationViolation'] = 0 #   PopulationViolation :  No
white_list['PhysicalID'] = 0 #   PhysicalID :  0x0026
white_list['DimmHandle'] = 0 #   DimmHandle :  0x0001
white_list['DimmUID'] = 0 #   DimmUID :  8089-a2-1836-00002c4b
white_list['SocketID'] = 0 #   SocketID :  0x0000
white_list['MemControllerID'] = 0 #   MemControllerID :  0x0000
white_list['ChannelID'] = 0 #   ChannelID :  0x0000
white_list['ChannelPos'] = 0 #   ChannelPos :  1
white_list['MemoryType'] = 0 #   MemoryType :  Logical Non-Volatile Device
white_list['Manufacturer'] = 0 #   Manufacturer :  Intel
white_list['VendorID'] = 0 #   VendorID :  0x8089
white_list['DeviceID'] = 0 #   DeviceID :  0x5141
white_list['RevisionID'] = 0 #   RevisionID :  0x0000
white_list['SubsystemVendorID'] = 0 #   SubsystemVendorID :  0x8089
white_list['SubsystemDeviceID'] = 0 #   SubsystemDeviceID :  0x097a
white_list['SubsystemRevisionID'] = 0 #   SubsystemRevisionID :  0x0018
white_list['DeviceLocator'] = 0 #   DeviceLocator :  CPU1_DIMM_A2
white_list['ManufacturingInfoValid'] = 0 #   ManufacturingInfoValid :  1
white_list['ManufacturingLocation'] = 0 #   ManufacturingLocation :  0xa2
white_list['ManufacturingDate'] = 0 #   ManufacturingDate :  18-36
white_list['SerialNumber'] = 0 #   SerialNumber :  0x00002c4b
white_list['PartNumber'] = 0 #   PartNumber :  NMA1XBD256GQS
white_list['BankLabel'] = 0 #   BankLabel :  NODE 1
white_list['DataWidth'] = 0 #   DataWidth :  64 b
white_list['TotalWidth'] = 0 #   TotalWidth :  72 b
white_list['Speed'] = 0 #   Speed :  2666 MT/s
white_list['FormFactor'] = 0 #   FormFactor :  DIMM
white_list['ManufacturerID'] = 0 #   ManufacturerID :  0x8089
white_list['ControllerRevisionID'] = 0 #   ControllerRevisionID :  B0, 0x0020
white_list['MemoryCapacity'] = 0 #   MemoryCapacity :  0.000 GiB
white_list['AppDirectCapacity'] = 0 #   AppDirectCapacity :  252.000 GiB
white_list['UnconfiguredCapacity'] = 0 #   UnconfiguredCapacity :  0.000 GiB
white_list['InaccessibleCapacity'] = 0 #   InaccessibleCapacity :  0.454 GiB
white_list['ReservedCapacity'] = 0 #   ReservedCapacity :  0.000 GiB
white_list['PackageSparingCapable'] = 0 #   PackageSparingCapable :  1
white_list['PackageSparingEnabled'] = 0 #   PackageSparingEnabled :  1
white_list['PackageSparesAvailable'] = 0 #   PackageSparesAvailable :  1
white_list['IsNew'] = 0 #   IsNew :  0
white_list['ViralPolicy'] = 0 #   ViralPolicy :  0
white_list['ViralState'] = 0 #   ViralState :  0
white_list['PeakPowerBudget'] = 0 #   PeakPowerBudget :  20000 mW
white_list['AvgPowerLimit'] = 0 #   AvgPowerLimit :  15000 mW
white_list['MaxAveragePowerLimit'] = 0 #   MaxAveragePowerLimit :  18000 mW
white_list['LatchedLastShutdownStatus'] = 0 #   LatchedLastShutdownStatus :  PM S5 Received, PMIC 12V/DDRT 1.2V Power Loss (PLI) ...
white_list['UnlatchedLastShutdownStatus'] = 0 #   UnlatchedLastShutdownStatus :  PMIC 12V/DDRT 1.2V Power Loss (PLI) ...
white_list['ThermalThrottleLossPercent'] = 0 #   ThermalThrottleLossPercent :  N/A
white_list['LastShutdownTime'] = 0 #   LastShutdownTime :  Mon Dec 27 17:43:55 UTC 2021
white_list['ModesSupported'] = 0 #   ModesSupported :  Memory Mode, App Direct
white_list['SecurityCapabilities'] = 0 #   SecurityCapabilities :  Encryption, Erase
white_list['MasterPassphraseEnabled'] = 0 #   MasterPassphraseEnabled :  0
white_list['ConfigurationStatus'] = 0 #   ConfigurationStatus :  Valid
white_list['SKUViolation'] = 0 #   SKUViolation :  0
white_list['ARSStatus'] = 0 #   ARSStatus :  Completed
white_list['OverwriteStatus'] = 0 #   OverwriteStatus :  Unknown
white_list['AitDramEnabled'] = 0 #   AitDramEnabled :  1
white_list['BootStatus'] = 0 #   BootStatus :  Success
white_list['BootStatusRegister'] = 0 #   BootStatusRegister :  0x00000004_981d00f0
white_list['ErrorInjectionEnabled'] = 0 #   ErrorInjectionEnabled :  0
white_list['MediaTemperatureInjectionEnabled'] = 0 #   MediaTemperatureInjectionEnabled :  0
white_list['SoftwareTriggersEnabled'] = 0 #   SoftwareTriggersEnabled :  0
white_list['SoftwareTriggersEnabledDetails'] = 0 #   SoftwareTriggersEnabledDetails :  None
white_list['PoisonErrorInjectionsCounter'] = 0 #   PoisonErrorInjectionsCounter :  0
white_list['PoisonErrorClearCounter'] = 0 #   PoisonErrorClearCounter :  0
white_list['MediaTemperatureInjectionsCounter'] = 0 #   MediaTemperatureInjectionsCounter :  0
white_list['SoftwareTriggersCounter'] = 0 #   SoftwareTriggersCounter :  0
white_list['MaxControllerTemperature'] = 0 #   MaxControllerTemperature :  80 C
white_list['MaxMediaTemperature'] = 0 #   MaxMediaTemperature :  78 C
white_list['MixedSKU'] = 0 #   MixedSKU :  0

white_list['FWActiveAPIVersion'] = 0 #   MixedSKU :  0
white_list['LatchSystemShutdownState'] = 0 #   MixedSKU :  0
#
# TODO - Get updates from Thomas

'''Here are the keys we care about'''
white_list['Capacity'] = 1 # 'Capacity': '252.454 GiB'
white_list['DimmUID'] = 1 # 'DimmUID': '8089-a2-1836-00002c4b'
white_list['HealthState'] = 1 #   HealthState :  Healthy
white_list['HealthStateReason'] = 1 #   HealthStateReason :  None
white_list['NmemID'] = 1 # 'NmemID': 'nmem0'
white_list['DimmID'] = 1 # 'DimmID': '0x0001'
white_list['FWVersion'] = 1 # 'FWVersion': '01.02.00.5446'
white_list['PhysicalID'] = 1 # 'PhysicalID': '0x0026'
white_list['DimmHandle'] = 1 # 'DimmHandle': '0x0001'
white_list['SocketID'] = 1 # 'SocketID': '0x0000'
white_list['MemControllerID'] = 1 # 'MemControllerID': '0x0000'
white_list['ChannelID'] = 1 # 'ChannelID': '0x0000'
white_list['ChannelPos'] = 1 # 'ChannelPos': '1'
white_list['DeviceLocator'] = 1 # 'DeviceLocator': 'CPU1_DIMM_A2'
white_list['ManufacturingLocation'] = 1 # 'ManufacturingLocation': '0xa2'
white_list['ManufacturingDate'] = 1 # 'ManufacturingDate': '18-36'
white_list['SerialNumber'] = 1 # 'SerialNumber': '0x00002c4b'
white_list['PartNumber'] = 1 # 'PartNumber': 'NMA1XBD256GQS'


def clean_up():
    '''clean up all tmp files associated with this mdule'''
    name = 'clean_up()'
    tic = time.perf_counter()

    status = False

    file_name = '/tmp/ipmctl*.xml'
    status = c.clean_up(file_name)

    toc = time.perf_counter()
    delta_t = toc - tic
    td = {'name': name, "elapsed": delta_t, 'tic': tic, 'toc': toc}
    timers.append(td)

    return status

def show_socket(xml_file = socket_xml_file, command = show_socket_cmd):
    '''executes show socket cmd string, sending output to xml_file'''
    name = 'show_socket()'
    tic = time.perf_counter()


    status = False
    #
    msg = "%s %s %s %s" % (get_linenumber(), ":show_socket():", xml_file, command)
    message(msg, D1)

    # TODO - check if file exists, skip recreating if it does
    # add message skipping creation
    #
    cmd = command + ' > ' + xml_file
    ret_val = os.system(cmd)
    if ret_val == 0:
        status = True
    #
    msg = "%s %s %s %s" % (get_linenumber(), ":show_socket():", 'returned', ret_val)
    message(msg, D1)
    #
    toc = time.perf_counter()
    delta_t = toc - tic
    td = {'name': name, "elapsed": delta_t, 'tic': tic, 'toc': toc}
    timers.append(td)

    return status

def parse_socket(xml_file = socket_xml_file):
    '''
    parses output of show -a -socket command
    returns socket dict with data from xml file
    '''
    name = 'parse_socket()'
    tic = time.perf_counter()

    sockets = {}
    #
    msg = "%s %s %s %s" % (get_linenumber(), ":parse_socket:", xml_file, 'Beginning')
    message(msg, D3)
    #
    tree = ET.parse(xml_file)
    root = tree.getroot()
    #
    msg = "%s %s %s %s" % (get_linenumber(), ":parse_socket:", xml_file, 'ET.parse Complete')
    message(msg, D3)

    for socket in range( len(root)):
        tmp = {}
        for socket_attr in range(len(root[socket])):
            msg = "%s %s %s %s" % (get_linenumber(), "for socket_attr in range", root[socket][socket_attr].tag, root[socket][socket_attr].text)
            message(msg, D4)
            tmp[root[socket][socket_attr].tag] = root[socket][socket_attr].text

        socket_id = 'SocketID_{}'.format(tmp['SocketID'])

        sockets[socket_id] = tmp

    toc = time.perf_counter()
    delta_t = toc - tic
    td = {'name': name, "elapsed": delta_t, 'tic': tic, 'toc': toc}
    timers.append(td)

    return sockets

def show_dimm(xml_file = dimm_xml_file, command = show_dimm_cmd):
    '''executes show dimm cmd string, sending output to xml_file'''
    name = 'show_dimm()'
    tic = time.perf_counter()

    status = False
    #
    msg = "%s %s %s %s" % (get_linenumber(), ":show_dimm():", xml_file, command)
    message(msg, D1)
    #
    #
    if os.path.exists(xml_file):
        ret_val = 'File Exists ... Skipped'
        status = True
    else:
        cmd = command + ' > ' + xml_file
        ret_val = os.system(cmd)
        if ret_val == 0:
            status = True
    #
    msg = "%s %s %s %s" % (get_linenumber(), ":show_dimm():", 'returned', ret_val)
    message(msg, D1)
    #
    toc = time.perf_counter()
    delta_t = toc - tic
    td = {'name': name, "elapsed": delta_t, 'tic': tic, 'toc': toc}
    timers.append(td)

    return status

def parse_dimm(xml_file = dimm_xml_file):
    '''
    parses output of show -a -dimm command
    returns dimms dict with data from xml file
    see white_list for fields of interest
    '''
    name = 'parse_dimm()'
    tic = time.perf_counter()

    dimms = {}
    #
    msg = "%s %s %s %s" % (get_linenumber(), ":parse_dimms:", xml_file, 'Beginning')
    message(msg, D3)
    #
    tree = ET.parse(xml_file)
    root = tree.getroot()
    #
    msg = "%s %s %s %s" % (get_linenumber(), ":parse_dimms:", xml_file, 'ET.parse Complete')
    message(msg, D3)
    #
    dimms = {}
    #
    for dimm in range( len(root)):
        tmp = {}
        for dimm_attr in range(len(root[dimm])):

            tmp[root[dimm][dimm_attr].tag] = root[dimm][dimm_attr].text

            #
            # TODO: can we find a way to
            # if white_list[root[dimm][dimm_attr].tag] == 1:
            #   msg = "%s %s %s %s" % (get_linenumber(), "for dimm_attr in range", root[dimm][dimm_attr].tag, root[dimm][dimm_attr].text)
            #   message(msg, D4)
            #   tmp[root[dimm][dimm_attr].tag] = root[dimm][dimm_attr].text
            #
            #

        '''
        creating multiple indexes for accessing different ways
        expicitly indexing for clarity
        '''
        dimm_number = 'DimmNumber_{}'.format(dimm)
        dimm_id = 'DimmID_{}'.format(tmp['DimmID'])
        dimm_uid = 'DimmUID_{}'.format(tmp['DimmUID'])
        dimm_locator = 'DeviceLocator_{}'.format(tmp['DeviceLocator'])
        #
        dimms[dimm_number] = tmp     # search by .startswith('DimmNumber_')
        msg = "%s %s %s %s" % (get_linenumber(), "... Indexing", dimm_number, '')
        message(msg, D3)
        #
        dimms[dimm_id] = tmp         # search by .startswith('0x')
        msg = "%s %s %s %s" % (get_linenumber(), "... Indexing", dimm_id, '')
        message(msg, D3)
        #
        dimms[dimm_uid] = tmp       # search by .startswith('8089')
        msg = "%s %s %s %s" % (get_linenumber(), "... Indexing", dimm_uid, '')
        message(msg, D3)
        #
        dimms[dimm_locator] = tmp    # OEM specific on naming, but provides physical & logical correlation
        msg = "%s %s %s %s" % (get_linenumber(), "... Indexing", dimm_locator, '')
        message(msg, D3)

    # print("%s %s %s %s" % (get_linenumber(), ":parse_dimms:", xml_file, 'End'))

    toc = time.perf_counter()
    delta_t = toc - tic
    td = {'name': name, "elapsed": delta_t, 'tic': tic, 'toc': toc}
    timers.append(td)

    return dimms

def show_region(xml_file = region_xml_file, command = show_region_cmd):
    '''
    runs show dimm cmd string, sending output to xml_file
    returns True if sucessful
    '''
    name = 'show_region()'
    tic = time.perf_counter()

    status = False

    msg = "%s %s %s %s" % (get_linenumber(), ":show_region():", xml_file, command)
    message(msg, D1)
    #
    # TODO - check if file exists, skip recreating if it does
    # add message skipping creation
    #
    cmd = command + ' > ' + xml_file
    ret_val = os.system(cmd)
    if ret_val == 0:
        status = True
    #
    msg = "%s %s %s %s" % (get_linenumber(), ":show_region():", 'returned', ret_val)
    message(msg, D1)

    toc = time.perf_counter()
    delta_t = toc - tic
    td = {'name': name, "elapsed": delta_t, 'tic': tic, 'toc': toc}
    timers.append(td)

    return status

def parse_region(xml_file = region_xml_file):
    '''
    parses output of show -a -regions command
    returns regions dict with data from xml file
    '''
    name = 'parse_region()'
    tic = time.perf_counter()

    msg = "%s %s %s %s" % (get_linenumber(), "parse_region: Parse Beginning:", xml_file, '')
    message(msg, D1)
    regions = {}

    tree = ET.parse(xml_file)
    root = tree.getroot()

    for region in range( len(root)):
        tmp = {}
        for region_attr in range(len(root[region])):
            tmp[root[region][region_attr].tag] = root[region][region_attr].text
            msg = "%s %s %s %s" % (get_linenumber(), "for region_attr in range", root[region][region_attr].tag, root[region][region_attr].text)
            message(msg, D3)

        '''
        creating multiple indexes for accessing different ways
        expicitly indexing for clarity
        '''
        region_socket_id = 'SocketID_{}'.format(tmp['SocketID'])
        msg = "%s %s %s %s" % (get_linenumber(), "... Indexing", region_socket_id, '')
        message(msg, D2)
        regions[region_socket_id] = tmp

        region_id = 'RegionID_{}'.format(tmp['RegionID'])
        msg = "%s %s %s %s" % (get_linenumber(), "... Indexing", region_id, '')
        message(msg, D2)
        regions[region_id] = tmp

        region_iset_id = 'ISetID_{}'.format(tmp['ISetID'])
        msg = "%s %s %s %s" % (get_linenumber(), "... Indexing", region_iset_id, '')
        message(msg, D2)
        regions[region_iset_id] = tmp

    msg = "%s %s %s %s" % (get_linenumber(), "parse_region: Parse Complete:", xml_file, '')
    message(msg, D1)

    toc = time.perf_counter()
    delta_t = toc - tic
    td = {'name': name, "elapsed": delta_t, 'tic': tic, 'toc': toc}
    timers.append(td)

    return regions

def list_dimms(dimms):
    '''
    Print a list of PMEM DIMMs with select details
    '''
    name = 'list_dimms()'
    tic = time.perf_counter()

    print('%-6s' %  'DIMMID', end="  ")
    print('%-15s' %  'Health State', end="  ")
    print('%-21s' % 'PMEM DIMM UUID', end="  ")
    print('%-11s' % 'Capacity', end="  ")
    print('%-4s' %  'Skt', end="  ")
    print('%-4s' %  'iMC', end="  ")
    print('%-4s' %  'Chan', end="  ")
    print('%-4s' %  'Slot', end="  ")
    print('%-14s' %  'FW Version', end="  ")
    print('%-20s' % 'Device Locator', end="  ")
    print()
    
    print('%-6s' %  '------', end="  ")
    print('%-15s' %  '---------------', end="  ")
    print('%-21s' % '---------------------', end="  ")
    print('%-11s' % '-----------', end="  ")
    print('%4s' %  '----', end="  ")
    print('%4s' %  '----', end="  ")
    print('%4s' %  '----', end="  ")
    print('%4s' %  '----', end="  ")
    print('%14s' %  '--------------', end="  ")
    print('%-20s' % '--------------------', end="  ")
    print()
    
    for key in sorted(dimms.keys()):
        print('%-6s' % (dimms[key]['DimmID']), end="  ")
        print('%-15s' % (dimms[key]['HealthState']), end="  ")
        print('%-21s' % (dimms[key]['DimmUID']), end="  ")
        print('%-11s' % (dimms[key]['Capacity']), end="  ")
        print('%-4d' % (int(dimms[key]['SocketID'], 16)), end="  ")
        print('%-4d' % (int(dimms[key]['MemControllerID'], 16)), end="  ")
        print('%-4d' % (int(dimms[key]['ChannelID'], 16)), end="  ")
        print('%-4d' % (int(dimms[key]['ChannelPos'], 16)), end="  ")
        print('%-14s' % (dimms[key]['FWVersion']), end="  ")
        print('%-20s' % (dimms[key]['DeviceLocator']), end="  ")
        print()
    print()

    toc = time.perf_counter()
    delta_t = toc - tic
    td = {'name': name, "elapsed": delta_t, 'tic': tic, 'toc': toc}
    timers.append(td)

def get_dimms(filter = 'DimmNumber_'):
    '''
    returns dict of DIMM's with attributes for specified filter 

    dimms is a dict of dicts describing each DIMM's attributes
    several keys are used to enable looking up DIMM attributes with different methods
    depending on need
    dict indexes look like this
        DimmNumber_*    example: DimmNumber_0
        DimmID_*        example: DimmID_0x001
        DimmUID_*       example: DimmUID_8089-a2-1836-00002c4b
        DeviceLocator_* example: DeviceLocator_CPU1_DIMM_A2
    '''
    name = 'get_dimms()'
    tic = time.perf_counter()

    if show_dimm():
        d = parse_dimm()

    tmp = {}
    for key in sorted(d.keys()):
        if key.startswith(filter):
            tmp[key] = d[key]

    toc = time.perf_counter()
    delta_t = toc - tic
    td = {'name': name, "elapsed": delta_t, 'tic': tic, 'toc': toc}
    timers.append(td)

    return tmp

def get_dimm_list(socket_num = 0):
    '''returns list of DimmID's '''
    name = 'get_dimm_list()'
    tic = time.perf_counter()

    my_list = []

    my_filter = 'DimmID_0x' + str(socket_num)
    my_dict = get_dimms(my_filter)
    for i in sorted(my_dict.keys()):
        my_list.append(my_dict[i]['DimmID'])

    toc = time.perf_counter()
    delta_t = toc - tic
    td = {'name': name, "elapsed": delta_t, 'tic': tic, 'toc': toc}
    timers.append(td)

    return my_list


def get_socket(filter = 'SocketID_'):
    '''Returns list of sockets with attributes'''
    name = 'get_socket()'
    tic = time.perf_counter()

    if show_socket():
        s = parse_socket()

    tmp = {}
    for key in sorted(s.keys()):
        if key.startswith(filter):
            tmp[key] = s[key]

    toc = time.perf_counter()
    delta_t = toc - tic
    td = {'name': name, "elapsed": delta_t, 'tic': tic, 'toc': toc}
    timers.append(td)

    return tmp

def get_socket_list():
    '''returns list of SocketID's '''
    name = 'get_socket_list()'
    tic = time.perf_counter()

    my_list = []
    my_dict = get_socket()
    for i in sorted(my_dict.keys()):
        my_list.append(my_dict[i]['SocketID'])

    toc = time.perf_counter()
    delta_t = toc - tic
    td = {'name': name, "elapsed": delta_t, 'tic': tic, 'toc': toc}
    timers.append(td)

    return my_list

def get_region(filter = 'RegionID'):
    '''Returns list of regions with index keys'''
    name = 'get_region()'
    tic = time.perf_counter()

    if show_region():
        r = parse_region()

    tmp = {}

    for i in sorted(r.keys()):
        if i.startswith(filter):
            tmp[i] = r[i]

    toc = time.perf_counter()
    delta_t = toc - tic
    td = {'name': name, "elapsed": delta_t, 'tic': tic, 'toc': toc}
    timers.append(td)

    return tmp

def get_region_list():
    '''returns list of RegionID's '''
    name = 'get_region_list()'
    tic = time.perf_counter()

    my_list = []
    my_dict = get_region()

    for i in sorted(my_dict.keys()):
        my_list.append(my_dict[i]['RegionID'])

    toc = time.perf_counter()
    delta_t = toc - tic
    td = {'name': name, "elapsed": delta_t, 'tic': tic, 'toc': toc}
    timers.append(td)

    return my_list

def print_timers(t = timers):
    '''
    ------------ipmctl function timers---------------------
                Function  Elapsed       Start         End
    -------------------- --------- ----------- ------------
           show_socket()    0.5140 941291.4208  941291.9348
          parse_socket()    0.0004 941291.9348  941291.9352
             show_dimm()    2.0074 941291.9352  941293.9426
            parse_dimm()    0.0068 941293.9426  941293.9494
           show_region()    3.8237 941293.9494  941297.7731
          parse_region()    0.0006 941297.7732  941297.7737
             show_dimm()    2.5911 941297.7781  941300.3692
            parse_dimm()    0.0051 941300.3692  941300.3743
             get_dimms()    2.5962 941297.7781  941300.3744
            list_dimms()    0.0004 941300.3744  941300.3748
    '''
    print('------------Start ipmctl function timers---------------')
    print('%20s %8s %11s %11s' % ('Function', 'Elapsed', 'Start', 'End') )
    print('%20s %8s %11s %11s' % ('--------------------', '---------', '-----------', '------------') )

    first = t[0]['tic']
    last = t[len(t) -1]['toc']

    for i in t:
        print('%20s %9.4f %11.4f  %11.4f' % (i['name'], i['elapsed'], i['tic'], i['toc']) )

    print('%20s %9.4f %11.4f  %11.4f' % ('IPMCTL Overall', last - first, first, last) )

    print()
    print('------------End ipmctl function timers-----------------')

def main():
    '''
    main() calls functions wihtin this module to verify they function
    properly in this environment prior to being called from an external
    routine.
    '''
    name = 'main()'
    tic = time.perf_counter()

    import argparse

    global show_dimm_cmd
    global show_region_cmd
    global dimm_xml_file
    global region_xml_file

    global VERBOSE
    global white_list

    ap = argparse.ArgumentParser()
    # ap.add_argument("--dimm_xml_file", required=False, help="NVMXML input file from ipmctl show -o nvmxml show -a -dimm")
    # ap.add_argument("--region_xml_file", required=False, help="NVMXML input file from ipmctl show -o nvmxml show -a -region")
    ap.add_argument("--verbose", required=False, help="verbosity level ... verbose depths:1..5, debug depths:10..15")

    args = vars(ap.parse_args())

    # if args['dimm_xml_file']:  dimm_xml_file = args['dimm_xml_file']
    # if args['region_xml_file']:  region_xml_file = args['region_xml_file']
    if args['verbose']:  VERBOSE = args['verbose']

    msg = "%s %s %s %s" % (get_linenumber(), "Main:Begin:", '', '')
    message(msg, V0)

    '''DIMM Related Functions'''
    msg = "%s %s %s %s" % (get_linenumber(), "Main: calling show_dimm:", dimm_xml_file, '')
    message(msg, V0)
    if show_dimm(dimm_xml_file, show_dimm_cmd):
        msg = "%s %s %s %s" % (get_linenumber(), "Main: calling parse_dimms:", dimm_xml_file, '')
        message(msg, V0)
        dimms = parse_dimm()

        short_dimms = get_dimms()
        list_dimms(short_dimms)


    '''Socket Related Functions'''
    msg = "%s %s %s %s" % (get_linenumber(), "Main: calling show_socket:", socket_xml_file, '')
    message(msg, V0)
    if show_socket(socket_xml_file, show_socket_cmd):
        msg = "%s %s %s %s" % (get_linenumber(), "Main: calling parse_socket:", socket_xml_file, '')
        message(msg, V0)
        socket = parse_socket(socket_xml_file)
        #
        message('pp_dict socket',V0)
        pretty_print(socket)

    print('Verbosity:', VERBOSE)

    msg = "%s %s %s %s" % (get_linenumber(), "Main: calling get_dimm_list():", '', '')
    message(msg, V0)
    d = get_dimm_list()
    pretty_print(d)

    msg = "%s %s %s %s" % (get_linenumber(), "Main: calling get_socket_list():", '', '')
    message(msg, V0)
    d = get_socket_list()
    pretty_print(d)

    msg = "%s %s %s %s" % (get_linenumber(), "Main: calling get_region_list():", '', '')
    message(msg, V0)
    d = get_region_list()
    pretty_print(d)


    '''Region Related Functions'''
    msg = "%s %s %s %s" % (get_linenumber(), "Main: calling show_region:", region_xml_file, '')
    message(msg, V0)
    if show_region(region_xml_file, show_region_cmd):
        msg = "%s %s %s %s" % (get_linenumber(), "Main: calling parse_region:", region_xml_file, '')
        message(msg, V0)
        regions = parse_region(region_xml_file)
        #
        message('pp_dict regions',V0)
        pretty_print(regions)

        message('calling get_region()', V0)
        r = get_region()
        message('PP regions',V0)
        pretty_print(r)

        message('calling get_region_list()', V0)
        r = get_region_list()
        message('PP region list',V0)
        pretty_print(r)

    toc = time.perf_counter()
    delta_t = toc - tic
    td = {'name': name, "elapsed": delta_t, 'tic': tic, 'toc': toc}
    timers.append(td)

    print_timers()

if __name__ == '__main__':
    main()

