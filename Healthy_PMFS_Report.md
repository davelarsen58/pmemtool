| Functionality | Reports | Help & Reference | Developers |
| ------------- | ------- | ---------------- | ---------- |
| [PMEM Tool](README.md) | [DIMM Report](Optane_DIMM_Report.md) | [External Refs](References.md) | [Theory of Operation](TheoryofOperation.md) |
| [Guided Recovery](Guided_Recovery.md) | [DIMM Status](DIMM_Status.md) | [IPMCTL User Guide](https://docs.pmem.io/ipmctl-user-guide/) | [Function Timers](Function_Timers.md) |
| [Recovery Script](Recovery_Script.md) | [PMEM FS](PMFS_Report.md)  | [NDCTL User Guide](https://docs.pmem.io/ndctl-user-guide/) | [TO DO](ToDo.md) |
|   | [PMFS Health Report](Healthy_PMFS_Report.md)  | [Steve Scargall](https://stevescargall.com/)  | [PMEM Programming Book](https://pmem.io/books/) |

# Healthy Persistent Filesystem Report

This report provides a list of healthy filesystems that can be copies into a software configuration to enable that application to leverage available PMEM Filesystems.
This particular report is formatted for the configuration of a popular *In Memory* database.

pmt provide options to specify the list delimiter as well as specifying any required suffix to the mount point list to reflect addition directory depth on those mount points to support multi-tenancy of that application.

## Example Report
```
PMFS with OK status: /pmemfs0; /pmemfs1; /pmemfs2; /pmemfs3;
```
