| Functionality | Reports | Help & Reference | Developers |
| ------------- | ------- | ---------------- | ---------- |
| [PMEM Tool](README.md) | [DIMM Report](Optane_DIMM_Report.md) | [External Refs](References.md) | [Theory of Operation](TheoryofOperation.md) |
| [Guided Recovery](Guided_Recovery.md) | [DIMM Status](DIMM_Status.md) | [IPMCTL User Guide](https://docs.pmem.io/ipmctl-user-guide/) | [Function Timers](Function_Timers.md) |
| [Recovery Script](Recovery_Script.md) | [PMEM FS](PMFS_Report.md)  | [NDCTL User Guide](https://docs.pmem.io/ndctl-user-guide/) | [TO DO](ToDo.md) |
|   | [PMFS Health Report](Healthy_PMFS_Report.md)  | [Steve Scargall](https://stevescargall.com/)  | [PMEM Programming Book](https://pmem.io/books/) |

# Recovery Script Example Run

Ideally, you ran pmt --recovery on a healthy system as one of those preventive measures,
and kept those scripts that were generated in a safe place for later use.

You should also periodically generate new versions as your infrastructure changes.

**Note that pmt depends on a system to be fully configured and healthy to generate the recovery scripts.**

The recovery script has 3 states of execution.

1. Cleanup Phase - umounts PMFS if mounted, disables the PM namespace and PM region
2. Provisioning Phase - Creates new namespace, filesystem on that namespace, and generates new fstab entry
3. Done - Safety intelock to prevent accidentaly overwriting the new configuration


## Phase 1 Example Run

This is the clean up phase where we clean up any demands against the physical and logical
components, so we can create a new configuration.

```
root@insp01:~# ./recover_socket_2.sh

 --- Pre Boot Clean Up ---
Unmounting /pmem2
deleting PMEM configuration for socket 0x0002 for dimms 0x2001,0x2011,0x2021,0x2101,0x2111,0x2121

Clear Config partition(s) on DIMM 0x0001: Success
Clear Config partition(s) on DIMM 0x0011: Success
Clear Config partition(s) on DIMM 0x0021: Success
Clear Config partition(s) on DIMM 0x0101: Success
Clear Config partition(s) on DIMM 0x0111: Success
Clear Config partition(s) on DIMM 0x0121: Success
Clear Config partition(s) on DIMM 0x1001: Success
Clear Config partition(s) on DIMM 0x1011: Success
Clear Config partition(s) on DIMM 0x1021: Success
Clear Config partition(s) on DIMM 0x1101: Success
Clear Config partition(s) on DIMM 0x1111: Success
Clear Config partition(s) on DIMM 0x1121: Success
Clear Config partition(s) on DIMM 0x2001: Success
Clear Config partition(s) on DIMM 0x2011: Success
Clear Config partition(s) on DIMM 0x2021: Success
Clear Config partition(s) on DIMM 0x2101: Success
Clear Config partition(s) on DIMM 0x2111: Success
Clear Config partition(s) on DIMM 0x2121: Success
Clear Config partition(s) on DIMM 0x3001: Success
Clear Config partition(s) on DIMM 0x3011: Success
Clear Config partition(s) on DIMM 0x3021: Success
Clear Config partition(s) on DIMM 0x3101: Success
Clear Config partition(s) on DIMM 0x3111: Success
Clear Config partition(s) on DIMM 0x3121: Success

Data dependencies may result in other commands being affected. A system reboot is required before all changes will take effect.
creating new PMEM configuration for socket 0x0002

The following configuration will be applied:
 SocketID | DimmID | MemorySize | AppDirect1Size | AppDirect2Size
==================================================================
 0x0002   | 0x2001 | 0.000 GiB  | 252.000 GiB    | 0.000 GiB
 0x0002   | 0x2011 | 0.000 GiB  | 252.000 GiB    | 0.000 GiB
 0x0002   | 0x2021 | 0.000 GiB  | 252.000 GiB    | 0.000 GiB
 0x0002   | 0x2101 | 0.000 GiB  | 252.000 GiB    | 0.000 GiB
 0x0002   | 0x2111 | 0.000 GiB  | 252.000 GiB    | 0.000 GiB
 0x0002   | 0x2121 | 0.000 GiB  | 252.000 GiB    | 0.000 GiB

Do you want to continue? [y/n] y

Created following region configuration goal
 SocketID | DimmID | MemorySize | AppDirect1Size | AppDirect2Size
==================================================================
 0x0002   | 0x2001 | 0.000 GiB  | 252.000 GiB    | 0.000 GiB
 0x0002   | 0x2011 | 0.000 GiB  | 252.000 GiB    | 0.000 GiB
 0x0002   | 0x2021 | 0.000 GiB  | 252.000 GiB    | 0.000 GiB
 0x0002   | 0x2101 | 0.000 GiB  | 252.000 GiB    | 0.000 GiB
 0x0002   | 0x2111 | 0.000 GiB  | 252.000 GiB    | 0.000 GiB
 0x0002   | 0x2121 | 0.000 GiB  | 252.000 GiB    | 0.000 GiB

A reboot is required to process new memory allocation goals.

Cleanup Complete. Run this script again after rebooting to resume recovery
Exiting

## Phase 2 Execution Example

```
After the reboot, running the script again will resume recovery of
the pmem filesystem.

```
Skipping to PHASE 2
Beginning Phase 2
 --- Post Boot provisioning ---
Creating namespace on region: region1
{
  "dev":"namespace1.0",
  "mode":"fsdax",
  "map":"dev",
  "size":"1488.37 GiB (1598.13 GB)",
  "uuid":"b33702b3-c179-4eea-8878-b16c01e98529",
  "sector_size":512,
  "align":2097152,
  "blockdev":"pmem1"
}
Creating filesystem on region1:namespace1.0->/dev/pmem1
meta-data=/dev/pmem1             isize=512    agcount=4, agsize=97542016 blks
         =                       sectsz=4096  attr=2, projid32bit=1
         =                       crc=1        finobt=1, sparse=1, rmapbt=0
         =                       reflink=0
data     =                       bsize=4096   blocks=390168064, imaxpct=5
         =                       sunit=0      swidth=0 blks
naming   =version 2              bsize=4096   ascii-ci=0, ftype=1
log      =internal log           bsize=4096   blocks=190511, version=2
         =                       sectsz=4096  sunit=1 blks, lazy-count=1
realtime =none                   extsz=4096   blocks=0, rtextents=0
Checking mount point
creating /pmemfs1
--- Create updated fstab entry for /pmemfs1---
--- Get the PMFS UUID ---
UUID="015d5c1d-6c05-4c61-abdb-454180667e3a"
--- extracting fstab entry for mount point /pmemfs1 ---
--- merging new uuid UUID="015d5c1d-6c05-4c61-abdb-454180667e3a" with original /pmemfs1 xfs     noatime,nodiratime,nodiscard,dax        0       0 ---
Writing new fstab entry to /tmp/fstab_socket_0x0001
cat /tmp/fstab_socket_* to see all of the new fstab entries
Recovery Complete. Be sure to update /etc/fstab with contents from:
/tmp/fstab_socket_*

### Extracting the New entry for /etc/fstab
This new entry should be copied into the /etc/fstab to replace the existing entry.

Note that the only difference between the new and old entries are the UUID value.
The rest of the entry are extracted from the current entry.

```
root@insp01:~# cat /tmp/fstab_socket_*
UUID="015d5c1d-6c05-4c61-abdb-454180667e3a" /pmemfs1 xfs noatime,nodiratime,nodiscard,dax 0 0

root@insp01:~# cat /tmp/fstab_socket_* >> /etc/fstab
```

## Configuration Protection
The following example shows what happens when you run the script a 3rd time.

This functionality is intended to protect the configuration from being accidentally
affected should the recovery script be run following a recovery.

```
./recover_socket_1.sh

Found DONE Flag, /var/tmp/socket_0x0001-DONE
Remove that flag rerun script again
```
