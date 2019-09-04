#!/usr/bin/env python
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='xiaomi_mijia',
    version='0.0.2',
    description='A library for reading Xiaomi temperature and humidity tags.',
    author='Kimmo Huoman',
    author_email='kipenroskaposti@gmail.com',
    url='https://github.com/kipe/xiaomi_mijia',
    license='MIT',
    packages=[
        'xiaomi',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Topic :: Home Automation',
        'Topic :: Software Development :: Libraries',
    ],
    install_requires=[
        'bitstring>=3.1.5',
        'bluepy>=1.3.0',
        'pendulum==2.0.4',
    ])
