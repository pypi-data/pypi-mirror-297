# -*- coding: utf-8 -*-
# pylint: disable=line-too-long,missing-module-docstring

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
    
setuptools.setup(
    name="backgrounds",
    version="0.1.1",
    author="Quentin Baghi",
    author_email="quentin.baghi@protonmail.com",
    description="Tools for the detection of stochastic gravitational-wave backgrounds based on J.B. Bayle's LISA GW Response.",
    license="BSD-3-Clause",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.in2p3.fr/qbaghi/backgrounds",
    packages=setuptools.find_packages(),
    install_requires=[
        'h5py',
        'numpy',
        'scipy',
        'matplotlib',
        'healpy',
        'lisaconstants',
        'lisagwresponse',
    ],
    python_requires='>=3.7',
)
