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
    This function loads data from the Solar Particle Monitor (SPM)
    
    Parameters (Draft)
    ------------
        trange: list or str  
            time range of interest [starttime, endtime] with the format 
            ['YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']
            (default: ["2021-8-10","2021-8-11"])
        
        level: str
            Data level (default: l2pre) --> after MOI default will be l2
        
        prefix: str
            The tplot variable names will be given this prefix.
            If not specified, a default prefix "mmo_spm_<level>_"
            (e.g. "mmo_spm_l2pre_") is added automatically.
            Pass your own string to override it.
            (default: "" -> "mmo_mgf_l2pre_")

        suffix: str
            The tplot variable names will be given this suffix.
            By default, no suffix is added.

        get_support_data: bool
            Data with an attribute "VAR_TYPE" with a value of "support_data"
            will be loaded into tplot. 
            By default, only loads in data with a 
            "VAR_TYPE" attribute of "data".
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

    Sample data of the SPM is located at the CHS repository
    https://chs.isee.nagoya-u.ac.jp/data/chs/satellite/mmo/cdf/spm/l2pre/cnt/2021/08/bc_mmo_spm_l2p_cnt_20210810_r01-v00-00.cdf
    """

    
    # --- Normalize the requested level FIRST, before deciding prefix/suffix or
    #     building the path, so that `level` becomes a single clean canonical
    #     value we can rely on everywhere below (path, prefix, load() call).
    #
    # normalization / use lower capitals --> remove space --> "level" to "l"
    # e.g. "level 2 pre", "L2PRE", "l2 p" --> "l2pre"
    level_key = level.lower().replace(" ", "").replace("level", "l")

    if level_key in ("l2pre", "l2p"):
        level = "l2pre"
    
    # elif level_key in ("l2", "l3") # an l2 function will be equipped

    else:
        raise ValueError(f"Unsupported level: {level!r}")
    
    if level == "l2pre":
        pathformat = (
                "satellite/mmo/cdf/mgf/" + level
                + "/cnt/%Y/%m/"
                + "bc_mmo_mgf_" + level[:3]
                + "_cnt_%Y%m%d_r??-v??-??.cdf"
                )
            # https://chs.isee.nagoya-u.ac.jp/data/chs/satellite/mmo/cdf/spm/l2pre/cnt/2021/08/bc_mmo_spm_l2p_cnt_20210810_r01-v00-00.cdf
            # for spm: level=l2pre, datatype=
            # The directory uses `level` (=l2pre) directly, while the file name uses the
            # short token "l2p", derived here from `level` so we keep only one variable.
    

    # Add a default prefix ONLY when the user did not specify one, so that tplot
    # variable names identify the mission/instrument/level. A user-supplied
    # prefix is respected and never overwritten.
    if prefix == "":
        prefix = "mmo_mgf_" + level + "_"

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
