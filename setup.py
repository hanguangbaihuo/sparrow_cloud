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
    author='sparrow',
    author_email='',  # SEE NOTE BELOW (*)
    packages=find_packages(include=['sparrow_cloud', 'sparrow_cloud.*', '*.sparrow_cloud.*', '*.sparrow_cloud']),
    include_package_data=True,
    install_requires=[
        'requests>=2.12.1',
        'python-consul>=1.1.0',
        'coreapi>=2.3.3',
        'PyJWT>=1.7.1',
        "sparrow-task-sender>=0.0.3",        # 消息发送
        "sparrow-rabbitmq-consumer>=0.0.8",  # 消息处理
    ],
    python_requires=">=3.7",
    zip_safe=False,
    classifiers=[
        'Development Status :: Production/Stable',
        'Environment :: Web Environment',
        # 'Framework :: Django',
        'Framework :: Django :: 1.9',
        # 'Framework :: Django :: 2.0',
        # 'Framework :: Django :: 2.1',
        'Framework :: Django :: 2.2',
        # 'Intended Audience :: Developers',
        # 'Operating System :: OS Independent',
        # 'Programming Language :: Python',
        # 'Programming Language :: Python :: 3',
        # 'Programming Language :: Python :: 3.5',
        # 'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
    ],

)
