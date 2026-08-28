from ....mmo.load import load

from pyspedas import (
    get_data,
    options,
    store_data,
    tnames,
    ylim,
    zlim,
)

from typing import List, Optional
import logging
import numpy as np


def efd(
    trange: Optional[List[str]] = None,
    level: str = "l2",
    data_mode: str = "l",
    datatype: str = "spec",
    obs_mode: str = "",
    coord: str = "",
    prefix: str = "",
    suffix: str = "",
    local_dir: Optional[str] = None,
    get_support_data: bool = False,
    varformat: Optional[str] = None,
    varnames: Optional[List[str]] = None,
    downloadonly: bool = False,
    notplot: bool = False,
    no_update: bool = False,
    uname: Optional[str] = None,
    passwd: Optional[str] = None,
    time_clip: bool = False,
    force_download: bool = False,
):
    """
    Load PWI/EFD data onboard the BepiColombo Mio spacecraft.

    Parameters
    ----------
    trange : list of str
        Time range [start_time, end_time].

    level : str
        Data level: "l2" or "l3".

    data_mode : str
        Data-rate mode: "l", "m" or "h".

    datatype : str
        "e_spin", "e_waveform", "pot",
        "pot_waveform" or "spec".

    obs_mode : str
        Observation mode. Reserved for compatibility.

    coord : str
        Coordinate system for e_waveform:
        "pwi" or "xsm".

    prefix, suffix : str
        Strings added to tplot variable names.

    local_dir : str, optional
        Local EFD data directory.

    get_support_data : bool
        Load CDF support_data variables.

    varformat : str, optional
        CDF variable wildcard.

    varnames : list of str, optional
        CDF variable names to load.

    downloadonly : bool
        Download files without making tplot variables.

    notplot : bool
        Return dictionaries instead of tplot variables.

    no_update : bool
        Use only locally cached files.

    uname, passwd : str, optional
        Authentication credentials.

    time_clip : bool
        Clip loaded variables to trange.

    force_download : bool
        Force file download.

    Returns
    -------
    list or dict
        Loaded variables, downloaded files, or notplot data.
    """

    if trange is None:
        trange = ["2018-11-19", "2018-11-20"]

    if varnames is None:
        varnames = []

    initial_notplot_flag = notplot

    level = level.lower()
    data_mode = data_mode.lower()
    datatype = datatype.lower()
    obs_mode = obs_mode.lower()
    coord = coord.lower()

    if level not in ("l2", "l3"):
        logging.error("level must be 'l2' or 'l3'.")
        return []

    if data_mode not in ("l", "m", "h"):
        logging.error("data_mode must be 'l', 'm' or 'h'.")
        return []

    valid_datatypes = (
        "e_spin",
        "e_waveform",
        "pot",
        "pot_waveform",
        "spec",
    )

    if datatype not in valid_datatypes:
        logging.error(
            "datatype must be one of %s",
            valid_datatypes,
        )
        return []

    # Coordinate is used only for electric-field waveform data.
    if datatype == "e_waveform":
        if coord == "":
            coord = "pwi"

        if coord not in ("pwi", "xsm"):
            logging.error(
                "coord must be 'pwi' or 'xsm'."
            )
            return []
    else:
        coord = ""

    file_res = 86400.0

    # Revised IDL:
    # prefix = mmo_pwi_efd_<level>_<datatype>_
    tplot_prefix = (
        f"{prefix}mmo_pwi_efd_{level}_{datatype}_"
    )

    coord_part = f"{coord}_" if coord else ""

    filename = (
        f"bc_mmo_pwi-efd_{level}_"
        f"{data_mode}-{datatype}_"
        f"{coord_part}"
        "%Y%m%d_r??-v??-??.cdf"
    )

    if local_dir:
        pathformat = (
            f"{local_dir}/%Y/%m/{filename}"
        )
    else:
        pathformat = (
            "satellite/mmo/cdf/pwi/efd/"
            f"{level}/{data_mode}/{datatype}/"
            f"%Y/%m/{filename}"
        )

    loaded_data = load(
        trange=trange,
        instrument="efd",
        pathformat=pathformat,
        level=level,
        datatype=datatype,
        prefix=tplot_prefix,
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
    )

    if initial_notplot_flag or downloadonly:
        return loaded_data

    if loaded_data is None:
        return []

    if datatype == "e_spin":
        _configure_e_spin(
            tplot_prefix,
            suffix,
            level,
            data_mode,
        )

    elif datatype == "e_waveform":
        _process_waveform(
            tplot_prefix,
            suffix,
            level,
            data_mode,
            coord,
        )

    elif datatype == "pot":
        _configure_potential(
            tplot_prefix,
            suffix,
            level,
            data_mode,
            waveform=False,
        )

    elif datatype == "pot_waveform":
        _configure_potential(
            tplot_prefix,
            suffix,
            level,
            data_mode,
            waveform=True,
        )

    elif datatype == "spec":
        _configure_spectra(
            tplot_prefix,
            suffix,
            level,
            data_mode,
        )

    return loaded_data


def _configure_e_spin(
    prefix: str,
    suffix: str,
    level: str,
    data_mode: str,
) -> None:

    if data_mode == "l":
        components = [
            "Eu_4hz_xsm",
            "Ev_4hz_xsm",
        ]
        labels = [
            ["Eu_4hz_x_xsm", "Eu_4hz_y_xsm"],
            ["Ev_4hz_x_xsm", "Ev_4hz_y_xsm"],
        ]

    elif data_mode == "m":
        components = [
            "Eu_8hz_xsm",
            "Ev_8hz_xsm",
        ]
        labels = [
            ["Eu_8hz_x_xsm", "Eu_8hz_y_xsm"],
            ["Ev_8hz_x_xsm", "Ev_8hz_y_xsm"],
        ]

    else:
        logging.warning(
            "e_spin is unavailable for h mode."
        )
        return

    titles = [
        f"PWI/EFD\nE-field (WPT)\nLv.{level[1:]}",
        f"PWI/EFD\nE-field (MEF)\nLv.{level[1:]}",
    ]

    for component, legend, title in zip(
        components,
        labels,
        titles,
    ):
        name = prefix + component + suffix

        options(name, "ytitle", title)
        options(name, "ysubtitle", "[mV/m]")
        options(name, "legend_names", legend)
        options(name, "constant", 0)


def _process_waveform(
    prefix: str,
    suffix: str,
    level: str,
    data_mode: str,
    coord: str,
) -> None:

    rate = {
        "l": "4hz",
        "m": "8hz",
        "h": "128hz",
    }[data_mode]

    fields = (
        ("Eu", "Ev")
        if coord == "pwi"
        else ("Ex", "Ey")
    )

    for field in fields:
        component = (
            f"{field}_waveform_{rate}_{coord}"
        )
        name = prefix + component + suffix
        data = get_data(name)

        if data is None:
            logging.warning(
                "Cannot find tplot variable: %s",
                name,
            )
            continue

        packet_time = np.asarray(
            data.times,
            dtype=np.float64,
        )
        waveform = np.asarray(data.y)

        if data.v is None:
            logging.warning(
                "Time offsets were not found: %s",
                name,
            )
            continue

        time_offset = np.asarray(
            data.v,
            dtype=np.float64,
        )

        if waveform.ndim != 2:
            logging.warning(
                "%s is not a two-dimensional waveform.",
                name,
            )
            continue

        if waveform.shape[1] != time_offset.size:
            raise ValueError(
                "Time-offset dimension does not match "
                f"waveform data: {name}"
            )

        # CDF time offsets are interpreted as milliseconds.
        time_new = (
            packet_time[:, None]
            + time_offset[None, :] * 1.0e-3
        ).reshape(-1)

        data_new = waveform.reshape(-1)

        metadata = get_data(
            name,
            metadata=True,
        )

        store_data(
            name,
            data={
                "x": time_new,
                "y": data_new,
            },
            attr_dict=metadata,
        )

        if coord == "xsm":
            title = (
                f"PWI/EFD\n{field} (XSM)\n"
                f"Lv.{level[1:]}"
            )
        else:
            title = (
                f"PWI/EFD\n{field}\n"
                f"Lv.{level[1:]}"
            )

        options(name, "ytitle", title)
        options(name, "ysubtitle", "[mV/m]")
        ylim(name, -20, 20)


def _configure_potential(
    prefix: str,
    suffix: str,
    level: str,
    data_mode: str,
    waveform: bool,
) -> None:

    if not waveform and data_mode == "h":
        logging.warning(
            "pot is unavailable for h mode."
        )
        return

    if waveform:
        rate = {
            "l": "1hz",
            "m": "8hz",
            "h": "32hz",
        }[data_mode]
        components = ["Vu1", "Vv1", "Vu2", "Vv2"]
    else:
        rate = {
            "l": "1hz",
            "m": "8hz",
        }[data_mode]
        components = [
            "Vu1",
            "Vv1",
            "Vu2",
            "Vv2",
            "Vave",
        ]

    for component in components:
        if waveform:
            variable_component = (
                f"{component}_waveform_{rate}"
            )
            description = f"{component} waveform"
        else:
            variable_component = (
                f"{component}_{rate}"
            )
            description = component

        name = (
            prefix + variable_component + suffix
        )

        options(
            name,
            "ytitle",
            f"PWI/EFD\nPot. ({description})\n"
            f"Lv.{level[1:]}",
        )
        options(name, "ysubtitle", "[V]")
        options(
            name,
            "legend_names",
            [variable_component],
        )
        options(name, "constant", 0)

        ylim(name, -2, 2)

    _configure_quality(
        prefix,
        suffix,
        level,
        "Pot.",
    )


def _configure_spectra(
    prefix: str,
    suffix: str,
    level: str,
    data_mode: str,
) -> None:

    if data_mode == "l":
        components = {
            "Eu_power_ave": "Eu ave. spec.",
            "Ev_power_ave": "Ev ave. spec.",
            "Eu_power_peak": "Eu peak spec.",
            "Ev_power_peak": "Ev peak spec.",
        }

    elif data_mode == "m":
        components = {
            "Eu_power": "Eu spec.",
            "Ev_power": "Ev spec.",
        }

    else:
        logging.warning(
            "spec is unavailable for h mode."
        )
        return

    for component, description in components.items():
        name = prefix + component + suffix

        options(name, "Spec", 1)
        options(
            name,
            "ytitle",
            f"PWI/EFD\n{description}\n"
            f"Lv.{level[1:]}",
        )
        options(
            name,
            "ysubtitle",
            "Frequency [Hz]",
        )
        options(
            name,
            "ztitle",
            "[mV^2/m^2/Hz]",
        )
        options(name, "ylog", 0)
        options(name, "zlog", 1)
        options(name, "Colormap", "jet")

        ylim(name, 0, 40)
        zlim(name, 1.0e-8, 1.0e-2)

    _configure_quality(
        prefix,
        suffix,
        level,
        "spec.",
    )


def _configure_quality(
    prefix: str,
    suffix: str,
    level: str,
    product: str,
) -> None:

    quality_flag = tnames(
        prefix + "quality_flag*" + suffix
    )
    quality_level = tnames(
        prefix + "quality_level*" + suffix
    )

    if quality_flag:
        options(
            quality_flag,
            "ytitle",
            f"PWI/EFD\n{product}\nLv.{level[1:]}",
        )
        options(
            quality_flag,
            "ysubtitle",
            "quality flag",
        )

    if quality_level:
        options(
            quality_level,
            "ytitle",
            f"PWI/EFD\n{product}\nLv.{level[1:]}",
        )
        options(
            quality_level,
            "ysubtitle",
            "quality level",
        )