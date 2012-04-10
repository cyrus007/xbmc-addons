"""
    Numi - Khoj
    cyrus007
"""
import sys

#plugin constants
__plugin__ = "NUMI Khoj"
__author__ = "cyrus007 <swapan@yahoo.com>"
__url__ = ""
__version__ = "0.2.3"

print "[PLUGIN] '%s: version %s' initialized!" % (__plugin__, __version__)

if __name__ == "__main__":
    import lib.numi as numi
    numi.Main()

sys.modules.clear()
