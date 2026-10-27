from ....mmo.load import load
from pyspedas import store_data, tplot_names,tnames
from pyspedas import options, ylim, zlim, get_data

from typing import List, Optional


import logging

def ofa(
        trange: List[str] = ["2021-10-1","2021-10-2"],
        level: str = 'l2p',
        data_mode: str = 'l',
        datatype: str = 'spec',
        obs_mode: str ='ms',
        field_mode: str = 'b',
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
        force_download=False
): 
    """
    This function loads data from the Plasma Wave Investigation (PWI) - Onboard Frequency Analyzer (OFA) onboard the MMO spacecraft.
    
    Parameters
    ------------
        trange: list or str  
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']
            (default: ["2021-8-10","2021-8-11"])
        
        level: str
            Data level (default: l2pre)
        
        data_mode: str
            Data mode, 'l' for the low data mode (L-mode; default), 'm' for M-mode
        
        datatype: str
            Data type, 'spec' for F-t diagram all data (default)
        
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
            Return the data in hash tables instead of creating tplot variables.
            (default: False)
        
        no_update: bool
            If set, only load data from your local cache.
            (default: False)
        
        force_download: bool,
            Download file even if local version is more recent than server version.
            (default: False)
        
        uname = str
        passwd = str
            Password for accessing restricted data products.
            Please contact the PI teams (or the project team) to obtain authentication credentials.
            Access to l2pre data is restricted and generally limited to project members.

        time_clip: bool
            Time clip the variables to exactly the range specified in the trange keyword.
            (default: True)
            
    Returns
    ----------
        List of tplot variables created.

    Sample data of the MIA is located at the CHS repository
    https://chs.isee.nagoya-u.ac.jp/data/chs/satellite/mmo/cdf/pwi/ofa/l2pre/spec/2021/10/bc_mmo_pwi-ofa_l2p_l-spec-ms_20211001_r01-v00-00.cdf
    """

    initial_notplot_flag = False
    if notplot:
        initial_notplot_flag = True

    file_res = 3600. * 24
    prefix = 'mmo_pwi_ofa_'+level+'_'+data_mode+'_'+obs_mode+'_'
    if level == 'l2p': 
        leveldir = 'l2pre'
    
    if local_dir: 
        pathformat = local_dir+\
            '/%Y/%m/bc_mmo_pwi-ofa_'+level+'_'+data_mode+'-'+datatype+'-'+field_mode+'-'+obs_mode+'_%Y%m%d_r??-v??-??.cdf'
    else:
        pathformat = 'satellite/mmo/cdf/pwi/ofa/'+leveldir+'/'+datatype+'/'+data_mode + \
            '/%Y/%m/bc_mmo_pwi-ofa_'+level+'_'+data_mode+'-'+datatype+'-'+field_mode+'-'+obs_mode+'_%Y%m%d_r??-v??-??.cdf'

    loaded_data = load(trange=trange,
                    instrument='ofa', 
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
            store_data(prefix+field_mode+'_spectra_merged', data=tnames(prefix+'spec_'+field_mode+'*'))
            options(prefix+field_mode+'_spectra_merged', 'ytitle', 'MIO PWI/OFA-SPEC ('+field_mode.upper()+')')
            
        case 'm':
            match field_mode:
                case 'e':
                    store_data(prefix+'eu_spectra_merged', data=tnames(prefix+'spec_eu*'))
                    store_data(prefix+'ev_spectra_merged', data=tnames(prefix+'spec_ev*'))
                    options(prefix+'eu_spectra_merged', 'ytitle', 'MIO PWI/OFA-SPEC (Eu)')
                    options(prefix+'ev_spectra_merged', 'ytitle', 'MIO PWI/OFA-SPEC (Ev)')
                
                case 'b':
                    b_comp = ['alpha','beta','gamma']
                    for cs in range(3):
                        if tnames(prefix+['spec_b'+b_comp[cs]+'_*']) != '':
                            store_data(prefix+'b'+b_comp[cs]+'_spectra_merged', data=tnames(prefix+'spec_b'+b_comp[cs]+'*'))
                            options(prefix+'b'+b_comp[cs]+'_spectra_merged', 'ytitle', 'MIO PWI/OFA-SPEC (B'+b_comp[cs]+')')

    # set ysubtitle
    options(prefix+'*_spectra_*'+suffix,  'ysubtitle', 'frequency [kHz]')
    
    # set yrange
    options(prefix+'*_spectra_*'+suffix,  'yrange', [1e1,1e5])
    
    # set y axis to logscale
    options(prefix+'*_spectra_*'+suffix,  'ylog', 1)
    
    # set ztitle
    options(prefix+'e*_spectra_*'+suffix,  'ztitle', 'dBmVpp')
    options(prefix+'b*_spectra_*'+suffix,  'ztitle', 'pT^2/Hz')

    # set z axis to logscale
    options(prefix+'e*_spectra_*'+suffix,  'zlog', 1)
    options(prefix+'e*_spectra_*'+suffix,  'zlog', 1)

    # change colormap option
    options(prefix+'e*_spectra_*'+suffix,  'Colormap', 'jet')
    options(prefix+'e*_spectra_*'+suffix,  'Colormap', 'jet')

    return loaded_data
