from pyspedas.utilities.dailynames import dailynames
from pyspedas.utilities.download import download
from pytplot import time_clip as tclip
from pytplot import cdf_to_tplot

from miopyspedas.config import CONFIG

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
    Load BepiColombo/MMO SPM data from the CHS repository

    https://chs.isee.nagoya-u.ac.jp/data/chs/satellite/mmo/cdf/spm/l2pre/cnt/2021/08/bc_mmo_spm_l2p_cnt_20210810_r01-v00-00.cdf
    """

    out_files = [] # list of local files downloaded
    tvars = [] # list of tplot variables created


    pathformat = (
        "satellite/mmo/cdf/spm/" + str(level) 
        + "/cnt/%Y/%M/"
        + "bc_mmo_spm_l2p_cnt_%Y%M%D_r??-v??-??.cdf"
    )

    remote_names = dailynames(file_format=pathformat, trange=trange)
    remote_data_dir = CONFIG['remote_data_dir']
    prefix = 'mmo_spm_l2p_'

    files = download(
        remote_file=remote_names,
        remote_path=remote_data_dir,
        local_path=CONFIG['local_data_dir'],
        no_download=no_update,
        force_download=force_download,
        username=uname, password=passwd,
    )

    out_files_local = []
    if files is not None:
        for file in files:
            out_files_local.append(file)
    
    out_files.extend(out_files_local)

    tvars_local = []
    if not downloadonly:
        tvars_local = cdf_to_tplot(
            out_files_local,
            prefix=prefix,
            suffix=suffix,
            get_support_data=get_support_data,
            varformat=varformat,
            varnames=varnames,
            notplot=notplot,
        )

        tvars.extend(tvars_local)

        if time_clip:
            tclip(tvars_local, trange[0], trange[1], suffix="")
    
    if downloadonly:
        return out_files
    
    return tvars





