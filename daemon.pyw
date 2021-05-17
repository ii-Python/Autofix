import os
import sys
import subprocess

subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), "daemon.py")], shell = True)
