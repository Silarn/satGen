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
import common

file = g2g.goes_nearesttime(
    attime=datetime(year=2021, month=7, day=15, hour=20, minute=0),  # set desired date after ~2016
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

RGB = common.compile_rgb(R, G, B)

# Amount of contrast
contrast_amount = 5

# Apply contrast correction
RGB_contrast = common.contrast_correction(RGB, contrast_amount)

im = Image.fromarray((RGB_contrast * 255).astype(np.uint8))

Path.mkdir(Path('~').expanduser() / 'images', exist_ok=True)
im.save(Path('~').expanduser() / 'images' / '{}_{}_RGB_{}.jpg'.format(F.orbital_slot, F.scene_id.replace(' ', '_'), file_created.strftime('%Y-%m-%d_%I.%M.%S_%p_%Z')), quality=95, subsampling=0)
