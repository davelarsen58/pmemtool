#!/usr/bin/python3
#
# PMTOOL NDCTL Python Module
#
# @ Copyright Intel 2021
# Released under NDA to Walgreens for use with Optane Persistent Memory
# All rights reserved
# Provided as Sample Code with no warranty
# December 06, 2021
# Version: 0.71


# Available Functions
# ------------------------
# ndctlDump(f = ndctlFile)
# ndctlParse(f = ndctlFile)
#
# getDimmList()
# getRegionList()
# getRegionDimmList(region)
# getRegionNsList(region)
#
# getRegionByDimm(dimm)
# getNsDeviceListByDimm(dimm)
# getNsNameListByDimm(dimm)

import os
import json

ndctlFile = "/tmp/ndctl_list_NDRH.txt"
ndctl = {}
debug = 0
verbose = 0

# dump the config to a file to parse
def dump(f = ndctlFile):

    if debug: print("DEBUG: Function:", __name__, "File:", f )
    if verbose: print('  Querying ndctl data:', f, end="...")
    
    # ndctl list -NDRH
    cmd = "/usr/bin/ndctl list -NDRH > " + f
    os.system(cmd)

    if verbose: print('Done')

# parse ndctl dump file into dict: ndctl
def parse(f = ndctlFile):

    global ndctl

    if debug: print("DEBUG: Function:", __name__, "File:", ndctlFile )
    if verbose: print('  Parsing ndctl data:', ndctlFile, end="...")

    with open(ndctlFile, 'r') as f:
        ndctl  =  json.load(f)

    if verbose: print('Done')
    if debug: print("Debug:", __name__, ":",  ndctl)

    return ndctl

# - +- +- +- +- +- +- +- +- +- +- +- +- +- +- +- +- +- +- +- +
# Accessor Functions
#
# DIMM List
# returns list of pmem dimms assocaited with pmem region
def getRegionDimmList(region):
    global ndctl
    dimmList = []

    if debug: print("DEBUG: Function:", __name__, "Region:", region )
    if verbose: print('  getting:', __name__, end="...")

    for r in range(len(ndctl['regions'])):
        # if this region matches arg, get DIMM mappings
        if ndctl['regions'][r]['dev'] == region:
            for d in range(len(ndctl['regions'][r]['mappings'])):
               if debug: print('  ndctl[regions][r]mappings', ndctl['regions'][r]['mappings'][d]['dimm'])
               dimmList.append(ndctl['regions'][r]['mappings'][d]['dimm'])
        continue

    if verbose: print('Done')
    if debug: print("Debug:", __name__, region, "DIMMS",  dimmList)

    return dimmList

# Region List
# returns list of all pmem regions
def getRegionList():
    global ndctl
    regionList = []

    if debug: print("DEBUG: Function:", __name__ )
    if verbose: print('  getting:', __name__, end="...")

    for r in range(len(ndctl['regions'])):
        regionList.append(ndctl['regions'][r]['dev'])

    if verbose: print('Done')
    if debug: print("Debug:", __name__, ":",  regionList)

    return regionList


# Region Namespace Device List
# returns list of all pmem namespaces names associated w/ pmem region
def getRegionNsDeviceList(region):
    # global ndctl
    nsList = []

    if debug: print("DEBUG: Function:", __name__, "Region:", region )
    if verbose: print('  getting:', __name__, end="...")

    for r in range(len(ndctl['regions'])):
        # if this region matches arg, get DIMM mappings
        if ndctl['regions'][r]['dev'] == region:
            for d in range(len(ndctl['regions'][r]['namespaces'])):
               if debug: print('  ndctl[regions][r]mappings', ndctl['regions'][r]['mappings'][d]['dimm'])
               nsList.append(ndctl['regions'][r]['namespaces'][d]['blockdev'])
        continue

    if verbose: print('Done')

    return nsList


# Region Namespace List
# returns list of all pmem namespaces names associated w/ pmem region
def getRegionNsNameList(region):
    # global ndctl
    nsList = []

    if debug: print("DEBUG: Function:", __name__, "Region:", region )
    if verbose: print('  getting:', __name__, end="...")

    for r in range(len(ndctl['regions'])):
        # if this region matches arg, get DIMM mappings
        if ndctl['regions'][r]['dev'] == region:
            for d in range(len(ndctl['regions'][r]['namespaces'])):
               if debug: print('  ndctl[regions][r]mappings', ndctl['regions'][r]['mappings'][d]['dimm'])
               nsList.append(ndctl['regions'][r]['namespaces'][d]['dev'])
        continue

    if verbose: print('Done')

    return nsList


# DIMM List
# returns status of given dimm
def getDimmStatus(dimm):

    dimmList = []

    if debug: print("DEBUG: Function:", __name__ )
    if verbose: print('  getting:', __name__, end="...")

    for d in range(len(ndctl['dimms'])):
        if debug: print(ndctl['dimms'][d]['dev'], ndctl['dimms'][d]['health']['health_state'])

        if ndctl['dimms'][d]['dev'] == dimm:
            status = ndctl['dimms'][d]['health']['health_state']
            break


    if verbose: print('Done')
    if debug: print("Debug:", __name__, ":",  dimmList)

    return status


# DIMM List
# returns list of all pmem devices in system
def getDimmList():
    # global ndctl
    dimmList = []

    if debug: print("DEBUG: Function:", __name__ )
    if verbose: print('  getting:', __name__, end="...")

    # dimmList.append("nmemX")
    for d in range(len(ndctl['dimms'])):
        dimmList.append(ndctl['dimms'][d]['dev'])


    if verbose: print('Done')
    if debug: print("Debug:", __name__, ":",  dimmList)

    return dimmList


# Get Region by DIMM 
# returns region associated with PMEM device
def getRegionByDimm(dimm):
    # global ndctl
    region = "regionX"

    if debug: print("DEBUG: Function:", __name__ )
    if verbose: print('  getting:', __name__, end="...")

    # loop through regions, get dimmList for each, check if match
    for r in range(len(ndctl['regions'])):
        region = ndctl['regions'][r]['dev']
        dimmList = getRegionDimmList(region)
        # print("getRegionByDimm.r", r, region, dimmList )
        if dimm in dimmList: break

    if verbose: print('Done')
    if debug: print("Debug:", __name__, ":",  region)

    return region


# Get PMEM Namespace name by DIMM 
# returns list of pmem namespaces associated with  name
# WIP - not qite working right
def getNsNameListByDimm(dimm):
    # global ndctl
    nsNameList = []

    if debug: print("DEBUG: Function:", __name__ )
    if verbose: print('  getting:', __name__, end="...")

    # loop through regions, get dimmList for each, check if match
    for r in range(len(ndctl['regions'])):
        region = ndctl['regions'][r]['dev']
        dimmList = getRegionDimmList(region)

        # we should have a region to lookup namespaces
        nsNameList = getRegionNsNameList(region)

        if dimm in dimmList: break

    if verbose: print('Done')
    if debug: print("Debug:", __name__, ":",  nsNameList)

    return nsNameList


# Get Namespace Devices by DIMM 
# returns pmem namespace device for given DIMM
def getNsDeviceListByDimm(dimm):
    nsDeviceList = []

    if debug: print("DEBUG: Function:", __name__ )
    if verbose: print('  getting:', __name__, end="...")

    # loop through regions, get dimmList for each, check if match
    for r in range(len(ndctl['regions'])):
        region = ndctl['regions'][r]['dev']
        dimmList = getRegionDimmList(region)

        # we should have a region to lookup namespaces
        nsDeviceList = getRegionNsDeviceList(region)

        if dimm in dimmList: break

    if verbose: print('Done')
    if debug: print("Debug:", __name__, ":",  nsDeviceList)

    return nsDeviceList

def listDimmTable():

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

    global verbose
    global debug

    verbose = 0
    debug = 0

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
    dimmList = getDimmList()
    print("  MAIN:getDimmList:dimmList:", dimmList)

    # OK
    regionList = getRegionList()
    print("  MAIN:getRegionList:regionList:", regionList)

    # OK
    dimmList   = getRegionDimmList(region)
    print("  MAIN:getRegionDimmList:dimmList", " Region:", region, "DIMM's",  dimmList)

    # OK
    region = "region0"
    nsList     = getRegionNsNameList(region)
    print("  MAIN:getRegionNsNameList:nsList", " Region:", region, "NS", nsList)
    # OK
    region = "region1"
    nsList     = getRegionNsDeviceList(region)
    print("  MAIN:getRegionNsDeviceList:nsList", " Region:", region, "NS", nsList)

    dimm = "nmem1"
    region = getRegionByDimm(dimm)
    print("  MAIN:getRegionByDimm:region", " DIMM:", dimm, "Region:", region)

    nsDeviceList = getNsDeviceListByDimm(dimm)
    print("  MAIN:getNsDeviceListByDimm:nsDeviceList", nsDeviceList)

    nsNameList = getNsNameListByDimm(dimm)
    print("  MAIN:getNsNameListByDimm:nsNameList", nsNameList)

    dimm = "nmem8"
    dimmStatus = getDimmStatus(dimm)
    print("  MAIN:getDimmStatus:dimmStatus", dimm, dimmStatus)

    print("  MAIN:listDimmsFull")
    listDimmTable()


def main():
    print("This module is not intended to run standalone")
    print("import this module into your script to use or use")
    print("Persistent Memory Tool, pmt")

if __name__ == "__main__":
    main()

