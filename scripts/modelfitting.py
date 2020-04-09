import numpy as np
from astropy.modeling.models import Sersic2D
from astropy.io import fits

def fit_sersic_to_stamp(image):
	im = fits.open(image)
	data = im[0].data
	mod = Sersic2D(amplitude =1, r_eff=1, n=3)
	img = mod(data, data.T)
	
	print(img)
	
	return img

