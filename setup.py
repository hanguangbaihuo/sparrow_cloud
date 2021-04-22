#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import print_function

# import io
import os
import sys
import shutil
from setuptools import find_packages, setup

version = "v3.2.0"

def read(f):
    return open(f, 'r', encoding='utf-8').read()


if sys.argv[-1] == 'publish':
    if os.system("pip freeze | grep twine"):
        print("twine not installed.\nUse `pip install twine`.\nExiting.")
        sys.exit()
    os.system("python setup.py sdist bdist_wheel")
    if os.system("twine check dist/*"):
        print("twine check failed. Packages might be outdated.")
        print("Try using `pip install -U twine wheel`.\nExiting.")
        sys.exit()
    os.system("twine upload dist/*")
    print("You probably want to also tag the version now:")
    print("  git tag -a %s -m 'version %s'" % (version, version))
    print("  git push --tags")
    shutil.rmtree('dist')
    shutil.rmtree('build')
    shutil.rmtree('sparrowcloud.egg-info')
    sys.exit()


setup(
    name='sparrowcloud',
    version=version,
    license='MIT',
    description='',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    author='sparrow',
    author_email='',  # SEE NOTE BELOW (*)
    url='https://github.com/hanguangbaihuo/sparrow_cloud',
    packages=find_packages(include=['sparrow_cloud', 'sparrow_cloud.*', '*.sparrow_cloud.*', '*.sparrow_cloud']),
    include_package_data=True,
    install_requires=[
        'requests>=2.12.1',
        'python-consul>=1.1.0',
        'coreapi>=2.3.3',
        'PyJWT>=1.7.1',
        'openapi_codec>=1.3.2',
        'dulwich>=0.19.13',
        'pika',
        'django-redis>=4.10.0',
        'cryptography>=2.8',
        'opentracing',
        'jaeger-client',
    ],
    python_requires=">=3.6",
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        # 'Framework :: Django',
        'Framework :: Django :: 1.9',
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
