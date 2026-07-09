#/miopyspedas/miopyspedas/__init__.py
"""
This module contains routines for loading BepiColombo data

from .bc.mmo.instrument.instrument import instrument
from .bc.mpo.instrument.instrument import instrument 
"""

from functools import wraps

from .bc.mmo.load import load
from .bc.mmo.spm.spm import spm
from .bc.mmo.mgf.mgf import mgf

from .bc.mmo.mppe.mia.mia import mia
from .bc.mmo.mppe.msa.msa import msa
from .bc.mmo.mppe.ena.ena import ena
from .bc.mmo.pwi.ofa import ofa
