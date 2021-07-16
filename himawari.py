##
# Sourced from Australian NCI
# https://dapds00.nci.org.au/thredds/catalog/rr5/satellite/obs/himawari8/FLDK/catalog.html
#
# Not all files are accessible, but full sized images are available for 2020.
# Default path is at ~/data/himawari | %UserProfile%\data\himawari
#
# Images saved to ~/images
#
# Adapted from Brian Blaylock's work at:
# https://unidata.github.io/python-gallery/examples/mapping_GOES16_TrueColor.html
##
import dateutil.parser
from pathlib import Path
import xarray
import numpy as np
from PIL import Image
import common

FILE_TIMESTAMP = '20191217035000'
FILE_PATTERN = '{}-P1S-ABOM_BRF_B0{}-PRJ_GEOS141_1000-HIMAWARI8-AHI.nc'
B1_FILE = FILE_PATTERN.format(FILE_TIMESTAMP, '1')
B2_FILE = FILE_PATTERN.format(FILE_TIMESTAMP, '2')
B3_FILE = FILE_PATTERN.format(FILE_TIMESTAMP, '3')

B1 = xarray.load_dataset(Path('~').expanduser() / 'data' / 'himawari' / B1_FILE)
B2 = xarray.load_dataset(Path('~').expanduser() / 'data' / 'himawari' / B2_FILE)
B3 = xarray.load_dataset(Path('~').expanduser() / 'data' / 'himawari' / B3_FILE)

time_end = dateutil.parser.isoparse(B1.time_coverage_end)

R = np.squeeze(B3['channel_0003_brf'].data, axis=0)
G = np.squeeze(B2['channel_0002_brf'].data, axis=0)
B = np.squeeze(B1['channel_0001_brf'].data, axis=0)

RGB = common.compile_rgb(R, G, B)

# Amount of contrast
contrast_amount = 5

# Apply contrast correction
RGB_contrast = common.contrast_correction(RGB, contrast_amount)

im = Image.fromarray((RGB_contrast * 255).astype(np.uint8))

Path.mkdir(Path('~').expanduser() / 'images', exist_ok=True)
im.save(Path('~').expanduser() / 'images' / '{}_RGB_{}.jpg'.format(B1.wmo_platform_name, time_end.strftime('%Y-%m-%d_%I.%M.%S_%p_%Z')), quality=95, subsampling=0)
