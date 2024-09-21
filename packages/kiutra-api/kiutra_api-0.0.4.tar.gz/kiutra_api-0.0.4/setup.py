#!/usr/bin/env python
#  -*- coding: utf-8 -*-
#
# Copyright 2020 by kiutra GmbH
# All rights reserved.
# This file is part of Kiutra-Core,
# and is released under the "Apache Version 2.0 License". Please see the LICENSE
# file that should have been included as part of this package.

import sys
from setuptools import setup, find_packages

requires = ['jsonrpclib-pelix>=0.4.3.1', 'filelock>=3.4.2', 'werkzeug>=2.0.2', 'numpy>=1.21.4']

desc = """A python package to interface with kiutra hardware."""

setup(
    name='kiutra-api',
    version="0.0.4",
    author='kiutra GmbH',
    author_email='support@kiutra.com',
    license = 'Apache Version 2.0 License',
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        "License :: OSI Approved :: Apache Software License",
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    description=desc,
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires,
)

