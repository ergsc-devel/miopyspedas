from ..load import load
from pyspedas import options

import logging

def mgf(
    trange=["2025-01-07","2025-01-09"],
    level="l2pre",
    rate="l",
    coord="",
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
    This function loads data from Fluxgate Magnetometer (MGF) on
    board Mercury Magnetospheric Orbiter (MMO/Mio).
    
    Parameters (Draft)
    ------------
        trange: list or str  
            time range of interest [starttime, endtime] with the format 
            ['YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']
            (default: ["2025-01-07","2025-01-09"])
        
        level: str
            Data level
            (default: "l2pre") --> after MOI default will be "l2"

        rate: str
            Date rate mode "l", "m1", "m2", or "h"
            L-mode: ~4s, M1-mode: 8 Hz, M2-mode: 4 Hz, H-mode: 128 Hz
            (default: "l")
        
        coord: str
            Reference frame of a magnetic vector
            (default: l2pre --> "scf", l2 --> "xsm")

        prefix: str
            The tplot variable names will be given this prefix.
            If not specified, a default prefix "mmo_mgf_<level>_<rate>_".
            (e.g. "mmo_mgf_l2pre_l_") is added automatically.
            Pass your own string to override it.
            (default: "" -> "mmo_mgf_l2pre_l_")

        suffix: str
            The tplot variable names will be given this suffix.
            By default, no suffix is added.

        get_support_data: bool
            Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot. 
            By default, only loads in data with a "VAR_TYPE" attribute of "data".
            (default: False)

        varformat: str
            The file variable formats to load into tplot.
            Wildcard character "*" is accepted.
            By default, all variables are loaded in.

        varnames: list of str
            List of variable names to load
            If not specified, all data variables are loaded.
            (default: [])
        
        downloadonly: bool
            Set this flag to download the CDF files, but not load them into 
            tplot variables.
            (default: False)
        
        notplot: bool
            Return the data in dict instead of creating tplot variables.
            (default: False)
        
        no_update: bool
            If set, only load data from your local cache.
            (default: False)

        time_clip: bool
            Time clip the variables to exactly the range specified in the trange keyword.
            (default: True)

        force_download: bool,
            Download file even if local version is more recent than server version.
            (default: False)
        
        uname: str
        passwd: str
            Password for accessing restricted data products.
            Please contact the PI teams (or the project team) to obtain authentication credentials.
            Access to l2pre data is restricted and generally limited to project members.

    Returns
    ----------
        List of tplot variables created.

    """

    
    # Normalize the requested level FIRST, before deciding prefix/suffix or
    # building the path, so that `level` becomes a single clean canonical
    # value we can rely on everywhere below (path, prefix, load() call).
    #
    # normalization / use lower capitals --> remove space --> "level" to "l"
    # e.g. "level 2 pre", "L2PRE", "l2 p" --> "l2pre"
    level_key = level.lower().replace(" ", "").replace("level", "l")

    if level_key in ("l2pre", "l2p"):
        level = "l2pre"
    
    # elif level_key in ("l2", "l3") # an l2 function will be equipped

    else:
        raise ValueError(f"Unsupported level: {level!r}")
    
    # Normalize the requested data rate
    rate_key = rate.lower().replace(" ","").replace("-","").replace("mode","")

    match rate_key:
        case "l" | "low":
            rate = "l"
        case "m1" | "m":
            rate = "m1"
        case "m2":
            rate = "m2"
        case "h" | "high":
            rate = "h"
        case _:
            raise ValueError(f"Unsupported data rate: {rate!r}")

    # Set a format of file path
    if level == "l2pre":
        # "satellite/mmo/cdf/mgf/l2pre/l/2025/01/bc_mmo_mgf_l2p_l_scf_20250107_r01-v00-00.cdf"
        pathformat = (
                "satellite/mmo/cdf/mgf/" + level
                + "/" + rate + "/%Y/%m/"
                + "bc_mmo_mgf_" + level[:3] + '_' + rate
                + "_" + coord + "_%Y%m%d_r??-v??-??.cdf"
                )

    # Normalize the reference frame name
    coord = coord.lower()

    # Set reference frame
    if coord == "":
        match level:
            case "l2pre":
                coord = "scf"
            case "l2":
                coord = "xsm"
            case _:
                raise ValueError(f"Unsupported level: {level!r}")
            
    # Add a default prefix ONLY when the user did not specify one, so that tplot
    # variable names identify the mission/instrument/level. A user-supplied
    # prefix is respected and never overwritten.
    if prefix == "":
        prefix = "mmo_mgf_" + level + "_" + rate + "_" 

    mgf_vars = load(trange=trange,
                    instrument='mgf',
                    pathformat=pathformat,
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
                    uname=uname, passwd=passwd
                    )

    return mgf_vars
