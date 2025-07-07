## Description

View OUI information for provided MAC addresses.

This program uses information from IEEE to display the organization information of registered MAC addresses.

Input MACs or just the OUI portion (first half of the MAC [6 digits]) as arguments and the vendor name is display.

The `oui.csv` file must be downloaded and converted to `oui.json` first. Use the command `${script} -d` to obtain this file. It will download the file and also convert it to `oui.json` at the location specified in `${script} --help`.

Run `${script}` by supplying one or more MACs or OUIs as arguments. You can use just about any format as the input will be automatically converted.

By default, if no arguments are supplied, the script will enter an interactive mode and prompt the user to enter a MAC/OUI.

_OUI Lookup_ (`${script}`) is written in _Python_.
