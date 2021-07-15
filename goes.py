##
# GOES RGB image compiler
# Automatically downloads data files based on a target date & time
#
# Data is saved to ~/data/ | %UserProfile%\data\
#
# Images saved to ~/images
#
# Significantly sourced from Brian Blaylock's example:
# https://unidata.github.io/python-gallery/examples/mapping_GOES16_TrueColor.html
##

from datetime import datetime
import dateutil.parser
from pathlib import Path
import xarray
import numpy as np
from PIL import Image
import goes2go.data as g2g

file = g2g.goes_nearesttime(
    attime=datetime(year=2020, month=8, day=20, hour=16, minute=30),  # set desired date after ~2016
    satellite='goes16',  # goes16 (East) or goes17 (West)
    product='ABI',
    domain='F',
    return_as='filelist'
)

file = Path('~').expanduser() / 'data' / file.at[0, 'file']

F = xarray.load_dataset(file)

file_created = dateutil.parser.isoparse(F.date_created)

R = F['CMI_C02'].data
G = F['CMI_C03'].data
B = F['CMI_C01'].data

R = np.clip(R, 0, 1)
G = np.clip(G, 0, 1)
B = np.clip(B, 0, 1)

gamma = 2.2
R = np.power(R, 1/gamma)
G = np.power(G, 1/gamma)
B = np.power(B, 1/gamma)

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
im.save(Path('~').expanduser() / 'images' / '{}_{}_RGB_{}.jpg'.format(F.orbital_slot, F.scene_id.replace(' ', '_'), file_created.strftime('%Y-%m-%d_%I.%M.%S_%p_%Z')), quality=95, subsampling=0)
