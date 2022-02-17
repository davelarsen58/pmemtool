| Functionality | Reports | Help & Reference | Developers |
| ------------- | ------- | ---------------- | ---------- |
| [PMEM Tool](README.md) | [DIMM Report](Optane_DIMM_Report.md) | [External Refs](References.md) | [Theory of Operation](TheoryofOperation.md) |
| [Guided Recovery](Guided_Recovery.md) | [DIMM Status](DIMM_Status.md) | [IPMCTL User Guide](https://docs.pmem.io/ipmctl-user-guide/) | [Function Timers](Function_Timers.md) |
| [Recovery Script](Recovery_Script.md) | [PMEM FS](PMFS_Report.md)  | [NDCTL User Guide](https://docs.pmem.io/ndctl-user-guide/) | [TO DO](ToDo.md) |
|   | [PMFS Health Report](Healthy_PMFS_Report.md)  | [Steve Scargall](https://stevescargall.com/)  | [PMEM Programming Book](https://pmem.io/books/) |

# Optane DIMM Report
The Optane DIMM report provides the following details, gleaned from the output of ipmctl XML output.

At a glance, DIMM pysical location, status, capacity, CPU socket, CPU memory controller, memory channel, and DIMM slot can be observed.
Additionally the DIMM firmware version for as well as the OEM specific Device Locator for each device in that chassis.

The PMEM UUID is unique per DIMM.

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
