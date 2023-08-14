import os
import sys
import multiprocessing
import pickle

import numpy as np
from pandas import DataFrame, Series
from scipy.stats import norm

def common_radius_fit_lambda_2_mass_ratio_to_lambda_1(lambda_2, mass_ratio):
    """
    Convert from symmetric tidal terms and mass ratio to antisymmetric tidal terms
    using common radius assumption.
    This function does only the fit itself, and doesn't account for marginalisation
    over the uncertanties in the fit

    See De+, https://arxiv.org/abs/1804.08583
    and Chatziioannou, Haster, Zimmerman, https://arxiv.org/abs/1804.03221

    This function will use the implementation from the CHZ paper, but will
    marginalize over the common radius fit instead of binary Love.


    Parameters
    ==========
    lambda_symmetric: float
        Symmetric tidal parameter.
    mass_ratio: float
        Mass ratio (mass_2/mass_1, with mass_2 < mass_1) of the binary

    Returns
    ======
    lambda_antisymmetric: float
        Antisymmetric tidal parameter.
    """
    q = mass_ratio

    lambda_1 = q ** 6 * lambda_2

    return lambda_1


def common_radius_lambda_2_to_lambda_1_lambda_2_manual_marginalisation(common_radius_uniform,
                                                                       lambda_2, mass_ratio):
    """
    Convert from symmetric tidal terms to lambda_1 and lambda_2
    using common radius assumption.

    See De+, https://arxiv.org/abs/1804.08583
    and Chatziioannou, Haster, Zimmerman, https://arxiv.org/abs/1804.03221

    This function will use the implementation from the CHZ paper, but will
    marginalize over the common radius fit instead of binary Love.

    Parameters
    ==========
    common_radius_uniform: float (defined in the range [0,1])
        Uniformly distributed variable used in common radius uncertainty marginalisation
    lambda_symmetric: float
        Symmetric tidal parameter.
    mass_ratio: float
        Mass ratio (mass_2/mass_1, with mass_2 < mass_1) of the binary

    Returns
    ======
    lambda_1: float
        Tidal parameter of more massive neutron star.
    lambda_2: float
        Tidal parameter of less massive neutron star.
    """
    lambda_1_fitOnly = common_radius_fit_lambda_2_mass_ratio_to_lambda_1(lambda_2, mass_ratio)

    q = mass_ratio

    # mu_i and sigma_i coefficients are given in Table II of CHZ

    mu_a = 0.0093
    mu_r = 11.2  # km

    sigma_a = 0.0007
    sigma_r = 0.11  # km

    lambda_1_meanCorr = 0

    lambda_1_stdCorr = \
        np.sqrt((2 * (sigma_a / mu_a) ** 2) + (72 * (sigma_r / mu_r) ** 2)) * ((q ** 6) * lambda_2)

    # Draw a correction on the fit from a
    # Gaussian distribution with width lambda_antisymmetric_stdCorr
    # this is done by sampling a percent point function  (inverse cdf)
    # through a U{0,1} variable called binary_love_uniform

    #     try:
    #         if common_radius_uniform < 0 or common_radius_uniform > 1:
    #             common_radius_uniform = np.random.uniform(0, 1)
    #     except:
    #         if any(common_radius_uniform < 0) or any(common_radius_uniform > 1):
    #             common_radius_uniform = np.random.uniform(0, 1)

    lambda_1_scatter = norm.ppf(common_radius_uniform, loc=0., scale=lambda_1_stdCorr)

    # Add the correction of the residual mean
    # and the Gaussian scatter to the lambda_antisymmetric_fitOnly value

    lambda_1 = lambda_1_fitOnly + \
               (lambda_1_meanCorr + lambda_1_scatter)

    # The BinaryLove model is only physically valid where
    # lambda_2 > lambda_1 as it assumes mass_1 > mass_2
    # It also assumes both lambda1 and lambda2 to be positive
    # This is an explicit feature of the "raw" model fit,
    # but since this implemefntation also incorporates
    # marginalisation over the fit uncertainty, there can
    # be instances where those assumptions are randomly broken.
    # For those cases, set lambda_1 and lambda_2 to negative
    # values, which in turn will cause (effectively all) the
    # waveform models in LALSimulation to fail, thus setting
    # logL = -infinity

    #     print('lambda_1:', lambda_1, type(lambda_1))
    #     print('lambda_2:', lambda_2, type(lambda_2))
    #     print('common_radius_uniform:', common_radius_uniform, type(common_radius_uniform))

    #     try:
    #         if np.isnan(lambda_1):
    #             print('lambda_1 isnan')
    #         elif np.isnan(lambda_2):
    #             print('lambda_2 isnan')
    #     except:
    #         if any(np.isnan(lambda_1)):
    #             print('lambda_1 contains nan')
    #         elif any(np.isnan(lambda_2)):
    #             print('lambda_2 contains nan')

    #     if np.greater(lambda_1, lambda_2) or np.less(lambda_1, 0) or np.less(lambda_2, 0):
    #        lambda_1 = -np.inf
    #        lambda_2 = -np.inf

    # For now set this through an explicit constraint prior instead

    return lambda_1, lambda_2


def common_radius_lambda_2_to_lambda_1_lambda_2_automatic_marginalisation(lambda_2, mass_ratio):
    """
    Convert from symmetric tidal terms to lambda_1 and lambda_2
    using common radius assumption.

    See De+, https://arxiv.org/abs/1804.08583
    and Chatziioannou, Haster, Zimmerman, https://arxiv.org/abs/1804.03221

    This function will use the implementation from the CHZ paper, but will
    marginalize over the common radius fit instead of binary Love.

    This function should be used when the common radius marginalisation wasn't
    explicitly active in the sampling stage. It will draw a random number in U[0,1]
    here instead.

    Parameters
    ==========
    lambda_symmetric: float
        Symmetric tidal parameter.
    mass_ratio: float
        Mass ratio (mass_2/mass_1, with mass_2 < mass_1) of the binary

    Returns
    ======
    lambda_1: float
        Tidal parameter of more massive neutron star.
    lambda_2: float
        Tidal parameter of less massive neutron star.
    """
    from ..core.utils.random import rng

    if np.isscalar(lambda_2):
        common_radius_uniform = rng.uniform(0, 1, 1)
    else:
        common_radius_uniform = rng.uniform(0, 1, len(lambda_2))

    lambda_1, lambda_2 = common_radius_lambda_2_to_lambda_1_lambda_2_manual_marginalisation(
        common_radius_uniform, lambda_2, mass_ratio)

    return lambda_1, lambda_2