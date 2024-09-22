#!/usr/bin/env python
#-*- coding:utf-8 -*-
import os
from setuptools import setup, find_packages

MAJOR =1
MINOR =1
PATCH =0
VERSION = f"{MAJOR}.{MINOR}.{PATCH}"
fp = open('README.md',encoding="utf-8")
setup(
    name="nonebot_plugin_wol",
    version=VERSION,
    author="TwoOnefour",
    author_email="lys214412@gmail.com",
    long_description_content_type="text/markdown",
    url='https://github.com/twoonefour/nonebot_plugin_wol.git',
    long_description=fp.read(),
    python_requires=">=3.6",
    install_requires=['ping3>=4.0.4', "nonebot2>=2.0.0rc2", "nb-cli>=0.6.8", "nonebot-plugin-apscheduler>=0.2.0"],
    packages=find_packages(),
    license='MIT License',
    custom_metadata={
        "License-Expression": "MIT"
    },
    classifiers=[
       'Natural Language :: English',
       'Operating System :: OS Independent',
       'Programming Language :: Python :: 3.6',
       'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    package_data={'': ["tools/*.py"]},
    include_package_data=True

)
fp.close()