#
# Cura PostProcessingPlugin
# Author:   Jérôme Wiedemann
# Date:     November 24 2021
# Modified: November 24 2021 Initial Version
#
# Description:  This script modifies the Square Corner Velocity only for the Sparse Infill.
#               It will massively accelerate the gyroid infill print speed.
#               It only works with Klipper with specific macro configured
#
from ..Script import Script
from UM.Application import Application

GCODE_NORMAL_SQV = "_USE_NORMAL_SQV"
GCODE_INFILL_SQV = "_USE_INFILL_SQV"

class FastGyroidInfill(Script):

    def __init__(self):
        super().__init__()

    def getSettingDataString(self):
        return """{
            "name": "Faster Gyroid Infill with Klipper",
            "key": "FastGyroidInfill",
            "metadata": {},
            "version": 2,
            "settings": {}
        }"""

    def execute(self, data):
        inInfill = False
        init = False
        for layerIndex, layer in enumerate(data):
            if layerIndex == 0 and not init:
                layer += "; Ensure Macros are setup in Klipper\n" + GCODE_INFILL_SQV + "\n" + GCODE_NORMAL_SQV + "\n"
                init = True
            lines = layer.split("\n")
            for lineIndex, line in enumerate(lines):
                if line.startswith(";TYPE:FILL"):
                    lines.insert(lineIndex + 1, GCODE_INFILL_SQV)
                    inInfill = True
                elif (line.startswith(";TYPE") or line.startswith(";LAYER:")) and inInfill:
                    lines.insert(lineIndex + 1, GCODE_NORMAL_SQV)
                    inInfill = False

            data[layerIndex] = "\n".join(lines)

        return data
