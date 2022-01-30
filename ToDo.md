# To Do List

- [ ] update online docs
- [ ]
- [ ] Consider a top down report ( mount point, file system, namespace, region, dimm, iMC, socket )
- [ ] Consider a bottom up report( socket, iMC, dimm, region, namespace, file system, mount point )
- [ ]

# Feature List

## Release 0.80.0
- [ ] Added support for ipmctl data via the ipmctl.py module to add functionality for fw version
- [ ] Add [Guided Recovery](Guided_Recovery.md) Option to recover from Failed DIMM senario

## Release 0.80.0
- [X] Create [PMEM DIMM Report](PMEM_DIMM_Report.md) (Linux Dev, Health, Temp, Remaining Life)
- [X] Create [PMFS Report](PMFS_Report.md) for each entry in FSTAB (Health, Region, NS Dev, NS Type, Mount Pt, Dimm Deps) 
- [X] Create [Healthy PMFS List Report](Healthy_PMFS_Report.md) with List of healthy PMFS from those in FSTAB (Mount Point [; Mount Point]
- [X] Add option to [Healthy PMFS Report](Healthy_PMFS_Report.md) to override default separator (;) with a different one
- [X] Add option to [Healthy PMFS Report](Healthy_PMFS_Report.md) to append path to each mount point
- [X] Add option to skip creating a new ndctl data file to enable testing w/ static file
- [X] Add option to use alternate fstab file to enable testing w/ static file
- [X] Add option to use a self contained sandbox path instead of root path to resolve files. Used for testing
