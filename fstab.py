#!/usr/bin/python3
#
# PMEMTOOL (PMT) FSTAB Module
# @ Copyright Intel 2021
# Released under NDA to Walgreens for use with Optane Persistent Memory
# All rights reserved
# Provided as Sample Code with no warranty
# December 03, 2021
# Version: 0.7

import os

verbose = 0
debug = 0

# fs uuid path: /dev/disk/by-uuid/367d56f1-c47f-47f0-8350-1e3d543eebfd
#      fs uuid: UUID="367d56f1-c47f-47f0-8350-1e3d543eebfd"

# Input: UUID="eb0caaa8-8191-490d-b955-f3a73ed6fe26"
# Output: /dev/disk/by-uuid/eb0caaa8-8191-490d-b955-f3a73ed6fe26
def fsUUIDToPath(uuid):
    path = "/dev/disk/by-uuid/"

    # strip chars from input
    tmp1 = uuid.replace('"', '')
    tmp2 = tmp1.replace('UUID=', '')
    # append to path

    path = "/dev/disk/by-uuid/" + tmp2

    return path

#  input: blockdev path: /dev/pmem0
#  output: blockdev: pmem0
def blockDevPathToBlockDev(path):
    blockDev = path.replace('/dev/','')
    return blockDev

def fsUUIDPathToBlockDev(path):
    blockDev = "pmemX"

    # if dev is a link, get actual device from link
    if os.path.islink(path):
        target = os.readlink(path)

    #strip the preceeding relative path
    # cheating a bit cuz I know the real path
    blockDev = path.replace('../../','')

    return blockDev

# dict: fstab
# parses fstab for pmem entrys and populates fstab dict
# retrns populated fstab
def parse(fstabFile = '/etc/fstab'):
    fstab = {}
    blockDev = ''

    m  = {} # tmp dict for fstab pmem mount data

    if debug: print("DEBUG: Function:", parseFstab.__name__, "File:", fstabFile )
    if verbose: print('  Parsing fstab:', fstabFile, end="...")

    with open(fstabFile,"r") as f:
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

            if debug: print("DEBUG DEV:", dev)

            # three possible formats for the dev
            # - - - - - - - - - - - - - - - - - - - - -
            #      fs uuid: UUID="367d56f1-c47f-47f0-8350-1e3d543eebfd"
            if dev.startswith("UUID="):
                print('startswith("UUID=")')
                path = fsUUIDToPath(dev)
                blockDev = fsUUIDPathToBlockDev(path)

            # fs uuid path: /dev/disk/by-uuid/367d56f1-c47f-47f0-8350-1e3d543eebfd
            if dev.startswith("/dev/disk/by-uuid"):
                blockDev = fsUUIDPathToBlockDev(dev)

            #  blockdev path: /dev/pmem0
            if dev.startswith("/dev/pmem"):
                blockDev = blockDevPathToBlockDev(dev)


            print('parse: blockDev:', blockDev)

            # populate fstab dict with metadata for the dev listed in fstab
            if blockDev.startswith("pmem"):
                fstab[blockDev] = { \
                        'status': 'unknown', \
                        'mount': mnt, \
                        'fs_guid': dev, \
                        'fs_type': fs_type, \
                        'fs_opts': fs_opts, \
                        'pm_region': 'regionX', \
                        'pm_ns_name': 'namespaceX.Y', \
                        'pm_ns_dev': short_dev, \
                        'pm_ns_type': 'fsdaX', \
                        'dimms': 'dimms' \
                        }

    if verbose: print('Done')
    if debug: print("FSTAB")
    if debug: print(fstab)

    return fstab

def printFstabTable(fstab):

    print("%-6s %-8s %-10s %-8s %-8s %-20s %20s" % ( \
            'Health', \
            'Region', \
            'NS dev', \
            'NS Type', \
            'fs_type', \
            'mount', \
            'dimms') )

    print("%-6s %-8s %-10s %-8s %-8s %-20s %20s" % (\
            '------', 
            '-------', 
            '------', 
            '------', 
            '------', 
            '--------------------', 
            '--------------------' \
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

def printFsMounts(fstab, status='ok', delimiter=';'):
    for k in fstab.keys():
        if fstab[k]['status'] == status:
            print(fstab[k]['mount'], end=delimiter)
    print()

def setFsStatus(fstab, dev, status='ok'):
    #print("setFsStatus: dev:", dev, " status:", status)
    fstab[dev]['status'] = status

def setFsRegion(fstab, dev, region):
    # print("setFsStatus: dev:", dev, " status:", status)
    fstab[dev]['pm_region'] = region

def setFsDimms(fstab, dev, dimms):
    # print("setFsStatus: dev:", dev, " status:", status)
    fstab[dev]['dimms'] = dimms


def module_test():
    import sys
    import os

    global verbose
    global debug

    fstab = {}
    fstabFile = "/etc/fstab"
    # fstabFile = "fstab"

    fstab = parse(fstabFile)

    print(fstab)

    setFsStatus(fstab, dev, status='ok')
    setFsRegion(fstab, dev, region)
    setFsDimms(fstab, dev, dimms)

    # status = 'ok'
    # dev = '/dev/disk/by-uuid/4174d9c4-4d31-46f8-9116-20408e1a4465'  # pmem0
    # setFsStatus(fstab, dev, status)

    # dev = '/dev/disk/by-uuid/823973eb-8f85-40ce-a670-e8481df3de17'  # pmem1
    # setFsStatus(fstab, dev, status)

    printFstabTable(fstab)

    print("PMFS with OK status: ", end='')
    printFsMounts(fstab)

def main():
    print("This module is not intended to run standalone")
    print("import this module into your script to use or use")
    print("Persistent Memory Tool, pmt")


if __name__ == "__main__":
    main()

