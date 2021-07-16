import numpy as np


def compile_rgb(r, g, b):
    gamma = 2.2
    r = np.power(r, 1 / gamma)
    g = np.power(g, 1 / gamma)
    b = np.power(b, 1 / gamma)

    # Calculate the "True" Green
    g_true = 0.45 * r + 0.1 * g + 0.45 * b
    g_true = np.clip(g_true, 0, 1)  # apply limits again, just in case.

    return np.dstack([r, g_true, b])


def contrast_correction(color, contrast):
    """
    Modify the contrast of an RGB
    See:
    https://www.dfstudios.co.uk/articles/programming/image-programming-algorithms/image-processing-algorithms-part-5-contrast-adjustment/

    Input:
        color    - an array representing the R, G, and/or B channel
        contrast - contrast correction level
    """
    factor = (259*(contrast + 255))/(255.*259-contrast)
    color = factor*(color-.5)+.5
    color = np.clip(color, 0, 1)  # Force value limits 0 through 1.
    return color
