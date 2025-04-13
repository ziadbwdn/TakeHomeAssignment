# src/__init__.py
"""
Linear Feedback Shift Register (LFSR) Implementation Package

This package provides implementations of Linear Feedback Shift Registers
for use in cryptography, random number generation, and digital signal processing.
"""

from .basic_lfsr import BasicLFSR
from .general_lfsr import GeneralLFSR

__all__ = ['BasicLFSR', 'GeneralLFSR']