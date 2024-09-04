from miopyspedas.load import load
from pytplot import options

import logging

def spm(
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
    
    Parameters
    ------------
        trange: list or str  
            time range of interest [starttime, endtime] with the format 
            'YYYY-MM-DD','YYYY-MM-DD'] or to specify more or less than a day 
            ['YYYY-MM-DD/hh:mm:ss','YYYY-MM-DD/hh:mm:ss']
            (default: ["2021-8-10","2021-8-11"])
        
        level: str
            Data level (default: l2pre)
        
        prefix: str
            The tplot variable names will be given this prefix.
            By default, no prefix is added.

        suffix: str
            The tplot variable names will be given this suffix.
            By default, no prefix is added.

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

        time_clip: bool
            Time clip the variables to exactly the range specified in the trange keyword.
            (default: True)

        force_download=False,
            (default: False)
        
        uname = str
        passwd = str
            We constrain the person for providing l2pre data.
            Please ask the CHS members to issue your username and password.

    Returns
    ----------
        List of tplot variables created.

    Sample data of the SPM is located at the CHS repository
    https://chs.isee.nagoya-u.ac.jp/data/chs/satellite/mmo/cdf/spm/l2pre/cnt/2021/08/bc_mmo_spm_l2p_cnt_20210810_r01-v00-00.cdf
    """

    if prefix is None:
        prefix = ""
    
    if suffix is None:
        suffix = ""
        
    spm_vars = load(trange=trange,
                    instrument='spm', 
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
                    no_update=no_update,
                    force_download=False,
                    uname=None, passwd=None
                    )

    return spm_vars





