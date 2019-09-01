#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import print_function

import io
import os
import sys
import shutil
from setuptools import find_packages, setup


setup(
    name='sparrowcloud',
    version="v1.0",
    license='MIT',
    description='',
    long_description="",
    # long_description_content_type='text/markdown',
    author='',
    author_email='',  # SEE NOTE BELOW (*)
    packages=find_packages(include=['sparrow_cloud', 'sparrow_cloud.*', '*.sparrow_cloud.*', '*.sparrow_cloud']),
    include_package_data=True,
    install_requires=[
        'atomicwrites==1.3.0',
        'attrs==19.1.0',
        'certifi==2019.6.16',
        'chardet==3.0.4',
        'Django==2.2.4',
        'djangorestframework==3.10.2',
        'idna==2.8',
        'importlib-metadata==0.19',
        'more-itertools==7.2.0',
        'packaging==19.1',
        'pluggy==0.12.0',
        'py==1.8.0',
        'pyparsing==2.4.2',
        'pytest==5.1.2',
        'python-consul==1.1.0',
        'pytz==2019.2',
        'requests==2.22.0',
        'six==1.12.0',
        'sqlparse==0.3.0',
        'urllib3==1.25.3',
        'wcwidth==0.1.7',
        'zipp==0.6.0',
    ],
    python_requires=">=3.7",
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        # # 'Framework :: Django :: 1.11',
        # 'Framework :: Django :: 2.0',
        # 'Framework :: Django :: 2.1',
        # 'Framework :: Django :: 2.2',
        # 'Intended Audience :: Developers',
        # # 'License :: OSI Approved :: BSD License',
        # 'Operating System :: OS Independent',
        # 'Programming Language :: Python',
        # 'Programming Language :: Python :: 3',
        # 'Programming Language :: Python :: 3.5',
        # 'Programming Language :: Python :: 3.6',
        # 'Programming Language :: Python :: 3.7',
        # 'Programming Language :: Python :: 3 :: Only',
        'Topic :: Internet :: WWW/HTTP',
    ],

)
