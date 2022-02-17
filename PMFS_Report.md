| Functionality | Reports | Help & Reference | Developers |
| ------------- | ------- | ---------------- | ---------- |
| [PMEM Tool](README.md) | [DIMM Report](Optane_DIMM_Report.md) | [External Refs](References.md) | [Theory of Operation](TheoryofOperation.md) |
| [Guided Recovery](Guided_Recovery.md) | [DIMM Status](DIMM_Status.md) | [IPMCTL User Guide](https://docs.pmem.io/ipmctl-user-guide/) | [Function Timers](Function_Timers.md) |
| [Recovery Script](Recovery_Script.md) | [PMEM FS](PMFS_Report.md)  | [NDCTL User Guide](https://docs.pmem.io/ndctl-user-guide/) | [TO DO](ToDo.md) |
|   | [PMFS Health Report](Healthy_PMFS_Report.md)  | [Steve Scargall](https://stevescargall.com/)  | [PMEM Programming Book](https://pmem.io/books/) |

# Persistent Memory Filesystem Report
This report provides key operational information regarding a Persistent Memory Filesystem configured in /etc/fstab.

Columns Presented are as follows:
| Column | Purpose |
| ------ | ------- |
| Mount Point | The directory where the filesystem is normally mounted as specified in fstab |
| Mounted | indicates whether the filesystem is mounted or not when report was run |
| NS Size | Namespace size for the underlying Persistent Memory region exposed as the filesystem |
| Health  | Health reflects the roll up status of the underlying PMEM devices, Region, and namespace |
| Region  | Name of the logical Persistent Memory Region providing the namespace is mapped within |
| NS Dev  | The logical device exposed by the OS to access the PMEM nemory space, and typically exposed as a DAX mounted filesystem |
| NS Type | The namespace mode as described in ([Managing PMEM Namespaces](https://docs.pmem.io/ndctl-user-guide/managing-namespaces)) |
| FS Type | Filesystem type specified in fstab |
| PMEM Devices | DIMM ID's of the physical PMEM DIMM's supporting that PMEM Region and namespace.  They are listed to enable corrlation of the filesystem service dependency on the hardware |


```
Mount Point  Mounted NS Size   Health   Region     NS dev   NS Type  fs_type  PMEM Devices
------------ ------- --------- -------- ---------- -------- -------- -------- --------------------------------------
/pmemfs0     True    1488 GiB  ok       region0    pmem0    fsdaX    xfs      0x0001 0x0011 0x0021 0x0101 0x0111 0x0121
/pmemfs1     True    1488 GiB  ok       region1    pmem1    fsdaX    xfs      0x1001 0x1011 0x1021 0x1101 0x1111 0x1121
/pmemfs2     True    1488 GiB  ok       region2    pmem2    fsdaX    xfs      0x2001 0x2011 0x2021 0x2101 0x2111 0x2121
/pmemfs3     True    1488 GiB  ok       region3    pmem3    fsdaX    xfs      0x3001 0x3011 0x3021 0x3101 0x3111 0x3121
```
