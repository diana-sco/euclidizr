import os
import logging
logger = logging.getLogger(__name__)
import galsim
import matplotlib.pyplot as plt

def write_image(image, filepath, workdir=None):

    if workdir:
        outpath = os.path.join(workdir, filepath)
    else:
        outpath = filepath

    logger.info("Writing image to {}".format(outpath))

    image.write(outpath)


def read_as_interpolatedimage(filepath, pixelscale, hdu=None):
    """
    Reads a FITS image into a galsim interpolatedImage object
    """

    image = galsim.fits.read(filepath, hdu=hdu)

    int_image = galsim.InterpolatedImage(image, scale=pixelscale)
    return int_image


def draw_image_conv(image, size, pixelscale, filename, workdir):
    """
    Draw a
    """

    im = galsim.Image(size, size, scale=pixelscale)
    im = image.drawImage(image=im)
    im.write(workdir+"/"+filename)
    


def print_image(image, dir_path, file_name):
	
	plt.figure()
	plt.imshow(image, origin='lower')
	plt.savefig(dir_path + file_name + '.png')
