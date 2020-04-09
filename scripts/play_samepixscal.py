import euclidizr
from euclidizr.config import *
from euclidizr.convol import conv_with_PSF, decon_with_PSF
import galsim
from euclidizr.modelfitting  import open_image, make_a_fit
import matplotlib.pyplot as plt
import numpy as np
from astropy.io import fits
from euclidizr.summarize_result import summary_result


mock = euclidizr.input.create_mock(
    n=3,
    half_light_radius=1.0, #1.0 in origin or 0.3
    g1 = 0.2,  #0.2
    g2 = 0.1,  #0.1
    flux=100.0)

'''
Import and load data
'''
euclidizr.tools.write_image(mock, "mock_Sers_smal_ell.fits", workdir=workdir)
mock_image = euclidizr.tools.read_as_interpolatedimage(workdir+'/mock_Sers_smal_ell.fits', hst_psf_pixelscale)
mock_image_2 = euclidizr.tools.read_as_interpolatedimage(workdir+'/mock_Sers_smal_ell.fits', hst_psf_pixelscale) 
Euclid_psf=euclidizr.tools.read_as_interpolatedimage(euclid_psf_filepath, euclid_psf_pixelscale, hdu=1)
Hubble_psf=euclidizr.tools.read_as_interpolatedimage(hst_psf_filepath, hst_psf_pixelscale)

'''
Convolution mock image with Euclid PSF and model fitting of convolution image
I also add cosmic shear before convolution
'''
mock_lens = mock_image_2.lens(0.003, 0.005, 1.5)  #add this
Euclid_conv_image = conv_with_PSF(mock_lens, Euclid_psf)
euclidizr.tools.draw_image_conv(Euclid_conv_image, truth_stampsize, truth_pixelscale, "Euclid_conv_imag_t.fits", workdir)
img_convEu = open_image(workdir+'/Euclid_conv_imag_t.fits')
fit_mod_Eu, fitter_Eu = make_a_fit(img_convEu, 256)
#euclidizr.tools.print_image(img_convEu, workdir, '/Euclid_conv_imag_modfit_lens')  #to print the png image



'''
Convolution mock image with HST PSF and model fitting of convolution image
'''
HST_conv_image = conv_with_PSF(mock_image_2, Hubble_psf)
euclidizr.tools.draw_image_conv(HST_conv_image, truth_stampsize, hst_psf_pixelscale, "Hubble_conv_imag_t.fits", workdir)
img_convHST = open_image(workdir+'/Hubble_conv_imag_t.fits')
fit_mod_HST, fitter_HST = make_a_fit(img_convHST, 256)


'''
Deconvolution of convolution image with HST PSF and model fitting of deconvolution image
'''
HST_mock = euclidizr.tools.read_as_interpolatedimage(workdir+'/Hubble_conv_imag_t.fits', hst_psf_pixelscale)
HST_deconv_image = decon_with_PSF(HST_mock, Hubble_psf)
euclidizr.tools.draw_image_conv(HST_deconv_image, truth_stampsize, hst_psf_pixelscale, "Hubble_deconv_imag_t.fits", workdir)
img_deconvHST = open_image(workdir+'/Hubble_deconv_imag_t.fits')
fit_mod_deconHST, fitter_deconHST = make_a_fit(img_deconvHST, 256)


'''
Convolution of deconvolution (HST IMAGE * HST PSF) image with Euclid PSF (time being  we convolve 
again with HST PSF insted od Euclid PSF) and model fitting of convolution image
I also add cosmic shear before convolution
'''
HST_Euclidiz = euclidizr.tools.read_as_interpolatedimage(workdir+'/Hubble_deconv_imag_t.fits', hst_psf_pixelscale)
HST_Euclidiz_lens = HST_Euclidiz.lens(0.003, 0.005, 1.5) #add this
HST_EU = conv_with_PSF(HST_Euclidiz_lens, Euclid_psf)  #Euclid_psf or Hubble_psf
euclidizr.tools.draw_image_conv(HST_EU, truth_stampsize, euclid_psf_pixelscale, "Hubble_Euclidiz_imag_t.fits", workdir)
img_Euclidiz = open_image(workdir+'/Hubble_Euclidiz_imag_t.fits')
fit_mod_Euclidiz, fitter_Euclidiz = make_a_fit(img_Euclidiz, 256)


'''
Print result of model fitting in a dictionary
'''
result_Eu=summary_result(fit_mod_Eu)
result_HST=summary_result(fit_mod_HST)
result_deconHST=summary_result(fit_mod_deconHST)
result_Euclidiz=summary_result(fit_mod_Euclidiz)
f=open(workdir+ '/result_t.txt', 'a')
f.write('Euclid convolution \n'+ str(result_Eu) + '\n'
        'Hubble convolution \n'+ str(result_HST) + '\n'
        'Hubble deconvolution \n' + str(result_deconHST) + '\n'
        'Euclidization \n' + str(result_Euclidiz))

f.close()
