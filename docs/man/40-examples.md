# Examples


## Example 1

Lookup the vendor name for a MAC address.

```sh
$ ${script} 64:4e:d7:00:22:33
```

output:

```sh
64:4E:D7:00:22:33  644ED7  HP Inc.
```


## Example 2

Look up the vendor name for the OUI portion of a MAC address.

```sh
$ ${script} 000c29
```

output:

```sh
00:0C:29:00:00:00  000C29  VMware, Inc.
```


## Example 3

Look up the vendor name for multiple MAC addresses and OUI portions of MAC addreesses.

```sh
$ ${script} 000c29 000001.112233 64:4e:d7:00:22:33 64-1B-2F-2A-CC-5E
```

output:

```sh
00:0C:29:00:00:00  000C29  VMware, Inc.
00:00:01:11:22:33  000001  XEROX CORPORATION
64:4E:D7:00:22:33  644ED7  HP Inc.
64:1B:2F:2A:CC:5E  641B2F  Samsung Electronics Co.,Ltd
```


## Example 4

Use the file (-f) option to read MACs from a saved file.

```sh
${script} -f examples/macs.txt 
```

output:

```
E8:0A:B9:00:C1:A2  E80AB9  Cisco Systems, Inc
40:84:32:3D:42:B1  408432  Microchip Technology Inc.
70:F8:AE:EF:22:A4  70F8AE  Microsoft Corporation
64:51:06:AA:BB:C8  645106  Hewlett Packard
90:9B:6F:5B:F2:34  909B6F  Apple, Inc.
2C:AB:33:56:8A:62  2CAB33  Texas Instruments
50:02:38:83:AA:2B  500238  Nokia Shanghai Bell Co., Ltd.
44:49:88:E4:8B:33  444988  Intel Corporate
E4:F2:7C:88:B1:20  E4F27C  Juniper Networks
```

contents of `examples/macs.txt`

```
e80a.b900.c1a2
40:84:32:3d:42:b1
70-F8-AE-EF-22-A4
645106-aabbc8
90:9b:6f:5b:f2:34
2C-AB-33-56-8a-62
50023883aa2b
44:49:88:E4:8B:33
E4:F2:7C:88:B1:20
```
