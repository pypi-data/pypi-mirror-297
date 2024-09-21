"""importing this module register the Lemaitre passband loaders into the
`sncosmo` registry system.
"""

from importlib.resources import files
import h5py
from sncosmo.bandpasses import (
    Bandpass,
    GeneralBandpassInterpolator,
    Transforms,
    _BANDPASSES,
    _BANDPASS_INTERPOLATORS)

# this module does not export any symbols
__all__ = []


def load_general_bandpass_interpolator(filename, band, version, name=None):
    """load the general functions
    """
    ret = {}

    with h5py.File(filename, 'r') as f:
        static = f['static']
        static_transmissions = [static[k][...] for k in static]

        if 'qe' in f:
            qemap = f['/qe/map']
            # specific_sensor_qe = dict([(tuple(map(int, k.split('_'))), v[...]) for k,v in f['/qe/map'].items()])
            specific_sensor_qe = dict([(int(k), v[...]) for k,v in f['/qe/map'].items()])
        else:
            specific_sensor_qe = None

 #       to_focalplane = dict([(tuple(map(int, k.split('_'))), v[...]) \
 #                             for k,v in f['/transforms/to_focalplane'].items()])
 #       to_filter = dict([(tuple(map(int, k.split('_'))), v[...]) \
 #                         for k,v in f['/transforms/to_filter'].items()])
        to_focalplane = dict([(int(k), v[...]) \
                              for k,v in f['/transforms/to_focalplane'].items()])
        to_filter = dict([(int(k), v[...]) \
                          for k,v in f['/transforms/to_filter'].items()])
        tr = Transforms(to_focalplane, to_filter)

        g = f['bandpasses'][band]
        if 'radii' in g:
            vtrans = g['radii'][...], g['wave'][...], g['trans'][...]
            ret = GeneralBandpassInterpolator(static_transmissions=static_transmissions,
                                              specific_sensor_qe=specific_sensor_qe,
                                              variable_transmission=vtrans,
                                              transforms=tr,
                                              bounds_error=False,
                                              fill_value=0.)
        elif 'X' in g and 'Y' in g:
            vtrans = g['X'][...], g['Y'][...], g['wave'][...], g['trans'][...]
            ret = GeneralBandpassInterpolator(static_transmissions=static_transmissions,
                                              specific_sensor_qe=specific_sensor_qe,
                                              variable_transmission=vtrans,
                                              transforms=tr,
                                              bounds_error=False,
                                              fill_value=0.)

        return ret


def load_default_bandpasses(filename, band, version, name=None):
    """load the default bandpasses
    """

    with h5py.File(filename, 'r') as f:
        bp = f['averaged_bandpasses'][band]
        wave = bp['wave'][...]
        trans = bp['trans'][...]
        ret = Bandpass(wave, trans, name=name)
    return ret


# ZTF variable bandpasses
ztf_meta = {
    'filterset': 'ztf',
    'retrieved': '22 December 2023',
    'description': 'A re-determination of the ZTF filters by P. Rosnet et al (ZTF-II IN2P3 participation group)'
}


filename = files(__package__).joinpath('data', 'ztf_v0.hdf5')
for band in ['g', 'r', 'I']:
    full_band_name = 'ztf::' + band
    _BANDPASS_INTERPOLATORS.register_loader(full_band_name,
                                            load_general_bandpass_interpolator,
                                            args=(filename, band, ),
                                            version='0.1',
                                            meta=ztf_meta)

# ZTF default bandpasses
ztf_meta_default = {
    'filterset': 'ztf',
    'retrieved': '22 December 2023',
    'description': 'A re-determination of the ZTF filters by P. Rosnet et al (ZTF-II IN2P3 participation group) - focal plane average'
}


filename = files(__package__).joinpath('data', 'ztf_v0.hdf5')
for band in ['g', 'r', 'I']:
    full_band_name = 'ztf::' + band
    _BANDPASSES.register_loader(full_band_name,
                                load_default_bandpasses,
                                args=(filename, band, ),
                                version='0.1',
                                meta=ztf_meta_default)


# megacam6 (re-measurements of the decommissioned MegaCam filters @ LMA)
megacam6_meta = {
    'filterset': 'megacam6',
    'retrieved': '22 December 2023',
    'description': 'A re-determination of the decommissioned MegaCam filters by M. Betoule and LMA )',
    'reference': 'XX'
}
filename = files(__package__).joinpath('data', 'megacam6_v0.hdf5')
for band in ['g', 'r', 'i', 'i2', 'z']:
    full_band_name = 'megacam6::' + band
    _BANDPASS_INTERPOLATORS.register_loader(full_band_name,
                                            load_general_bandpass_interpolator,
                                            args=(filename, band, ),
                                            version='0.1',
                                            meta=megacam6_meta)


# megacam6 default bandpasses
megacam6_meta_default = {
    'filterset': 'megacam6',
    'retrieved': '22 December 2023',
    'description': 'A re-determination of the decommissioned MegaCam filters by M. Betoule and LMA )',
}

filename = files(__package__).joinpath('data', 'megacam6_v0.hdf5')
for band in ['g', 'r', 'i', 'i2', 'z']:
    full_band_name = 'megacam6::' + band
    _BANDPASSES.register_loader(full_band_name,
                                load_default_bandpasses,
                                args=(filename, band, ),
                                version='0.1',
                                meta=megacam6_meta_default)

    
# HSC - Tanaki  version
hsc_meta = {
    'filterset': 'hsc',
    'retrieved': '22 December 2023',
    'description': 'A model of the HSC filters - built on a series of measurements by et al.',
    'reference': 'XX'
}
filename = files(__package__).joinpath('data', 'hsc_v0.hdf5')
for band in ['g', 'r', 'r2', 'i', 'i2', 'z', 'Y']:
    full_band_name = 'hsc::' + band
    _BANDPASS_INTERPOLATORS.register_loader(full_band_name,
                                            load_general_bandpass_interpolator,
                                            args=(filename, band, ),
                                            version='0.1',
                                            meta=hsc_meta)


hsc_meta_default = {
    'filterset': 'hsc',
    'retrieved': '22 December 2023',
    'description': 'A model of the HSC filters - built on a series of measurements by et al. -- focal plane average',
    'reference': 'XX'
}
filename = files(__package__).joinpath('data', 'hsc_v0.hdf5')
for band in ['g', 'r', 'r2', 'i', 'i2', 'z', 'Y']:
    full_band_name = 'hsc::' + band
    _BANDPASSES.register_loader(full_band_name,
                                load_default_bandpasses,
                                args=(filename, band, ),
                                version='0.1',
                                meta=hsc_meta_default)
