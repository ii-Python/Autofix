# Copyright 2021 iiPython

# Modules
import os
import sys
import psutil
from time import sleep
from internals.parser import Parser
from internals.drives import locate_drives

# Metadata
__version__ = "1.0.1"
__author__ = "iiPython"
__license__ = "MIT"
__copyright__ = "Copyright 2021; iiPython"

# Initialization
DRIVES = []  # Prevent an additional call to locate_drives()
if os.name != "nt":
    print("Autofix is for windows only.")
    sys.exit(-1)

print_ = print
def print(*args, **kwargs):
    if sys.argv[0].endswith(".py"):
        print_(*args, *kwargs)

# Handle drives
def drive_attached(drive):
    print("Attached: " + drive)

    # Scan for an autorun.inf file
    autorun = os.path.join(drive, "autorun.inf")
    if not os.path.exists(autorun):
        return

    # Read from it
    try:
        with open(autorun, "r") as file:
            data = file.read()

    except (PermissionError, UnicodeDecodeError):
        return

    # Try to load it
    run = Parser(data).to_dict()
    file = run.get("open")

    crd = os.getcwd()

    if file is not None:

        # Move to drive
        try:
            os.chdir(drive)

        except Exception as error:
            return print("Failed moving to drive: " + str(error))

        # Launch the given file
        if not os.path.exists(file):
            return print("autorun.inf ({}): path '{}' not found".format(drive, file))

        else:
            try:
                os.startfile(file)

            except OSError:
                pass  # Canceled by user

        # Move back to launch dir
        os.chdir(crd)

def drive_detached(drive):
    print("Detached: " + drive)

# Main loop
PROC = psutil.Process(os.getpid())
while True:

    # Rescan drives
    CR_DRVS = locate_drives()
    for CR_DRV in CR_DRVS:
        if CR_DRV not in DRIVES:
            drive_attached(CR_DRV)

    for OD_DRV in DRIVES:
        if OD_DRV not in CR_DRVS:
            drive_detached(OD_DRV)

    DRIVES = CR_DRVS

    # Handle waiting
    PERC = PROC.cpu_percent()
    WAIT = 1
    if PERC < .1:
        WAIT = .1  # Allows us to run faster given we aren't taking up CPU

    try:
        sleep(WAIT)  # Stops us from ripping CPUs

    except KeyboardInterrupt:
        print("Drive daemon stopped.")
        break
