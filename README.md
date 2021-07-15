# satGen
Python scripts to fetch and / or composite RGB imagery from raw satellite data.

### Dependencies
Ensure the following python packages are installed

All:
* xarray - Data file reader
* netCDF4 - Data format support for netCDF data
* numpy - Provides core data array functionality
* PIL - Image processing and saving

GOES:
* goes2go - Utility to download GOES data files

### Usage
The scripts do not currently take arguments. You will need to manually modify the values
near the top of the scripts in order to set the target image data files or change the
output locations.

Simply run the scripts to fetch and generate the image files for the desired satellite data.

### Todo
Package the scripts to allow for an interface with parameters so editing code isn't necessary.

### Author
Jeremy Rimpo

### Credits
[Brian Blaylock](http://home.chpc.utah.edu/~u0553130/Brian_Blaylock/home.html) -
Much of the
image processing code was sourced from his [GOES-16: True Color Recipe](https://unidata.github.io/python-gallery/examples/mapping_GOES16_TrueColor.html) document / scripts.

### License
MIT