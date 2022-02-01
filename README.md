# pmemtool
This multipurpose tool provides health and configuration details for server platforms integrating 
Intel Optane Persistent Memory (PMEM) amd provides guided recovery from a pmem device fault.
Data is collected from ndctl, ipmctl,  and /etc/fstab and  integrated to enable rapid interpretation
of PMEM DIMM, Region, namespace, and filesystem Status.

The recovery option guides the user through the process of rebuilding an persistent memory interleave set to
restore a persistent memory region to healthy state, creates a persistent memory namespace and filesystem within
that region, and provides details to update /etc/fstab with the new blockid.

Python modules were created to interact with data from [ndctl](https://docs.pmem.io/ndctl-user-guide/), [DAX Mounted File Systems](https://www.kernel.org/doc/Documentation/filesystems/dax.txt) and [fstab](https://en.wikipedia.org/wiki/Fstab) data with pmt
providing the primary user interface through a command line.

## Reports
Three Reports are currently generated through this tool with each targeting specific functionally and status.

### Optane DIMM Report
The OPtane DIMM Report presents DIMM DIMM name, Status

```
DIMMID  Health State     PMEM DIMM UUID         Capacity     Skt   iMC   Chan  Slot  FW Version      Device Locator
------  ---------------  ---------------------  -----------  ----  ----  ----  ----  --------------  --------------------
0x0001  Healthy          8089-a2-1836-00002c4b  252.454 GiB  0     0     0     1     01.02.00.5446   CPU1_DIMM_A2
0x0011  Healthy          8089-a2-1836-0000214e  252.454 GiB  0     0     1     1     01.02.00.5446   CPU1_DIMM_B2
0x1111  Healthy          8089-a2-1836-00002639  252.454 GiB  1     1     1     1     01.02.00.5446   CPU2_DIMM_E2
0x1121  Healthy          8089-a2-1836-00002617  252.454 GiB  1     1     2     1     01.02.00.5446   CPU2_DIMM_F2
0x0021  Healthy          8089-a2-1836-00002716  252.454 GiB  0     0     2     1     01.02.00.5446   CPU1_DIMM_C2
0x0101  Healthy          8089-a2-1836-000025c2  252.454 GiB  0     1     0     1     01.02.00.5446   CPU1_DIMM_D2
0x0111  Healthy          8089-a2-1842-00002352  252.454 GiB  0     1     1     1     01.02.00.5446   CPU1_DIMM_E2
0x0121  Healthy          8089-a2-1836-000025fc  252.454 GiB  0     1     2     1     01.02.00.5446   CPU1_DIMM_F2
0x1001  Healthy          8089-a2-1836-000025be  252.454 GiB  1     0     0     1     01.02.00.5446   CPU2_DIMM_A2
0x1011  Healthy          8089-a2-1836-00001db5  252.454 GiB  1     0     1     1     01.02.00.5446   CPU2_DIMM_B2
0x1021  Healthy          8089-a2-1836-00001e90  252.454 GiB  1     0     2     1     01.02.00.5446   CPU2_DIMM_C2
0x1101  Healthy          8089-a2-1836-000020bf  252.454 GiB  1     1     0     1     01.02.00.5446   CPU2_DIMM_D2
```

### Persistent Memory Filesystem (PMFS) Report

The PMFS report is driven from contents of /etc/fstab and shows PM Region, namespace device, mount point, and 
PMEM DIMM's associated with the region and namespace.  The intent is to roll up the namespace health based upon
teh health of teh underlying PMEM DIMM's.
```
Mount Point  Mounted NS Size   Health   Region     NS dev   NS Type  fs_type  PMEM Devices
------------ ------- --------- -------- ---------- -------- -------- -------- --------------------------------------
/pmemfs0     False   1488 GiB  ok       region0    pmem0    fsdaX    xfs      nmem5 nmem4 nmem3 nmem2 nmem1 nmem0
/pmemfs1     True    1488 GiB  ok       region1    pmem1    fsdaX    xfs      nmem11 nmem10 nmem9 nmem8 nmem7 nmem6
```
## Healthy Persistent Memory Mount Points
This report lists healthy PMFS filesystems with its initial use targeted for consumption by by specific database
 application that leverages DAX mounted PMFS to accelerate its in-memory database.  By copying the line into
 the database configuration, the DB engine will map its objects to those Persistent Memory Filesystems.
```buildoutcfg
PMFS with OK status: /pmemfs0; /pmemfs1;
```
# Help
```buildoutcfg
usage: pmt [-h] [--delimiter DELIMITER] [--suffix SUFFIX] [--ndctl_file NDCTL_FILE] [--fstab_file FSTAB_FILE] [--sandbox SANDBOX]
           [--skip_ndctl_dump SKIP_NDCTL_DUMP] [--verbose VERBOSE] [--debug DEBUG]

optional arguments:
  -h, --help            show this help message and exit
  --delimiter DELIMITER
                        Delimiter for pmfs mount path. Default:';'
  --suffix SUFFIX       string to append to pmfs mount path Default:''
  --ndctl_file NDCTL_FILE
                        path to ndctl data file. Default:''
  --fstab_file FSTAB_FILE
                        path to fstab file. Default:''
  --sandbox SANDBOX     path to optional sandbox environment. Default:''
  --skip_ndctl_dump SKIP_NDCTL_DUMP
                        flag to control whether to create a new ndctl data file. default:'False'
  --verbose VERBOSE     enable Verbose mode
  --debug DEBUG         enable debug mode

```
# Common Usage
```./pmt```
# Extending Capabilities
Many additional capabilities can be added to [pmt](./pmt) through the modules [ndctl.py](./ndctl.py), [fsab.py](./fstab.py), and [common.py](./common.py)
refer to the modules themselves
  
