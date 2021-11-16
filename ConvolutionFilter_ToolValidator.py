#-------------------------------------------------------------------------------
# Name:        GEOG 567 - Term Project: Convolution Filtering - Tool Validator
# Author:      CW
#
# Created:     Dec 10, 2017
# Purpose:     Input raster dataset to be filtered and output a raster as tif or img
#               1. filters: can select from multiple presets or custom 3x3 or custom 5x5
#               2. convolution: has zero padding included in processing
#               3. Input a raster and then select the band to filter
# Input:        raster dataset filepath
# Output:       raster dataset stored where user specifies in: tif or img
#-------------------------------------------------------------------------------

#NOTE: THIS NEEDS TO BE COPY/PASTED INTO TOOL_VALIDATOR PORTION OF SCRIPT PROPERTIES
#CANNOT BE DIRECTLY LINKED UNLIKE THE SCRIPT

import arcpy
class ToolValidator(object):
  """Class for validating a tool's parameter values and controlling
  the behavior of the tool's dialog."""

  def __init__(self):
    """Setup arcpy and the list of tool parameters."""
    self.params = arcpy.GetParameterInfo()

  def initializeParameters(self):
    """Refine the properties of a tool's parameters.  This method is
    called when the tool is opened."""
    return

  def updateParameters(self):
    """Modify the values and properties of parameters before internal
    validation is performed.  This method is called whenever a parameter
    has been changed."""

    #user inputs raster (filepath)
    raster = self.params[0]

    #user selects raster band
    #if there is more than 1 band, user selects which they want to use
    #if there is only 1 band, will default to that one

    #create describe object
    descR = arcpy.Describe(raster)
    #get list of raster bands in raster
    Rbands = [] #initialize raster bands list
    for Rband in descR.children:
      Rbands.append(Rband.name) #list raster bands

    #Create filter to list bands in that raster - dynamically update script tool interface
    self.params[1].filter.list = Rbands

    #select filter: preset or custom (3x3, 5x5)
    filter = self.params[2].value

    #Enable or disable parameters given the format of the filter
    if filter == "custom - 3x3":
        self.params[3].enabled = True
        self.params[4].enabled = True
        self.params[5].enabled = True
        self.params[6].enabled = False
        self.params[7].enabled = False

    elif filter == "custom - 5x5":
        self.params[3].enabled = True
        self.params[4].enabled = True
        self.params[5].enabled = True
        self.params[6].enabled = True
        self.params[7].enabled = True

    else: #if using preset filter
        self.params[3].enabled = False
        self.params[4].enabled = False
        self.params[5].enabled = False
        self.params[6].enabled = False
        self.params[7].enabled = False

    return

  def updateMessages(self):
    """Modify the messages created by internal validation for each tool
    parameter.  This method is called after internal validation."""
    return