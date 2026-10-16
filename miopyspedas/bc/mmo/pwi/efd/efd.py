"""Loader for BepiColombo/Mio PWI/EFD Level-2 data.

This module is the PySPEDAS counterpart of ``mmo_load_pwi_efd.pro``.
"""

from __future__ import annotations

import logging
from typing import List, Optional, Sequence, Union

import numpy as np

from ....mmo.load import load
from pyspedas import get_data, options, store_data, tnames, ylim, zlim

logger = logging.getLogger(__name__)

_VALID_LEVELS = ("l2", "l3")
_VALID_DATA_MODES = ("l", "m", "h")
_VALID_DATATYPES = ("e_spin", "e_waveform", "pot", "pot_waveform", "spec")

# CDF file names use hyphens, while directory and tplot product names use
# underscores.  This mapping follows mmo_load_pwi_efd.pro.
_FILE_DATATYPE = {
    "e_spin": "e-spin",
    "e_waveform": "e-waveform",
    "pot": "pot",
    "pot_waveform": "pot-waveform",
    "spec": "spec",
}


def efd(
    trange: Optional[Sequence[str]] = None,
    level: str = "l2",
    data_mode: str = "l",
    datatype: str = "spec",
    datatypes: Optional[Union[str, Sequence[str]]] = None,
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
    """Load BepiColombo/Mio PWI/EFD data.

    Parameters
    ----------
    trange
        Time range as ``[start_time, end_time]``.  If omitted, the historical
        loader default, 2018-11-19 through 2018-11-20, is used.
    level
        Data-product level, ``"l2"`` or ``"l3"``.
    data_mode
        Instrument data-rate mode, ``"l"``, ``"m"`` or ``"h"``.
    datatype
        Product type: ``"e_spin"``, ``"e_waveform"``, ``"pot"``,
        ``"pot_waveform"`` or ``"spec"``.
    datatypes
        IDL-compatible alias for ``datatype``.  A one-element sequence is
        accepted.  If supplied, it takes precedence over ``datatype``.
    obs_mode
        Observation mode.  Retained for API compatibility with the IDL
        routine; it does not alter the current archive path.
    coord
        Reference frame for electric-field waveform data: ``"pwi"`` or
        ``"xsm"``.  The default for ``e_waveform`` is ``"pwi"``.
    prefix, suffix
        Text prepended/appended to loaded tplot variable names.
    local_dir
        Optional local root replacing the standard MMO archive root.
    get_support_data, varformat, varnames
        CDF-to-tplot selection options passed to the common MMO loader.
    downloadonly, notplot, no_update, time_clip, force_download
        Standard PySPEDAS loading options.
    uname, passwd
        Credentials for restricted data, when required.

    Returns
    -------
    list or dict
        Loaded tplot variable names, downloaded file names, or notplot data,
        according to the selected loading mode.
    """
    if trange is None:
        trange = ["2018-11-19", "2018-11-20"]
    if varnames is None:
        varnames = []

    if datatypes is not None:
        if isinstance(datatypes, str):
            datatype = datatypes
        else:
            values = list(datatypes)
            if len(values) != 1:
                logger.error("efd loads one datatype per call; received %d.", len(values))
                return []
            datatype = values[0]

    level = str(level).lower()
    data_mode = str(data_mode).lower()
    datatype = str(datatype).lower()
    obs_mode = str(obs_mode).lower()
    coord = str(coord).lower()

    if level not in _VALID_LEVELS:
        logger.error("level must be one of %s.", _VALID_LEVELS)
        return []
    if data_mode not in _VALID_DATA_MODES:
        logger.error("data_mode must be one of %s.", _VALID_DATA_MODES)
        return []
    if datatype not in _VALID_DATATYPES:
        logger.error("datatype must be one of %s.", _VALID_DATATYPES)
        return []

    if not _mode_is_available(datatype, data_mode):
        logger.error("datatype=%r is unavailable for data_mode=%r.", datatype, data_mode)
        return []

    if datatype == "e_waveform":
        coord = coord or "pwi"
        if coord not in ("pwi", "xsm"):
            logger.error("coord must be 'pwi' or 'xsm' for e_waveform.")
            return []
    else:
        coord = ""

    # One CDF per day, matching file_dailynames(..., /unique) in the IDL code.
    file_res = 86400.0
    tplot_prefix = f"{prefix}mmo_pwi_efd_{level}_{datatype}_"

    file_datatype = _FILE_DATATYPE[datatype]
    product_token = f"{data_mode}-{file_datatype}"
    if coord:
        product_token += f"-{coord}"
    filename = f"bc_mmo_pwi-efd_{level}_{product_token}_%Y%m%d_r??-v??-??.cdf"

    if local_dir:
        pathformat = f"{local_dir.rstrip('/')}/%Y/%m/{filename}"
    else:
        pathformat = (
            f"satellite/mmo/cdf/pwi/efd/{level}/{data_mode}/{datatype}/"
            f"%Y/%m/{filename}"
        )

    loaded_data = load(
        trange=list(trange),
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

    if notplot or downloadonly:
        return loaded_data
    if loaded_data is None:
        return []

    if datatype == "e_spin":
        _configure_e_spin(tplot_prefix, suffix, level, data_mode)
    elif datatype == "e_waveform":
        _process_e_waveform(tplot_prefix, suffix, level, data_mode, coord)
    elif datatype == "pot":
        _configure_potential(tplot_prefix, suffix, level, data_mode, waveform=False)
    elif datatype == "pot_waveform":
        _configure_potential(tplot_prefix, suffix, level, data_mode, waveform=True)
    else:
        _configure_spectra(tplot_prefix, suffix, level, data_mode)

    return loaded_data


def _mode_is_available(datatype: str, data_mode: str) -> bool:
    """Return whether the IDL loader defines the requested combination."""
    if datatype in ("e_spin", "pot", "spec"):
        return data_mode in ("l", "m")
    return data_mode in _VALID_DATA_MODES


def _configure_e_spin(prefix: str, suffix: str, level: str, data_mode: str) -> None:
    rate = {"l": "4hz", "m": "8hz"}[data_mode]
    products = (
        (f"Eu_{rate}_xsm", [f"Eu_{rate}_x_xsm", f"Eu_{rate}_y_xsm"], "WPT"),
        (f"Ev_{rate}_xsm", [f"Ev_{rate}_x_xsm", f"Ev_{rate}_y_xsm"], "MEF"),
    )

    for component, legend, receiver in products:
        name = prefix + component + suffix
        options(name, "ytitle", f"PWI/EFD\nE-field ({receiver})\nLv.{level[1:]}")
        options(name, "ysubtitle", "[mV/m]")
        options(name, "legend_names", legend)
        options(name, "constant", 0)


def _process_e_waveform(
    prefix: str,
    suffix: str,
    level: str,
    data_mode: str,
    coord: str,
) -> None:
    rate = {"l": "4hz", "m": "8hz", "h": "128hz"}[data_mode]
    fields = ("Eu", "Ev") if coord == "pwi" else ("Ex", "Ey")

    for field in fields:
        name = prefix + f"{field}_waveform_{rate}_{coord}" + suffix
        data = get_data(name)
        if data is None:
            logger.warning("Cannot find tplot variable: %s", name)
            continue

        packet_time = np.asarray(data.times, dtype=np.float64).reshape(-1)
        waveform = np.asarray(data.y)
        if getattr(data, "v", None) is None:
            logger.warning("Time offsets were not found: %s", name)
            continue
        time_offset = np.asarray(data.v, dtype=np.float64).squeeze()

        if waveform.ndim != 2 or time_offset.ndim != 1:
            logger.warning("Unexpected waveform or offset dimensions for %s.", name)
            continue

        if waveform.shape[1] == time_offset.size:
            waveform_samples = waveform
        elif waveform.shape[0] == time_offset.size:
            waveform_samples = waveform.T
        else:
            logger.error(
                "Offset size does not match %s: waveform=%s, offset=%d",
                name,
                waveform.shape,
                time_offset.size,
            )
            continue

        if waveform_samples.shape[0] != packet_time.size:
            logger.error(
                "Packet-time size does not match %s: packets=%d, rows=%d",
                name,
                packet_time.size,
                waveform_samples.shape[0],
            )
            continue

        # The IDL routine uses time1 + dt directly.  In tplot, packet times and
        # DEPEND_1 offsets are both represented in seconds for this product.
        time_new = (packet_time[:, None] + time_offset[None, :]).reshape(-1)
        data_new = waveform_samples.reshape(-1)
        metadata = get_data(name, metadata=True)
        store_data(name, data={"x": time_new, "y": data_new}, attr_dict=metadata)

        if coord == "xsm":
            title = f"PWI/EFD\n{field} (XSM)\nLv.{level[1:]}"
        else:
            title = f"PWI/EFD\n{field}\nLv.{level[1:]}"
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
    if waveform:
        rate = {"l": "1hz", "m": "8hz", "h": "32hz"}[data_mode]
        components = ("Vu1", "Vv1", "Vu2", "Vv2")
    else:
        rate = {"l": "1hz", "m": "8hz"}[data_mode]
        components = ("Vu1", "Vv1", "Vu2", "Vv2", "Vave")

    for component in components:
        if waveform:
            variable_component = f"{component}_waveform_{rate}"
            description = f"{component} waveform"
        else:
            variable_component = f"{component}_{rate}"
            description = component

        name = prefix + variable_component + suffix
        options(name, "ytitle", f"PWI/EFD\nPot. ({description})\nLv.{level[1:]}")
        options(name, "ysubtitle", "[V]")
        options(name, "legend_names", [variable_component])
        options(name, "constant", 0)
        ylim(name, -2, 2)

    _configure_quality(prefix, suffix, level, "Pot.")


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
    else:
        components = {"Eu_power": "Eu spec.", "Ev_power": "Ev spec."}

    for component, description in components.items():
        name = prefix + component + suffix
        options(name, "Spec", 1)
        options(name, "ytitle", f"PWI/EFD\n{description}\nLv.{level[1:]}")
        options(name, "ysubtitle", "Frequency [Hz]")
        options(name, "ztitle", "[mV^2/m^2/Hz]")
        options(name, "ylog", 0)
        options(name, "zlog", 1)
        ylim(name, 0, 40)
        zlim(name, 1.0e-8, 1.0e-2)

    _configure_quality(prefix, suffix, level, "spec.")


def _configure_quality(
    prefix: str,
    suffix: str,
    level: str,
    product: str,
) -> None:
    quality_flag = tnames(prefix + "quality_flag*" + suffix)
    quality_level = tnames(prefix + "quality_level*" + suffix)

    if quality_flag:
        options(quality_flag, "ytitle", f"PWI/EFD\n{product}\nLv.{level[1:]}")
        options(quality_flag, "ysubtitle", "quality flag")
    if quality_level:
        options(quality_level, "ytitle", f"PWI/EFD\n{product}\nLv.{level[1:]}")
        options(quality_level, "ysubtitle", "quality level")
