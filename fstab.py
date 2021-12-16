#!/usr/bin/python3
#
# PMEMTOOL (PMT) FSTAB Module
# Copyright (C) David P Larsen
# Released under MIT License

import os
import sys

VERBOSE = 0
DEBUG = 0

DEFAULT_FSTAB_FILE = "/etc/fstab"
DEFAULT_DEVDIR = "/dev"
DEFAULT_DEV_UUID_DIR = DEFAULT_DEVDIR + "/disk/by-uuid/"

# If working in a test sandbox, change paths
# to start with path to sandbox
#
if not os.getenv('SANDBOX'):
    SANDBOX = ''
else:
    SANDBOX = os.environ['SANDBOX']
    print('Enabling Sandbox at:', SANDBOX)

FSTAB = SANDBOX + DEFAULT_FSTAB_FILE
DEVDIR = SANDBOX + DEFAULT_DEVDIR
DEV_UUID = DEVDIR + DEFAULT_DEV_UUID_DIR

if VERBOSE: print("FSTAB", FSTAB)
if VERBOSE: print("DEVDIR", DEVDIR)
if VERBOSE: print("DEV_UUID", DEV_UUID)

def unit_test_result(name, status):
    print("%-30s %-10s" % (name, status))

def fs_uuid_to_path(uuid):
    """
        Converts fstab UUID= entry to absolute path
         Input: UUID='eb0caaa8-8191-490d-b955-f3a73ed6fe26'
        Output: /dev/disk/by-uuid/eb0caaa8-8191-490d-b955-f3a73ed6fe26
    """
    # path = SANDBOX
    path = "/homes/dplarsen/src/pmemtool/sandbox/dev/disk/by-uuid"
    if DEBUG: print("    DEBUG: fs_uuid_to_path", uuid, path)

    # strip 'UUID="..."'chars from input
    tmp1 = uuid.replace('"', '')     # replace teh quotes
    tmp2 = tmp1.replace('UUID=', '') # remove UUID=

    # append UUID to path
    path = path + "/" + tmp2

    return path

def test_fs_uuid_to_path():
    """
        unit test for function
        depends on setting sandbox test env using mksandbox script
    """
    path = ''
    status = 'new'
    uuid = 'UUID="5038fb23-6374-4d03-81b9-93d6c984eb0x0"'
    real_path = DEV_UUID + '5038fb23-6374-4d03-81b9-93d6c984eb0x0'
    path = fs_uuid_to_path(uuid)

    if path == real_path:
        status = 'Pass'
    else:
        status = 'Fail'
    unit_test_result('fs_uuid_to_path()', status)

    return status

def block_dev_path_to_block_dev(path):
    """
        converts block device path (/dev/pmemX)
        to the device name (pmemX)
    """
    block_dev = os.path.basename(path)
    return block_dev

def test_block_dev_path_to_block_dev():
    """
        leverages sandbox static configuration and values
        unit test for block_dev_path_to_block_dev()
    """
    dev = 'pmem0'
    status = 'new'
    real_path = DEVDIR + '/pmem0'

    block_dev = block_dev_path_to_block_dev(real_path)

    if dev == block_dev:
        status = 'Pass'
    else:
        status = 'Fail'
        print('Details:', dev, block_dev)
    unit_test_result('block_dev_path_to_block_dev()', status)

    return status


def fs_uuid_path_to_block_dev(path):
    """get the link to actual device from FS uuid
        path: /dev/disk/by-uuid/UUID
        return: pmemX
    """
    block_dev = "pmemX"
    target = ''

    # if dev is a link, get actual device from link
    if os.path.islink(path):
        target = os.readlink(path)

    if DEBUG: print("fs_uuid_path_to_block_dev:", path, target)
    #strip the preceeding relative path
    # cheating a bit cuz I know the real path
    # block_dev = path.replace('../../','')
    block_dev = os.path.basename(target)

    return block_dev

def test_fs_uuid_path_to_block_dev():
    """
        leverages sandbox static configuration and values
    """
    dev = "pmem0"
    real_path = DEV_UUID + '5038fb23-6374-4d03-81b9-93d6c984eb0x0'

    if os.path.islink(real_path):
        target = os.readlink(real_path)

    block_dev = os.path.basename(target)

    if dev == block_dev:
        status = 'Pass'
    else:
        status = 'Fail'
        print('Details:', dev, block_dev)
    unit_test_result('fs_uuid_path_to_block_dev()', status)

    return status


def parse_fstab(file_name=FSTAB):
    """
        parses fstab into a dict, and returned to the caller
    """
    fstab = {}
    block_dev = ''

    # DEBUG = 1

    if DEBUG: print("DEBUG: Function:", __name__, "File:", file_name)
    if VERBOSE: print('  Parsing fstab:', file_name, end="...")

    with open(file_name, "r") as f:
        for line in f:
            stripped_line = line.strip()

            # skip empty and commented lines
            if stripped_line.startswith("#"): continue
            if len(stripped_line) == 0: continue

            # parse line into fields
            line = stripped_line.split()

            # extract dev and mnt point fields
            dev = ' '.join(line[0:1])
            mnt = ' '.join(line[1:2])
            fs_type = ' '.join(line[2:3])
            fs_opts = ' '.join(line[3:4])

            # if DEBUG: print("DEBUG DEV:", dev)

            if not dev.startswith("UUID=") and not dev.startswith("/dev/disk/by-uuid") and not dev.startswith("/dev/pmem"):
                if DEBUG: print("   skipping", dev)
                continue
            # three possible formats for the dev
            # - - - - - - - - - - - - - - - - - - - - -
            #      fs uuid: UUID="367d56f1-c47f-47f0-8350-1e3d543eebfd"
            if dev.startswith("UUID="):
                if DEBUG: print('startswith("UUID=")')
                uuid_path = fs_uuid_to_path(dev)
                if DEBUG: print("    DEBUG: uuid_path", uuid_path)
                block_dev = fs_uuid_path_to_block_dev(uuid_path)
                if DEBUG: print("    DEBUG: block_dev:", block_dev)

            # fs uuid path: /dev/disk/by-uuid/367d56f1-c47f-47f0-8350-1e3d543eebfd
            if dev.startswith("/dev/disk/by-uuid"):
                if DEBUG: print('startswith("/dev/disk/by-uuid")')
                dev_path = SANDBOX + dev
                block_dev = fs_uuid_path_to_block_dev(dev_path)

            #  blockdev path: /dev/pmem0
            if dev.startswith("/dev/pmem"):
                if DEBUG: print('startswith("/dev/pmem)')
                block_dev = block_dev_path_to_block_dev(dev)

            if DEBUG: print('  block_dev:', block_dev, end=",")
            if DEBUG: print('  dev:', dev)

            # populate fstab dict with metadata for the dev listed in fstab
            if block_dev.startswith("pmem"):
                fstab[block_dev] = { \
                        'status': 'ok', \
                        'mount': mnt, \
                        'fs_guid': dev, \
                        'fs_type': fs_type, \
                        'fs_opts': fs_opts, \
                        'pm_region': 'regionX', \
                        'pm_ns_name': 'namespaceX.Y', \
                        'pm_ns_dev': block_dev, \
                        'pm_ns_type': 'fsdaX', \
                        'dimms': 'dimms' \
                      }

    if VERBOSE: print('Done')
    if DEBUG: print("FSTAB")
    if DEBUG: print(fstab)

    return fstab

def print_fstab_table(fstab):

    print("%-6s %-8s %-10s %-8s %-8s %-20s %20s" % ( \
            'Health', \
            'Region', \
            'NS dev', \
            'NS Type', \
            'fs_type', \
            'mount', \
            'dimms'))

    print("%-6s %-8s %-10s %-8s %-8s %-20s %20s" % (\
            '------',
            '-------',
            '------',
            '------',
            '------',
            '--------------------',
            '--------------------'\
            ))
    for k in fstab.keys():
        print("%-6s %-8s %-10s %-8s %-8s %-20s %-20s" % ( \
               fstab[k]['status'], \
               fstab[k]['pm_region'], \
               fstab[k]['pm_ns_dev'], \
               fstab[k]['pm_ns_type'], \
               fstab[k]['fs_type'], \
               fstab[k]['mount'], \
               fstab[k]['dimms'] \
               ))

def print_fs_mounts(fstab, status='ok', delimiter=';'):
    """
    """
    for k in fstab.keys():
        if fstab[k]['status'] == status:
            print(fstab[k]['mount'], end=delimiter)
    print()

def set_fs_status(fstab, dev, status='ok'):
    if DEBUG: print("set_fs_status: dev:", dev, " status:", status)
    fstab[dev]['status'] = status

def test_set_fs_status():
    status = 'Skipped'

    unit_test_result('test_set_fs_status()', status)
    return status

def set_fs_region(fstab, dev, region):
    # print("set_fs_status: dev:", dev, " status:", status)
    fstab[dev]['pm_region'] = region

def test_set_fs_region():
    status = 'Skipped'

    unit_test_result('test_set_fs_region()', status)
    return status

def set_fs_dimms(fstab, dev, dimms):
    # print("set_fs_status: dev:", dev, " status:", status)
    fstab[dev]['dimms'] = dimms

def test_set_fs_dimms():
    status = 'Skipped'

    unit_test_result('test_set_fs_dimms()', status)
    return status


def unitTests():
    # Module Unit Tests
    # # Unit Test counters
    utCounters = {'Attempted': 0, 'Pass': 0, 'Fail': 0, 'Skipped': 0}

    print("Unit Tests")
    print("%-30s %-10s" % ('Function Name', 'status'))
    print("%-30s %-10s" % ('------------------------------', '----------'))

    utCounters['Attempted'] += 1
    test_status = test_fs_uuid_to_path()
    utCounters[test_status] += 1

    utCounters['Attempted'] += 1
    test_status = test_block_dev_path_to_block_dev()
    utCounters[test_status] += 1

    utCounters['Attempted'] += 1
    test_status = test_fs_uuid_path_to_block_dev()
    utCounters[test_status] += 1

    utCounters['Attempted'] += 1
    test_status = test_set_fs_status()
    utCounters[test_status] += 1

    utCounters['Attempted'] += 1
    test_status = test_set_fs_region()
    utCounters[test_status] += 1

    utCounters['Attempted'] += 1
    test_status = test_set_fs_dimms()
    utCounters[test_status] += 1

    passed = utCounters['Pass']
    failed = utCounters['Fail']
    skipped = utCounters['Skipped']
    attempted = utCounters['Attempted']

    print("\nSummary\n")
    print("%-9s %-4s %-4s %-4s" % ('Attempted', 'Pass', 'Fail', 'Skip'))
    print("%-9s %-4s %-4s %-4s" % ('---------', '----', '----', '----'))
    print("%9s %4s %4s %4s" % (attempted, passed, failed, skipped))

    fstab = {}
    file_name = FSTAB
    fstab = parse_fstab(file_name)

    print_fstab_table(fstab)

    print("PMFS with OK status: ", end='')
    print_fs_mounts(fstab)



def main():
    unitTests()


if __name__ == "__main__":
    main()

