
import os
from pyspedas.utilities.download import download
from ...config import CONFIG
import spiceypy as spice


def load_kernels(
    no_update=False,
    no_ck=False
):
    mk_fn = "bc_kernel_list.txt"
    mk_dir = os.path.dirname(os.path.abspath(__file__))
    mk_fpath = os.path.join(mk_dir, mk_fn)
    with open(mk_fpath, "r", encoding="utf-8") as f:
        kernel_list = [
            line.strip()
            for line in f
            if line.strip() and not line.strip().startswith("#")
        ]
    
    if no_ck:
        kernel_list = [k for k in kernel_list if "/ck/" not in k]

    esa_spice_url = "http://spiftp.esac.esa.int/data/SPICE/BEPICOLOMBO/kernels/"
    remote_files = [ k.replace( esa_spice_url, "" ) for k in kernel_list ]

    files = download(
        remote_file = remote_files, 
        remote_path=esa_spice_url,
        local_path=CONFIG["local_data_dir"]+"/misc/spice/naif/BEPICOLOMBO/kernels/",
        no_download=no_update
    )

    for f in files:
        if os.path.isfile(f):
            spice.furnsh(f)

    return files




    
