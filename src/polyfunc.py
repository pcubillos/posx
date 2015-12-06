import numpy as np

import tools as tools

def evaluate(xvals, coeff, data, variance, spec):
  """
  Evaluate polynomial at xvals, repairing values where variance==0
  with data/spec.

  Parameters:
  -----------
     xvals:  1D float ndarray
         X values for data.
     coeff:  1D float ndarray
         The polynomial coefficients (highest to lowest power).
     data:  1D float ndarray
         The data vector to fit.
     variance:  1D float ndarray
         The variance vector.
     spec:  1D float ndarray
         The spectrum vector.
     deg:  Integer
         Degree of the polynomial.

  Returns:
  --------
     fiteval: 1D float ndarray
         The estimated spectrum

  Example:
  --------
    See example in polyfunc.fit()
  """

  # Check inputs:
  nx = np.size(xvals)
  nd = np.size(data)
  nv = np.size(variance)
  ns = np.size(spec)

  if nx != nd or nx != nv or nx != ns:
    tools.error("The length of data ({:d}), variance ({:d}), spec ({:d}), "
                "and/or xvals ({:d}) are incompatible.".format(nd, nv, ns, nx))
  # Find values with zero variance:
  zerov = (variance == 0.0)

  # Evaluate coefficients:
  fiteval = np.polyval(coeff, xvals)

  # Use actual data where varv is 0:
  fiteval[zerov] = data[zerov] / spec[zerov]

  return fiteval


def fit(xvals, data, variance, spec, deg=2):
  """
  Fit data/spectrum using the variances as weights, using a polynomial
  function.

  Parameters:
  -----------
     xvals:  1D float ndarray
         X values for data.
     data:  1D float ndarray
         The data vector to fit.
     variance:  1D float ndarray
         The variance vector.
     spec:  1D float ndarray
         The spectrum vector.
     deg:  Integer
         Degree of the polynomial.

  Returns:
  --------
     est: 1D float ndarray
         The estimated spectrum.
     coeff: 1D float ndarray
         The polynomial coefficients (from highest to lowest power).

  Example:
  --------
     >>> nx = 100
     >>> xvals = np.arange(nx, dtype=np.double)
     >>> prof = ((-(xvals/nx*2 - 1)**2 + 1)*0.75)/nx*2
     >>> sbump = 10
     >>> spec = np.sin(xvals/nx * np.pi * 6) + sbump
     >>> gain = 10
     >>> basey = profv*specv
     >>> data = basey + basey * np.random.normal(0.0, 1.0, nx)/gain
     >>> variance = basey/gain
     >>> badloc = np.random.randint(0, 50, 4)
     >>> data[badloc] = np.random.uniform(0, 2*np.amax(data), 4)
     >>> prof[badloc] = 0
     >>> deg = 2
     >>> est, coeffv = pf.fit(xvals, data, variance, spec, deg)

     >>> plt.figure(1)
     >>> plt.clf()
     >>> plt.plot(data/spec, 'or')
     >>> plt.plot(xvals, est, 'b')

     >>> est = pf.evaluate(xvals, coeffv, data, variance, spec)
     >>> plot(xvals, est, 'ob')
  """
  # Check inputs:
  nd = np.size(data)
  nv = np.size(variance)
  ns = np.size(spec)
  nx = np.size(xvals)

  if nx != nd or nx != nv or nx != ns:
    tools.error("The length of data ({:d}), variance ({:d}), spec ({:d}), "
                "and/or xvals ({:d}) are incompatible.".format(nd, nv, ns, nx))
  if deg < 0 or nx <= deg:
    tools.error("Invalid polynomial degree ({:d}), must be: 0 < deg < nx-1 "
                "= {:d}.".format(deg, nx-1))

  # Initial estimate:
  est = data / spec

  # Find where the variance has non-zero values:
  nzerov = (variance != 0.0)

  # Fit polynomial where variance != 0:
  merrors = variance/spec**2
  # Use all pixels for estimation
  merrors = np.clip(merrors, 1e-8, np.amax(merrors))
  coeff = np.polyfit(xvals, data/spec, deg, w=merrors)
  est[nzerov] = np.polyval(coeff, xvals[nzerov])

  return est, coeff
