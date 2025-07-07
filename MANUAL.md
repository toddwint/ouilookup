---
title: OUILOOKUP
section: 1
header: User Commands
footer: ouilookup 0.0.5
date: 2025-07-07
author: Todd Wintermute
---


# Name

ouilookup - Tool to obtain vendor name / organizationally unique identifier (OUI) for MAC addresses


# Synopsis

**`ouilookup`** `[`**`-h`**`]` `[`**`-f`** _`FILE`_`]` `[`**`--download`**`]` `[`**`--completion`** `{`**`bash`**,**`zsh`**,**`fish`**`}]` `[`**`--version`**`]` `[`**`--quiet`**`]` _`MAC`_ `[`_`MAC`_ `...]`


# Description

This program takes one or more MAC addresses and returns the Org Name. It uses information from `https://standards- oui.ieee.org/oui/oui.csv`.


## Positional Arguments

_`MAC`_
: the full MAC address or the OUI portion (first 6 hex digits). If providing multiple items, separate each MAC/OUI with a space. Within the MAC/OUI separating characters such as `:`, `-`, or `.` are allowed at any interval. Examples: 74:13:ea:9a:22:2e 28-EA-0B-6C-A9-E5 b4df.9181.7fb1 e073e7-ec3802 080030


## Option Flags

**`-h`**, **`--help`**
: show this help message and exit


**`-f`** _`FILE`_, **`--file`** _`FILE`_
: use a file with one MAC address per line.


**`--version`**, **`-v`**
: show the version number and exit


**`--quiet`**, **`-q`**
: suppress warning messages when MAC is not found to be valid


## Download Ieee Oui File

**`--download`**, **`-d`**
: download the IEEE OUI file `oui.csv` and save to `{HOME}/.local/share/ouilookup` on Linux or `{APPDATA}\ouilookup` on Windows as `oui.csv`. Also convert CSV to JSON and save as `oui.json`


## Shell Completion Options

**`--completion`** `{`**`bash`**,**`zsh`**,**`fish`**`}`
: print ouilookup shell completion to the terminal and exit


# Examples


## Example 1

Lookup the vendor name for a MAC address.

```sh
$ ouilookup 64:4e:d7:00:22:33
```

output:

```sh
64:4E:D7:00:22:33  644ED7  HP Inc.
```


## Example 2

Look up the vendor name for the OUI portion of a MAC address.

```sh
$ ouilookup 000c29
```

output:

```sh
00:0C:29:00:00:00  000C29  VMware, Inc.
```


## Example 3

Look up the vendor name for multiple MAC addresses and OUI portions of MAC addreesses.

```sh
$ ouilookup 000c29 000001.112233 64:4e:d7:00:22:33 64-1B-2F-2A-CC-5E
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
ouilookup -f examples/macs.txt 
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