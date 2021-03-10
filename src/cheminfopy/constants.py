# -*- coding: utf-8 -*-
__all__ = ["VALID_SPECTRUM_TYPES", "DEFAULT_SOURCE_DICT"]

VALID_SPECTRUM_TYPES = [
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
