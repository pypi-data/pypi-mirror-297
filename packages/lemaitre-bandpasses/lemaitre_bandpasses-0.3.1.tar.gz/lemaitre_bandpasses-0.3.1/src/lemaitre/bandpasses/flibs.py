"""Standard filterlibs

We may want to add this to a sncosmo-like registry.
Not sure we really need that.

"""

import logging
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.INFO)

import numpy as np

from bbf import FilterLib
from bbf.bspline import BSpline
from bbf import get_cache_dir



def ccdid_qid_to_rcid(ccdid, qid):
    """stolen from ztfimg.tools.

    .. note::
       Would love to use the original, but dask deps...
    """
    return 4*(ccdid - 1) + qid - 1


def get_filterlib(name='lemaitre', rebuild=False):
    """
    """
    cached_version_path = get_cache_dir().joinpath(f'{name}_flib.pkl')
    if cached_version_path.is_file() and not rebuild:
        fl = FilterLib.load(cached_version_path)
        return fl
    fl = rebuild_filterlib()
    return fl


def rebuild_filterlib():
    """
    """
    logging.info('rebuilding filterlib')
    fl = FilterLib(basis=np.arange(3000., 11010., 10.))


    # MegaCam6: the only tricky part is g, which requires
    # a higher resolution for the spatial spline basis
    logging.info('megacam6...')
    fl.insert(fl.fetch('megacam6::g', xy_size=40, xy_order=4),  'megacam6::g')
    fl.insert(fl.fetch('megacam6::r', xy_size=20, xy_order=2),  'megacam6::r')
    fl.insert(fl.fetch('megacam6::i', xy_size=20, xy_order=2),  'megacam6::i')
    fl.insert(fl.fetch('megacam6::i2', xy_size=20, xy_order=2), 'megacam6::i2')
    fl.insert(fl.fetch('megacam6::z', xy_size=20, xy_order=2),  'megacam6::z')

    logging.info('megacam6 default (averaged) bandpasses')
    fl.insert(fl.fetch('megacam6::g', average=True),  'megacam6::g', average=True)
    fl.insert(fl.fetch('megacam6::r', average=True),  'megacam6::r', average=True)
    fl.insert(fl.fetch('megacam6::i', average=True),  'megacam6::i', average=True)
    fl.insert(fl.fetch('megacam6::i2', average=True), 'megacam6::i2', average=True)
    fl.insert(fl.fetch('megacam6::z' , average=True),  'megacam6::z', average=True)

    logging.info('megacampsf default (averaged) bandpasses [used in JLA]')
    fl.insert(fl.fetch('megacampsf::g', average=True, radius=0.),  'megacampsf::g', average=True)
    fl.insert(fl.fetch('megacampsf::r', average=True, radius=0.),  'megacampsf::r', average=True)
    fl.insert(fl.fetch('megacampsf::i', average=True, radius=0.), 'megacampsf::i', average=True)
    fl.insert(fl.fetch('megacampsf::z' , average=True, radius=0.),  'megacampsf::z', average=True)

    logging.info('HSC')
    fl.insert(fl.fetch('hsc::g', xy_size=20, xy_order=2), 'hsc::g')
    fl.insert(fl.fetch('hsc::r', xy_size=20, xy_order=2), 'hsc::r')
    fl.insert(fl.fetch('hsc::r2', xy_size=20, xy_order=2), 'hsc::r2')
    fl.insert(fl.fetch('hsc::i', xy_size=20, xy_order=2), 'hsc::i')
    fl.insert(fl.fetch('hsc::i2', xy_size=20, xy_order=2), 'hsc::i2')
    fl.insert(fl.fetch('hsc::z', xy_size=20, xy_order=2), 'hsc::z')
    fl.insert(fl.fetch('hsc::Y', xy_size=20, xy_order=2), 'hsc::Y')

    logging.info('HSC default (averaged) bandpasses')
    fl.insert(fl.fetch('hsc::g', average=True), 'hsc::g', average=True)
    fl.insert(fl.fetch('hsc::r', average=True), 'hsc::r', average=True)
    fl.insert(fl.fetch('hsc::r2', average=True), 'hsc::r2', average=True)
    fl.insert(fl.fetch('hsc::i', average=True), 'hsc::i', average=True)
    fl.insert(fl.fetch('hsc::i2', average=True), 'hsc::i2', average=True)
    fl.insert(fl.fetch('hsc::z', average=True), 'hsc::z', average=True)
    fl.insert(fl.fetch('hsc::Y', average=True), 'hsc::Y', average=True)


    # for ZTF, we have basically two models: one for single coatings and another
    # for the double coatings. Both include the transforms for the entire filter set.
    #
    logging.info('ZTF')
    # Single coating
    sensor_id = ccdid_qid_to_rcid(1, 1) + 1
    bp_g_single = fl.fetch('ztf::g', xy_size=20, xy_order=2, sensor_id=sensor_id)
    bp_r_single = fl.fetch('ztf::r', xy_size=20, xy_order=2, sensor_id=sensor_id)
    bp_I_single = fl.fetch('ztf::I', xy_size=20, xy_order=2, sensor_id=sensor_id)
    sensors_single = [ccdid_qid_to_rcid(ccdid, qid) + 1
                      for qid in range(1, 5)
                      for ccdid in [1, 2, 3, 4, 13, 14, 15, 16]
                      ]

    # Single coating
    sensor_id = ccdid_qid_to_rcid(5, 1) + 1
    bp_g_double = fl.fetch('ztf::g', xy_size=20, xy_order=2, sensor_id=sensor_id)
    bp_r_double = fl.fetch('ztf::r', xy_size=20, xy_order=2, sensor_id=sensor_id)
    bp_I_double = fl.fetch('ztf::I', xy_size=20, xy_order=2, sensor_id=sensor_id)
    sensors_double = [ccdid_qid_to_rcid(ccdid, qid) + 1
                      for qid in range(1, 5)
                      for ccdid in [5, 6, 7, 8, 9, 10, 11, 12]
                      ]
    for b_single, b_double, bname in zip([bp_g_single, bp_r_single, bp_I_single],
                                         [bp_g_double, bp_r_double, bp_I_double],
                                         ['ztf::g', 'ztf::r', 'ztf::I']):
        fl.insert(dict(zip(sensors_single +\
                           sensors_double,
                           [b_single]*len(sensors_single) +\
                           [b_double]*len(sensors_double))),
                  bname)

    logging.info('ZTF default (averaged) bandpasses')
    fl.insert(fl.fetch('ztf::g', average=True), 'ztf::g', average=True)
    fl.insert(fl.fetch('ztf::r', average=True), 'ztf::r', average=True)
    fl.insert(fl.fetch('ztf::I', average=True), 'ztf::I', average=True)

    # the sncosmo version of various filters
    fl.insert(fl.fetch('ztfg', average=True), 'ztfg', average=True)
    fl.insert(fl.fetch('ztfr', average=True), 'ztfr', average=True)
    fl.insert(fl.fetch('ztfi', average=True), 'ztfi', average=True)

    fl.insert(fl.fetch('lsstu', average=True), 'lsstu', average=True)
    fl.insert(fl.fetch('lsstg', average=True), 'lsstg', average=True)
    fl.insert(fl.fetch('lsstr', average=True), 'lsstr', average=True)
    fl.insert(fl.fetch('lssti', average=True), 'lssti', average=True)
    fl.insert(fl.fetch('lsstz', average=True), 'lsstz', average=True)
    fl.insert(fl.fetch('lssty', average=True), 'lssty', average=True)


    # dump it to cache
    cache_dir = get_cache_dir()
    # dst = cache_dir.joinpath('lemaitre_flib.hdf5')
    # fl.to_hdf5(dst, compression='lzf')
    dst = cache_dir.joinpath('lemaitre_flib.pkl')
    logging.info(f'to cache -> {dst}')
    fl.save(dst)

    logging.info('done')

    return fl
