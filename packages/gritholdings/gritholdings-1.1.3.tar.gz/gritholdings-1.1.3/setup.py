#!/usr/bin/env python

"""
"""
import os
import re

from setuptools import find_packages, setup

ROOT = os.path.dirname(__file__)
VERSION_RE = re.compile(r'''__version__ = ['"]([0-9.]+)['"]''')


def get_version():
    init = open(os.path.join(ROOT, 'gritholdings', '__init__.py')).read()
    return VERSION_RE.search(init).group(1)


setup(
    name='gritholdings',
    version=get_version(),
    description='The Grit Holdings SDK for Python',
    long_description=open('README.md').read(),
    author='Grit Holdings, Inc',
    url='https://github.com/gritholdings/gritholdings-sdk-py',
    scripts=[],
    packages=find_packages(exclude=['tests*']),
    include_package_data=True,
    install_requires=open('requirements.txt').read().split('\n'),
    license="Apache License 2.0",
    python_requires=">= 3.8",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3'
    ],
    project_urls={
        'Documentation': 'https://gritholdings.gitbook.io/',
        'Source': 'https://github.com/gritholdings/gritholdings-sdk-py',
    },
)