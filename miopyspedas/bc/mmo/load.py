#/miopyspedas/miopyspedas/bc/mmo/load.py

import cdflib
from pyspedas.utilities.dailynames import dailynames
from pyspedas.utilities.download import download
from pyspedas import time_clip as tclip
from pyspedas import cdf_to_tplot

from .config import CONFIG

    """
    This function is not meant to be called directly; please see the instrument specific wrappers:
        pyspedas.projects.mmo.spm()

    Load MMO data files for a given time range and instrument.
    
    
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
    list of str
        List of loaded data variables or files downloaded.
    """

    # elif instrument == "": # other instruments
    # Modules for other instruments will be added...


    # find the full remote path names using the trange
    remote_names = dailynames(file_format=pathformat,
                              trange=trange, 
                              res=file_res)
    
    out_files = []
    # Download data files and set their paths unless local file paths are explicitly given
    if files is None:
        files = download(remote_file=remote_names,
                         remote_path=CONFIG["remote_data_dir"],
                         local_path=CONFIG["local_data_dir"],
                         no_download=no_update,
                         last_version=True,
                         force_download=force_download,
                         username=uname,
                         password=passwd)
    
    if files is not None:
        for file in files:
            out_files.append(file)

    out_files = sorted(out_files)

    if downloadonly:
        return out_files

    tvars = cdf_to_tplot(out_files, 
                         prefix=prefix, 
                         suffix=suffix, 
                         get_support_data=get_support_data,
                         varformat=varformat, 
                         varnames=varnames, 
                         notplot=notplot)

    if notplot:
        if len(out_files) > 0:
            cdf_file = cdflib.CDF(out_files[-1])
            cdf_info = cdf_file.cdf_info()
            # cdflib >= 1.0 returns a CDFInfo dataclass, so use attribute access.
            all_cdf_variables = cdf_info.rVariables + cdf_info.zVariables
            gatt = cdf_file.globalattsget()
            for var in all_cdf_variables:
                t_plot_name = prefix + var + suffix
                if t_plot_name in tvars:
                    vatt = cdf_file.varattsget(var)
                    tvars[t_plot_name]['CDF'] = {"VATT":vatt,
                                                "GATT":gatt,
                                                "FILENAME":out_files}
        return tvars

    if time_clip:
        for new_var in tvars:
            tclip(new_var, trange[0], trange[1], suffix="")

    return tvars
