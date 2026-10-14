import cdflib
import numpy as np

# PySPEDAS (> v.2.*)
import pyspedas
from pyspedas import tnames
from pyspedas import clip, get_data, options, ylim

import spiceypy as spice

from ..spice import load_kernels

rm_in_km = 2439.9 #mean mercury radius [km]

def orb(trange=['2023-06-19', '2023-06-20'],
        datatype='def',
        target='MMO',
        ref_frame='BC_MSM',
        observer='MERCURY',
        aberration='NONE',
        dt=60,
        units='rm',
        suffix='',
        no_ck=True,
        get_support_data=False,
        varformat=None,
        varnames=[],
        downloadonly=False,
        notplot=False,
        no_update=False,
        time_clip=False,
        version=None,
        velocity=False
):
    
    bc_kernels = load_kernels(no_ck=no_ck, no_update=no_update)
    prefix = target.lower() + '_orb_'+ref_frame.lower()+'_'
    
    et_start = spice.utc2et(trange[0])
    et_stop = spice.utc2et(trange[1])
    # Time in ephemeris
    time_spice = np.arange(et_start, et_stop, dt)

    # time in TT2000
    time_double = pyspedas.time_ephemeris(time_spice, et2ut=True)
    time_double = pyspedas.time_double(time_double)
    stored_variables = []

    time_separation = "2026-12-09T00:00:00" # tentative datetime for Mio's separation
    et_separation = spice.utc2et(time_separation)

    if et_stop < et_separation:
        positions, lightTimes = spice.spkezr(targ = "MPO", et = time_spice, ref = ref_frame, abcorr = aberration, obs = observer)
    elif et_start > et_separation:
        positions, lightTimes = spice.spkezr(targ = target, et = time_spice, ref = ref_frame, abcorr = aberration, obs = observer)
    else:
        time_beforesep = np.arange(et_start, et_separation, dt)
        time_aftersep = np.arange(et_separation, et_stop, dt)
        positions1, lightTimes1 = spice.spkezr(targ = "MPO", et = time_beforesep, ref = ref_frame, abcorr = aberration, obs = observer)
        positions2, lightTimes2 = spice.spkezr(targ = target, et = time_aftersep, ref = ref_frame, abcorr = aberration, obs = observer)
        positions = np.append(positions1, positions2, axis=0)


    pos = positions[:, 0:3]
    vel = positions[:, 3:]

    if units=='rm':
        pos /= rm_in_km # convert from km to mercury radii 
        pyspedas.store_data(prefix+'pos'+suffix, data={'x':time_double, 'y':pos})

    elif units=='km':
        pyspedas.store_data(prefix+'pos'+suffix, data={'x':time_double, 'y':pos})

    pyspedas.store_data(prefix+'vel'+suffix, data={'x':time_double, 'y':vel})
    pyspedas.store_data(prefix+'R'+suffix, data={'x':time_double, 'y':np.linalg.norm(pos, axis = 1)})
    
    pyspedas.set_units(prefix+'pos'+suffix, units)
    pyspedas.set_units(prefix+'R'+suffix, units)
    pyspedas.set_units(prefix+'vel'+suffix, 'km/s')

    stored_variables.append(prefix+'pos'+suffix)
    stored_variables.append(prefix+'vel'+suffix)
    stored_variables.append(prefix+'R'+suffix)    

    return stored_variables