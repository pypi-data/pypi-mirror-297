# Project Description

Duple is a small package that will find and remove duplicate files.  I created duple only because there is no port of rmlint to Windows.  I suggest using rmlint on unix/linux systems instead - it is far superior to duple.

Duple will iterate through all files and directories that is given and calculate a hash value, hash can be specified.  Then, it groups all of those results into a dictionary with the hashes as the key.  Dictionary entries with 2 or more values constitute a duplicate.  The duplicate that will be kept is specified with an optional flag.  To see the flags and their descriptions:

    duple scan --help

Once the scan is complete, you can review the output file (duple.delete) and modify at your discretion.  Once you have reviewed and modified, run the following command to send the duplicates to the trash:

    duple rm

# Installation
It is strongly recommended to use the latest version of duple.

    pip install duple

or if you need to upgrade:

    pip install duple --upgrade


You may need to add the Python Scripts folder on your computer to the PATH.

## Windows
Open PowerShell (Start > [search for powershell]) and copy/paste the following text to the command line:

    python3 -c "from duple.info import get_user_scripts_path
    get_user_scripts_path()"

Go to Start > [search for 'edit environment variables for your account'] > Users Variables for [user name] > Select Path in top list box > Click Edit...

Once the window pops up, add to the bottom of the list the result from the PowerShell command above

# Usage

duple has two primary sub-commands: scan and rm.  Scan scans your system based on the arguments given to scan and reports those results in output files reported by duple scan.

An Example:

The command below will scan the currenty directory and calculate a hash for each file to determine if there are duplicates:

    duple scan -d . 'sha256'

|Argument|Description|
|--------|-----------|
|-d|specifies the duplicate resolution behavior, in this case, duple will keep the duplicate with the lowest filesystem depth.|
|.|specifies the current directory, to be scanned|
|'sha256'|specifies the hash function to use when duple calculates hashes to determine if files are duplicates|

# Version History
## 1.0.0 Refactored and Improved Output and Reporting
-refactored code to be easier to follow and more modular<br>
-improved reporting of results to duple.delete and duple.json<br>
-improved duple.json output, adding additional data<br>
-added dry run and verbose flags to duple rm<br>
-added hash-stats to calculate performance times for each available hash<br>
-added make-test-files to make test files for the user to learn how duple works on test data<br>
-Improved README for better installation and setup instructions

## 0.5.0 Improve Data Outputs
-added dictionary to duple.json for file stats, now each entry has a key to describe the number<br>
-fixed progress bar for pre-processing directories<br>
-added output file duple.all_files.json with file statistics on all files within the specified path for 'duple scan'<br>
-Improved summary statistics output for 'duple scan'

## 0.4.0 Performance Improvements
-adding multiprocessing, taking advantage of multiple cores<br>
-eliminated files with unique sizes from analysis - files with unique size are not duplicates of another file

## 0.3.0 Added Capability
-added mv function that will move 'duple.delete' paths instead of deleting them

## 0.2.0 Added license
-Added license

## 0.1.1 Misc. Fixes
-Fixed typos in help strings<br>
-Added support for sending duplicates to trash ('duple rm')

## 0.1.0 Initial Release
This is the initial release of duple