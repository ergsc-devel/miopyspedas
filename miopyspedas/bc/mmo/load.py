#/miopyspedas/miopyspedas/bc/mmo/load.py

from pyspedas.utilities.dailynames import dailynames
from pyspedas.utilities.download import download
from pytplot import time_clip as tclip
from pytplot import cdf_to_tplot

from .config import CONFIG

def load(trange=["2021-8-10","2021-8-11"], 
        pathformat=None,
        instrument='spm',
        datatype=None,
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
        uname=None, 
        passwd=None,
        mode=None,
        site=None,
        model=None,
        file_res=None,
        version=None,
        ):

    """
    This function is not meant to be called directly; please see the instrument specific wrappers:
        pyspedas.projects.mmo.spm()
    """


    """
    Load MMO data files for a given time range and instrument.
    **このコメント文はまだMAVENのload moduleからコピペしただけのため要編集
    
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
            **force_downloadの説明文を追記する
            (default: False)
        
        uname = str
        passwd = str
            We constrain the person for providing l2pre data.
            Please ask the CHS members to issue your username and password.
            **uname, passwordを使っている理由を確認する

    Returns
    ----------
    list of str
        List of loaded data variables or files downloaded.
    """

    if instrument == "spm":
        # https://chs.isee.nagoya-u.ac.jp/data/chs/satellite/mmo/cdf/spm/l2pre/cnt/2021/08/bc_mmo_spm_l2p_cnt_20210810_r01-v00-00.cdf
        # for spm: level=l2pre, datatype=
        pathformat = (
            "satellite/mmo/cdf/spm/" + str(level) 
            + "/cnt/%Y/%m/"
            + "bc_mmo_spm_l2p_cnt_%Y%m%d_r??-v??-??.cdf"
        )

        remote_names = dailynames(file_format=pathformat, trange=trange)
        prefix = 'mmo_spm_l2p_'

    # elif instrument == "": # other instruments
    # Modules for other instruments will be added...


# find the full remote path names using the trange
    remote_names = dailynames(file_format=pathformat, trange=trange)
    out_files = []

    files = download(
            remote_file=remote_names,
            remote_path=CONFIG["remote_data_dir"],
            local_path=CONFIG['local_data_dir'],
            no_update=no_update,
            force_download=force_download,
            username=uname, password=passwd,
        )

    if files is not None:
        for file in files:
            out_files.append(file)

    out_files = sorted(out_files)

    if downloadonly:
        return out_files


    tvars = cdf_to_tplot(
        out_files,
        prefix=prefix,
        suffix=suffix,
        get_support_data=get_support_data,
        varformat=varformat,
        varnames=varnames,
        notplot=notplot,
    )

    if tvars is None or notplot:
        return tvars

    if time_clip:
        for new_var in tvars:
            tclip(new_var, trange[0], trange[1], suffix="")

    return tvars