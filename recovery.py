#!/usr/bin/python3

import sys
import os
from common import message, get_linenumber, version
from common import V0, V1, V2, V3, V4, V5, D0, D1, D2, D3, D4, D5
import common as c

import time
timers = []


'''
recovery.py provides functions to recover various kinds of failure conditions
with optional guidance
'''

script_path = '/tmp'
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


# ---------------------------------------------------------------------
def recover_socket(data):
    '''
    the data dict contains everything needed to generate recover script
    for this socket as shown below with example data.
        data['socket_id']   =  '0x0001'
        data['socket_num']  =  '0'
        data['dimms']       =  ['0x0001', '0x0011', '0x0021', '0x0101', '0x0111', '0x0121']
        data['nmem']        =  ['nmem0', 'nmem1', 'nmem2', 'nmem3', 'nmem4', 'nmem5']
        data['region']     =  'region0'
        data['ns_name']     =  'namespace0.0'
        data['ns_dev']      =  'pmem0'
        data['mount_point'] =  '/pmem0'
        data['fs_type']     =  'xfs'
        data['file_name']   =  '/tmp/recover_socket_0.sh'

    '''
    name = __name__ + ':recover_socket()'
    tic = time.perf_counter()

    msg = "%s %s %s %s" % (get_linenumber(), "Beginning recover():", '', '')
    message(msg, D1)

    import datetime  # used to get timestamp.now()
    import socket    # used to get hostname
    
    tmp = ' '.join(data['dimms'])
    dimms = tmp.replace(' ', '')
    nmem = data['nmem']
    #
    region_name = data['region']
    namespace_name = data['ns_name']
    namespace_dev = data['ns_dev']
    fs_type = data['fs_type']
    capacity = data['Capacity']
    mount_point = data['mount_point']
    #
    socket_id = data['socket_id']
    socket_num = data['socket_num']
    #
    file_name = data['file_name']
    #
    pmem_device_path = '/dev/' + namespace_dev
    #
    time_stamp = datetime.datetime.now()
    host_name = socket.gethostname()
    #
    msg = "%s %s %s %s %s" % (get_linenumber(), "recover(): Socket:", socket_id, ' DIMMs: ',dimms)
    message(msg, D2)
    #
    old_uuid = 'UUID="xxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx"'
    fstab_opts = 'defaults,dax'
    fstab_type = 'xfs'
    fstab_check = '0    0'
    #
    fstab_entry = old_uuid + ' ' + mount_point + ' ' + fstab_type + ' ' + fstab_opts + ' ' + fstab_check
    #

    '''container to hold the script'''
    script_txt = []

    message('Opening File Name: ' + file_name, D2)
    f = open(file_name, "w")

    msg = "%s %s %s" % (get_linenumber(), "recover(): creating script:", file_name)
    message(msg, D2)

    '''Build Script line-by-line'''
    script_txt.append('#!/bin/bash\n')
    script_txt.append('#\n')
    script_txt.append('# Script created: %s\n' % ( time_stamp))
    script_txt.append('# Created on system: %s\n' % ( host_name))
    script_txt.append('# PMT script version: %s\n'  % ( version()))
    script_txt.append('# Recoverying:\n')
    script_txt.append('#   Socket: %s\n'  % (socket_id))
    script_txt.append('#   Region: %s\n'  % (region_name))
    script_txt.append('#   Dimms: %s\n'   % (dimms))
    script_txt.append('\n')

    script_txt.append('\n')
    script_txt.append('# Variables & Values\n')
    script_txt.append('%s="%s"\n' % ('HOST', host_name ))
    script_txt.append('%s="%s"\n' % ('SKT_ID', socket_id ))
    script_txt.append('%s="%s"\n' % ('SKT_NUM', socket_num ))
    script_txt.append('%s="%s"\n' % ('DIMMS', dimms ))
    script_txt.append('%s="%s"\n' % ('REGION', region_name ))
    script_txt.append('%s="%s"\n' % ('NS_NAME', namespace_name ))
    script_txt.append('%s="%s"\n' % ('NS_DEV', namespace_dev ))
    script_txt.append('%s="%s"\n' % ('NS_DEV_PATH', pmem_device_path ))
    script_txt.append('%s="%s"\n' % ('FS_TYPE', fs_type ))
    script_txt.append('%s="%s"\n' % ('MT_PT', mount_point ))
    script_txt.append('%s="%s"\n' % ('FSTAB_OPTS', fstab_opts ))
    script_txt.append('%s="%s"\n' % ('FSTAB_TYPE', fstab_type ))
    script_txt.append('%s="%s"\n' % ('FSTAB_CHK', fstab_check ))

    # script_txt.append('%s="%s"\n' % ('TIME', time_stamp ))
    # script_txt.append('%s="%s"\n' % ('FSTAB_ENTRY', fstab_entry ))
    # script_txt.append('%s="%s"\n' % ('CAPACITY', capacity ))
    # script_txt.append('%s="%s"\n' % ('FNAME', file_name ))
    # script_txt.append('%s="%s"\n' % ('OLD_UUID', old_uuid ))

    script_txt.append('\n')

    # script_txt.append('# NOTE: Recovering from a failed DIMM, these commands\n')
    # script_txt.append('#       may fail due to filesystem not being mounted,\n')
    # script_txt.append('#       namespaces being re-enumerated due to nmem changes,\n')
    # script_txt.append('#       and regions being hidden due to failed interleave-set\n')
    # script_txt.append('#       nmem devices, namespace devices, and regions are all\n')
    # script_txt.append('#       dynamically enumerated at boot time based upon hardware\n')
    # script_txt.append('#       availability\n')
    # script_txt.append('\n')

    script_txt.append('# Cleanup Phase\n')
    script_txt.append('PHASE1="/var/tmp/socket_%s-phase-1"\n' % (socket_id))

    script_txt.append('# Recover Phase\n')
    script_txt.append('PHASE2="/var/tmp/socket_%s-phase-2"\n' % (socket_id))

    script_txt.append('# Safety Interlock to prevent undoing what we just did\n')
    script_txt.append('DONE="/var/tmp/socket_%s-DONE"\n' % (socket_id))
    script_txt.append('\n')

    script_txt.append('# if the DONE flag exists, complain & exit\n')
    script_txt.append('if [ -f "$DONE" ] ; then\n')
    script_txt.append('\techo "Found Overwrite Protection Flag, $DONE"\n')
    script_txt.append('\techo "Remove that file to rerun this script"\n')
    script_txt.append('\texit 1\n')
    script_txt.append('fi\n')

    script_txt.append('# if the flags dont exist, create them\n')
    script_txt.append('# We can be PHASE1 or PHASE2, but not both\n')
    script_txt.append('if [ ! -f $PHASE2 ] && [ ! -f "$PHASE1" ] ; then\n')
    script_txt.append('\ttouch $PHASE1\n')
    script_txt.append('fi\n')

    script_txt.append('# Check for phase 1 flag, clean up the old stuff\n')
    script_txt.append('if [ -f $PHASE1 ] ; then\n')

    script_txt.append('\n')
    script_txt.append('\n')

    script_txt.append('\t# --- Clean Up Old Provisioning ---\n')
    script_txt.append('\t# Remove demand against PMEM, so we can reconfigure\n')
    script_txt.append('\n')
    script_txt.append('\techo " --- Pre Boot Clean Up ---"\n')
    script_txt.append('\tlogger Beginning Recovery of PMEM on socket %s\n' % (socket_id))
    script_txt.append('\n')
    script_txt.append('\tif [ ! `mountpoint -q %s` ]; then\n' % (mount_point))
    script_txt.append('\t\t echo "Unmounting %s"\n' % (mount_point))
    script_txt.append('\t\t logger unmounting %s\n' % (mount_point))
    script_txt.append('\t\t umount %s\n' % (mount_point))
    script_txt.append('\telse\n')
    script_txt.append('\t\techo "%s is not mounted"\n' % (mount_point))
    script_txt.append('\n')
    script_txt.append('\tfi\n')
    script_txt.append('\n')
    script_txt.append('\t# Note: These two commands will fail if re-enumeration has happened\n')
    script_txt.append('\tndctl disable-namespace %s > /dev/null 2>&1\n' % (namespace_name))
    script_txt.append('\tndctl disable-region %s > /dev/null 2>&1\n' % (region_name))
    script_txt.append('\n')

    script_txt.append('\t# --- Erasing PMEM Devices used by this region ---\n')
    script_txt.append('\t# Note: On completion, ipmctl will respond that all DIMMs have been cleared.\n')
    script_txt.append('\t#       There is no cause for concern\n')
    script_txt.append('\tlogger deleting PMEM configuration for socket %s for dimms %s\n' % (socket_id, dimms))
    script_txt.append('\techo "deleting PMEM configuration for socket %s for dimms %s"\n' % (socket_id, dimms))
    script_txt.append('\tipmctl delete -f -dimm -pcd %s\n' % (dimms))
    script_txt.append('\n')

    script_txt.append('\t# Create new PMEM Region for this socket\n')
    script_txt.append('\tlogger creating new PMEM configuration for socket %s\n' % (socket_id))
    script_txt.append('\techo "creating new PMEM configuration for socket %s"\n' % (socket_id))
    script_txt.append('\tipmctl create -goal -socket %s\n' % (socket_id))
    script_txt.append('\n')

    script_txt.append('\t# Reboot at this point to create the pmem region\n')
    script_txt.append('\t# unless there are more regions to be created now\n')
    script_txt.append('\n')

    # script_txt.append('\tREBOOT_NOW=0\n')
    # script_txt.append('\n')
    # script_txt.append('\twhile [ true ] ; do\n')
    # script_txt.append('\t\t read -p "Do you wish to reboot now?" yn\n')
    # script_txt.append('\t\t case $yn in\n')
    # script_txt.append('\t\t\t [Yy]* ) echo "Rebooting Now"; REBOOT_NOW=1; break;;\n')
    # script_txt.append('\t\t\t [Nn]* ) echo "Reboot Later";  break;;\n')
    # script_txt.append('\t\t\t * ) echo "Please answer yes or no.";;\n')
    # script_txt.append('\t\t esac\n')
    # script_txt.append('\tdone\n')
    # script_txt.append('\n')

    script_txt.append('\t# Clear the Phase 1 flag, now that we are done w/ Phase 1\n')
    script_txt.append('\t/usr/bin/rm -f $PHASE1\n')
    script_txt.append('\n')
    script_txt.append('\t# Set the Phase 2 flag, now that we are done w/ Phase 1\n')
    script_txt.append('\ttouch $PHASE2\n')

    # script_txt.append('\tif [ "$REBOOT_NOW" -eq 1] ; then\n')
    # script_txt.append('\t\tshutdown -r now\n')
    # script_txt.append('\tfi\n')

    script_txt.append('\techo "Cleanup Complete. Run this script again after rebooting to resume recovery"\n')
    script_txt.append('\techo "Exiting"\n')
    script_txt.append('\texit 0\n')
    script_txt.append('\n')

    script_txt.append('else\n')
    script_txt.append('\techo "Skipping to PHASE 2"\n')
    script_txt.append('fi #END PHASE1\n')

    script_txt.append('\n')
    script_txt.append('\n')

    script_txt.append('if [ -f $PHASE2 ] ; then\n')
    script_txt.append('\n')
    script_txt.append('\techo "Beginning Phase 2"\n')

    script_txt.append('\techo " --- Post Boot provisioning ---"\n')
    script_txt.append('\n')
    script_txt.append('\t# namespace will contain 0 if there are no namespaces in this region.\n')
    script_txt.append('\tnamespaces=`ndctl list -N -r %s | wc -l`\n' % (region_name))
    script_txt.append('\tif [ "$namespaces" -ne 0 ] ; then\n')
    script_txt.append('\t\t echo "Namespace Exists on region: %s"\n' % (region_name))
    script_txt.append('\t\t echo "You Cannot Create a new namespace if there is no room on %s"\n' % (region_name))
    script_txt.append('\t\t exit 1\n')
    script_txt.append('\tfi\n')

    script_txt.append('\n')
    script_txt.append('\techo "Creating namespace on region: %s"\n' % (region_name))
    script_txt.append('\tndctl create-namespace --mode fsdax --region %s\n' % (region_name))

    #TODO: integrate dymamic fs_type into command below
    script_txt.append('\n')
    script_txt.append('\t# --- Create PMFS on pmem device ---\n')
    script_txt.append('\techo "Creating filesystem on %s:%s->%s"\n' % (region_name, namespace_name, pmem_device_path))
    script_txt.append('\tmkfs -t xfs -m reflink=0 -f %s\n' % (pmem_device_path))

    script_txt.append('\n')
    script_txt.append('\t# --- Create PMFS Mount Point ---\n')
    script_txt.append('\techo "Checking mount point"\n')
    script_txt.append('\tif [ ! -d %s ] ; then\n' % (mount_point))
    script_txt.append('\t\t echo "creating %s"\n' % (mount_point))
    script_txt.append('\t\t mkdir %s\n' % (mount_point))
    script_txt.append('\telse \n')
    script_txt.append('\t\t echo "Mount point exists!"\n')
    script_txt.append('\tfi \n')

    script_txt.append('\techo "--- Create updated fstab entry for %s---" \n' % (mount_point))
    script_txt.append('\n')
    script_txt.append('\techo "--- Get the PMFS UUID ---"\n')
    script_txt.append('\tnew_uuid=`blkid %s | cut -d" " -f2`\n' % (pmem_device_path))
    script_txt.append('\techo "$new_uuid"\n')
    script_txt.append('\n')
    script_txt.append('\techo "--- extracting fstab entry for mount point %s ---"\n'% (mount_point))
    script_txt.append('\trest=`grep %s /etc/fstab | cut -f2-`\n' % (mount_point))
    script_txt.append('\techo "--- merging new uuid $new_uuid with original $rest ---"\n')
    script_txt.append('\n')
    script_txt.append('\tnew_entry=`echo $new_uuid $rest`\n')
    script_txt.append('\n')
    script_txt.append('\techo "Writing new fstab entry to /tmp/fstab_socket_%s"\n' % (socket_id))
    script_txt.append('\techo "$new_entry" > /tmp/fstab_socket_%s\n' % (socket_id))
    script_txt.append('\n')
    script_txt.append('\techo "cat /tmp/fstab_socket_* to see all of the new fstab entries"\n')

    script_txt.append('\t/usr/bin/rm $PHASE2\n')
    script_txt.append('\n')
    script_txt.append('\techo "Recovery Complete. Be sure to update /etc/fstab with contents from:"\n')
    script_txt.append('\techo "/tmp/fstab_socket_*"\n')
    script_txt.append('\ttouch $DONE\n')
    script_txt.append('\n')
    script_txt.append('fi # end PHASE2\n')

    script_txt.append('\n')
    script_txt.append('# --- End of Script ---\n')

    f.writelines(script_txt)
    f.close()

    msg = "%s %s %s" % (get_linenumber(), "recover(): closed file:", file_name)
    message(msg, D2)

    msg = "%s %s %s %s" % (get_linenumber(), "End:recover_socket()", '', '')
    message(msg, D1)

    toc = time.perf_counter()
    delta_t = toc - tic
    td = {'name': name, "elapsed": delta_t, 'tic': tic, 'toc': toc}
    timers.append(td)

    return file_name


# ---------------------------------------------------------------------
def recover_all():
    name = __name__ + ':recover_all()'
    tic = time.perf_counter()

    status = True
    message("------ Recovery Script Begin --------",V3)

    import ipmctl as i
    import fstab as f
    import ndctl as n

    '''SocketID are ['0x0000', '0x0001']'''
    sockets = i.get_socket_list()

    script_list = []

    for socket_id in sockets:
        socket_num = int(socket_id,0)

        data = {}

        data['socket_num'] = socket_num
        data['socket_id'] = socket_id
        # print("data['socket_id']", data['socket_id'])

        data['file_name'] =  '/tmp/recover_socket_' + str(socket_num) + '.sh'
        # print("data['file_name']", data['file_name'])

        data['region'] = ''.join(n.get_region_dev_list(socket_num))
        # print("data['region']", data['region'])

        # data['nmem'] =  ['nmem0' 'nmem1' 'nmem2' 'nmem3' 'nmem4' 'nmem5']
        nmem_list =  n.get_nmem_dev_list(socket_num)
        data['nmem'] = ' '.join(nmem_list)
        # print("data['nmem']", data['nmem'])

        # data['dimms']       =  ['0x0001', '0x0011', '0x0021', '0x0101', '0x0111', '0x0121']
        data['dimms']  = ','.join(i.get_dimm_list(socket_num))
        # print("data['dimms']", data['dimms'])

        data['ns_name']     =  ''.join(n.get_ns_dev(socket_num))
        # print("data['ns_name']", data['ns_name'])

        data['ns_dev']      =  ''.join(n.get_ns_block_dev(socket_num))
        # print("data['ns_dev']", data['ns_dev'])

        data['file_name']   =  script_path + '/recover_socket_' + str(data['socket_num']) + '.sh'
        # print("data['file_name']", data['file_name'])

        # lookup mount point using pmem device, ie: pmem0
        data['mount_point'] =  f.get_fstab_mount_pt(data['ns_dev'])
        # print("data['mount_point']", data['mount_point'])

        data['fs_type'] = f.get_fstab_fs_type(data['ns_dev'])
        # print("data['fs_type']", data['fs_type'])

        data['Capacity'] = 0
        # print("data['Capacity']", data['Capacity'])

        script_file = recover_socket(data)
        # print("recover_all() script->", script_file)
        script_list.append(script_file)

    for script in script_list:
        print('Generated Recover Script: ', script)

    toc = time.perf_counter()
    delta_t = toc - tic
    td = {'name': name, "elapsed": delta_t, 'tic': tic, 'toc': toc}
    timers.append(td)

    return status

def print_timers(t = timers):
    '''
    ------------Recovery function timers---------------------
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

    print('------------Start Recovery function timers---------------')
    print('%30s %8s %11s %11s' % ('Function', 'Elapsed', 'Start', 'End') )
    print('%30s %8s %11s %11s' % ('------------------------------', '---------', '-----------', '------------') )

    first = t[0]['tic']
    last = t[len(t) -1]['toc']

    for i in t:
        print('%30s %9.4f %11.4f  %11.4f' % (i['name'], i['elapsed'], i['tic'], i['toc']) )


    print('%30s %9.4f %11.4f  %11.4f' % ('Recovery Overall', last - first, first, last) )

    print()
    print('------------End Recovery function timers-----------------')



def main():

    name = __name__ + ':main()'
    tic = time.perf_counter()

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
    ap.add_argument("--verbose",     required=False, help="")

    args = vars(ap.parse_args())

    if args['verbose']:     VERBOSE = args['verbose']

    msg = "%s %s %s %s" % (get_linenumber(), "Main:Begin:", '', '')
    message(msg, D0)

    status = recover_all()

    # TODO: call c.cleanup() to cleanup all tmp files

    toc = time.perf_counter()
    delta_t = toc - tic
    td = {'name': name, "elapsed": delta_t, 'tic': tic, 'toc': toc}
    timers.append(td)

    print_timers()


if __name__ == '__main__':
    main()

