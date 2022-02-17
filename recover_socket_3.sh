#!/bin/bash
#
# Script created: 2022-02-17 10:58:20.940531
# Created on system: pmemtest
# PMT script version: 1.02.0
# Recoverying:
#   Socket: 0x0003
#   Region: region3
#   Dimms: 0x3001,0x3011,0x3021,0x3101,0x3111,0x3121


# Variables & Values
HOST="pmemtest"
SKT_ID="0x0003"
SKT_NUM="3"
DIMMS="0x3001,0x3011,0x3021,0x3101,0x3111,0x3121"
REGION="region3"
NS_NAME="namespace3.0"
NS_DEV="pmem3"
NS_DEV_PATH="/dev/pmem3"
FS_TYPE="xfs"
MT_PT="/pmemfs3"
FSTAB_OPTS="defaults,dax"
FSTAB_TYPE="xfs"
FSTAB_CHK="0    0"

# Cleanup Phase
PHASE1="/var/tmp/socket_0x0003-phase-1"
# Recover Phase
PHASE2="/var/tmp/socket_0x0003-phase-2"
# Safety Interlock to prevent undoing what we just did
DONE="/var/tmp/socket_0x0003-DONE"

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
	logger Beginning Recovery of PMEM on socket 0x0003

	if [ ! `mountpoint -q /pmemfs3` ]; then
		 echo "Unmounting /pmemfs3"
		 logger unmounting /pmemfs3
		 umount /pmemfs3
	else
		echo "/pmemfs3 is not mounted"

	fi

	# Note: These two commands will fail if re-enumeration has happened
	ndctl disable-namespace namespace3.0 > /dev/null 2>&1
	ndctl disable-region region3 > /dev/null 2>&1

	# --- Erasing PMEM Devices used by this region ---
	# Note: On completion, ipmctl will respond that all DIMMs have been cleared.
	#       There is no cause for concern
	logger deleting PMEM configuration for socket 0x0003 for dimms 0x3001,0x3011,0x3021,0x3101,0x3111,0x3121
	echo "deleting PMEM configuration for socket 0x0003 for dimms 0x3001,0x3011,0x3021,0x3101,0x3111,0x3121"
	ipmctl delete -f -dimm -pcd 0x3001,0x3011,0x3021,0x3101,0x3111,0x3121

	# Create new PMEM Region for this socket
	logger creating new PMEM configuration for socket 0x0003
	echo "creating new PMEM configuration for socket 0x0003"
	ipmctl create -goal -socket 0x0003

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
	namespaces=`ndctl list -N -r region3 | wc -l`
	if [ "$namespaces" -ne 0 ] ; then
		 echo "Namespace Exists on region: region3"
		 echo "You Cannot Create a new namespace if there is no room on region3"
		 exit 1
	fi

	echo "Creating namespace on region: region3"
	ndctl create-namespace --mode fsdax --region region3

	# --- Create PMFS on pmem device ---
	echo "Creating filesystem on region3:namespace3.0->/dev/pmem3"
	mkfs -t xfs -m reflink=0 -f /dev/pmem3

	# --- Create PMFS Mount Point ---
	echo "Checking mount point"
	if [ ! -d /pmemfs3 ] ; then
		 echo "creating /pmemfs3"
		 mkdir /pmemfs3
	else 
		 echo "Mount point exists!"
	fi 
	echo "--- Create updated fstab entry for /pmemfs3---" 

	echo "--- Get the PMFS UUID ---"
	new_uuid=`blkid /dev/pmem3 | cut -d" " -f2`
	echo "$new_uuid"

	echo "--- extracting fstab entry for mount point /pmemfs3 ---"
	rest=`grep /pmemfs3 /etc/fstab | cut -f2-`
	echo "--- merging new uuid $new_uuid with original $rest ---"

	new_entry=`echo $new_uuid $rest`

	echo "Writing new fstab entry to /tmp/fstab_socket_0x0003"
	echo "$new_entry" > /tmp/fstab_socket_0x0003

	echo "cat /tmp/fstab_socket_* to see all of the new fstab entries"
	/usr/bin/rm $PHASE2

	echo "Recovery Complete. Be sure to update /etc/fstab with contents from:"
	echo "/tmp/fstab_socket_*"
	touch $DONE

fi # end PHASE2

# --- End of Script ---
