from ....mmo.load import load
from pyspedas import options

import logging

def mia(
        trange=["2021-10-1","2021-10-2"],
        level="l2pre",
        data_mode="l",
        datatype="et-all",
        obs_mode=None,
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
        files=None,
):
    """
    This function loads data from the Mercury Plasma Particle Experiment (MPPE) - Mercury Ion Analyzer (MIA) onboard the MMO spacecraft.
    
    Parameters
    ------------
        trange: list or str  
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']
            (default: ["2021-10-1","2021-10-2"])
        
        level: str
            Data level (default: l2pre)
        
        data_mode: str
            Data rate mode, 'l' for the low data rate mode (L-mode; default), 'm' for M-mode
        
        datatype: str
            Data type, 'et-all' for E-t all data (default), 'et-swall' for E-t swall data
        
        obs_mode: str
            Observation mode (Currently not used; may be used in future updates)

        prefix: str
            The tplot variable names will be given this prefix.
            By default, no prefix is added.

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
        
        files: list of str
            Set data file paths explicitly to load data from local files.
            (default: None)

    Returns
    ----------
        List of tplot variables created.

    Sample data of the MIA is located at the CHS repository
    https://chs.isee.nagoya-u.ac.jp/data/chs/satellite/mmo/cdf/mppe/mia/l2pre/et-all/2021/10/bc_mmo_mppe-mia_l2p_l-et-all_20211001_r01-v00-00.cdf
    """

    if suffix is None:
        suffix = ""
    
    if level == "l2pre":
        lev = "l2p"
    else:
        lev = level
    
    if prefix == "":
        prefix = "mmo_mia_"+lev+"_"+data_mode+"_"+datatype+"_"
    
    
    if files is None:
        pathformat = f"satellite/mmo/cdf/mppe/mia/{level}/{datatype}/%Y/%m/" + \
            f"bc_mmo_mppe-mia_{lev}_{data_mode}-{datatype}_%Y%m%d_r??-v??-??.cdf"
    
    tvars = load(trange=trange,
                    instrument='mia', 
                    pathformat=pathformat,
                    level=level,
                    data_mode=data_mode,
                    datatype=datatype,
                    prefix=prefix, 
                    suffix=suffix,
                    get_support_data=get_support_data, 
                    varformat=varformat, 
                    varnames=varnames, 
                    downloadonly=downloadonly,
                    notplot=notplot,
                    no_update=no_update,
                    time_clip=time_clip,
                    force_download=False,
                    uname=None, passwd=None,
                    files=files
                    )
    if downloadonly is True:    
        return None
    
    # Decorate tplot variables
    if level == "l2pre":
        if data_mode == "l":
            match datatype:
                case "et-all" | "et-swall":
                    options( prefix+"count_d?", "spec", 1)
                    options( prefix+"count_d?", "yrange", [1e1, 2.6e4])
                    options( prefix+"count_d?", "ylog", 1)
                    options( prefix+"count_d?", "ysubtitle", "[eV]")
                    options( prefix+"count_d?", "zlog", 1)
                    options( prefix+"count_d?", "zrange", [1e0, 1e4])
                    options( prefix+"count_d?", "ztitle", "[cnt/smpl]")
                    for i in range(1,5):
                        options( prefix+f"count_d{i}", "ytitle", f"BC/MMO\nMIA L2p\ncount d{i}")
                    
                    options( prefix+"deflux_d?", "spec", 1)
                    options( prefix+"deflux_d?", "yrange", [1e1, 2.6e4])
                    options( prefix+"deflux_d?", "ylog", 1)
                    options( prefix+"deflux_d?", "ysubtitle", "[eV]")
                    options( prefix+"deflux_d?", "zlog", 1)
                    options( prefix+"deflux_d?", "zrange", [1e5, 1e9])
                    options( prefix+"deflux_d?", "ztitle", "[eV/cm^2/s/sr/eV]")
                    for i in range(1,5):
                        options( prefix+f"deflux_d{i}", "ytitle", f"BC/MMO\nMIA L2p\nEneFlux d{i}")
            
        elif data_mode == "m":
            # Currently, only L-mode data is available
            print("M-mode data is currently not available.")
    


    return tvars





