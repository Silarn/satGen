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
B1_FILE = '20200709012000-P1S-ABOM_BRF_B01-PRJ_GEOS141_1000-HIMAWARI8-AHI.nc'
B2_FILE = '20200709012000-P1S-ABOM_BRF_B02-PRJ_GEOS141_1000-HIMAWARI8-AHI.nc'
B3_FILE = '20200709012000-P1S-ABOM_BRF_B03-PRJ_GEOS141_1000-HIMAWARI8-AHI.nc'

import dateutil.parser
from pathlib import Path
import xarray
import numpy as np
from PIL import Image

B1 = xarray.load_dataset(Path('~').expanduser() / 'data' / 'himawari' / B1_FILE)
B2 = xarray.load_dataset(Path('~').expanduser() / 'data' / 'himawari' / B2_FILE)
B3 = xarray.load_dataset(Path('~').expanduser() / 'data' / 'himawari' / B3_FILE)

time_end = dateutil.parser.isoparse(B1.time_coverage_end)

R = np.squeeze(B3['channel_0003_brf'].data, axis=0)
G = np.squeeze(B2['channel_0002_brf'].data, axis=0)
B = np.squeeze(B1['channel_0001_brf'].data, axis=0)

R = np.clip(R, 0, 1)
G = np.clip(G, 0, 1)
B = np.clip(B, 0, 1)

gamma = 2.2
R = np.power(R, 1/gamma)
G = np.power(G, 1/gamma)
B = np.power(B, 1/gamma)

# Calculate the "True" Green
G_true = 0.45 * R + 0.1 * G + 0.45 * B
G_true = np.clip(G_true, 0, 1)  # apply limits again, just in case.

RGB = np.dstack([R, G_true, B])


def contrast_correction(color, contrast):
    """
    Modify the contrast of an RGB
    See:
    https://www.dfstudios.co.uk/articles/programming/image-programming-algorithms/image-processing-algorithms-part-5-contrast-adjustment/

    Input:
        color    - an array representing the R, G, and/or B channel
        contrast - contrast correction level
    """
    F = (259*(contrast + 255))/(255.*259-contrast)
    COLOR = F*(color-.5)+.5
    COLOR = np.clip(COLOR, 0, 1)  # Force value limits 0 through 1.
    return COLOR


# Amount of contrast
contrast_amount = 5

# Apply contrast correction
RGB_contrast = contrast_correction(RGB, contrast_amount)

im = Image.fromarray((RGB_contrast * 255).astype(np.uint8))

Path.mkdir(Path('~').expanduser() / 'images', exist_ok=True)
im.save(Path('~').expanduser() / 'images' / '{}_RGB_{}.jpg'.format(B1.wmo_platform_name, time_end.strftime('%Y-%m-%d_%I.%M.%S_%p_%Z')), quality=95, subsampling=0)
