#/miopyspedas/miopyspedas/__init__.py
"""
Routines for loading and plotting BepiColombo/Mio (MMO) data with pySPEDAS.

    import miopyspedas
    miopyspedas.mgf(trange=[...])       
    miopyspedas.mmo.mgf(trange=[...])
"""

from functools import wraps

from .bc import mmo                     # miopyspedas.mmo.*
from .bc.mmo import *                   # miopyspedas.*
from .bc.mmo import __all__ as _mmo_all

__all__ = ["mmo"] + list(_mmo_all)