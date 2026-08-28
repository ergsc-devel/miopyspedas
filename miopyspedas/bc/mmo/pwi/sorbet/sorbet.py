from ....mmo.load import load
from pyspedas import options

import logging
from typing import List, Optional

def sorbet( trange: List[str] = ['2025-4-10','2025-4-11'],
        level: str = 'l2p',
        data_mode: str = 'lm',
        datatype: str = 'tnr-e',
        obs_mode: str = '',
        prefix: str = '',
        suffix: str = '',
        local_dir:Optional[str] = None,
        bool = False,
        get_support_data=False,
        varformat: Optional[str] = None,
        varnames: List[str] = [],
        downloadonly: bool = False,
        notplot: bool = False,
        no_update: bool = False,
        uname: Optional[str] = None,
        passwd: Optional[str] = None,
        time_clip: bool = False,
        force_download=False,
        files=None
):
    """
    This function loads data from the Plasma Wave Investigation (PWI) - Spectroscopie Ondes Radio & Bruit Electrostatique Thermique (SORBET) onboard the MMO spacecraft.
    
    Parameters
    ------------
        trange: list or str  
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']
            (default: ["2021-10-1","2021-10-2"])
        
        level: str
            Data level (default: l2p)
        
        data_mode: str
            Data rate mode, 'lm' for the low-medium data rate mode (LM-mode; default)
        
        datatype: str
            Data type, 'tnr-e' (default), 'hfr-e', 'tnr-dbsc', 'tnr-e-cross-b'
        
        obs_mode: str
            Observation mode, ''

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

        varformat = str
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

    Sample data of the SORBET is located at the CHS repository
    https://chs.isee.nagoya-u.ac.jp/data/chs/satellite/mmo/cdf/pwi/sorbet/l2pre/lm/tnr-e/2025/04/bc_mmo_pwi-sorbet_l2p_lm-tnr-e_20250410_r00-v00-02.cdf
    """

    if suffix is None:
        suffix = ''
    
    if level == 'l2pre':
        lev = 'l2p'
    else:
        lev = level
    
    if level == 'l2p':
        level = 'l2pre'
    
    if prefix == '':
        if obs_mode == '':
            prefix = 'mmo_pwi_sorbet_'+lev+'_'+data_mode+'_'+datatype+'_'
        else:
            prefix = 'mmo_pwi_sorbet_'+lev+'_'+data_mode+'_'+obs_mode+'_'+datatype+'_'
    
    if obs_mode != '':
        data_mode = data_mode+'-'+obs_mode

    initial_notplot_flag = False
    if notplot:
        initial_notplot_flag = True

    file_res = 3600. * 24

    if files is None:
        if local_dir: 
            pathformat = local_dir+\
                f'/%Y/%m/bc_mmo_pwi-sorbet_{lev}_{data_mode}-{datatype}_%Y%m%d_r??-v??-??.cdf'
        else:
            pathformat = f'satellite/mmo/cdf/pwi/sorbet/{level}/{data_mode}/{datatype}' + \
                f'/%Y/%m/bc_mmo_pwi-sorbet_{lev}_{data_mode}-{datatype}_%Y%m%d_r??-v??-??.cdf'

    
    loaded_data = load(trange=trange,
                    instrument='sorbet', 
                    pathformat=pathformat,
                    level=level,
                    datatype=datatype,
                    prefix=prefix, 
                    suffix=suffix,
                    get_support_data=get_support_data, 
                    varformat=varformat, 
                    varnames=varnames,
                    downloadonly=downloadonly,
                    notplot=notplot,
                    file_res=file_res,
                    no_update=no_update,
                    time_clip=time_clip,
                    force_download=force_download,
                    uname=uname,
                    passwd=passwd,
                    files=files
                    )

    if initial_notplot_flag or downloadonly:
        return loaded_data
    
    # Decorate tplot variables
    if level == 'l2pre':
        if data_mode == 'lm':
            match datatype:
                case 'tnr-e':
                    options( prefix+'E?_power*', 'spec', 1)
                    options( prefix+'E?_power*', 'yrange', [2e3, 7e5])
                    options( prefix+'E?_power*', 'ylog', 1)
                    options( prefix+'E?_power*', 'ysubtitle', '[Hz]')
                    options( prefix+'E?_power*', 'zlog', 1)
                    options( prefix+'E?_power'+suffix, 'ztitle', '[W/m^2/Hz] rms')
                    options( prefix+'E?_power_v2'+suffix, 'ztitle', '[V^2/Hz] rms')
                    options( prefix+'E?_power_db'+suffix, 'ztitle', '[edB] rms')
                    options( prefix+'Eu_power'+suffix, 'ytitle', 'BC/MMO-PWI\nSORBET L2p\nSpectral flux density!CEu (WPT)')
                    options( prefix+'Ev_power'+suffix, 'ytitle', 'BC/MMO-PWI\nSORBET L2p\nSpectral flux density!CEv (MEF)')
                    options( prefix+'Eu_power_v2'+suffix, 'ytitle', 'BC/MMO-PWI\nSORBET L2p\nPower spectral density!CEu (WPT)')
                    options( prefix+'Ev_power_v2'+suffix, 'ytitle', 'BC/MMO-PWI\nSORBET L2p\nPower spectral density!CEv (MEF)')
                    options( prefix+'Eu_power_db'+suffix, 'ytitle', 'BC/MMO-PWI\nSORBET L2p\nPower above BG!CEu (WPT)')
                    options( prefix+'Ev_power_db'+suffix, 'ytitle', 'BC/MMO-PWI\nSORBET L2p\nPower above BG!CEv (MEF)')
                    options( prefix+'EuEv_cross_?'+suffix, 'spec', 1)
                    options( prefix+'EuEv_cross_?'+suffix, 'yrange', [2e3, 7e5])
                    options( prefix+'EuEv_cross_?'+suffix, 'ylog', 1)
                    options( prefix+'EuEv_cross_?'+suffix, 'ysubtitle', '[Hz]')
                    options( prefix+'EuEv_cross_?'+suffix, 'zlog', 1)
                    options( prefix+'EuEv_cross_?'+suffix, 'ztitle', '')
                    options( prefix+'EuEv_cross_r'+suffix, 'ytitle', 'BC/MMO-PWI\nSORBET L2p\nReal part of!Ccross-correlation (EuEv)')
                    options( prefix+'EuEv_cross_i'+suffix, 'ytitle', 'BC/MMO-PWI\nSORBET L2p\nImaginary part of!Ccross-correlation (EuEv)')
                case 'hfr-e':
                    options( prefix+'Eu_power*', 'spec', 1)
                    options( prefix+'Eu_power*', 'yrange', [5e5, 1.1e7])
                    options( prefix+'Eu_power*', 'ylog', 1)
                    options( prefix+'Eu_power*', 'ysubtitle', '[Hz]')
                    options( prefix+'Eu_power*', 'zlog', 1)
                    options( prefix+'Eu_power'+suffix, 'ztitle', '[W/m^2/Hz] rms')
                    options( prefix+'Eu_power_v2'+suffix, 'ztitle', '[V^2/Hz] rms')
                    options( prefix+'Eu_power_db'+suffix, 'ztitle', '[edB] rms')
                    options( prefix+'Eu_power'+suffix, 'ytitle', 'BC/MMO-PWI\nSORBET L2p\nSpectral flux density!CEu (WPT)')
                    options( prefix+'Eu_power_v2'+suffix, 'ytitle', 'BC/MMO-PWI\nSORBET L2p\nPower spectral density!CEu (WPT)')
                    options( prefix+'Eu_power_db'+suffix, 'ytitle', 'BC/MMO-PWI\nSORBET L2p\nPower above BG!CEu (WPT)')


        elif data_mode == "m":
            # Currently, only L-mode data is available
            print("M-mode data is currently not available.")
    


    return loaded_data





