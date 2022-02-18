| Functionality | Reports | Help & Reference | Developers |
| ------------- | ------- | ---------------- | ---------- |
| [PMEM Tool](README.md) | [DIMM Report](Optane_DIMM_Report.md) | [External Refs](References.md) | [Theory of Operation](TheoryofOperation.md) |
| [Guided Recovery](Guided_Recovery.md) | [DIMM Status](DIMM_Status.md) | [IPMCTL User Guide](https://docs.pmem.io/ipmctl-user-guide/) | [Function Timers](Function_Timers.md) |
| [Recovery Script](Recovery_Script.md) | [PMEM FS](PMFS_Report.md)  | [NDCTL User Guide](https://docs.pmem.io/ndctl-user-guide/) | [TO DO](ToDo.md) |
|   | [PMFS Health Report](Healthy_PMFS_Report.md)  | [Steve Scargall](https://stevescargall.com/)  | [PMEM Programming Book](https://pmem.io/books/) |


# How It Works
We first begin by dumping ndctl namespace, region, DIMM, and DIMM health statistics into a json file in /tmp where it is parsed and imported into a python dictionary named ndctl.
Next, we dump socket, region, and dimm data using ipmctl into a series of XML files in /tmp, and imported int python dictionaries sockets, dimms, and regions respectively. Functions from the [ipmctl module](ipmctl.py)

WIP


# Feature List
## Reports
The reports defined in this initial tool were to identify current status of persistent memory filesystems and underlying logical and physical devices to enable operations personnel to quickly identify subsystem status and direct operation changes as needed to maintain application SLA.

The key reports are specified here with additional levels of detail:
- [PMEM DIMM Health & Status Report](Optane_DIMM_Report.md)
- [Persistent Memory Filesystem Health & Status Report](PMFS_Report.md)
- [Healthy Filesystem Report](Healthy_PMFS_Report.md)

## PMEM Filesystem Recovery Scripts
Recovery functionality was requested to enable rapid restoration of services in the event of a hardware failure.
Recovery Scripts are generated with an optional flag to pmt with one script generated per socket.
The expectation is that prior to script generation, the system has been previously configured and healthy.

Additional details can be found in each of these links:
- [Example Recovery Script for Socket 0](recover_socket_0.sh)
- [Guide Recovery of PMEM Filesystem](Guided_Recovery.md)
- [Recovery Script Example Run](Recovery_Script.md)

## Baseline Tool Support
This tool leverages open source tools ipmctl and ndctl to acquire physical and logical topology and relationships then corrlates that information into various reports to address specific kinds of questions required by operations personnel.

### Python Wrapper Interface for IPMCTL (NVM XML)
The [ipmctl module](ipmctl.py) provides access functions to socket, dimm, status, and topolgy information.
This module is heavily used throughout the tool.

### Python Wrapper Interface for NDCTL (JSON)
The [ndctl module](ndctl.py) provides access to the generic NVDIMM operating system interface used to manage namespaces, and logical PMEM hierarchy of pmem namespaces, regions, nmem (generic PMEM DIMM interface)
This module is heavily leveraged throughout this tool.

### FSTAB Module
The [fstab module](fstab.py) provide accessors to extract and correlate PMEM related info in teh /etc/fstab file.
This module is heavily leveraged throughout this tool.

### Recovery Module
The [recovery module](recovery.py) provides functions leveraged by the recovery process to generate the recovery scripts.

