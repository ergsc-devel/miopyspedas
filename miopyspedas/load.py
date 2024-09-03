from pyspedas.utilities.dailynames import dailynames
from pyspedas.utilities.download import download
from pytplot import time_clip as tclip
from pytplot import cdf_to_tplot

from .config import CONFIG

def load(trange=["2021-8-10","2021-8-11"], 
        instrument='spm',
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
    

# find the full remote path names using the trange
    remote_names = dailynames(file_format=pathformat, trange=trange)

    out_files = []


    files = download(
            remote_file=remote_names,
            remote_path=CONFIG["remote_data_dir"],
            local_path=CONFIG['local_data_dir'],
            no_download=no_update,
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