#!/usr/bin/python3

import xml.etree.ElementTree as ET
import sys
import os


'''
this is the current list of fields available from Optane PMEM 100 series
They are included here for completeness
'''
white_list = {}
white_list[' DimmID '] = 0 #   DimmID :  0x0001
white_list[' Capacity '] = 0 #   Capacity :  252.454 GiB
white_list[' LockState '] = 0 #   LockState :  Disabled
white_list[' SVNDowngrade '] = 0 #   SVNDowngrade :  Unknown
white_list[' SecureErasePolicy '] = 0 #   SecureErasePolicy :  Unknown
white_list[' S3ResumeOptIn '] = 0 #   S3ResumeOptIn :  Unknown
white_list[' FwActivateOptIn '] = 0 #   FwActivateOptIn :  Unknown
white_list[' HealthState '] = 0 #   HealthState :  Healthy
white_list[' HealthStateReason '] = 0 #   HealthStateReason :  None
white_list[' FWVersion '] = 0 #   FWVersion :  01.02.00.5446
white_list[' FWAPIVersion '] = 0 #   FWAPIVersion :  01.15
white_list[' InterfaceFormatCode '] = 0 #   InterfaceFormatCode :  0x0301 (Non-Energy Backed Byte Addressable)
white_list[' ManageabilityState '] = 0 #   ManageabilityState :  Manageable
white_list[' PopulationViolation '] = 0 #   PopulationViolation :  No
white_list[' PhysicalID '] = 0 #   PhysicalID :  0x0026
white_list[' DimmHandle '] = 0 #   DimmHandle :  0x0001
white_list[' DimmUID '] = 0 #   DimmUID :  8089-a2-1836-00002c4b
white_list[' SocketID '] = 0 #   SocketID :  0x0000
white_list[' MemControllerID '] = 0 #   MemControllerID :  0x0000
white_list[' ChannelID '] = 0 #   ChannelID :  0x0000
white_list[' ChannelPos '] = 0 #   ChannelPos :  1
white_list[' MemoryType '] = 0 #   MemoryType :  Logical Non-Volatile Device
white_list[' Manufacturer '] = 0 #   Manufacturer :  Intel
white_list[' VendorID '] = 0 #   VendorID :  0x8089
white_list[' DeviceID '] = 0 #   DeviceID :  0x5141
white_list[' RevisionID '] = 0 #   RevisionID :  0x0000
white_list[' SubsystemVendorID '] = 0 #   SubsystemVendorID :  0x8089
white_list[' SubsystemDeviceID '] = 0 #   SubsystemDeviceID :  0x097a
white_list[' SubsystemRevisionID '] = 0 #   SubsystemRevisionID :  0x0018
white_list[' DeviceLocator '] = 0 #   DeviceLocator :  CPU1_DIMM_A2
white_list[' ManufacturingInfoValid '] = 0 #   ManufacturingInfoValid :  1
white_list[' ManufacturingLocation '] = 0 #   ManufacturingLocation :  0xa2
white_list[' ManufacturingDate '] = 0 #   ManufacturingDate :  18-36
white_list[' SerialNumber '] = 0 #   SerialNumber :  0x00002c4b
white_list[' PartNumber '] = 0 #   PartNumber :  NMA1XBD256GQS
white_list[' BankLabel '] = 0 #   BankLabel :  NODE 1
white_list[' DataWidth '] = 0 #   DataWidth :  64 b
white_list[' TotalWidth '] = 0 #   TotalWidth :  72 b
white_list[' Speed '] = 0 #   Speed :  2666 MT/s
white_list[' FormFactor '] = 0 #   FormFactor :  DIMM
white_list[' ManufacturerID '] = 0 #   ManufacturerID :  0x8089
white_list[' ControllerRevisionID '] = 0 #   ControllerRevisionID :  B0, 0x0020
white_list[' MemoryCapacity '] = 0 #   MemoryCapacity :  0.000 GiB
white_list[' AppDirectCapacity '] = 0 #   AppDirectCapacity :  252.000 GiB
white_list[' UnconfiguredCapacity '] = 0 #   UnconfiguredCapacity :  0.000 GiB
white_list[' InaccessibleCapacity '] = 0 #   InaccessibleCapacity :  0.454 GiB
white_list[' ReservedCapacity '] = 0 #   ReservedCapacity :  0.000 GiB
white_list[' PackageSparingCapable '] = 0 #   PackageSparingCapable :  1
white_list[' PackageSparingEnabled '] = 0 #   PackageSparingEnabled :  1
white_list[' PackageSparesAvailable '] = 0 #   PackageSparesAvailable :  1
white_list[' IsNew '] = 0 #   IsNew :  0
white_list[' ViralPolicy '] = 0 #   ViralPolicy :  0
white_list[' ViralState '] = 0 #   ViralState :  0
white_list[' PeakPowerBudget '] = 0 #   PeakPowerBudget :  20000 mW
white_list[' AvgPowerLimit '] = 0 #   AvgPowerLimit :  15000 mW
white_list[' MaxAveragePowerLimit '] = 0 #   MaxAveragePowerLimit :  18000 mW
white_list[' LatchedLastShutdownStatus '] = 0 #   LatchedLastShutdownStatus :  PM S5 Received, PMIC 12V/DDRT 1.2V Power Loss (PLI), Controller's FW State Flush Complete, Write Data Flush Complete, PM Idle Received, Extended Flush Not Complete
white_list[' UnlatchedLastShutdownStatus '] = 0 #   UnlatchedLastShutdownStatus :  PMIC 12V/DDRT 1.2V Power Loss (PLI), PM Warm Reset Received, Controller's FW State Flush Complete, Write Data Flush Complete, PM Idle Received, Extended Flush Not Complete
white_list[' ThermalThrottleLossPercent '] = 0 #   ThermalThrottleLossPercent :  N/A
white_list[' LastShutdownTime '] = 0 #   LastShutdownTime :  Mon Dec 27 17:43:55 UTC 2021
white_list[' ModesSupported '] = 0 #   ModesSupported :  Memory Mode, App Direct
white_list[' SecurityCapabilities '] = 0 #   SecurityCapabilities :  Encryption, Erase
white_list[' MasterPassphraseEnabled '] = 0 #   MasterPassphraseEnabled :  0
white_list[' ConfigurationStatus '] = 0 #   ConfigurationStatus :  Valid
white_list[' SKUViolation '] = 0 #   SKUViolation :  0
white_list[' ARSStatus '] = 0 #   ARSStatus :  Completed
white_list[' OverwriteStatus '] = 0 #   OverwriteStatus :  Unknown
white_list[' AitDramEnabled '] = 0 #   AitDramEnabled :  1
white_list[' BootStatus '] = 0 #   BootStatus :  Success
white_list[' BootStatusRegister '] = 0 #   BootStatusRegister :  0x00000004_981d00f0
white_list[' ErrorInjectionEnabled '] = 0 #   ErrorInjectionEnabled :  0
white_list[' MediaTemperatureInjectionEnabled '] = 0 #   MediaTemperatureInjectionEnabled :  0
white_list[' SoftwareTriggersEnabled '] = 0 #   SoftwareTriggersEnabled :  0
white_list[' SoftwareTriggersEnabledDetails '] = 0 #   SoftwareTriggersEnabledDetails :  None
white_list[' PoisonErrorInjectionsCounter '] = 0 #   PoisonErrorInjectionsCounter :  0
white_list[' PoisonErrorClearCounter '] = 0 #   PoisonErrorClearCounter :  0
white_list[' MediaTemperatureInjectionsCounter '] = 0 #   MediaTemperatureInjectionsCounter :  0
white_list[' SoftwareTriggersCounter '] = 0 #   SoftwareTriggersCounter :  0
white_list[' MaxControllerTemperature '] = 0 #   MaxControllerTemperature :  80 C
white_list[' MaxMediaTemperature '] = 0 #   MaxMediaTemperature :  78 C
white_list[' MixedSKU '] = 0 #   MixedSKU :  0

'''
Here are the values we care about for now
'''
white_list['Capacity'] = 1 # 'Capacity': '252.454 GiB'
white_list['DimmUID'] = 1 # 'DimmUID': '8089-a2-1836-00002c4b'
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


def show_dimm(xml_file, show_dimm_cmd):
    '''
    runs show dimm cmd string, sending output to xml_file
    returns True if sucessful
    '''
    status = False

    return status

def parse_dimms(xml_file):
    '''
    parses output of show -a -dimm command
    returns dimms dict with data from xml file
    see white_list for fields of interest
    '''
    dimms = {}

    tree = ET.parse(file_name)
    root = tree.getroot()
    dimms = {}

    for dimm in range( len(root)):
        tmp = {}
        for dimm_attr in range(len(root[dimm])):
            tmp[root[dimm][dimm_attr].tag] = root[dimm][dimm_attr].text

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

    return dimms

def show_region((xml_file, show_region_cmd):
    '''
    runs show dimm cmd string, sending output to xml_file
    returns True if sucessful
    '''
    status = False
    return status

def parse_regions(xml_file):
    '''
    parses output of show -a -regions command
    returns regions dict with data from xml file
    '''
    regions = {}

    return regions

def main():

    global show_dimm_cmd
    global show_region_cmd
    global dimm_xml_file
    global region_xml_file

    if show_dimm(dimm_xml_file, show_dimm_cmd):
        parse_dimms(dimm_xml_file)

    if show_region((region_xml_file, show_region_cmd):
        parse_regions(region_xml_file)


if __name__ == '__main__':
    main()

