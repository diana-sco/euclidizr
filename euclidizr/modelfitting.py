import numpy as np
from astropy.modeling import models, fitting
from astropy.stats import sigma_clip
from astropy.modeling import Fittable2DModel, Parameter
from scipy.special import gamma, gammaincinv

from astropy.io import fits
import matplotlib.pyplot as plt


def open_image(image):
	im = fits.open(image)
	data = im[0].data

	return data



class EllipSersic2D(Fittable2DModel):
	"""Custom Sersic Model, with ellipticity defined using (g1, g2), and total flux instead of amplitude
	
	This is based on astropy's Sersic2D from here:
	http://docs.astropy.org/en/stable/api/astropy.modeling.functional_models.Sersic2D.html#astropy.modeling.functional_models.Sersic2D
    
    Relations for the total flux:
    http://ned.ipac.caltech.edu/level5/March05/Graham/Graham2.html
    
    Instructions on how to build new models:
    http://docs.astropy.org/en/stable/modeling/new.html
	
	"""
	
	flux = Parameter(default=1.0, min=0.0)
	r_eff = Parameter(default=1.0, min=0.0001, max=100.0)
	n = Parameter(default=4.0, min=0.1, max=6.0)
	x_0 = Parameter(default=0.0)
	y_0 = Parameter(default=0.0)
	g1 = Parameter(default=0.0, min=-1.0, max=1.0)
	g2 = Parameter(default=0.0, min=-1.0, max=1.0)
   
	@staticmethod
	def evaluate(x_array, y_array, flux, r_eff, n, x_0, y_0, g1, g2):
		
		theta = 0.5 * np.arctan2(g2, g1)
		g = np.hypot(g1, g2)
		a, b = r_eff, r_eff*(1-g)/(1+g)
		
		bn = gammaincinv(2.0*n, 0.5)
		flux_n_factor =  n * np.exp(bn) * bn**(-2.0*n) * gamma(2.0*n)
		amplitude = flux / (2.0 * np.pi * flux_n_factor * a * b) # The amplitude from astropy's Sersic2D
		
		cos_theta, sin_theta = np.cos(theta), np.sin(theta)
		x_maj = (x_array - x_0) * cos_theta + (y_array - y_0) * sin_theta
		x_min = -(x_array - x_0) * sin_theta + (y_array - y_0) * cos_theta
		z = np.hypot(x_maj/a, x_min/b)
		
		return amplitude * np.exp(-bn * (z ** (1 / n) - 1))	
		
		
		
		
		
		
def make_a_fit(image, stampsize, ini_flux=None, ini_r_eff=None):
	
        # Do the fit
		
		stamp = image
		weights = np.ones(stamp.shape)
		x_array, y_array = np.meshgrid(np.arange(stampsize), np.arange(stampsize))
		
		

		ini_flux = 1000.0
		ini_r_eff = 10.0
		
		
		
		ini_mod = EllipSersic2D(flux=ini_flux, r_eff=ini_r_eff, n=2.0, x_0=stampsize/2.0, y_0=stampsize/2.0, g1=0.0, g2=0.0)

		
		fitter = fitting.LevMarLSQFitter()
	
		
		fit_mod = fitter(ini_mod, x_array, y_array, stamp, weights=weights, maxiter = 1000, acc=1.0e-7, epsilon=1.0e-6, estimate_jacobian=False)

		plt.figure()
		plt.imshow(fit_mod(x_array, y_array), origin='lower')
		plt.savefig('model.png')
		
		plt.figure()
		plt.imshow(stamp - fit_mod(x_array, y_array), origin='lower')
		plt.savefig('residual.png')

		
		return fit_mod, fitter
	

		



