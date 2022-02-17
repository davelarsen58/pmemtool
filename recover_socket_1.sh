#!/bin/bash
#
# Script created: 2022-02-17 10:58:20.811649
# Created on system: pmemtest
# PMT script version: 1.02.0
# Recoverying:
#   Socket: 0x0001
#   Region: region1
#   Dimms: 0x1001,0x1011,0x1021,0x1101,0x1111,0x1121


# Variables & Values
HOST="pmemtest"
SKT_ID="0x0001"
SKT_NUM="1"
DIMMS="0x1001,0x1011,0x1021,0x1101,0x1111,0x1121"
REGION="region1"
NS_NAME="namespace1.0"
NS_DEV="pmem1"
NS_DEV_PATH="/dev/pmem1"
FS_TYPE="xfs"
MT_PT="/pmemfs1"
FSTAB_OPTS="defaults,dax"
FSTAB_TYPE="xfs"
FSTAB_CHK="0    0"

# Cleanup Phase
PHASE1="/var/tmp/socket_0x0001-phase-1"
# Recover Phase
PHASE2="/var/tmp/socket_0x0001-phase-2"
# Safety Interlock to prevent undoing what we just did
DONE="/var/tmp/socket_0x0001-DONE"

# if the DONE flag exists, complain & exit
if [ -f "$DONE" ] ; then
	echo "Found Overwrite Protection Flag, $DONE"
	echo "Remove that file to rerun this script"
	exit 1
fi
# if the flags dont exist, create them
# We can be PHASE1 or PHASE2, but not both
if [ ! -f $PHASE2 ] && [ ! -f "$PHASE1" ] ; then
	touch $PHASE1
fi
# Check for phase 1 flag, clean up the old stuff
if [ -f $PHASE1 ] ; then


	# --- Clean Up Old Provisioning ---
	# Remove demand against PMEM, so we can reconfigure

	echo " --- Pre Boot Clean Up ---"
	logger Beginning Recovery of PMEM on socket 0x0001

	if [ ! `mountpoint -q /pmemfs1` ]; then
		 echo "Unmounting /pmemfs1"
		 logger unmounting /pmemfs1
		 umount /pmemfs1
	else
		echo "/pmemfs1 is not mounted"

	fi

	# Note: These two commands will fail if re-enumeration has happened
	ndctl disable-namespace namespace1.0 > /dev/null 2>&1
	ndctl disable-region region1 > /dev/null 2>&1

	# --- Erasing PMEM Devices used by this region ---
	# Note: On completion, ipmctl will respond that all DIMMs have been cleared.
	#       There is no cause for concern
	logger deleting PMEM configuration for socket 0x0001 for dimms 0x1001,0x1011,0x1021,0x1101,0x1111,0x1121
	echo "deleting PMEM configuration for socket 0x0001 for dimms 0x1001,0x1011,0x1021,0x1101,0x1111,0x1121"
	ipmctl delete -f -dimm -pcd 0x1001,0x1011,0x1021,0x1101,0x1111,0x1121

	# Create new PMEM Region for this socket
	logger creating new PMEM configuration for socket 0x0001
	echo "creating new PMEM configuration for socket 0x0001"
	ipmctl create -goal -socket 0x0001

	# Reboot at this point to create the pmem region
	# unless there are more regions to be created now

	# Clear the Phase 1 flag, now that we are done w/ Phase 1
	/usr/bin/rm -f $PHASE1

	# Set the Phase 2 flag, now that we are done w/ Phase 1
	touch $PHASE2
	echo "Cleanup Complete. Run this script again after rebooting to resume recovery"
	echo "Exiting"
	exit 0

else
	echo "Skipping to PHASE 2"
fi #END PHASE1


if [ -f $PHASE2 ] ; then

	echo "Beginning Phase 2"
	echo " --- Post Boot provisioning ---"

	# namespace will contain 0 if there are no namespaces in this region.
	namespaces=`ndctl list -N -r region1 | wc -l`
	if [ "$namespaces" -ne 0 ] ; then
		 echo "Namespace Exists on region: region1"
		 echo "You Cannot Create a new namespace if there is no room on region1"
		 exit 1
	fi

	echo "Creating namespace on region: region1"
	ndctl create-namespace --mode fsdax --region region1

	# --- Create PMFS on pmem device ---
	echo "Creating filesystem on region1:namespace1.0->/dev/pmem1"
	mkfs -t xfs -m reflink=0 -f /dev/pmem1

	# --- Create PMFS Mount Point ---
	echo "Checking mount point"
	if [ ! -d /pmemfs1 ] ; then
		 echo "creating /pmemfs1"
		 mkdir /pmemfs1
	else 
		 echo "Mount point exists!"
	fi 
	echo "--- Create updated fstab entry for /pmemfs1---" 

	echo "--- Get the PMFS UUID ---"
	new_uuid=`blkid /dev/pmem1 | cut -d" " -f2`
	echo "$new_uuid"

	echo "--- extracting fstab entry for mount point /pmemfs1 ---"
	rest=`grep /pmemfs1 /etc/fstab | cut -f2-`
	echo "--- merging new uuid $new_uuid with original $rest ---"

	new_entry=`echo $new_uuid $rest`

	echo "Writing new fstab entry to /tmp/fstab_socket_0x0001"
	echo "$new_entry" > /tmp/fstab_socket_0x0001

	echo "cat /tmp/fstab_socket_* to see all of the new fstab entries"
	/usr/bin/rm $PHASE2

	echo "Recovery Complete. Be sure to update /etc/fstab with contents from:"
	echo "/tmp/fstab_socket_*"
	touch $DONE

fi # end PHASE2

# --- End of Script ---
