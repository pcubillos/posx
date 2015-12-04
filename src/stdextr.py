import numpy as np
import scipy.interpolate as si

import tools

def stdextr(data, x1, x2, variance=None, mask=None, interp=False):
  """
  Standard box extraction of spectrum.  Step 4 of Horne (1989).

  Parameters:
  -----------
    data:  2D float ndarray
        Sky-subtracted spectrum image of shape [nwavelength, nposition].
    x1:  Integer
        Left X boundary of region to extract the spectrum.
    x2:  Integer
        Right X boundary of region to extract the spectrum.
        Note that:  0 <= x1 <= x2 <= nx
    variance:  2D float ndarray
        Variance image from processed image.
    mask:  2D integer ndarray
        Mask of the data image (1 = good pixel, 0 = bad pixel).
    interp:  Bool
        If True, lineraly interpolate the data for bad pixels.

  Returns:
  --------
    stdspec:  1D float ndarray
        The extracted spectrum.
    stdvar:  1D float ndarray
        Variance of extracted spectrum.

  Example:
  --------
    >>> import sys
    >>> import astropy.io.fits as fits
    >>> import matplotlib.pyplot as plt
    
    >>> sys.path.append("./src/")
    >>> import stdextr as se
    
    >>> data = fits.getdata("./images/ex1.fits")
    >>> spec, sstd = se.stdextr(data, 230, 270)
    
    >>> plt.plot(spec)
  """

  # Check inputs:
  nwave, nx = np.shape(data)

  if variance is None:
    variance = np.ones((nwave, nx), np.double)
  if mask is None:
    mask = np.ones((nwave, nx), np.byte)

  if x1 < 0 or x2 <= x1 or nx < x2:
    tools.error("Invalid x1, x2 boundaries (={:d}, {:d}), the values must "
                "satisfy:\n   0 <= x1 < x2 <= nx (={:d}).".format(x1, x2, nx))
  if np.shape(variance) != (nwave, nx):
    tools.error("Incompatible shapes between data image ({:d}, {:d}) and "
          "variance image ({:d}, {:d}).".format(nwave, nx, *np.shape(variance)))
  if np.shape(mask) != (nwave, nx):
    tools.error("Incompatible shapes between data image ({:d}, {:d}) and "
                "mask image ({:d}, {:d}).".format(nwave, nx, *np.shape(mask)))

  # Interpolate over bad pixels:
  if interp:
    for i in np.arange(nwave):
      bad  = np.where(mask[i, x1:x2] == 0)
      good = np.where(mask[i, x1:x2] == 1)
      datav = data[i, x1:x2]
      if len(bad) != 0:
        interpol = si.interp1d(datav[good], good[0], kind="linear")
        datav[bad] = interpol(bad[0])

  # Standard extraction:
  stdspec = np.sum((data     * mask)[:, x1:x2], axis=1)
  stdvar  = np.sum((variance * mask)[:, x1:x2], axis=1)

  return stdspec, stdvar
