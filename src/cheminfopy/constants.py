# -*- coding: utf-8 -*-
"""Globals to be reused across the cheminfopy package"""
__all__ = ["VALID_DATA_TYPES", "DEFAULT_SOURCE_DICT"]

VALID_DATA_TYPES = [
    "chromatogram",
    "cyclicVoltammetry",
    "dynamicAdsorptionAnalysis",
    "differentialCentrifugalSedimentation",
    "differentialScanningCalorimetry",
    "elementalAnalysis",
    "hgPorosimetry",
    "ir",
    "isotherm",
    "iv",
    "mass",
    "nmr",
    "raman",
    "thermogravimetricAnalysis",
    "uv",
    "xps",
    "xrd",
    "xrf",
    "xray",
]


DEFAULT_SOURCE_DICT = {
    "name": "cheminfopy",
    "url": "https://github.com/cheminfo-py/c6h6py",
    "doi": "",
    "uuid": "",
}
