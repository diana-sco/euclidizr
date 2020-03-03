import euclidizr
from euclidizr.config import *



mock = euclidizr.input.create_mock(
    n=3,
    half_light_radius=1.0,
    g1 = 0.2,
    g2 = 0.1,
    flux=100.0)

euclidizr.tools.write_image(mock, "test.fits", workdir=workdir)
