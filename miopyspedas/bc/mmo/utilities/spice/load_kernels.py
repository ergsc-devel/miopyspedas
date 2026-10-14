import os
import re
import spiceypy as spice
from pyspedas.utilities.download import download
from ...config import CONFIG


def load_kernels(
    no_update=False,
    no_ck=False,
    only_for_orb=False,
    pred=False, 
    clear=False, 
    download_only=False
):
    """
    Download and furnish SPICE kernels for BepiColombo/Mio.

    Parameters
    ----------
    no_update : bool, default=False
        If True, do not download files if they already exist locally.
    no_ck : bool, default=False
        If True, exclude C-matrix (pointing/orientation, /ck/) kernels from loading.
    only_for_orb : bool, default=False
        If True, load only kernels necessary for obtaining trajectory data of the MMO spacecraft.
    pred : bool, default=False
        If True, load predictive kernels instead of operational ones.
    clear : bool, default=False
        If True, clear the SPICE pool before loading kernels.
    download_only : bool, default=False
        If True, return only the list of downloaded files without loading them into SPICE.

    Returns
    -------
    list of str
        List of local file paths of kernels successfully loaded into SPICE.
    """

    #  Define the paths to the required SPICE kernels
    esa_spice_url = "http://spiftp.esac.esa.int/data/SPICE/BEPICOLOMBO/kernels/"
    if only_for_orb:    # necessary only for obtaining trajectory data of the MMO spacecraft
        kernel_list = [
            'lsk/naif0012.tls',
            'pck/pck00011_bc_v00.tpc', 
            'pck/de-403-masses.tpc',
            'spk/bc_mpo_fcp_00237_20181020_20270411_v02.bsp',
            'spk/de432s.bsp',
            'spk/bc_sci_v02.bsp', 
            'fk/bc_mpo_v40.tf',
            'fk/bc_sci_v12.tf',
            'fk/bc_ops_v02.tf'
        ]
    else:  # Download all kernels using a meta kernel
        mk_fn = "mk/bc_ops.tm"
        if pred:
            mk_fn = "mk/bc_plan.tm"
        mk_fpath = download(
            remote_file=mk_fn,
            remote_path=esa_spice_url,
            local_path=CONFIG["local_data_dir"].replace("/chs", "") + "/misc/spice/naif/BEPICOLOMBO/kernels/",
            no_download=no_update
        )
        if not os.path.isfile(mk_fpath[0]):
            raise FileNotFoundError(f"Could not find SPICE kernel file: {mk_fpath[0]}")
            return ""
        # Read the meta kernel and get the list of kernels to load in the relative path format
        spice.ldpool(mk_fpath[0])
        n_items = spice.dtpool("KERNELS_TO_LOAD")[0]
        k_list = spice.gcpool("KERNELS_TO_LOAD", 0, n_items)
        kernel_list = [re.sub(r"^\$KERNELS/", "", k.strip()) for k in k_list]

        # Optionally exclude CK (attitude/pointing) kernels to speed up loading
        if no_ck:
            kernel_list = [k for k in kernel_list if not re.search(r"^ck/", k)]

    
    # Download kernels from ESA server to the local data directory 
    files = download(
        remote_file=kernel_list,
        remote_path=esa_spice_url,
        local_path=CONFIG["local_data_dir"].replace("/chs", "") + "/misc/spice/naif/BEPICOLOMBO/kernels/",
        no_download=no_update
    )

    # Return the list of downloaded files and quit if download_only is True
    if download_only:
        return files     

    # Load (furnish) downloaded kernels into the SPICE pool
    if clear:
        print("Clear SPICE pool")
        spice.kclear()
    loaded_kernels = []
    for f in files:
        if os.path.isfile(f):
            spice.furnsh(f)
            loaded_kernels.append(f)

    return loaded_kernels
