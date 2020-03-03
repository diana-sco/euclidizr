import os
import logging
logger = logging.getLogger(__name__)



def write_image(image, filepath, workdir=None):

    if workdir:
        outpath = os.path.join(workdir, filepath)
    else:
        outpath = filepath

    logger.info("Writing image to {}".format(outpath))

    image.write(outpath)
