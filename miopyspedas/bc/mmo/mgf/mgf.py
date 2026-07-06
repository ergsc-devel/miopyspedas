from ..load import load
from pyspedas import options

import logging

def mgf(
    trange=["2021-8-10","2021-8-11"],
    level="l2pre",
    prefix="",
    suffix="",
    get_support_data=False,
    varformat=None,
    varnames=[],
    downloadonly=False,
    notplot=False,
    no_update=False,
    time_clip=True,
    force_download=False,
    uname=None, passwd=None,
):

    """
    This function loads data from the MGF experiment from Mercury Magnetospheric Orbiter (MMO) of the Bepicolombo mission

    Parameters
    ----------

    """
    
    if prefix is None:
        prefix = ""

    if suffix is None:
        suffix = ""

    mgf_vars = load(trange=trange,
                    instrument='mgf',
                    level=level,
                    prefix=prefix,
                    suffix=suffix,
                    get_support_data=get_support_data,
                    varformat=varformat,
                    varnames=varnames,
                    downloadonly=downloadonly,
                    notplot=notplot,
                    no_update=no_update,
                    time_clip=time_clip,
                    force_download=force_download,
                    uname=uname, passwd=uname,
                    )

    return mgf_vars
