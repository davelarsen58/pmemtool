#!/usr/bin/python3
#
# PMTOOL NDCTL Python Module
# Copyright (C) David P Larsen
# Released under MIT License

import os
import json
from common import message, get_linenumber, pretty_print
from common import V0, V1, V2, V3, V4, V5, D0, D1, D2, D3, D4, D5
import common as c

import time

DEFAULT_FSTAB_FILE = "/etc/fstab"
DEFAULT_NDCTL_FILE = "/tmp/ndctl_list_NDRH.txt"

DEBUG = 0
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

# FSTAB = SANDBOX + '/etc/fstab'
DEVDIR = SANDBOX + '/dev'
DEV_UUID = DEVDIR + '/disk/by-uuid/'
NDCTL_FILE = SANDBOX + "/tmp/ndctl_list_NDRH.txt"

ndctl = {}

# ---------------------------------------------------------------------
def clean_up():
    '''clean up all tmp files associated with this mdule'''
    name = 'clean_up()'
    tic = time.perf_counter()

    status = False

    file_name = '/tmp/ndctl*.txt'
    status = c.clean_up(file_name)

    toc = time.perf_counter()
    delta_t = toc - tic
    td = {'name': name, "elapsed": delta_t, 'tic': tic, 'toc': toc}
    timers.append(td)

    return status

def get_nmem_dev_list(node):
    ''' returns list of nmems['nmem0' 'nmem1' 'nmem2' 'nmem3' 'nmem4' 'nmem5']
    ndctl list -D -U 0
    {
    "dev":"nmem2",
    "id":"8089-a2-1836-00002716",
    "handle":33,
    "phys_id":42,
    "flag_failed_flush":true,
    "flag_smart_event":true,
    "security":"disabled"
    }
    '''

    name = 'get_nmem_dev_list()'
    tic = time.perf_counter()

    file_name = '/tmp/ndctl_list_-D_-U_node' + str(node) + '.txt'
    cmd = "/usr/bin/ndctl list -D -U " + str(node) + " > " + file_name

    if not os.path.exists(file_name):
        os.system(cmd)
    
    tmp = {}
    my_list = []

    with open(file_name, 'r') as f:
        tmp  =  json.load(f)

    for t in range(len(tmp)):
        my_list.append(tmp[0]['dev'])
        
    toc = time.perf_counter()
    delta_t = toc - tic
    td = {'name': name, "elapsed": delta_t, 'tic': tic, 'toc': toc}
    timers.append(td)

    return my_list

# ---------------------------------------------------------------------
def get_region_dev_list(node):
    ''' returns list of regions devices, ie: "region0"
    ndctl list -U 0
    [
        {
        "dev":"region0",
        "size":1623497637888,
        "available_size":0,
        "max_available_extent":0,
        "type":"pmem",
        "iset_id":-7155516910447809332,
        "persistence_domain":"memory_controller"
        }
    ]
    '''
    name = 'get_region_dev_list()'
    tic = time.perf_counter()

    file_name = '/tmp/ndctl_list_-R_-U_node' + str(node) + '.txt'
    cmd = "/usr/bin/ndctl list -R -U " + str(node) + " > " + file_name
    if not os.path.exists(file_name):
        os.system(cmd)
    
    #
    tmp = {}
    with open(file_name, 'r') as f:
        tmp  =  json.load(f)

    my_list = []
    for t in range(len(tmp)):
        my_list.append(tmp[0]['dev'])

    toc = time.perf_counter()
    delta_t = toc - tic
    td = {'name': name, "elapsed": delta_t, 'tic': tic, 'toc': toc}
    timers.append(td)

    return my_list


# ---------------------------------------------------------------------
def get_ns_dev(node):
    ''' returns list of namespace names, ie: "namespace0.0"
    ndctl list -U 0
    [
        {
            "dev":"namespace0.0",
            "mode":"fsdax",
            "map":"dev",
            "size":1598128390144,
            "uuid":"115ff8e8-bd52-47b8-a678-9b200902d864",
            "sector_size":512,
            "align":2097152,
            "blockdev":"pmem0"
        }
        ]
    '''
    name = 'get_ns_dev()'
    tic = time.perf_counter()

    file_name = '/tmp/ndctl_list_-N_-U' + str(node) + '.txt'
    cmd = "/usr/bin/ndctl list -N -U " + str(node) + " > " + file_name
    os.system(cmd)
    #
    tmp = {}
    with open(file_name, 'r') as f:
        tmp  =  json.load(f)
    #
    my_list = []
    for t in range(len(tmp)):
        my_list.append(tmp[0]['dev'])
    #
    toc = time.perf_counter()
    delta_t = toc - tic
    td = {'name': name, "elapsed": delta_t, 'tic': tic, 'toc': toc}
    timers.append(td)

    return my_list


# ---------------------------------------------------------------------
def get_ns_block_dev(node):
    ''' returns list of ns blockdevs, ie: "pmem0"
    ndctl list -U 0
    [
        {
            "dev":"namespace0.0",
            "mode":"fsdax",
            "map":"dev",
            "size":1598128390144,
            "uuid":"115ff8e8-bd52-47b8-a678-9b200902d864",
            "sector_size":512,
            "align":2097152,
            "blockdev":"pmem0"
        }
        ]
    '''
    name = 'get_ns_block_dev()'
    tic = time.perf_counter()


    file_name = '/tmp/ndctl_list_-N_-U' + str(node) + '.txt'
    cmd = "/usr/bin/ndctl list -N -U " + str(node) + " > " + file_name
    os.system(cmd)
    #
    tmp = {}
    with open(file_name, 'r') as f:
        tmp  =  json.load(f)
    #
    my_list = []
    for t in range(len(tmp)):
        my_list.append(tmp[0]['blockdev'])
    #
    toc = time.perf_counter()
    delta_t = toc - tic
    td = {'name': name, "elapsed": delta_t, 'tic': tic, 'toc': toc}
    timers.append(td)

    return my_list

# ---------------------------------------------------------------------
def dump(file_name = NDCTL_FILE):
    """
    dump the config to a file to parse
    """
    name = 'dump()'
    tic = time.perf_counter()


    # message("Function:", __name__, "File:", file_name )
    # if VERBOSE: print('  Querying ndctl data:', file_name, end="...")
    
    # ndctl list -NDRH
    cmd = "/usr/bin/ndctl list -NDRH > " + file_name
    os.system(cmd)

    # if VERBOSE: print('Done')

def parse(file_name = NDCTL_FILE):
    """
    parse ndctl dump file into dict: ndctl
    """
    name = 'parse()'
    tic = time.perf_counter()


    global ndctl

    # if DEBUG: print("DEBUG: Function:", __name__, "File:", file_name )
    # if VERBOSE: print('  Parsing ndctl data:', file_name, end="...")

    with open(file_name, 'r') as f:
        ndctl  =  json.load(f)

    # if VERBOSE: print('Done')
    # if DEBUG: print("Debug:", __name__, ":",  ndctl)

    toc = time.perf_counter()
    delta_t = toc - tic
    td = {'name': name, "elapsed": delta_t, 'tic': tic, 'toc': toc}
    timers.append(td)

    return ndctl

# - +- +- +- +- +- +- +- +- +- +- +- +- +- +- +- +- +- +- +- +
# Accessor Functions
#
def get_region_dimm_list(region):
    """
        returns list of pmem dimms assocaited with pmem region
    """
    name = 'get_region_dimm_list()'
    tic = time.perf_counter()

    global ndctl
    dimm_list = []

    # if DEBUG: print("DEBUG: Function:", __name__, "Region:", region )
    # if VERBOSE: print('  getting:', __name__, end="...")

    for r in range(len(ndctl['regions'])):
        # if this region matches arg, get DIMM mappings
        if ndctl['regions'][r]['dev'] == region:
            for d in range(len(ndctl['regions'][r]['mappings'])):
               if DEBUG: print('  ndctl[regions][r]mappings', ndctl['regions'][r]['mappings'][d]['dimm'])
               dimm_list.append(ndctl['regions'][r]['mappings'][d]['dimm'])
        continue

    # if VERBOSE: print('Done')
    # if DEBUG: print("Debug:", __name__, region, "DIMMS",  dimm_list)

    toc = time.perf_counter()
    delta_t = toc - tic
    td = {'name': name, "elapsed": delta_t, 'tic': tic, 'toc': toc}
    timers.append(td)

    return dimm_list

def get_region_list():
    """
        Region List
        returns list of all pmem regions
    """
    name = 'get_region_list()'
    tic = time.perf_counter()

    global ndctl
    region_list = []

    # if DEBUG: print("DEBUG: Function:", __name__ )
    # if VERBOSE: print('  getting:', __name__, end="...")

    for r in range(len(ndctl['regions'])):
        region_list.append(ndctl['regions'][r]['dev'])

    # if VERBOSE: print('Done')
    # if DEBUG: print("Debug:", __name__, ":",  region_list)

    toc = time.perf_counter()
    delta_t = toc - tic
    td = {'name': name, "elapsed": delta_t, 'tic': tic, 'toc': toc}
    timers.append(td)

    return region_list


def get_region_ns_device_list(region):
    """
        Region Namespace Device List
        returns list of all pmem namespaces names associated w/ pmem region
    """
    name = 'get_region_ns_device_list()'
    tic = time.perf_counter()

    ns_list = []

    # if DEBUG: print("DEBUG: Function:", __name__, "Region:", region )
    # if VERBOSE: print('  getting:', __name__, end="...")

    for r in range(len(ndctl['regions'])):
        # if this region matches arg, get DIMM mappings
        if ndctl['regions'][r]['dev'] == region:
            for d in range(len(ndctl['regions'][r]['namespaces'])):
               if DEBUG: print('  ndctl[regions][r]mappings', ndctl['regions'][r]['mappings'][d]['dimm'])
               ns_list.append(ndctl['regions'][r]['namespaces'][d]['blockdev'])
        continue

    # if VERBOSE: print('Done')

    toc = time.perf_counter()
    delta_t = toc - tic
    td = {'name': name, "elapsed": delta_t, 'tic': tic, 'toc': toc}
    timers.append(td)

    return ns_list


def get_region_ns_name_list(region):
    """
        Region Namespace List
        returns list of all pmem namespaces names associated w/ pmem region
    """
    name = 'get_region_ns_name_list()'
    tic = time.perf_counter()

    ns_list = []

    # if DEBUG: print("DEBUG: Function:", __name__, "Region:", region )
    # if VERBOSE: print('  getting:', __name__, end="...")

    for r in range(len(ndctl['regions'])):
        # if this region matches arg, get DIMM mappings
        if ndctl['regions'][r]['dev'] == region:
            for d in range(len(ndctl['regions'][r]['namespaces'])):
               if DEBUG: print('  ndctl[regions][r]mappings', ndctl['regions'][r]['mappings'][d]['dimm'])
               ns_list.append(ndctl['regions'][r]['namespaces'][d]['dev'])
        continue

    # if VERBOSE: print('Done')

    toc = time.perf_counter()
    delta_t = toc - tic
    td = {'name': name, "elapsed": delta_t, 'tic': tic, 'toc': toc}
    timers.append(td)

    return ns_list


def get_dimm_status(dimm):
    """
        DIMM List
        returns status of given dimm
    """
    name = 'get_dimm_status()'
    tic = time.perf_counter()


    # dimm_list = []

    # if DEBUG: print("DEBUG: Function:", __name__ )
    # if VERBOSE: print('  getting:', __name__, end="...")

    for d in range(len(ndctl['dimms'])):
        if DEBUG: print(ndctl['dimms'][d]['dev'], ndctl['dimms'][d]['health']['health_state'])

        if ndctl['dimms'][d]['dev'] == dimm:
            status = ndctl['dimms'][d]['health']['health_state']
            break

    # if VERBOSE: print('Done')
    # if DEBUG: print("Debug:", __name__, ":",  dimmList)

    toc = time.perf_counter()
    delta_t = toc - tic
    td = {'name': name, "elapsed": delta_t, 'tic': tic, 'toc': toc}
    timers.append(td)

    return status


def get_dimm_list():
    """
        DIMM List
        returns list of all pmem devices in system
    """
    name = 'get_dimm_list()'
    tic = time.perf_counter()

    dimm_list = []

    # if DEBUG: print("DEBUG: Function:", __name__ )
    # if VERBOSE: print('  getting:', __name__, end="...")

    for d in range(len(ndctl['dimms'])):
        dimm_list.append(ndctl['dimms'][d]['dev'])


    # if VERBOSE: print('Done')
    # if DEBUG: print("Debug:", __name__, ":",  dimmList)

    toc = time.perf_counter()
    delta_t = toc - tic
    td = {'name': name, "elapsed": delta_t, 'tic': tic, 'toc': toc}
    timers.append(td)

    return dimm_list


def get_region_by_dimm(dimm):
    """
        Get Region by DIMM 
        returns region associated with PMEM device
    """
    name = 'get_region_by_dimm()'
    tic = time.perf_counter()

    region = "regionX"

    # if DEBUG: print("DEBUG: Function:", __name__ )
    # if VERBOSE: print('  getting:', __name__, end="...")

    # loop through regions, get dimmList for each, check if match
    for r in range(len(ndctl['regions'])):
        region = ndctl['regions'][r]['dev']
        dimmList = get_region_dimm_list(region)
        # print("get_region_by_dimm.r", r, region, dimmList )
        if dimm in dimmList: break

    # if VERBOSE: print('Done')
    # if DEBUG: print("Debug:", __name__, ":",  region)

    toc = time.perf_counter()
    delta_t = toc - tic
    td = {'name': name, "elapsed": delta_t, 'tic': tic, 'toc': toc}
    timers.append(td)

    return region


def get_ns_name_list_by_dimm(dimm):
    """
        Get PMEM Namespace name by DIMM 
        returns list of pmem namespaces associated with  name
    """
    name = 'get_ns_name_list_by_dimm()'
    tic = time.perf_counter()

    nsNameList = []

    # if DEBUG: print("DEBUG: Function:", __name__ )
    # if VERBOSE: print('  getting:', __name__, end="...")

    # loop through regions, get dimmList for each, check if match
    for r in range(len(ndctl['regions'])):
        region = ndctl['regions'][r]['dev']
        dimmList = get_region_dimm_list(region)

        # we should have a region to lookup namespaces
        nsNameList = get_region_ns_name_list(region)

        if dimm in dimmList: break

    # if VERBOSE: print('Done')
    # if DEBUG: print("Debug:", __name__, ":",  nsNameList)

    toc = time.perf_counter()
    delta_t = toc - tic
    td = {'name': name, "elapsed": delta_t, 'tic': tic, 'toc': toc}
    timers.append(td)

    return nsNameList


def get_ns_device_list_by_dimm(dimm):
    """
        Get Namespace Devices by DIMM 
        returns pmem namespace device for given DIMM
    """
    name = 'get_ns_device_list_by_dimm()'
    tic = time.perf_counter()

    ns_device_list = []
    dimm_list = []

    # if DEBUG: print("DEBUG: Function:", __name__ )
    # if VERBOSE: print('  getting:', __name__, end="...")

    # loop through regions, get dimmList for each, check if match
    for r in range(len(ndctl['regions'])):
        region = ndctl['regions'][r]['dev']
        dimm_list = get_region_dimm_list(region)

        # we should have a region to lookup namespaces
        ns_device_list = get_region_ns_device_list(region)

        if dimm in dimm_list: break

    # if VERBOSE: print('Done')
    # if DEBUG: print("Debug:", __name__, ":",  ns_device_list)

    toc = time.perf_counter()
    delta_t = toc - tic
    td = {'name': name, "elapsed": delta_t, 'tic': tic, 'toc': toc}
    timers.append(td)

    return ns_device_list

def list_dimm_table():
    name = 'list_dimm_table()'
    tic = time.perf_counter()


    print()
    print("Optane Persistent Memory DIMM Status")
    print()
    print("%-7s %-21s %-6s %-6s %-6s %-6s" % ("Linux", "DIMM", "DIMM", "DIMM", "Cntrl", "Remaining") )
    print("%-7s %-21s %-6s %-6s %-6s %-6s" % ("Device", "UID", "Health", "Temp", "Temp", "Life") )
    print("%-7s %-21s %-6s %-6s %-6s %-6s" % ("-------", "--------------------", "------", "------", "------", "----") )

    for x in range(len(ndctl['dimms'])):
        print("%-7s %-21s %6s %-6s %-6s %-6s" % (
                ndctl['dimms'][x]['dev'], \
                ndctl['dimms'][x]['id'], \
                ndctl['dimms'][x]['health']['health_state'], \
                ndctl['dimms'][x]['health']['temperature_celsius'], \
                ndctl['dimms'][x]['health']['controller_temperature_celsius'], \
                ndctl['dimms'][x]['health']['spares_percentage'] \
            ))


def module_test():
    name = 'module_test()'
    tic = time.perf_counter()

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

    toc = time.perf_counter()
    delta_t = toc - tic
    td = {'name': name, "elapsed": delta_t, 'tic': tic, 'toc': toc}
    timers.append(td)

def print_timers(t = timers):
    '''
    ------------ndctl function timers---------------------
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
    print('------------Start ndctl function timers---------------')
    print('%30s %8s %11s %11s' % ('Function', 'Elapsed', 'Start', 'End') )
    print('%30s %8s %11s %11s' % ('------------------------------', '---------', '-----------', '------------') )

    first = t[0]['tic']
    last = t[len(t) -1]['toc']

    for i in t:
        print('%30s %9.4f %11.4f  %11.4f' % (i['name'], i['elapsed'], i['tic'], i['toc']) )
    
    print('%30s %9.4f %11.4f  %11.4f' % ('NDCTL Overall', last - first, first, last) )
    print()
    print('------------End ndctl function timers-----------------')



def main():

    name = 'main()'
    tic = time.perf_counter()

    print("This module is not intended to run standalone")
    print("import this module into your script to use or use")
    print("Persistent Memory Tool, pmt")

    module_test()

    toc = time.perf_counter()
    delta_t = toc - tic
    td = {'name': name, "elapsed": delta_t, 'tic': tic, 'toc': toc}
    timers.append(td)

    print_timers()

if __name__ == "__main__":
    main()

