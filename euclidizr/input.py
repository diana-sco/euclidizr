"""
Functions that create input data for tests (real or parametric galaxies)
"""

import galsim
from . import config

import logging
logger = logging.getLogger(__name__)


def create_mock(g1=0.0, g2=0.0, **kwargs):
    """
    Creates a galaxy image for tests
    Returns a galsim image object
    """

    image = galsim.ImageF(config.truth_stampsize, config.truth_stampsize)

    gal = galsim.Sersic(**kwargs)
    gal = gal.shear(g1=g1, g2=g2)

    gal.drawImage(image=image, scale=config.truth_pixelscale)
    logger.info("Created mock image {}".format(str(image)))

    return image
