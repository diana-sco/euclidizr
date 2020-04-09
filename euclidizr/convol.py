"""
Functions for convolutions and deconvolutions
"""

from . import config
import galsim


def conv_with_PSF(image, psf):
    """
    image is a Galsim.image object
    psf is a Galsim.interpolatedImage object
    """
    Euclid_image = galsim.Convolve([image, psf])

    return Euclid_image



def decon_with_PSF(image, psf):
    """
    image is a Galsim.image object
    psf is a Galsim.interpolatedImage object
    """
    HST_inv_psf = galsim.Deconvolve(psf)
    deconv_HST_image = galsim.Convolve(HST_inv_psf, image)

    return deconv_HST_image
