#!/usr/bin/env python

from setuptools import setup


requirements = [
    'gunicorn',
    'gevent',

    'bottle',
    'falcon',
    'flask',
]

setup(
    name='scproto',
    version='0.1.0',
    description='scproto is prototyping for socorro collector',
    author="Will Kahn-Greene",
    author_email='willkg@mozilla.com',
    url='https://github.com/willkg/scproto',
    packages=[
        'scproto',
    ],
    package_dir={
        'scproto': 'scproto'
    },
    include_package_data=True,
    install_requires=requirements,
    license='MPLv2',
    zip_safe=False,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
