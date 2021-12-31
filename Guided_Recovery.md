# Guided Recovery Process

A new feature is being added to pmemtool to provide the admin with a guided
process to recover from various kinds of faults.

The first recovery process is restoring a PMFS from a DIMM Fatal Error, which
would cause a cascaded failure of the associated PMEM Region, PMEM NameSpace,
and file system residing on that namespace.

```
pmt --recover --dimm 0x0001 --region region0 --namespace namespace0.0 --pmfs /mount_point
```

# Triage Tree with Actions
## PMEM DIMM
- gather device status with ndctl or ipmctl
- if status < nominal, triage_dimm()

### triage_dimm()
- can system see DIMM?
    - sudo ipmctl show -dimm
```
 DimmID | Capacity    | LockState | HealthState | FWVersion
===============================================================
 0x0001 | 252.454 GiB | Disabled  | ==Healthy==     | 01.02.00.5446
 0x0011 | 252.454 GiB | Disabled  | Healthy     | 01.02.00.5446
 0x0021 | 252.454 GiB | Disabled  | Healthy     | 01.02.00.5446
 0x0101 | 252.454 GiB | Disabled  | Healthy     | 01.02.00.5446
 0x0111 | 252.454 GiB | Disabled  | Healthy     | 01.02.00.5446
 0x0121 | 252.454 GiB | Disabled  | Healthy     | 01.02.00.5446
 0x1001 | 252.454 GiB | Disabled  | Healthy     | 01.02.00.5446
 0x1011 | 252.454 GiB | Disabled  | Healthy     | 01.02.00.5446
 0x1021 | 252.454 GiB | Disabled  | Healthy     | 01.02.00.5446
 0x1101 | 252.454 GiB | Disabled  | Healthy     | 01.02.00.5446
 0x1111 | 252.454 GiB | Disabled  | Healthy     | 01.02.00.5446
 0x1121 | 252.454 GiB | Disabled  | Healthy     | 01.02.00.5446
```
    - sudo ndctl list -DH
```
  {
    "dev":"nmem1",
    "id":"8089-a2-1836-0000214e",
    "handle":17,
    "phys_id":40,
    "security":"disabled",
    "health":{
      =="health_state":"ok",==
      "temperature_celsius":31.0,
      "controller_temperature_celsius":31.0,
      =="spares_percentage":100,==
      =="alarm_temperature":false,==
      =="alarm_controller_temperature":false,==
      =="alarm_spares":false,==
      "alarm_enabled_media_temperature":true,
      "temperature_threshold":82.0,
      "alarm_enabled_ctrl_temperature":true,
      "controller_temperature_threshold":98.0,
      "alarm_enabled_spares":true,
      "spares_threshold":50,
      "shutdown_state":"clean",
      "shutdown_count":4
    }
  },
```
- Is DIMM Health State OK / Healthy?
   - See above output
   - if not OK/Health, check further
      - Is Fault / Error Injection enabled / active?

## PMEM REGION
- identify region status
    - identify interleave set (ILS) DIMM dependencies
    - if any ILS dependency < nominal, triage_region()

### triage_region()

## PMEM NAMESPACE
- identify namespace status
    - identify region dependencies
    - if any region dependency < nominal, triage_namespace()

### triage_namespace()

## PMEM FILE SYSTEM
- identify PMFS status
    - is PMFS mounted?
    - can it be manually mounted?
    - if any PMFS namespace dependency < nominal, triage_pmfs()

### triage_pmfs()

## Identify affected structures
  filesystem, mount point
  namespace
  region
  socket
  dimm list

tear down existing structure
clear pcd
create goal



