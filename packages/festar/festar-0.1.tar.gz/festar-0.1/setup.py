#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
################################################################################
#
# Copyright (c) 2024 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
Setup script.

Authors: zhuxiaoxi(zhuxiaoxi@baidu.com)
Date:    2024/07/26 13:50:46
"""

from setuptools import setup, find_packages

print(find_packages())
setup(
    name="festar",
    version="0.1",
    packages=find_packages(),
    description="festar: standard feature production framework",
    author="zhanghaoran03",
    author_email="zhanghaoran03@baidu.com",
    entry_points={
        "console_scripts": [
            "festar = festar.cli.cli:main",
        ]
    }
)