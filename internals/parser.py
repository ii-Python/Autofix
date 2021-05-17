# Copyright 2021 iiPython

# Class to represent autorun files
class AutorunFile(object):
    def __init__(self, data: dict = {}):
        self.data = data

    def get(self, key: str):
        if key in self.data:
            return self.data[key]

        return None

# Class to parse autorun files
class Parser(object):
    def __init__(self, autorun_data: str):
        self.autorun_data = autorun_data

    def to_dict(self):

        # Initialize the dictionary
        lines = self.autorun_data.split("\n")
        self.dict = {}

        # Loop through our lines
        for line in lines:

            # Skip whitespace
            if not line.strip():
                continue

            # Skip section lines
            if line[0] == "[" and line[-1] == "]":
                continue

            # Attempt to grab our entries
            try:
                data = line.split("=")

                key = data[0]
                value = data[1]

                # Save to dictionary
                self.dict[key] = value

            # Invalid syntax
            except (ValueError, IndexError):
                pass

        # Send us an object with a .get function
        return AutorunFile(self.dict)
