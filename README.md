---
title: README
author: Todd Wintermute
date: 2025-07-07
---


# _OUI Lookup_ (`ouilookup`)


## Description

View OUI information for provided MAC addresses.

This program uses information from IEEE to display the organization information of registered MAC addresses.

Input MACs or just the OUI portion (first half of the MAC [6 digits]) as arguments and the vendor name is display.

The `oui.csv` file must be downloaded and converted to `oui.json` first. Use the command `ouilookup -d` to obtain this file. It will download the file and also convert it to `oui.json` at the location specified in `ouilookup --help`.

Run `ouilookup` by supplying one or more MACs or OUIs as arguments. You can use just about any format as the input will be automatically converted.

By default, if no arguments are supplied, the script will enter an interactive mode and prompt the user to enter a MAC/OUI.

_OUI Lookup_ (`ouilookup`) is written in _Python_.


## Features

- View the vendor name for each MAC address
- Can supply multiple MACs as arguments
- Can supply either the full MAC address or OUI portion of the MAC as arguments
- MACs can be in various formats


## Installing

See the **`INSTALL`** document for instructions on how to install this program.


## Usage

Use one of the following options to learn how to use this program.


### Manual

The program's command usage and also examples are included in a document named **`MANUAL`** in various formats including pdf, markdown, and html. 

On certain platforms, usage and examples can also be found in the program's **`man`** page. On systems which utilize **`man`** pages, you can view the manual with the command **`man ouilookup`**. 


### Help Option

You can type either **`ouilookup -h`** or **`ouilookup --help`** at the command line interface to see the program's options and usage.


## Examples

For examples see the **`Examples`** section in the **`MANUAL`** document. You can also see examples if you view the **`man`** page for this program.


