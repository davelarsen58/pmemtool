#!/usr/bin/python3

import sys
import os
from common import message, get_linenumber, version
from common import V0, V1, V2, V3, V4, V5, D0, D1, D2, D3, D4, D5
import common as c


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
    msg = "%s %s %s %s" % (get_linenumber(), "Beginning recover():", '', '')
    message(msg, D1)

    import datetime  # used to get timestamp.now()
    import socket    # used to get hostname
    
    tmp = ' '.join(data['dimms'])
    dimms = tmp.replace(' ', '')
    nmem = data['nmem']

    region_name = data['region']
    namespace_name = data['ns_name']
    namespace_dev = data['ns_dev']
    fs_type = data['fs_type']
    capacity = data['Capacity']
    mount_point = data['mount_point']

    socket_id = data['socket_id']
    socket_num = data['socket_num']

    file_name = data['file_name']

    pmem_device_path = '/dev/' + namespace_dev

    time_stamp = datetime.datetime.now()
    host_name = socket.gethostname()

    msg = "%s %s %s %s %s" % (get_linenumber(), "recover(): Socket:", socket_id, ' DIMMs: ',dimms)
    message(msg, D2)

    old_uuid = 'UUID="xxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx"'
    fstab_opts = 'defaults,dax'
    fstab_type = 'xfs'
    fstab_check = '0    0'

    fstab_entry = old_uuid + ' ' + mount_point + ' ' + fstab_type + ' ' + fstab_opts + ' ' + fstab_check

    '''container to hold the script'''
    script_txt = []

    message('Opening File Name: ' + file_name, D3)
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

    script_txt.append('# --- Clean Up Old Provisioning ---\n')
    script_txt.append('# Remove demand against PMEM, so we can reconfigure\n')
    script_txt.append('\n')
    script_txt.append('# NOTE: Recovering from a failed DIMM, these commands\n')
    script_txt.append('#       may fail due to filesystem not being mounted,\n')
    script_txt.append('#       namespaces being re-enumerated due to nmem changes,\n')
    script_txt.append('#       and regions being hidden due to failed interleave-set\n')
    script_txt.append('#       nmem devices, namespace devices, and regions are all\n')
    script_txt.append('#       dynamically enumerated at boot time based upon hardware\n')
    script_txt.append('#       availability\n')
    script_txt.append('\n')

    script_txt.append('logger Beginning Recovery of PMEM on socket %s\n' % (socket_id))
    script_txt.append('\n')
    script_txt.append('if [ ! `mountpoint -q %s` ]; then\n' % (mount_point))
    script_txt.append('\t echo "Unmounting %s"\n' % (mount_point))
    script_txt.append('\t logger unmounting %s\n' % (mount_point))
    script_txt.append('\t umount %s\n' % (mount_point))
    script_txt.append('else\n')
    script_txt.append('\techo "%s is not mounted"\n' % (mount_point))
    script_txt.append('\n')
    script_txt.append('fi\n')
    script_txt.append('\n')
    script_txt.append('# Note: These two commands will fail if re-enumeration has happened\n')
    script_txt.append('ndctl disable-namespace %s\n' % (namespace_name))
    script_txt.append('ndctl disable-region %s\n' % (region_name))
    script_txt.append('\n')

    script_txt.append('# --- Erasing PMEM Devices used by this region ---\n')
    script_txt.append('# Note: On completion, ipmctl will respond that all DIMMs have been cleared.\n')
    script_txt.append('#       There is no cause for concern\n')
    script_txt.append('logger deleting PMEM configuration for socket %s for dimms %s\n' % (socket_id, dimms))
    script_txt.append('echo deleting PMEM configuration for socket %s for dimms %s\n' % (socket_id, dimms))
    script_txt.append('ipmctl delete -f -dimm -pcd %s\n' % (dimms))
    script_txt.append('\n')

    script_txt.append('# Create new PMEM Region for this socket\n')
    script_txt.append('logger creating new PMEM configuration for socket %s\n' % (socket_id))
    script_txt.append('echo creating new PMEM configuration for socket %s\n' % (socket_id))
    script_txt.append('ipmctl create -goal -socket %s\n' % (socket_id))
    script_txt.append('\n')

    script_txt.append('# Reboot at this point to create the pmem region\n')
    script_txt.append('# unless there are more regions to be created now\n')
    script_txt.append('\n')

    script_txt.append('while [ true ] ; do\n')
    script_txt.append('\t read -p "Do you wish to reboot now?" yn\n')
    script_txt.append('\t case $yn in\n')
    script_txt.append('\t\t [Yy]* ) echo Rebooting Now; shutdown -r now; break;;\n')
    script_txt.append('\t\t [Nn]* ) reboot later after all changes are made;;\n')
    script_txt.append('\t\t * ) echo "Please answer yes or no.";;\n')
    script_txt.append('\t esac\n')
    script_txt.append('done\n')
    script_txt.append('\n')

    script_txt.append('# --- Post Boot provisioning ---\n')
    script_txt.append('\n')
    script_txt.append('# no_namespace will contain 0, if there are no namespaces in this region.\n')
    script_txt.append('namespaces_exist=`ndctl list -N -r %s | wc -l`\n' % (region_name))
    script_txt.append('if [ "namespace_exist" -ne 0 ] ; then\n')
    script_txt.append('\t echo Namespace Exists on region: %s\n' % (region_name))
    script_txt.append('\t echo You Cannot Create a new namespace if there is no room on %s\n' % (region_name))
    script_txt.append('\t exit 1\n')
    script_txt.append('fi\n')

    script_txt.append('echo Creating namespace on region: %s\n' % (region_name))
    script_txt.append('ndctl create-namespace --mode fsdax --region %s\n' % (region_name))

    #TODO: integrate dymamic fs_type into command below
    script_txt.append('# --- Create PMFS on pmem device ---\n')
    script_txt.append('echo Creating filesystem on %s:%s->%s\n' % (region_name, namespace_name, pmem_device_path))
    script_txt.append('mkfs -t xfs -m reflink=0 -f %s\n' % (pmem_device_path))

    script_txt.append('# --- Create PMFS Mount Point ---\n')
    script_txt.append('echo Checking mount point\n')
    script_txt.append('if [ ! -d %s ] ; then\n' % (mount_point))
    script_txt.append('\t echo creating %s\n' % (mount_point))
    script_txt.append('\t mkdir %s\n' % (mount_point))
    script_txt.append('else \n')
    script_txt.append('\t echo Mount point exists!\n')
    script_txt.append('fi \n')

    script_txt.append('echo --- Create updated fstab entry for %s--- \n' % (mount_point))
    script_txt.append('\n')
    script_txt.append('echo --- Get the PMFS UUID ---\n')
    script_txt.append('new_uuid=`blkid %s`\n' % (pmem_device_path))
    script_txt.append('echo $new_uuid\n')
    script_txt.append('echo --- extracting fstab entry for mount point %s ---\n'% (mount_point))
    script_txt.append('\n')
    script_txt.append('rest=`grep /etc/fstab | cut -f2- %s`\n' % (mount_point))
    script_txt.append('echo --- merging new uuid $new_uuid with original $rest %s ---\n')
    script_txt.append('new_entry=`echo $new_uuid $rest`\n')
    script_txt.append('\n')
    script_txt.append('# --- Use below line to update /etc/fstab.\n')
    script_txt.append('echo $new_entry\n')
    script_txt.append('# --- Use above line to update /etc/fstab.\n')


    script_txt.append('\n')

    #TODO: update this section so it creates properly formatted fstab entry
    #
    # script_txt.append('# --- Update /etc/fstab with new fs uuid --- \n')
    # script_txt.append('# This sed script can help, or edit it yourself\n')
    # script_txt.append('new_uuid=`blkid %s  | cut -d" " -f2`\n' % ( pmem_device_path))
    # script_txt.append('\n')

    # script_txt.append('# --- Example fstab entry ---\n')
    # script_txt.append('echo \'%s >> /etc/fstab\'\n' % (fstab_entry))
    # script_txt.append('\n')

    # script_txt.append("cat /etc/fstab | sed 's/%s/%s/' >> /tmp/new_fstab\n" % (old_uuid, 'new_uuid'))

    # script_txt.append('\n')
    # script_txt.append('\n')
    script_txt.append('# --- End of Script ---\n')

    f.writelines(script_txt)
    f.close()

    msg = "%s %s %s" % (get_linenumber(), "recover(): closed file:", file_name)
    message(msg, D2)

    msg = "%s %s %s %s" % (get_linenumber(), "End:recover_socket()", '', '')
    message(msg, D1)

    return file_name


# ---------------------------------------------------------------------
def recover_all():
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
    ap.add_argument("--verbose",     required=False, help="")

    args = vars(ap.parse_args())

    if args['verbose']:     VERBOSE = args['verbose']

    msg = "%s %s %s %s" % (get_linenumber(), "Main:Begin:", '', '')
    message(msg, D0)

    status = recover_all()

    # TODO: call c.cleanup() to cleanup all tmp files

if __name__ == '__main__':
    main()

