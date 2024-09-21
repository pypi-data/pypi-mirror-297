"""
``lemaitre.passbands``: a module to keep track of the passband work,
    exchange preliminary sncosmo-compatible passband models, and to
    load them automatically into the sncosmo registry system.
"""

from .builtins import *
from .flibs import *


__version__ = "0.3.0"



# import numpy as np
# from numpy.polynomial.polynomial import polyvander2d

# import h5py
# from sncosmo.bandpasses import GeneralBandpassInterpolator, Transforms
# from sncosmo.bandpasses import _BANDPASS_INTERPOLATORS


# def load_general_bandpass_interpolator(band, filename, version=None):
#     """load the general functions


#     """
#     ret = {}

#     with h5py.File(filename, 'r') as f:
#         static = f['static']
#         static_transmissions = [static[k][...] for k in static]

#         if 'qe' in f:
#             qemap = f['/qe/map']
#             specific_sensor_qe = dict([(tuple(map(int, k.split('_'))), v[...]) for k,v in f['/qe/map'].items()])
#         else:
#             specific_sensor_qe = None

#         to_focalplane = dict([(tuple(map(int, k.split('_'))), v[...]) \
#                               for k,v in f['/transforms/to_focalplane'].items()])
#         to_filter = dict([(tuple(map(int, k.split('_'))), v[...]) \
#                           for k,v in f['/transforms/to_filter'].items()])

#         #        for band in bands:
#         g = f['bandpasses'][band]
#         vtrans = g['radii'][...], g['wave'][...], g['trans'][...]
#         tr = Transforms(to_focalplane, to_filter)
#         ret = GeneralBandpassInterpolator(static_transmissions=static_transmissions,
#                                           specific_sensor_qe=specific_sensor_qe,
#                                           variable_transmission=vtrans,
#                                           transforms=tr,
#                                           bounds_error=False,
#                                           fill_value=0.)

#         return ret


# # ZTF passbands
# ztf_meta = {
#     'filterset': 'ztf',
#     'retrieved': '22 December 2023',
#     'description': 'A re-determination of the ZTF filters by P. Rosnet et al (ZTF-II IN2P3 participation group)'
# }
# for letter in ['g', 'r', 'I']:
#     _BANDPASS_INTERPOLATORS.register_loader('ztf::' + letter,
#                                             load_general_bandpass_interpolator,
#                                             args=([letter,], filename, '0.1'),
#                                             version='0.1',
#                                             meta=ztf_meta)

# # megacam6 (re-measurements of the decommissioned MegaCam filters @ LMA)
# megacam6_meta = {
#     'filterset': 'megacam6',
#     'retrieved': '22 December 2023',
#     'description': 'A re-determination of the decommissioned MegaCam filters by M. Betoule and LMA )',
#     'reference': 'XX'
# }
# for letter in ['g', 'r', 'i2', 'z']:
#     _BANDPASS_INTERPOLATORS.register_loader('megacam6::' + letter,
#                                             load_general_bandpass_interpolator,
#                                             args=([letter,], filename, '0.1'),
#                                             version='0.1',
#                                             meta=megacam6_meta)

# # HSC - Tanaki  version
# hsc_meta = {
#     'filterset': 'hsc',
#     'retrieved': '22 December 2023',
#     'description': 'A model of the HSC filters - built on a series of measurements by et al.',
#     'reference': 'XX'
# }
# for letter in ['g', 'r', 'r2', 'i', 'i2', 'z', 'Y']:
#     _BANDPASS_INTERPOLATORS.register_loader('hsc::' + letter,
#                                             load_general_bandpass_interpolator,
#                                             args=([letter,], filename, '0.1'),
#                                             version='0.1',
#                                             meta=hsc_meta)
