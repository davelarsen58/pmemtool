#!/usr/bin/python3
#
# PMEMTOOL (PMT) FSTAB Module
# @ Copyright Intel 2021
# Released under NDA to Walgreens for use with Optane Persistent Memory
# All rights reserved
# Provided as Sample Code with no warranty
# December 06, 2021
# Version: 0.71

import os

verbose = 0
debug = 0

# dict: fstab
# parses fstab for pmem entrys and populates fstab dict
# retrns populated fstab
def parse(fstabFile = '/etc/fstab'):
    fstab = {}

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

            # if dev is a link, get actual device from link
            if os.path.islink(dev):
                target = os.readlink(dev)

                #strip the preceeding relative path
                # cheating a bit cuz I know the real path
                short_dev = target.replace('../../','')

            # populate fstab dict with metadata for the dev listed in fstab
            if short_dev.startswith("pmem"):
                fstab[short_dev] = { \
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
    # print("setFsStatus: dev:", dev, " status:", status)
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

    fstab = parseFstab(fstabFile)

    status = 'ok'
    dev = '/dev/disk/by-uuid/4174d9c4-4d31-46f8-9116-20408e1a4465'  # pmem0
    setFsStatus(fstab, dev, status)

    dev = '/dev/disk/by-uuid/823973eb-8f85-40ce-a670-e8481df3de17'  # pmem1
    setFsStatus(fstab, dev, status)

    print("PMFS with OK status: ", end='')
    printFsMounts(fstab)

def main():
    print("This module is not intended to run standalone")
    print("import this module into your script to use or use")
    print("Persistent Memory Tool, pmt")


if __name__ == "__main__":
    main()

