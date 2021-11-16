GEOG 567: Term Project
Fall 2017
CW

Further explanation available in description in script tool.
---

Convolution Filtering

Summary:
Image processing or filtering is not easily doable within ArcGIS. 
This tool provides a method of filtering a single band of a raster dataset. 
There are multiple preset filters available. 
Custom filters are also processable with a matrix input by user.


Preset filters: 

Smoothing: Gaussian Blur 3x3

Smoothing: Gaussian Blur 5x5

Sharpen 3x3

Edge Detection: Laplacian 3x3

Outline 3x3

Neighbourhood average 3x3

Unsharp Masking



Custom filters:

custom - 3x3

custom - 5x5


---

Usage

Purpose: Input raster dataset to be filtered and output a raster as tif or img

Filters: can select from multiple presets or custom 3x3 or custom 5x5

Convolution: has zero padding included in processing

Input a raster and then select the band to filter

Input: raster dataset filepath

Output: raster dataset stored where user specifies in: tif or img

