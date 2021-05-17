# Copyright 2021 iiPython

# Modules
import os
import string

# Base functions
def unix_to_win(path):
    return path.replace("/", "\\")

def locate_drives():
    drives = []

    # Loop through our standard alphabet
    for id_ in string.ascii_uppercase:
        drive_ident = unix_to_win("{}:/".format(id_))

        # Check if drive is connected
        if os.path.exists(drive_ident):
            drives.append(drive_ident)

    # Return our drive list
    return drives
