## MacOS

Install the prerequisites using the instructions on the respective websites.

The program is installed using `python` and the `pip` module. There are no Python dependencies to this program. All code utilizes only the Python standard library.

If you do not wish to install this package to your system, a Python zipapp is included (`.pyz`). If you system has Python installed, the Pyzip zipapp can simply be downloaded and ran. It is located in the `releases` folder or on the github releases page and is named `${script}.pyz`.

Two installation files are included in the `releases` folder or on the github releases page. One is a Python "wheel" file (`.whl`) and the other one is a compressed `tar` file (`.tar.gz`). Either file can install the program, although it is recommended to install the `.whl`. The following are insturctions to install the `.whl`.

Open a `terminal` window.

Install with the following command:

```sh
python3 -m pip install <${script}-{version}-py3-none-{platform}.whl>
```

Python `pip` installs the program, the `man` page, and shell completions.
