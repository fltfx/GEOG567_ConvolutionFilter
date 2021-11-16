#-------------------------------------------------------------------------------
# Name:        GEOG 567 - Term Project: Convolution Filtering - MAIN
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

#import libraries needed
import arcpy #import arcpy site package
import os #import os library to be able to modify filenames
from scipy import signal #import for the convolution
import numpy as np #import to use for scipy
import sys #for stopping the program completely when errors found


################################################################################
################################################################################

#step 1: user to input raster
#test case: user doesn't enter in a raster but enters in another file, caught by interface
raster_filepath = arcpy.GetParameterAsText(0) #get filepath for raster
raster = arcpy.Raster(raster_filepath) #create raster from raster filepath

################################################################################
################################################################################

#step 2: select band
#accomplished through ToolValidator
bandname = arcpy.GetParameterAsText(1) #get name of the band
band = os.path.join(raster_filepath,bandname) #create the filepath of the raster band using raster filepath and bandname

################################################################################
################################################################################

#step 3: select filter - preset or custom 3x3 or custom 5x5
filter = arcpy.GetParameterAsText(2) #get the name of the filter
input_matrix = [] #initiate matrix (list of lists) to store custom (3x3 or 5x5) filter

################################################################################

#create kernels for custom filters
#if custom 3x3
if (filter == "custom - 3x3"):
    size=3 #set the size variable, used later for testing
    #get each row of kernel as a string
    first_row = arcpy.GetParameterAsText(3)
    second_row = arcpy.GetParameterAsText(4)
    third_row = arcpy.GetParameterAsText(5)
    #store string inside the matrix
    input_matrix.append(first_row)
    input_matrix.append(second_row)
    input_matrix.append(third_row)

#if custom 5x5
if (filter == "custom - 5x5"):
    size=5 #set the size variable, used later for testing
    #get each row of kernel as a string
    first_row = arcpy.GetParameterAsText(3)
    second_row = arcpy.GetParameterAsText(4)
    third_row = arcpy.GetParameterAsText(5)
    fourth_row = arcpy.GetParameterAsText(6)
    fifth_row = arcpy.GetParameterAsText(7)
    #store string inside the matrix
    input_matrix.append(first_row)
    input_matrix.append(second_row)
    input_matrix.append(third_row)
    input_matrix.append(fourth_row)
    input_matrix.append(fifth_row)

################################################################################

#initialize kernel to hold the filter/mask (which is currently inside input_matrix)
kernel = []

#check if custom 3x3 or custom 5x5 is correct matrix size and if full of numbers only
#input custom parameters into kernel
if (filter == "custom - 3x3") or (filter == "custom - 5x5"):
    for each_row in input_matrix:
        each_row_list = each_row.split(",") #seperate string into multiple strings by ","
        #test case 1: user enters in a matrix that's not 3x3 or not 5x5
        if len(each_row_list) <> size:
            arcpy.AddError(
                "\n" + "An error occurred while checking the matrix. Please try re-entering the matrix in the correct format. It is likely an issue with the size of the matrix." + "\n")
            sys.exit() #stop if there's a mistake in user input

        #test case 2: user enters letter/symbol (note: *solely* a space instead a number counts as a symbol here, ex: "1, ,1") instead of number in matrix
        for j in range(0, len(each_row_list)): #note: range goes to second parameter but NOT including (so no need to -1)
            try:
                each_row_list[j] = float(each_row_list[j])  #to remove any spaces in case user added spaces like "1, 0, 1" instead of "1,0,1" and convert from string to float
            except:
                arcpy.AddError(
                "\n" + "An error occurred while checking the matrix. Please try re-entering the matrix in the correct format. It is likely an issue with entering a character/symbol instead of a number" + "\n")
                sys.exit()
        #matrix passes test case 1 and 2
        kernel.append(each_row_list) #input custom parameters into kernel

################################################################################

#create kernels for preset filters:
#   https://en.wikipedia.org/wiki/Kernel_(image_processing)
#   http://setosa.io/ev/image-kernels/

if (filter == "Smoothing: Gaussian Blur 3x3"):
    kernel = [[1,2,1], [2,4,2], [1,2,1]]
    for i in range (0,3): #note: range goes to second parameter but NOT including,so need to +1 to 2nd parameter
        for j in range (0,3):
            kernel[i][j] = float(kernel[i][j])*(1.0/16.0) #do not forget 1/2=0 while 1.0/2.0=0.5, ensure divides properly

if (filter == "Smoothing: Gaussian Blur 5x5"):
    kernel = [[1,4,6,4,1], [4,16,24,16,4], [6,24,36,24,6], [4,16,24,16,4], [1,4,6,4,1]]
    for i in range(0, 5): #note: range goes to second parameter but NOT including,so need to +1 to 2nd parameter
        for j in range(0, 5):
            kernel[i][j] = float(kernel[i][j]) * (1.0 / 256.0) #do not forget 1/2=0 while 1.0/2.0=0.5, ensure divides properly

if (filter == "Sharpen 3x3"):
    kernel = [[0,-1,0], [-1,5,-1], [0,-1,0]]

if (filter == "Edge detection: Laplacian 3x3"):
    kernel = [[0,1,0], [1,-4,1], [0,1,0]]

if (filter == "Outline 3x3"):
    kernel = [[-1,-1,-1], [-1,8,-1], [-1,-1,-1]]

if (filter == "Neighbourhood average 3x3"):
    kernel = [[1,1,1], [1,1,1], [1,1,1]]
    for i in range (0,3): #note: range goes to second parameter but NOT including,so need to +1 to 2nd parameter
        for j in range (0,3):
            kernel[i][j] = float(kernel[i][j])*(1.0/9.0) #do not forget 1/2=0 while 1.0/2.0=0.5, ensure divides properly

if (filter == "Unsharp masking 5x5"):
    kernel = [[1,4,6,4,1], [4,16,24,16,4], [6,24,-476,24,6], [4,16,24,16,4], [1,4,6,4,1]]
    for i in range(0, 5): #note: range goes to second parameter but NOT including,so need to +1 to 2nd parameter
        for j in range(0, 5):
            kernel[i][j] = float(kernel[i][j]) * (-1.0 / 256.0) #do not forget 1/2=0 while 1.0/2.0=0.5, ensure divides properly

################################################################################
################################################################################

#step 4: filter raster band (convolve image/raster band with kernel)

# get dimensions of the raster, should be same as each band
rCols = arcpy.GetRasterProperties_management(raster, 'COLUMNCOUNT') #number of cols, not indexes
rRows = arcpy.GetRasterProperties_management(raster, 'ROWCOUNT') #number of rows, not indexes
#rCols/rRows in "result" format, need to use .getOutput to convert to string, then convert to int
rCols = int(rCols.getOutput(0))
rRows = int(rRows.getOutput(0))

#convert kernel to np.array
kernel_np = np.array(kernel)

#convert raster band image to np.array
lowerLeft = arcpy.Point(raster.extent.XMin , raster.extent.YMin) #set lower left corner value to get origin of raster
cellSize = raster.meanCellWidth
band_np = arcpy.RasterToNumPyArray(band,nodata_to_value=0) #use band filepath here from step2

#convolve image with kernel with zero padding on the image
kernel_np = kernel_np[::-1, ::-1] #mirror kernel, this is part of the theory behing convolution
outband_np = signal.convolve2d(band_np, kernel_np, mode='same', boundary='fill', fillvalue=0) #convolve

################################################################################
################################################################################

#step 5: output raster band results to new layer

#Convert Array to raster (keep the origin and cellsize the same as the input)
outband = arcpy.NumPyArrayToRaster(outband_np,lowerLeft,cellSize,value_to_nodata=0)
outband_filepath = arcpy.GetParameterAsText(8) #get filepath for output raster
outband.save(outband_filepath) #save output raster
arcpy.AddMessage("\n" + "The filtered raster is saved at: " + str(outband_filepath) + "\n")
