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
    download_only=False,
    local_dir=None
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
    local_dir : str, default=None
        Place for the downloaded kernels. If local_dir==None, we set local_dir as './chs_data/misc/spice/naif/BEPICOLOMBO/kernels/*'. 

    Returns
    -------
    list of str
        List of local file paths of kernels successfully loaded into SPICE.
    """
    # Set local_dir as './chs_data/misc/spice/naif/BEPICOLOMBO/kernels/*', if local_dir==None
    if local_dir == None:
            local_dir = CONFIG["local_data_dir"].replace("/chs", "") + "/misc/spice/naif/BEPICOLOMBO/kernels/"

    #  Define the paths to the required SPICE kernels
    esa_spice_url = "http://spiftp.esac.esa.int/data/SPICE/BEPICOLOMBO/kernels/"
    if only_for_orb:    # necessary only for obtaining trajectory data of the MMO spacecraft
        kernel_list = [
            'lsk/naif0012.tls',
            'pck/pck00011_bc_v00.tpc', 
            'pck/de-403-masses.tpc',
            'spk/bc_mmo_struct_v01.bsp',
            'spk/bc_mmo_cruise_v02.bsp',
            'spk/bc_mpo_cog_v03.bsp',
            'spk/bc_mpo_cog_fcp_00237_20181020_20261024_v02.bsp',
            'spk/bc_mpo_struct_v13.bsp',
            'spk/bc_mpo_prelaunch_v01.bsp',
            'spk/bc_mpo_mcp_50041_20181019_20251219_v02.bsp',
            'spk/bc_mpo_mlt_50037_20270301_20290516_v01.bsp',
            'spk/bc_mpo_slt_extension_20290516_20310516_v01.bsp',
            'spk/bc_mpo_fcp_00237_20181020_20270411_v02.bsp',
            'spk/bc_mpo_flp_00233_20270309_20300101_v02.bsp',
            'spk/de432s.bsp',
            'spk/bc_sci_v02.bsp', 
            'fk/bc_mpo_v40.tf',
            'fk/bc_mmo_v14.tf',
            'fk/bc_sci_v12.tf',
            'ck/bc_mmo_sc_cruise_v02.bc',
            'ck/bc_mpo_sc_sct_50041_20181019_20251219_f20181127_v03.bc',
            'ck/bc_mpo_sc_sct_50041_20230511_20261207_f20181127_v01.bc',
            'ck/bc_mpo_sc_prelaunch_f20181121_v01.bc',
            'ck/bc_mpo_sc_slt_20261117_20270307_f20181127_v02.bc',
            'ck/bc_mpo_sc_slt_00233_20270309_20291231_f20181127_v01.bc',
            'ck/bc_mpo_sc_fcp_00237_20181020_20261025_f20181127_v02.bc',
            'ck/bc_mpo_sc_slp_00211_20270314_20280507_f20181127_v01.bc',
            'sclk/bc_mpo_step_20261011.tsc',
            'sclk/bc_mpo_fict_20181127.tsc',
            'sclk/bc_mmo_step_20240103.tsc',
            'sclk/bc_mmo_fict_20231129.tsc'

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
        local_path=local_dir,
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
