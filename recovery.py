#!/usr/bin/python3

import sys
import os
from common import message, get_linenumber
from common import VERBOSE, V0, V1, V2, V3, V4, V5, D0, D1, D2, D3, D4, D5


'''
recovery.py provides functions to recover various kinds of failure conditions
with optional guidance
'''

tmp_dir = '/tmp'

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

def prototype(xml_file):
    '''
    '''
    msg = "%s %s %s %s" % (get_linenumber(), "Beginning:", xml_file, '')
    message(msg, D1)
    msg = "%s %s %s %s" % (get_linenumber(), "End:", xml_file, '')
    message(msg, D1)

    return regions

def recover_dimm(dimm_id, interactive = True):
    '''
    recover_dimm() issues a secure erase to dimm to clear any remaining
    configuration dimm.
    '''
    msg = "%s %s %s %s" % (get_linenumber(), "recover_dimm:Beginning:", dimm_id, interactive)
    message(msg, D1)

    message('show dimm details', D1)
    # message('', D1

    msg = "%s %s %s %s" % (get_linenumber(), "recover_dimm:End:", dimm_id, '')
    message(msg, D1)

def recover_socket(socket_id, interactive = True):
    '''
    recover_socket() calls recover_dimm() for each dimm associated with socket.
    a new goal is created after clearing config 
    '''
    msg = "%s %s %s %s" % (get_linenumber(), "Beginning:", xml_file, '')
    message(msg, D1)

    msg = "%s %s %s %s" % (get_linenumber(), "End:", xml_file, '')
    message(msg, D1)

def recover_i_set(iset_id, interactive = True):
    '''
    '''
    msg = "%s %s %s %s" % (get_linenumber(), "Beginning:", xml_file, '')
    message(msg, D1)
    msg = "%s %s %s %s" % (get_linenumber(), "End:", xml_file, '')
    message(msg, D1)

def recover_namespace(namespace, interactive = True):
    '''
    '''
    msg = "%s %s %s %s" % (get_linenumber(), "Beginning:", xml_file, '')
    message(msg, D1)
    msg = "%s %s %s %s" % (get_linenumber(), "End:", xml_file, '')
    message(msg, D1)

def recover_fs(mount_point, interactive = True):
    '''
    '''
    msg = "%s %s %s %s" % (get_linenumber(), "Beginning:", xml_file, '')
    message(msg, D1)
    msg = "%s %s %s %s" % (get_linenumber(), "End:", xml_file, '')
    message(msg, D1)

def main():

    # from common import VERBOSE
    import argparse

    from common import pretty_print

    # from ipmctl import show_dimm, parse_dimms, show_regions, parse_regions
    import ipmctl as i

    global VERBOSE

    interactive = False
    recover = False
    dimm_id = ''
    region_id = ''
    socket_id = ''
    mount_point = ''

    ap = argparse.ArgumentParser()
    ap.add_argument("--interactive", required=False, help="")
    ap.add_argument("--recover",     required=False, help="")
    ap.add_argument("--dimm",        required=False, help="")
    ap.add_argument("--region",      required=False, help="")
    ap.add_argument("--socket",      required=False, help="")
    ap.add_argument("--mount_point", required=False, help="")
    ap.add_argument("--verbose",     required=False, help="")

    ap.add_argument("--dimm_xml_file",   required=False, help="NVMXML input file from ipmctl show -o nvmxml show -a -dimm")
    ap.add_argument("--region_xml_file", required=False, help="NVMXML input file from ipmctl show -o nvmxml show -a -region")

    args = vars(ap.parse_args())

    if args['dimm_xml_file']:    dimm_xml_file = args['dimm_xml_file']
    if args['region_xml_file']:  region_xml_file = args['region_xml_file']

    if args['interactive']: interactive = True
    if args['recover']:     recover = True
    if args['dimm']:        dimm_id = args['dimm']
    if args['region']:      region_id = args['region']
    if args['socket']:      socket_id = args['socket']
    if args['mount_point']: mount_point = args['mount_point']

    if args['verbose']:     VERBOSE = args['verbose']


    msg = "%s %s %s %s" % (get_linenumber(), "Main:Begin:", '', '')
    message(msg, D0)

    if i.show_dimm():
        dimms = i.parse_dimms()
        if VERBOSE:
            message('pretty_print dimms',D0)
            for d in sorted(dimms.keys()):
                print(d)
            # pretty_print(dimms)
            print()

    if i.show_region():
        regions = i.parse_regions()
        if VERBOSE:
            message('pretty_print regions',D0)
            for r in sorted(regions.keys()):
                print(r)
            # pretty_print(regions)

    if recover:
        msg = "%s %s %s %s" % (get_linenumber(), "Main:Recovery:", 'Starting', '')
        message(msg, D0)
        if mount_point: recover_fs(mount_point, interactive)
        if dimm_id:     recover_dimm(dimm_id, interactive)
        if region_id:   recover_region(region_id, interactive)
        if socket_id:   recover_socket(socket_id, interactive)



if __name__ == '__main__':
    main()

