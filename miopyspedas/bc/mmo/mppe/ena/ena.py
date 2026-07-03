from ....mmo.load import load
from pyspedas import options

import logging

def ena(
        trange=["2020-04-09","2020-04-10"],
        level="l2pre",
        data_mode="l",
        datatype='mass',
        obs_mode="np01-nm04",
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
    This function loads data from the Mercury Plasma Particle Experiment (MPPE) - Energetic Neutral Atoms (ENA) onboard the MMO spacecraft.
    
    Parameters
    ------------
        trange: list or str  
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']
            (default: ["2020-04-09","2020-04-10"])
        
        level: str
            Data level (default: l2pre)
        
        data_mode: str
            Data rate mode, 'l' for the low data rate mode (L-mode; default)
        
        datatype: str
            Data type; 'mass' for the mass accumulation mode data (default), 'cnt' for the count accumulation mode data
        
        obs_mode: str
            Observation mode
            In this module, this represents the number of the spin phase and the TOF bin.
            For the count accumulation mode, 'np??', where ?? = 01, 02, 04, 08, and 16
            For the mass accumulation mode, 'np??-nm??', where ?? = 01, 02, 04, and 08

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
        
        uname = str
        passwd = str
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
    https://chs.isee.nagoya-u.ac.jp/data/chs/satellite/mmo/cdf/mppe/ena/l2pre/l/mass/np01-nm04/2020/04/bc_mmo_mppe-ena_l2p_l-mass-np01-nm04_20200409_r01-v00-00.cdf
    """

    if suffix is None:
        suffix = ""
    
    if level == "l2pre":
        lev = "l2p"
    else:
        lev = level
    
    if prefix == "":
        prefix = "mmo_ena_"+lev+"_"+data_mode+"_"+datatype+"-"+obs_mode+'_'
    
    
    if files is None:
        pathformat = f"satellite/mmo/cdf/mppe/ena/{level}/{data_mode}/{datatype}/{obs_mode}/%Y/%m/" + \
            f"bc_mmo_mppe-ena_{lev}_{data_mode}-{obs_mode}_%Y%m%d_r??-v??-??.cdf"
    
    tvars = load(trange=trange,
                    instrument='ena', 
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
                    uname=uname, passwd=uname,
                    files=files
                    )
    if downloadonly is True:    
        return None
    
    # Decorate tplot variables
    if level == "l2pre":

        if data_mode == "l":

            match datatype:
                case "mass":
                    # coincident count
                    options( prefix+"c_cnt_tot", "yrange", [20.0, 2560.0])
                    options( prefix+"c_cnt_tot", "ylog", 1)
                    options( prefix+"c_cnt_tot", "ysubtitle", "[eV]")
                    options( prefix+"c_cnt_tot", "zlog", 1)
                    options( prefix+"c_cnt_tot", "zrange", [1e0, 1e4])
                    options( prefix+"c_cnt_tot", "ztitle", "[cnt/smpl]")
                    options( prefix+"c_cnt_tot", "spec", 1)
                    # total coincident count
                    options( prefix+"c_cnt", "yrange", [20.0, 2560.0])
                    options( prefix+"c_cnt", "ylog", 1)
                    options( prefix+"c_cnt", "ysubtitle", "[eV]")
                    options( prefix+"c_cnt", "zlog", 1)
                    options( prefix+"c_cnt", "zrange", [1e0, 1e4])
                    options( prefix+"c_cnt", "ztitle", "[cnt/smpl]")
                    options( prefix+"c_cnt", "spec", 1)
                    # uncorrected flux
                    options( prefix+"uncorrected_flux", "yrange", [20.0, 2560.0])
                    options( prefix+"uncorrected_flux", "ylog", 1)
                    options( prefix+"uncorrected_flux", "ysubtitle", "[eV]")
                    options( prefix+"uncorrected_flux", "zlog", 1)
                    options( prefix+"uncorrected_flux", "zrange", [1e0, 1e4])
                    options( prefix+"uncorrected_flux", "ztitle", "[/s/cm^2/eV/sr]")
                    options( prefix+"uncorrected_flux", "spec", 1)
                    # corrected flux
                    options( prefix+"corrected_flux", "yrange", [20.0, 2560.0])
                    options( prefix+"corrected_flux", "ylog", 1)
                    options( prefix+"corrected_flux", "ysubtitle", "[eV]")
                    options( prefix+"corrected_flux", "zlog", 1)
                    options( prefix+"corrected_flux", "zrange", [1e0, 1e4])
                    options( prefix+"corrected_flux", "ztitle", "[/s/cm^2/eV/sr]")
                    options( prefix+"corrected_flux", "spec", 1)
                case "cnt":
                    # coincident start sector count
                    options( prefix+"c_sta_s_cnt", "yrange", [20.0, 2560.0])
                    options( prefix+"c_sta_s_cnt", "ylog", 1)
                    options( prefix+"c_sta_s_cnt", "ysubtitle", "[eV]")
                    options( prefix+"c_sta_s_cnt", "zlog", 1)
                    options( prefix+"c_sta_s_cnt", "zrange", [1e0, 1e4])
                    options( prefix+"c_sta_s_cnt", "ztitle", "[cnt/smpl]")
                    options( prefix+"c_sta_s_cnt", "spec", 1)
                    # coincident stop sector count
                    options( prefix+"c_sto_s_cnt", "yrange", [20.0, 2560.0])
                    options( prefix+"c_sto_s_cnt", "ylog", 1)
                    options( prefix+"c_sto_s_cnt", "ysubtitle", "[eV]")
                    options( prefix+"c_sto_s_cnt", "zlog", 1)
                    options( prefix+"c_sto_s_cnt", "zrange", [1e0, 1e4])
                    options( prefix+"c_sto_s_cnt", "ztitle", "[cnt/smpl]")
                    options( prefix+"c_sto_s_cnt", "spec", 1)
                    # uncorrected flux
                    options( prefix+"uncorrected_flux", "yrange", [20.0, 2560.0])
                    options( prefix+"uncorrected_flux", "ylog", 1)
                    options( prefix+"uncorrected_flux", "ysubtitle", "[eV]")
                    options( prefix+"uncorrected_flux", "zlog", 1)
                    options( prefix+"uncorrected_flux", "zrange", [1e0, 1e4])
                    options( prefix+"uncorrected_flux", "ztitle", "[/s/cm^2/eV/sr]")
                    options( prefix+"uncorrected_flux", "spec", 1)
                    # corrected flux
                    options( prefix+"corrected_flux", "yrange", [20.0, 2560.0])
                    options( prefix+"corrected_flux", "ylog", 1)
                    options( prefix+"corrected_flux", "ysubtitle", "[eV]")
                    options( prefix+"corrected_flux", "zlog", 1)
                    options( prefix+"corrected_flux", "zrange", [1e0, 1e4])
                    options( prefix+"corrected_flux", "ztitle", "[/s/cm^2/eV/sr]")
                    options( prefix+"corrected_flux", "spec", 1)
                case _:
                    print("Invalid observation mode")

        elif data_mode == "m":
            # Only L-mode data is available
            print("M-mode data is not available.")

        elif data_mode == "h":
            # Only L-mode data is available
            print("H-mode data is not available.")
    
    # Return
    return tvars
