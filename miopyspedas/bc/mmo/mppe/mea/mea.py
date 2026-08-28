from ....mmo.load import load
from pyspedas import options

import logging

def mea(
        trange=["2021-10-1","2021-10-2"],
        level="l2pre",
        data_mode="l",
        sensor="mea1",
        enestep="16",
        datatypes=["omniflux"],
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
    This function loads data from the Mercury Plasma Particle Experiment (MPPE) - Mercury Electron Analyzer (MEA) onboard the MMO spacecraft.
    
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

        sensor: str
            Sensor name, 'mea1' for MEA1 (default), 'mea2' for MEA2
        
        enestep: str
            Energy step, '16' for 16 energy steps (default)
        
        datatypes: list of str
            List of data types to load (default: ["omniflux"])
        
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
            Please contact the instrument team (or the project team) to obtain authentication credentials.
            Access to l2pre data is restricted and generally limited to project members.
        
        files: list of str
            Set data file paths explicitly to load data from local files.
            (default: None)

    Returns
    ----------
        List of tplot variables created.

    Sample data of the HEP electron is located at the CHS repository
    https://chs.isee.nagoya-u.ac.jp/data/chs/satellite/mmo/cdf/mppe/mea/l2pre/flux/2021/10/bc_mmo_mppe-mea1_l2p_l-omniflux-16e_20211001_r01-v00-00.cdf
    """

    if suffix is None:
        suffix = ""
    
    if level == "l2pre":
        lev = "l2p"
    elif level == "l2":
        lev = "l2"
    else:
        lev = level
    
    for datatype in datatypes:

        datatypedir = ""
        match datatype:
            case "omniflux":
                datatypedir = "flux"
            case "3dflux":
                datatypedir = "flux"
            case _:
                logging.warning(f"Unsupported datatype: {datatype}. Skipping.")
        if datatypedir == "":
            continue       
        
        if prefix == "":
            prefix = "mmo_"+sensor+"_"+lev+"_"+data_mode+"-"+datatype+enestep+"e_"
        
        
        if files is None:
            pathformat = (
                "satellite/mmo/cdf/mppe/mea/" + level +"/"
                + datatypedir + "/%Y/%m/"
                + "bc_mmo_mppe-"+sensor+"_" + lev + "_" + data_mode + "-" + datatype + "-"+enestep+"e_%Y%m%d_r??-v??-??.cdf"
            )
        
        tvars = load(trange=trange,
                        instrument='mea', 
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
                        force_download=force_download,
                        uname=uname, passwd=passwd,
                        files=files
                        )
        if downloadonly is True:    
            return None
        
        # Decorate tplot variables
        if level == "l2pre":
            if data_mode == "l":
                match datatype:
                    case "omniflux":
                        vn = prefix+"omni_deflux"
                        options( vn, "spec", 1)
                        options( vn, "yrange", [1e+0, 30e+3])
                        options( vn, "ylog", 1)
                        options( vn, "zrange", [1e+4, 1e+9])
                        options( vn, "zlog", 1)
                        options( vn, "ysubtitle", "[eV]")
                        options( vn, "ztitle", "[eV/cm^2/s/sr/eV]")
                        options( vn, "ytitle", "BC/MMO\n"+sensor.upper()+"\nL2p omni\nene flux")
                    case "3dflux":
                        vn = prefix+"omni_deflux"
                        options( vn, "spec", 1)
                        options( vn, "yrange", [1e+0, 30e+3])
                        options( vn, "ylog", 1)
                        options( vn, "zrange", [1e+4, 1e+9])
                        options( vn, "zlog", 1)
                        options( vn, "ysubtitle", "[eV]")
                        options( vn, "ztitle", "[eV/cm^2/s/sr/eV]")
                        options( vn, "ytitle", "BC/MMO\n"+sensor.upper()+"\nL2p 3D\nene flux")

            elif data_mode == "m":
                # Currently, only L-mode data is available
                print("M-mode data is currently not available.")
        
    
    
    return tvars





