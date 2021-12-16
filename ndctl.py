#!/usr/bin/python3
#
# PMTOOL NDCTL Python Module
# Copyright (C) David P Larsen
# Released under MIT License

import os
import json

DEFAULT_FSTAB_FILE = "/etc/fstab"
DEFAULT_NDCTL_FILE = "/tmp/ndctl_list_NDRH.txt"

DEBUG = 0
VERBOSE = 0

# If working in a test sandbox, change paths
# to start with path to sandbox
#
if not os.getenv('SANDBOX'):
    SANDBOX = ''
else:
    SANDBOX = os.environ['SANDBOX']
    print('Enabling Sandbox at:', SANDBOX)

# FSTAB = SANDBOX + '/etc/fstab'
DEVDIR = SANDBOX + '/dev'
DEV_UUID = DEVDIR + '/disk/by-uuid/'
NDCTL_FILE = SANDBOX + "/tmp/ndctl_list_NDRH.txt"

# print("FSTAB", FSTAB)
if VERBOSE: print("DEVDIR", DEVDIR)
if VERBOSE: print("DEV_UUID", DEV_UUID)
if VERBOSE: print("NDCTL_FILE", NDCTL_FILE)


# ndctlFile = "/tmp/ndctl_list_NDRH.txt"
ndctl = {}

def dump(file_name = NDCTL_FILE):
    """
    dump the config to a file to parse
    """

    if DEBUG: print("DEBUG: Function:", __name__, "File:", file_name )
    if VERBOSE: print('  Querying ndctl data:', file_name, end="...")
    
    # ndctl list -NDRH
    cmd = "/usr/bin/ndctl list -NDRH > " + file_name
    os.system(cmd)

    if VERBOSE: print('Done')

def parse(file_name = NDCTL_FILE):
    """
    parse ndctl dump file into dict: ndctl
    """

    global ndctl

    if DEBUG: print("DEBUG: Function:", __name__, "File:", file_name )
    if VERBOSE: print('  Parsing ndctl data:', file_name, end="...")

    with open(file_name, 'r') as f:
        ndctl  =  json.load(f)

    if VERBOSE: print('Done')
    if DEBUG: print("Debug:", __name__, ":",  ndctl)

    return ndctl

# - +- +- +- +- +- +- +- +- +- +- +- +- +- +- +- +- +- +- +- +
# Accessor Functions
#
def get_region_dimm_list(region):
    """
        returns list of pmem dimms assocaited with pmem region
    """
    global ndctl
    dimm_list = []

    if DEBUG: print("DEBUG: Function:", __name__, "Region:", region )
    if VERBOSE: print('  getting:', __name__, end="...")

    for r in range(len(ndctl['regions'])):
        # if this region matches arg, get DIMM mappings
        if ndctl['regions'][r]['dev'] == region:
            for d in range(len(ndctl['regions'][r]['mappings'])):
               if DEBUG: print('  ndctl[regions][r]mappings', ndctl['regions'][r]['mappings'][d]['dimm'])
               dimm_list.append(ndctl['regions'][r]['mappings'][d]['dimm'])
        continue

    if VERBOSE: print('Done')
    if DEBUG: print("Debug:", __name__, region, "DIMMS",  dimm_list)

    return dimm_list

def get_region_list():
    """
        Region List
        returns list of all pmem regions
    """
    global ndctl
    region_list = []

    if DEBUG: print("DEBUG: Function:", __name__ )
    if VERBOSE: print('  getting:', __name__, end="...")

    for r in range(len(ndctl['regions'])):
        region_list.append(ndctl['regions'][r]['dev'])

    if VERBOSE: print('Done')
    if DEBUG: print("Debug:", __name__, ":",  region_list)

    return region_list


def get_region_ns_device_list(region):
    """
        Region Namespace Device List
        returns list of all pmem namespaces names associated w/ pmem region
    """
    ns_list = []

    if DEBUG: print("DEBUG: Function:", __name__, "Region:", region )
    if VERBOSE: print('  getting:', __name__, end="...")

    for r in range(len(ndctl['regions'])):
        # if this region matches arg, get DIMM mappings
        if ndctl['regions'][r]['dev'] == region:
            for d in range(len(ndctl['regions'][r]['namespaces'])):
               if DEBUG: print('  ndctl[regions][r]mappings', ndctl['regions'][r]['mappings'][d]['dimm'])
               ns_list.append(ndctl['regions'][r]['namespaces'][d]['blockdev'])
        continue

    if VERBOSE: print('Done')

    return ns_list


def get_region_ns_name_list(region):
    """
        Region Namespace List
        returns list of all pmem namespaces names associated w/ pmem region
    """
    ns_list = []

    if DEBUG: print("DEBUG: Function:", __name__, "Region:", region )
    if VERBOSE: print('  getting:', __name__, end="...")

    for r in range(len(ndctl['regions'])):
        # if this region matches arg, get DIMM mappings
        if ndctl['regions'][r]['dev'] == region:
            for d in range(len(ndctl['regions'][r]['namespaces'])):
               if DEBUG: print('  ndctl[regions][r]mappings', ndctl['regions'][r]['mappings'][d]['dimm'])
               ns_list.append(ndctl['regions'][r]['namespaces'][d]['dev'])
        continue

    if VERBOSE: print('Done')

    return ns_list


def get_dimm_status(dimm):
    """
        DIMM List
        returns status of given dimm
    """

    # dimm_list = []

    if DEBUG: print("DEBUG: Function:", __name__ )
    if VERBOSE: print('  getting:', __name__, end="...")

    for d in range(len(ndctl['dimms'])):
        if DEBUG: print(ndctl['dimms'][d]['dev'], ndctl['dimms'][d]['health']['health_state'])

        if ndctl['dimms'][d]['dev'] == dimm:
            status = ndctl['dimms'][d]['health']['health_state']
            break

    if VERBOSE: print('Done')
    if DEBUG: print("Debug:", __name__, ":",  dimmList)

    return status


def get_dimm_list():
    """
        DIMM List
        returns list of all pmem devices in system
    """
    dimm_list = []

    if DEBUG: print("DEBUG: Function:", __name__ )
    if VERBOSE: print('  getting:', __name__, end="...")

    for d in range(len(ndctl['dimms'])):
        dimm_list.append(ndctl['dimms'][d]['dev'])


    if VERBOSE: print('Done')
    if DEBUG: print("Debug:", __name__, ":",  dimmList)

    return dimm_list


def get_region_by_dimm(dimm):
    """
        Get Region by DIMM 
        returns region associated with PMEM device
    """
    region = "regionX"

    if DEBUG: print("DEBUG: Function:", __name__ )
    if VERBOSE: print('  getting:', __name__, end="...")

    # loop through regions, get dimmList for each, check if match
    for r in range(len(ndctl['regions'])):
        region = ndctl['regions'][r]['dev']
        dimmList = get_region_dimm_list(region)
        # print("get_region_by_dimm.r", r, region, dimmList )
        if dimm in dimmList: break

    if VERBOSE: print('Done')
    if DEBUG: print("Debug:", __name__, ":",  region)

    return region


# WIP - not qite working right
def get_ns_name_list_by_dimm(dimm):
    """
        Get PMEM Namespace name by DIMM 
        returns list of pmem namespaces associated with  name
    """
    nsNameList = []

    if DEBUG: print("DEBUG: Function:", __name__ )
    if VERBOSE: print('  getting:', __name__, end="...")

    # loop through regions, get dimmList for each, check if match
    for r in range(len(ndctl['regions'])):
        region = ndctl['regions'][r]['dev']
        dimmList = get_region_dimm_list(region)

        # we should have a region to lookup namespaces
        nsNameList = get_region_ns_name_list(region)

        if dimm in dimmList: break

    if VERBOSE: print('Done')
    if DEBUG: print("Debug:", __name__, ":",  nsNameList)

    return nsNameList


def get_ns_device_list_by_dimm(dimm):
    """
        Get Namespace Devices by DIMM 
        returns pmem namespace device for given DIMM
    """
    ns_device_list = []
    dimm_list = []

    if DEBUG: print("DEBUG: Function:", __name__ )
    if VERBOSE: print('  getting:', __name__, end="...")

    # loop through regions, get dimmList for each, check if match
    for r in range(len(ndctl['regions'])):
        region = ndctl['regions'][r]['dev']
        dimm_list = get_region_dimm_list(region)

        # we should have a region to lookup namespaces
        ns_device_list = get_region_ns_device_list(region)

        if dimm in dimm_list: break

    if VERBOSE: print('Done')
    if DEBUG: print("Debug:", __name__, ":",  ns_device_list)

    return ns_device_list

def list_dimm_table():

    # Heading
    print("%-8s %-6s %-6s %-6s %-6s" % ("Linux", "DIMM", "DIMM", "Cntrl", "Remaining") )
    print("%-8s %-6s %-6s %-6s %-6s" % ("Device", "Health", "Temp", "Temp", "Life") )
    print("%-8s %-6s %-6s %-6s %-6s" % ("------", "------", "------", "------", "----") )

    for x in range(len(ndctl['dimms'])):
        print("%-8s %-6s %-6s %-6s %-6s" % (
                ndctl['dimms'][x]['dev'], \
                ndctl['dimms'][x]['health']['health_state'], \
                ndctl['dimms'][x]['health']['temperature_celsius'], \
                ndctl['dimms'][x]['health']['controller_temperature_celsius'], \
                ndctl['dimms'][x]['health']['spares_percentage'] \
            ))


def module_test():
    import sys
    import os

    global VERBOSE
    global DEBUG

    VERBOSE = 0
    DEBUG = 0

    # Dicts
    ndctl = {}

    # Lists
    regionList = []
    dimmList = []
    nsList = []
    nsDeviceList = []
    nsNameList = []

    region = "region1"
    dimm = "nmem0"

    print("Module: ndctl.py: Testing Functions")
    dump()
    ndctl = parse()

    # OK
    dimmList = get_dimm_list()
    print("  MAIN:get_dimm_list:dimmList:", dimmList)

    # OK
    regionList = get_region_list()
    print("  MAIN:get_region_list:regionList:", regionList)

    # OK
    dimmList   = get_region_dimm_list(region)
    print("  MAIN:get_region_dimm_list:dimmList", " Region:", region, "DIMM's",  dimmList)

    # OK
    region = "region0"
    nsList     = get_region_ns_name_list(region)
    print("  MAIN:get_region_ns_name_list:nsList", " Region:", region, "NS", nsList)
    # OK
    region = "region1"
    nsList     = get_region_ns_device_list(region)
    print("  MAIN:get_region_ns_device_list:nsList", " Region:", region, "NS", nsList)

    dimm = "nmem1"
    region = get_region_by_dimm(dimm)
    print("  MAIN:get_region_by_dimm:region", " DIMM:", dimm, "Region:", region)

    nsDeviceList = get_ns_device_list_by_dimm(dimm)
    print("  MAIN:get_ns_device_list_by_dimm:nsDeviceList", nsDeviceList)

    nsNameList = get_ns_name_list_by_dimm(dimm)
    print("  MAIN:get_ns_name_list_by_dimm:nsNameList", nsNameList)

    dimm = "nmem8"
    dimmStatus = get_dimm_status(dimm)
    print("  MAIN:get_dimm_status:dimmStatus", dimm, dimmStatus)

    print("  MAIN:listDimmsFull")
    list_dimm_table()


def main():
    print("This module is not intended to run standalone")
    print("import this module into your script to use or use")
    print("Persistent Memory Tool, pmt")

if __name__ == "__main__":
    main()

