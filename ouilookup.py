#!/usr/bin/env python3
"""
This program takes one or more MAC addresses and returns the Org Name.
It uses information from `https://standards-oui.ieee.org/oui/oui.csv`.
"""

__module__ = 'ouilookup'
__script__ = 'ouilookup'
__author__ = 'Todd Wintermute'
__version__ = '0.0.5'
__date__ = '2025-07-06'
__info__ = (
    'Tool to obtain vendor name / organizationally unique identifier (OUI) '
    'for MAC addresses'
    )

import argparse
import csv
import datetime
import importlib.resources
import json
import os
import pathlib
import re
import shlex
import string
import sys
import urllib.request


def get_config_location():
    """Return the location of the user config directory per platform"""
    if sys.platform == 'win32':
        appdata_dir = pathlib.Path(os.getenv('APPDATA'))
        conf_dir = appdata_dir / __script__
    else:
        home_dir = pathlib.Path.home()
        conf_dir = home_dir / '.local' / 'share' / __script__
    if not all([conf_dir.exists(),conf_dir.is_dir()]):
        conf_dir.mkdir(parents=True, exist_ok=True)
    return conf_dir


_user_config_dir = get_config_location()
_user_csv_file = _user_config_dir / 'oui.csv'
_user_json_file = _user_config_dir / 'oui.json'
_ieee_csv_url = "https://standards-oui.ieee.org/oui/oui.csv"
_ieee_txt_url = "https://standards-oui.ieee.org/oui/oui.txt"


def completion_parse_arguments():
    """Create command line arguments for shell completion"""
    completion_parser = argparse.ArgumentParser(add_help=False)
    completion_group = completion_parser.add_argument_group(
        title='shell completion options',
        )
    completion_group.add_argument(
        '--completion',
        choices=['bash', 'zsh', 'fish'],
        help=f"print {__script__} shell completion to the terminal and exit",
        )
    return completion_parser


def download_parser_arguments():
    """Create command line arguments for download option"""
    download_parser = argparse.ArgumentParser(add_help=False)
    download_group = download_parser.add_argument_group(
        title='download IEEE OUI file',
        )
    download_group.add_argument(
        '--download',
        '-d',
        action='store_true',
        help=(
            f"download the IEEE OUI file `oui.csv` and save to "
            f"`{{HOME}}/.local/share/{__script__}` on Linux or "
            f"`{{APPDATA}}\\{__script__}` on Windows as `oui.csv`. "
            f"Also convert CSV to JSON and save as `oui.json`"
            ),
        )
    return download_parser


def file_parser_arguments():
    """Create command line argument for file input option"""
    file_parser = argparse.ArgumentParser(add_help=False)
    file_parser.add_argument(
        '-f',
        '--file',
        type=pathlib.Path,
        nargs=1,
        action='extend',
        default=[],
        metavar='FILE',
        dest='files',
        help="use a file with one MAC address per line.",
        )
    file_parser.add_argument(
        '--pipe',
        action='store_const',
        const=None if sys.stdin.isatty() else sys.stdin,
        default=None if sys.stdin.isatty() else sys.stdin,
        help=argparse.SUPPRESS, # Hidden
        )
    return file_parser


def parse_arguments():
    """Create command line arguments and auto generated help"""
    compl_parser = completion_parse_arguments()
    compl_args, ukwn_args = compl_parser.parse_known_args()
    completion = compl_args.completion
    dl_parser = download_parser_arguments()
    dl_args, dl_ukwn_args = dl_parser.parse_known_args()
    download = dl_args.download
    file_parser = file_parser_arguments()
    file_args, file_ukwn_args = file_parser.parse_known_args()
    files = file_args.files
    pipe = file_args.pipe
    parser = argparse.ArgumentParser(
        prog=__script__,
        description=__doc__,
        parents=[file_parser, dl_parser, compl_parser],
        epilog = 'Have a great day!',
        )
    parser.add_argument(
        '--version',
        '-v',
        help='show the version number and exit',
        action='version',
        version=f"Version: %(prog)s  {__version__}  ({__date__})",
        )
    parser.add_argument(
        '--quiet',
        '-q',
        default=False,
        action='store_true',
        help=f"suppress warning messages when MAC is not found to be valid",
        )
    mac_optional = any([completion, download, files, pipe, not ukwn_args])
    parser.add_argument(
        'macs',
        nargs=('*' if mac_optional else '+'),
        metavar='MAC',
        action='extend',
        default=[],
        help=(
            f"the full MAC address or the OUI portion (first 6 hex digits). "
            f"If providing multiple items, separate each MAC/OUI with a "
            f"space. Within the MAC/OUI separating characters such as "
            f"`:`, `-`, or `.` are allowed at any interval. "
            f"Examples: 74:13:ea:9a:22:2e 28-EA-0B-6C-A9-E5 "
            f"b4df.9181.7fb1 e073e7-ec3802 080030"
            ),
        )
    return parser


def print_completion(shell):
    """Read a completion file and print the output"""
    resource = f"shell-completions/{shell}/{__script__}"
    completions = importlib.resources.files(__module__).joinpath(resource)
    if completions.exists():
        print(completions.read_text())
        return True
    else:
        print('Completions file not found')
        return False


def remove_separators(mac):
    """Takes a hex MAC str.
    Returns string with removed separating and white space characters.
    """
    xmac = re.sub(rf"[^{string.hexdigits}]", r'', mac)
    return xmac


def std_mac_format(mac, sep=':'):
    """Takes a hex MAC str. Returns string with separators."""
    strmac = f"{sep}".join(
        re.findall(r'.{1,2}', rf"{remove_separators(mac):0>12}")
        )
    return strmac


def std_oui_format(oui, sep=':'):
    """Takes a hex OUI str. Returns string with separators."""
    stroui = f"{sep}".join(
        re.findall(r'.{1,2}', rf"{remove_separators(oui):0>6}")
        )
    return stroui


def is_mac(mac):
    """Takes a hex MAC str. Validates it is a MAC."""
    xmac = remove_separators(mac)
    if not all([(char in string.hexdigits) for char in xmac]):
        return False
    if len(xmac) != 12:
        return False
    intmac = int(xmac, base=16)
    if intmac < 0 or intmac > 0xffffffffffff:
        return False
    return True


def is_oui(oui):
    """Takes a hex OUI str. Validates it is on OUI"""
    xoui = remove_separators(oui)
    if not all([char in string.hexdigits for char in xoui]):
        return False
    if len(xoui) != 6:
        return False
    intoui = int(xoui, base=16)
    if intoui < 0 or intoui > 0xffffff:
        return False
    return True


def get_oui_from_mac(mac):
    """Takes a hex MAC str. Returns OUI portion w/o separators."""
    oui = remove_separators(mac)[:6]
    return oui


def get_oui_as_mac(oui):
    """Takes a hex OUI str. Returns MAC using zeros w/o separators"""
    strmac = f"{remove_separators(oui):0<12}"
    return strmac


def find_oui_org(oui, oui_dict):
    """Takes a hex OUI str. Returns organization name if found."""
    oui = oui.upper()
    if (org_name := oui_dict.get(oui)):
        return org_name
    return 'unknown'


def find_mac_org(mac):
    """Takes a hex MAC str. Returns organization name if found."""
    oui = get_oui_from_mac(mac)
    mac_org = find_oui_org(oui)
    return mac_org


def download_file(url, dest):
    """Download file at URL to the specified destination"""
    print(f"Downloading `{url}` to: `{dest}`")
    try:
        req = urllib.request.urlopen(url, None, 5) # 5s timeout
        dat = req.read()
    except:
        print(f"Error while downloading `{url}`.")
        return False
    print('Download complete.')
    bytesw = dest.write_bytes(dat)
    if not bytesw:
        print(f"No data received.")
        print('Bye.')
        return False
    print(f"Bytes downloaded: {bytesw:,}")
    return True


def download_ieee_oui_csv():
    """Download the IEEE OUI file to user config dir"""
    if not _user_config_dir.exists():
        _user_config_dir.mkdir(parents=True, exist_ok=True)
    if _user_csv_file.exists():
        from_time_stamp = datetime.datetime.fromtimestamp
        mtime = from_time_stamp(_user_csv_file.stat().st_mtime)
        now = datetime.datetime.now()
        one_day = datetime.timedelta(days=1)
        if (now - mtime) < one_day:
            warning = 'RA assignment downloads are limited to one per day.'
            print(f"[ERROR] Please try again later. Per IEEE: {warning}")
            print(f"  Last download at: {mtime.replace(microsecond=0)}")
            remain = one_day - (now - mtime)
            remain -= datetime.timedelta(microseconds=remain.microseconds)
            print(f"  Next download in: {remain}")
            return False
    if not download_file(_ieee_csv_url, _user_csv_file):
        return False
    return True


def read_csv_to_list_of_dicts(file, fieldnames=None):
    """Reads the CSV file and returns the data in a list of dicts"""
    if isinstance(file, str):
        file = pathlib.Path(file)
    with file.open(encoding='utf-8') as f:
        csv_reader = csv.DictReader(f, fieldnames=fieldnames)
        if fieldnames:
            csv_header = next(csv_reader)
        csv_data = list(csv_reader)
    return csv_data


def convert_csv_to_oui_dict(csv_file):
    """Convert an OUI CSV to a dict of oui: org key value pairs"""
    data = read_csv_to_list_of_dicts(csv_file)
    csv_header = (
        'Registry','Assignment','Organization Name','Organization Address',
        )
    oui_dict = {}
    for row in data:
        oui = row['Assignment']
        org = row['Organization Name']
        if oui not in oui_dict:
            oui_dict.update({oui: org})
        elif isinstance(oui_dict.get(oui), str):
            value = [oui_dict[oui], org]
            oui_dict.update({oui: value})
        elif isinstance(oui_dict.get(oui), list):
            value = oui_dict[oui] + [org]
            oui_dict.update({oui: value})
        else:
            oui_dict.update({oui: org})
    return oui_dict


def read_json_file(file):
    """Takes a pathlib file obj. Returns a default json obj"""
    if isinstance(file, str):
        file = pathlib.Path(file)
    if (j := file).exists():
        jsonobj = json.load(j.open(encoding='utf-8'))
    else:
        jsonobj = {}
    return jsonobj


def write_json_file(jsonobj,file):
    """Takes a json obj and a pathlib file. Writes json obj to file.
    Returns the number of bytes written.
    """
    if isinstance(file, str):
        file = pathlib.Path(file)
    numbytes = file.write_text(json.dumps(jsonobj, indent=1))
    return numbytes


def convert_user_csv_file_to_user_json_file():
    """Converts a CSV list of dicts and then saves to JSON file"""
    print(f"Converting '{_user_csv_file}' to '{_user_json_file}'...")
    ouis_dict = convert_csv_to_oui_dict(_user_csv_file)
    numbytes = write_json_file(ouis_dict, _user_json_file)
    if not numbytes:
        print(f"There was an error saving file '{_user_json_file}'")
        return False
    print(f"Success. Wrote {numbytes} bytes to '{_user_json_file}'")
    return True


def check_user_data_files():
    """Verify user files exist. Convert CSV to JSON is possible"""
    if _user_csv_file.exists() and not _user_json_file.exists():
        print(f"Can not find file {_user_json_file}")
        print(f"Found source file {_user_csv_file}.")
        if not convert_user_csv_file_to_user_json_file():
            return False
    if not _user_json_file.exists():
        print(
            f"[ERROR]: Could not read OUI data.`{_user_json_file}`.\n"
            f"Use the `--download` option and try again."
            )
        return False
    return True


def read_stdin_to_list(stdin):
    """Input a stdin file obj. Return list of lines"""
    with stdin as f:
        data = [line.strip() for line in f]
    return data


def read_file_to_list(file=None, quiet=False):
    """Input a pathlib file obj. Return list of lines"""
    if not file:
        return False
    elif isinstance(file, str):
        file = pathlib.Path(file)
    if not file.exists():
        if not quiet:
            print(f"Could not open file: `{file}`")
        return False
    elif not file.stat().st_size:
        if not quiet:
            print(f"[WARNING]: No data found in file: `{file}`")
        return False
    else:
        with file.open(encoding='utf-8') as f:
            data = [line.strip() for line in f]
    return data


def strip_list_items(a_list):
    """Convert the list or file obj to usable format"""
    data = [i.strip() for i in a_list]
    return data


def display_report(macs, quiet=False):
    """Display the table after validating OUIs and MACs"""
    ouis_dict = read_json_file(_user_json_file)
    if not ouis_dict:
        print(f"Could not read {_user_json_file}")
        return False
    for mac in macs:
        if is_oui(mac):
            ieee_oui, std_mac = (
                std_oui_format(mac, sep='').upper(),
                std_mac_format(get_oui_as_mac(mac), sep=':').upper(),
                )
        elif is_mac(mac):
            ieee_oui, std_mac = (
                std_oui_format(get_oui_from_mac(mac), sep='').upper(),
                std_mac_format(mac, sep=':').upper(),
                )
        else:
            if not quiet:
                print(f"[WARNING]: Not a valid MAC/OUI address: `{mac}`")
            continue
        vendor = find_oui_org(ieee_oui, ouis_dict)
        if not vendor:
            # Should not reach this. Lookups should always return 'unknown'
            print('Vendor not found for: {std_mac}')
            return False
        print(f"{std_mac}  {ieee_oui}  {vendor}")
    return True


def interactive_mode():
    """Enter an interactive mode if no arguments are supplied"""
    parser = parse_arguments()
    parser_help = '\n\n'.join(parser.format_help().split('\n\n')[1:-2])
    interactive_help = "description:\n  " + parser_help + (
        '\n\n'
        'interactive commands:\n'
        f"  {'help':<20}  show this message again\n"
        f"  {'quit':<20}  exit program\n"
        )
    if not check_user_data_files():
        parser.print_usage()
    print("\nEnter MAC/OUI and/or options, 'h' for help, 'q' to quit")
    reply = shlex.split(input(f"{__script__}> "))
    if not reply:
        return True
    elif reply[0].lower().startswith('q'):
        print('Bye!')
        return False
    elif reply[0].lower().startswith('h'):
        print(interactive_help)
        return True
    args = parser.parse_args(reply)
    if args.download:
        if not (download_ieee_oui_csv()
                and convert_user_csv_file_to_user_json_file()):
            # Return True restarts interactive mode. False exits prog.
            return True
    macs = args.macs.copy()
    for file in args.files:
        macs_file = read_file_to_list(file, args.quiet)
        if macs_file:
            macs.extend(macs_file)
    macs = strip_list_items(macs)
    result = display_report(macs, args.quiet)
    return True


def main():
    """Start of main program"""
    parser = parse_arguments()
    args = parser.parse_args()
    if (shell := args.completion):
        retval = print_completion(shell)
        return True
    if not any([args.macs, args.files, args.pipe, args.download]):
        while interactive_mode():
            continue
        else:
            return True
    if args.download:
        if not (download_ieee_oui_csv()
                and convert_user_csv_file_to_user_json_file()):
            sys.exit(1)
    if not check_user_data_files():
        parser.print_usage()
        sys.exit(1)
    macs = args.macs.copy()
    if args.pipe:
        macs_pipe = read_stdin_to_list(args.pipe)
        macs.extend(macs_pipe)
        ## below: reset stdin non-interactive session to interactive again
        #sys.stdin = open(os.ttyname(sys.stdout.fileno()))
    for file in args.files:
        macs_file = read_file_to_list(file, args.quiet)
        if macs_file:
            macs.extend(macs_file)
    macs = strip_list_items(macs)
    result = display_report(macs, args.quiet)


if __name__ == '__main__':
    main()
