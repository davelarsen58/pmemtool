#!/usr/bin/python3

# PMTOOL (pmt)
# Copyright (C) David P Larsen
# Released under MIT License


import sys
import os
import argparse

# global VERBOSE
# global DEBUG

import common as c
import ipmctl as i
import fstab as f
import ndctl as n
import recovery as r
from common import message, get_linenumber, pretty_print, check_user_is_root
from common import V0, V1, V2, V3, V4, V5, D0, D1, D2, D3, D4, D5

VERBOSE = V0
DEBUG = D0

import time
timers = []

# Dicts used
ndctl = {}
fstab = {}

dimm_list = []
skip_ndctl_dump = False

def print_timers(t = timers):
    '''
    ------------Start Main function timers---------------
                      Function  Elapsed       Start         End
    ------------------------------ --------- ----------- ------------
            :main() Initialization    0.0035  98104.6441   98104.6476
           :main() Processing Data   11.2822  98104.6476   98115.9297
             main()->recover_all()    1.1836  98104.6476   98115.9297
         __main__:main() Reporting   12.4775  98104.6476   98117.1250
    ------------End Main function timers-----------------
    '''
    print('------------Start Main function timers---------------')
    print('%30s %8s %11s %11s' % ('Function', 'Elapsed', 'Start', 'End') )
    print('%30s %8s %11s %11s' % ('------------------------------', '---------', '-----------', '------------') )
    for i in t:
        print('%30s %9.4f %11.4f  %11.4f' % (i['name'], i['elapsed'], i['tic'], i['toc']) )
    print()
    print('------------End Main function timers-----------------')


def main(argv):
    # process command line arguments

    main_name = 'main()'
    main_tic = time.perf_counter()

    name = 'main()->Initialization'
    init_tic = time.perf_counter()

    global VERBOSE
    global DEBUG

    ndctl_file = n.DEFAULT_NDCTL_FILE
    fstab_file = f.DEFAULT_FSTAB_FILE

    generate_recovery = False
    show_timers = False
    script_path = r.script_path

    delimiter = '; '
    fsSuffix = ''

    ap = argparse.ArgumentParser(description='Persistent Memory Tool')

    ap.add_argument("--delimiter", help="specify delimiter for pmfs mount path. Default: %(const)s")
    ap.add_argument("--suffix", help="string to append to pmfs mount path Default: None")

    ap.add_argument("--recovery", action="store_true", help="Generate Recovery Scripts for each socket.")
    ap.add_argument("--timers", action="store_true", help="Turn on module execution timers to identify slow functions().")

    ap.add_argument("--script_prefix", help="change recover script name prefix. default: recover_socket")
    ap.add_argument("--script_path", help="change recovery script destination path.  default: /tmp")

    ap.add_argument("--verbose", type=int, choices=range(1,16), help="enable increasingly more verbosity. Verbose Values=1-5, Debug Values=10-15")
    ap.add_argument("--sandbox", required=False, help="path to optional sandbox environment. Default:''")

    # ap.add_argument("--ndctl_file", required=False, help=" path to ndctl data file.  Default:''")
    # ap.add_argument("--fstab_file", required=False, help="path to fstab file. Default:''")
    # ap.add_argument("--skip_ndctl_dump", required=False, help="flag to control whether to create a new ndctl data file. default:'False'")

    args = vars(ap.parse_args())

    # if args['ndctl_file']:  ndctl_file = args['ndctl_file']
    # if args['fstab_file']:  fstab_file = args['fstab_file']
    if args['delimiter']:   delimiter = args['delimiter']
    if args['suffix']:      fsSuffix = args['suffix']
    if args['script_path']: r.script_path = args['script_path']
    if args['recovery']: generate_recovery = True
    if args['timers']: show_timers = True

    if args['sandbox']:
        sandbox_path = args['sandbox']
        os.environ['SANDBOX'] = sandbox_path
        ndctl_file = sandbox_path + n.DEFAULT_NDCTL_FILE
        fstab_file = sandbox_path + f.DEFAULT_FSTAB_FILE

    if args['verbose']:
        VERBOSE = args['verbose']

        '''Tie Verbose flags for all modules'''
        c.VERBOSE = args['verbose']
        i.VERBOSE = args['verbose']
        n.VERBOSE = args['verbose']
        f.VERBOSE = args['verbose']
        r.VERBOSE = args['verbose']

    message("checking if current user is privileged", V1)
    if not check_user_is_root():
        message("No - not privileged", V0)
        sys.exit(1)
    else:
        message("Yes", V1)

    if os.path.exists(fstab_file):
        message("processing fstab data", V1)
        fstab = f.parse_fstab(fstab_file)
        message("done", V1)
    else:
        print("Error: missing fstab file:", fstab_file)
        sys.exit(3)

    if not fstab:
        message("\nFound no Persistent Memory Filesystems in fstab\n",V0,'   ')
        message("Checked for fstab block device entries:",V0,'   ')
        message("  starting with: /dev/disk/by-uuid/ with links to /dev/pmemX",V0,'   ')
        message("  starting with: UUID= with links to /dev/pmemX",V0,'   ')
        message("  starting with: /dev/pmem",V0,'   ')
        message("\nPlease verifiy fstab contains PMFS entries\n",V0,'   ')
        sys.exit(4)

    init_toc = time.perf_counter()
    delta_t = init_toc - init_tic
    td = {'name': name, "elapsed": delta_t, 'tic': init_tic, 'toc': init_toc}
    timers.append(td)

    name = 'main()->Processing Data'
    proc_tic = time.perf_counter()

    message("preparing ndctl data dump",V1)
    if not skip_ndctl_dump:
        n.dump(ndctl_file)
        message("done",V1)
    else:
        message("Skipped due to skip_ndctl_dump flag",V1)


    message("parsing ndctl data dump",V1)
    if os.path.exists(ndctl_file):
        ndctl = n.parse(ndctl_file)
        message("Finshed parsing ndcl data",V1)
    else:
        print("Missing NDCTL data file:", ndctl_file)
        sys.exit(2)


    message("ingesting ipmctl data",V1)
    i.sockets = {}
    i.dimms = {}
    i.regions = {}

    message("ingesting ipmctl socket data",V2)
    if i.show_socket():
        i.sockets = i.parse_socket()
    #
    message("ingesting ipmctl dimm data",V2)
    if i.show_dimm():
        i.dimms = i.parse_dimm()
    #
    message("ingesting ipmctl region data",V2)
    if i.show_region():
        i.regions = i.parse_region()

    # get list of all pmem dimms in system
    message("generating list of dimms",V1)
    dimm_list = n.get_dimm_list()
    dimm_list.sort()
    message("done",V1)

    if VERBOSE: print("ndctl and fstab data merge start")
    message("",V1)
    for dimm in dimm_list:
        status  = n.get_dimm_status(dimm)

        # get the list of namespace devices (pmemX) for this DIMM
        msg = "%s %s %s" % ("generating namespace device list for", dimm, '')
        message(msg,V1)
        nsDevList = n.get_ns_device_list_by_dimm(dimm)
        msg = "%s %s %s" % ("ns device list", '', '')
        message(msg,V1)

        # since DIMM status affects region status, which affects namespaces
        # on that region, we can use that status to infer the health of the namespace
        #
        # for each namespace device, update fs status with DIMM status
        msg = "%s %s %s" % ("updating namespace status from dimm status", '', '')
        message(msg,V1)
        for dev in nsDevList:
            msg = "%s %s %s" % ("updating namespace status from dimm status", dev, status)
            message(msg,V1)
            f.set_fs_status(fstab, dev, status)

            # hack, hack, hack
            mount_point = fstab[dev]['mount']
            is_mounted = os.path.ismount(mount_point)
            f.set_fs_mounted_state(fstab, dev, is_mounted)

            # TODO
            # ndctl['regions'][0]['namespaces'][0]['size']
            #
            #
            size = int(1598128390144 / 1024 / 1024 / 1024)
            f.set_ns_size(fstab, dev, size)

        msg = "%s %s %s" % ("done", '', '')
        message(msg,V1)

        msg = "%s %s %s" % ("updating fstab namespace region", dev, '')
        message("",V1)
        region  = n.get_region_by_dimm(dimm)
        f.set_fs_region(fstab, dev, region)
        message("",V1)
        msg = "%s %s %s" % ("", dev, '')

        msg = "%s %s %s" % ("updating namespace dimm list", dev, '')
        message(msg,V1)
        #
        # dList = n.get_region_dimm_list(region)
        # changed to show ipmctl DIMM ID, which is more useful for recovery
        x = region.replace('region','')
        dList = i.get_dimm_list(x) # use ipmctl dimm ID's
        #
        dimms = ' '.join(dList)
        f.set_fs_dimms(fstab, dev, dimms)
        msg = "%s %s %s %s" % ("updated entry ", dev, ' with:', dimms)
        message(msg,V1)

    message("ndctl and fstab data merge complete",V1)
    # ====================================================

    proc_toc = time.perf_counter()
    delta_t = proc_toc - proc_tic
    td = {'name': name, "elapsed": delta_t, 'tic': proc_tic, 'toc': proc_toc}
    timers.append(td)

    name = 'main()->Reporting'
    report_tic = time.perf_counter()

    message("Sending Reports",V1)

    import datetime
    time_stamp = datetime.datetime.now()
    version = 'PMT script version: %s\n'  % ( c.version())

    print('%s %s' % (time_stamp, version) )

    message("------ ipmctl Begin list_dimm_table --------",V3)
    d = i.get_dimms()
    i.list_dimms(d)
    message("------ ipmctl End list_dimm_table --------",V3)

    message("------ fstab Begin print_fstab_table --------",V3)
    f.print_fstab_table(fstab)
    message("------ ipmctl End print_fstab_table --------",V3)


    message("------ fstab Begin f.print_fs_mounts --------",V3)
    suffix = fsSuffix + delimiter
    print("\nPMFS with OK status: ", end='')
    f.print_fs_mounts(fstab,'ok', suffix)
    message("------ ipmctl End f.print_fs_mounts --------",V3)

    if generate_recovery:
        r_tic = time.perf_counter()
        r_name = 'main()->recover_all()'

        r.recover_all()

        r_toc = time.perf_counter()
        delta_t = r_toc - r_tic
        td = {'name': r_name, "elapsed": delta_t, 'tic': r_tic, 'toc': r_toc}
        timers.append(td)

    report_toc = time.perf_counter()
    # toc = time.perf_counter()
    delta_t = report_toc - report_tic
    td = {'name': name, "elapsed": delta_t, 'tic': report_tic, 'toc': report_toc}
    timers.append(td)

    i.clean_up()
    n.clean_up()

    main_toc = time.perf_counter()
    delta_t = main_toc - main_tic
    td = {'name': main_name, "elapsed": delta_t, 'tic': main_tic, 'toc': main_toc}
    timers.append(td)

    if show_timers:
        print('Execution Trace Timers')
        print('----------------------')
        i.print_timers()
        n.print_timers()
        r.print_timers()
        print_timers()


if __name__ == "__main__":
    main(sys.argv[1:])
