#!python
import sys
import re
import os
import time

sourceFile=sys.argv[1]

# Read the ENTIRE g-code file into memory
with open(sourceFile, "r") as f:
    lines = f.readlines()

if (sourceFile.endswith('.gcode')):
    destFile = re.sub('\.gcode$','',sourceFile)
    try:
        os.rename(sourceFile, destFile+".sqv.bak")
    except FileExistsError:
        os.remove(destFile+".sqv.bak")
        os.rename(sourceFile, destFile+".sqv.bak")
    destFile = re.sub('\.gcode$','',sourceFile)
    destFile = destFile + '.gcode'
else:
    destFile = sourceFile
    os.remove(sourceFile)

inInfill = False

with open(destFile, "w") as of:
    of.write('; Ensure macros are properly setup in klipper\n')
    of.write('_USE_INFILL_SQV\n')
    of.write('_USE_NORMAL_SQV\n')
    for lIndex in range(len(lines)):
        oline = lines[lIndex]
        # print(oline)
        # Parse gcode line
        if oline.startswith(';TYPE:Internal infill'):
            inInfill = True
            of.write(oline)
            of.write('_USE_INFILL_SQV\n')
        elif (oline.startswith(';TYPE:') or oline.startswith('; INIT')) and inInfill:
            inInfill = False
            of.write(oline)
            of.write('_USE_NORMAL_SQV\n')
        else:
            of.write(oline)

of.close()
f.close()
