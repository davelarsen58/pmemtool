| Functionality | Reports | Help & Reference | Developers |
| ------------- | ------- | ---------------- | ---------- |
| [PMEM Tool](README.md) | [DIMM Report](Optane_DIMM_Report.md) | [External Refs](References.md) | [Theory of Operation](TheoryofOperation.md) |
| [Guided Recovery](Guided_Recovery.md) | [DIMM Status](DIMM_Status.md) | [IPMCTL User Guide](https://docs.pmem.io/ipmctl-user-guide/) | [Function Timers](Function_Timers.md) |
| [Recovery Script](Recovery_Script.md) | [PMEM FS](PMFS_Report.md)  | [NDCTL User Guide](https://docs.pmem.io/ndctl-user-guide/) | [TO DO](ToDo.md) |
|   | [PMFS Health Report](Healthy_PMFS_Report.md)  | [Steve Scargall](https://stevescargall.com/)  | [PMEM Programming Book](https://pmem.io/books/) |

# To Do List

- [ ] Consider a top down report ( mount point, file system, namespace, region, dimm, iMC, socket )
- [ ] Consider a bottom up report( socket, iMC, dimm, region, namespace, file system, mount point )

# Releases
https://github.com/davelarsen58/pmemtool/releases

## Release Next
- Updated online docs

## Release 1.02.0

### Bug fixes
Fixed several recovery script generation errors that resulted in shell script execution errors.

### Enhancements
#### Recovery Script Features
- Added multiphase support to enable clean up followed by reprovisioning following a reboot by running the same script.
- Added 4 example scripts to repo.
- Working on changes to replace generated constants with self contained shell variable within each script to allow reuse of a script on new installation.
- Added Recovery_Script.md to show example test run of a script.

#### Module Profiling Features
- minor changes to the module timers and reporting

## Release 1.01.0
### Enhancements
 - updated fstab table to report ipmctl DIMM ID's instead of ndctl nmem devices to aid in hardware recovery if needed

### Performance improvements
- added check if we already have an XML file for input from current session & reused it.
- temporarily disabled the whitelist code to avoid key errors on different OEM systems
- added --timers option to report on function call profile to see identify time hogs / delays
- improved report and script generation time by 2-3X

### Details
    - pmt Changes
      Updated fs_table to use ipmctl dimm list instead of ndctl dimm list
      Added timer instrumentation to identify performance bottlenecks.
      Added --timers flag to pmt to report module timers for functions.
      Added clean_up() call to clean up tmp file from pmt after use

    - ipmctl.py Changes
      updated show_dimm dimm to see if xml file exits before calling ipmctl again
      improved show_dimm elapsed time by not calling again, since we already have data
      Added timer instrumentation to identify performance bottlenecks.

    - ndctl.py changes
      Added timer instrumentation to identify performance bottlenecks.

    - recovery.py changes
      Added timer instrumentation to identify performance bottlenecks.

## Release 1.00.0

## Release 0.90

### Enhancements:
  - replaced ndctl dimm list with ipmctl dimm list
  - added socket recovery script generation
  
## Release 0.80.0
- [X] Added support for ipmctl data via the ipmctl.py module to add functionality for fw version
- [X] Add [Guided Recovery](Guided_Recovery.md) Option to recover from Failed DIMM senario

## Release 0.80.0
- [X] Create [PMEM DIMM Report](PMEM_DIMM_Report.md) (Linux Dev, Health, Temp, Remaining Life)
- [X] Create [PMFS Report](PMFS_Report.md) for each entry in FSTAB (Health, Region, NS Dev, NS Type, Mount Pt, Dimm Deps) 
- [X] Create [Healthy PMFS List Report](Healthy_PMFS_Report.md) with List of healthy PMFS from those in FSTAB (Mount Point [; Mount Point]
- [X] Add option to [Healthy PMFS Report](Healthy_PMFS_Report.md) to override default separator (;) with a different one
- [X] Add option to [Healthy PMFS Report](Healthy_PMFS_Report.md) to append path to each mount point
- [X] Add option to skip creating a new ndctl data file to enable testing w/ static file
- [X] Add option to use alternate fstab file to enable testing w/ static file
- [X] Add option to use a self contained sandbox path instead of root path to resolve files. Used for testing
