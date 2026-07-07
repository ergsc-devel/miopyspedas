from ....mmo.load import load
from pyspedas import store_data, tplot_names,tnames
from pyspedas import options, ylim, zlim, get_data

from typing import List, Optional


import logging

def am2p(
        trange: List[str] = ["2023-02-28","2023-02-29"],
        level: str = 'l2',
        data_mode: str = 'l',
        datatype: str = 'spec',
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
): 
    """
    This function loads data from the Plasma Wave Investigation (PWI) - Onboard Frequency Analyzer (OFA) onboard the MMO spacecraft.
    
    Parameters (Draft)
    ------------
        trange: list or str  
            time range of interest [starttime, endtime] with the format 
            ['YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']
            (default: ["2021-8-10","2021-8-11"])
        
        level: str
            Data level (default: l2pre) --> after MOI default will be l2

        data_mode: str
            Data mode, 'l' for the low data mode (L-mode; default), 'm' for M-mode
        
        datatype: str
            Data type, 'spec' for calibrated science spectra data (default), and 'cal' for calibration data (=reference spectra data)
        
        obs_mode: str
            Observation mode, 'ms' for magnetosphere (default), 'sw' for the solar wind
        
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
            
    Returns
    ----------
        List of tplot variables created.

    Sample data of the MIA is located at the CHS repository
    https://chs.isee.nagoya-u.ac.jp/data/chs/satellite/mmo/cdf/pwi/ofa/l2/spec/2023/02/bc_mmo_pwi-am2p_l2_l-spec_20230228_r01-v00-00.cdf
    """

    initial_notplot_flag = False
    if notplot:
        initial_notplot_flag = True

    file_res = 3600. * 24

    # --- Normalize the requested level FIRST, before deciding prefix/suffix or
    #     building the path, so that `level` becomes a single clean canonical
    #     value we can rely on everywhere below (path, prefix, load() call).
    #
    # normalization / use lower capitals --> remove space --> "level" to "l"
    # e.g. "level 2 pre", "L2PRE", "l2 p" --> "l2pre"
    level_key = level.lower().replace(" ", "").replace("level", "l")

    if level_key in ("l2pre", "l2p"):
        level = "l2pre"
    elif level_key in ("l2", "l3"):
        level = level_key
    else:
        raise ValueError(f"Unsupported level: {level!r}")
    
    if datatype == "spec":
        prefix = 'mmo_pwi-am2p_'+level+'_'+data_mode+'_'+datatype+'_'

        if local_dir: 
            pathformat = local_dir+\
                '/%Y/%m/bc_mmo_pwi-am2p_'+level+'_'+data_mode+'-'+datatype+'_%Y%m%d_r??-v??-??.cdf'
        else:
            pathformat = 'satellite/mmo/cdf/pwi/am2p/'+level+'/'+datatype+'/'+data_mode + \
                '/%Y/%m/bc_mmo_pwi-am2p_'+level+'_'+data_mode+'-'+datatype+'_%Y%m%d_r??-v??-??.cdf'

    elif datatype == "cal":
        prefix = 'mmo_pwi-am2p_'+level+'_'+data_mode+'_'+datatype+'-' + obs_mode + '_'
        if local_dir: 
            pathformat = local_dir+\
                '/%Y/%m/bc_mmo_pwi-am2p_'+level+'_'+data_mode+'-'+datatype+ '-'+ obs_mode +'_%Y%m%d_r??-v??-??.cdf'
        else:
            pathformat = 'satellite/mmo/cdf/pwi/am2p/'+level+'/'+datatype+'/'+data_mode + \
                '/%Y/%m/bc_mmo_pwi-am2p_'+level+'_'+data_mode+'-'+datatype+ '-'+ obs_mode +'_%Y%m%d_r??-v??-??.cdf'


    loaded_data = load(trange=trange,
                    instrument='am2p', 
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
                    force_download=False,
                    uname=uname, passwd=passwd
                    )

    if initial_notplot_flag or downloadonly:
        return loaded_data

    # set spectrogram plot option
    options(prefix+'spec_e*'+suffix,  'Spec', 1)
    options(prefix+'spec_b*'+suffix,  'Spec', 1)

    # set y axis to logscale
    options(prefix+'spec_e*'+suffix,  'ylog', 1)
    options(prefix+'spec_b*'+suffix,  'ylog', 1)

    #  Merge spectrogram
    match data_mode:
        case 'l':
            store_data(prefix+'e_spectra_merged', data=tnames(prefix+'spec_e_*'))
            store_data(prefix+'b_spectra_merged', data=tnames(prefix+'spec_b_*'))  
            options(prefix+'e_spectra_merged', 'ytitle', 'MIO PWI/OFA-SPEC (E)')
            options(prefix+'b_spectra_merged', 'ytitle', 'MIO PWI/OFA-SPEC (B)')
        case 'm':
            store_data(prefix+'ex_spectra_merged', data=tnames(prefix+'spec_ex_*'))
            store_data(prefix+'ey_spectra_merged', data=tnames(prefix+'spec_ey_*'))

            store_data(prefix+'by_spectra_merged', data=tnames(prefix+'spec_by_*'))
            store_data(prefix+'bz_spectra_merged', data=tnames(prefix+'spec_bz_*'))

            options(prefix+'ex_spectra_merged', 'ytitle', 'MIO PWI/OFA-SPEC (Ex)')
            options(prefix+'ey_spectra_merged', 'ytitle', 'MIO PWI/OFA-SPEC (Ey)')

            options(prefix+'by_spectra_merged', 'ytitle', 'MIO PWI/OFA-SPEC (By)')
            options(prefix+'bz_spectra_merged', 'ytitle', 'MIO PWI/OFA-SPEC (Bz)')


    # set ysubtitle
    options(tnames(prefix+'*_spectra_*'+suffix),  'ysubtitle', 'frequency [kHz]')
    
    # set yrange
    options(tnames(prefix+'*_spectra_*'+suffix),  'yrange', [1e1,1e5])
    
    # set y axis to logscale
    options(tnames(prefix+'*_spectra_*'+suffix),  'ylog', 1)
    
    # set ztitle
    options(tnames(prefix+'e*_spectra_*'+suffix),  'ztitle', 'dBmVpp')
    options(tnames(prefix+'b*_spectra_*'+suffix),  'ztitle', 'pT^2/Hz')

    # set z axis to logscale
    options(tnames(prefix+'e*_spectra_*'+suffix),  'zlog', 1)
    options(tnames(prefix+'e*_spectra_*'+suffix),  'zlog', 1)

    # change colormap option
    options(tnames(prefix+'e*_spectra_*'+suffix),  'Colormap', 'jet')
    options(tnames(prefix+'e*_spectra_*'+suffix),  'Colormap', 'jet')

    return loaded_data
