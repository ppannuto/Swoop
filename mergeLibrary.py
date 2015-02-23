#!/usr/bin/env python
import argparse
from EagleUtil import *
from HighEagle import *
import sys
import re
import shutil

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Merge library into an eagle file")
    parser.add_argument("--src", required=True,  type=str, nargs=1, dest='src', help="libraries to merge into the other file")
    parser.add_argument("--dst", required=True,  type=str, nargs=1, dest='dst', help="the other file (sch, lbr, or pcb)")
    args = parser.parse_args()

    m = re.match("(.*\.(lbr|sch|pcb))(:(.+))?", args.src[0])
    if m is None:
        raise HighEagleError("Unparsable file name: '" + args.src[0] + "'")

    f = m.group(1)
    srcLib = m.group(4)
    suffix=m.group(2)

    if suffix == "sch":
        src = Schematic.from_file(f)
        srcLib = dst.get_library(srcLib)
    elif suffix == "brd":
        raise NotImplementedError("brd files not supported yet")
    elif suffix == "lbr":
        src = LibraryFile.from_file(f)
        srcLib = src.get_library()
    else:
        raise Exception("File with unknown suffix: " + suffix);    

    ####################################################################

    m = re.match("(.*\.(lbr|sch|pcb))(:(.+))?", args.dst[0])

    if m is None:
        raise HighEagleError("Unparsable file name: '" + args.dst[0] + "'")

    f = m.group(1)
    dstLibName = m.group(4)
    suffix=m.group(2)

    shutil.copy(f, f + ".bak")

    dst = EagleFile.from_file(f)
    
    if isinstance(dst, Schematic):
        dstLib = dst.get_library(dstLibName)
        if dstLib is None:
            newLib = Library(name=dstLibName)
            dst.add_library(newLib)
            dstLib = newLib
            
#    elif isinstance(dst, Board):
#        raise NotImplementedError("brd files not supported yet")
    elif isinstance(dst, LibraryFile):
        dstLib = dst.get_library()
    else:
        raise HighEagleError("Unknown type returned from EagleFile.from_file()")

    for i in srcLib.symbols.values():
        dstLib.add_symbol(i.clone())

    for i in srcLib.packages.values():
        dstLib.add_package(i.clone())

    for i in srcLib.devicesets.values():
        dstLib.add_deviceset(i.clone())

    
        
    dst.write(f)
