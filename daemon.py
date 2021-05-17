# Copyright 2021 iiPython

# Modules
import os
import psutil
from time import sleep
from internals.parser import Parser
from internals.drives import locate_drives

# Metadata
__version__ = "1.0.0"
__author__ = "iiPython"
__license__ = "MIT"
__copyright__ = "Copyright 2021; iiPython"

# Initialization
DRIVES = []  # Prevent an additional call to locate_drives()

# Handle drives
def drive_attached(drive):
    print("Attached: " + drive)

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
