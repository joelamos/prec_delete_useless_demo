#prec_delete_useless_demo
This program is to be used in conjunction with the Team Fortress 2 recording tool, [P-REC](https://bitbucket.org/olegko/p-rec/wiki/Home). The `pre_delete_useless-demo 1` command doesn't always work as expected, especially on public servers. This program checks `Killstreaks.txt` and deletes your useless TF2 demos. Any demos not in `Killstreaks.txt` **will be deleted**.

##Program arguments
If you are running the program using a `.py` or console `.exe`file, you can use `-h` for help, `-p` to specify the path to your demos folder, and `-d` (no parameter) to indicate that you only wish to delete demos with filenames containing P-REC's date format. Running the program with no arguments will run the GUI version.

## Installation
### Windows
Download the zip file [here](https://github.com/joelamos/prec_delete_useless_demo/releases/download/v1.1/UselessDemoDeleter.v1.1.zip), which contains two exes: `demo-deleter-gui.exe` and `demo-deleter-console.exe`. Use the former for a windowed experience and the latter with the command prompt (see `Program arguments` above).

If you experience problems, follow the instructions below.

###Mac and Linux
Install python. Download and extract the source zip file. Run the python file (see `Program arguments` above).
