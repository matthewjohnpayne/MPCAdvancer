#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages
import setuptools
import setuptools.command.develop
import setuptools.command.install
import subprocess
import pkg_resources
import sys, os
from setuptools import Extension

# -------------------------------------------------------------
# Classes & Functions to get C-code (Universal-Stepper) to compile
# -------------------------------------------------------------

def compileUniversal():
    loc = pkg_resources.Environment()['mpcadvancer'][0].location
    subprocess.check_call(
                          'bash README_COMPILE.txt',
                          cwd=os.path.join(loc, 'mpcadvancer'),
                          shell=True)

class CompileDevelop(setuptools.command.develop.develop):
    def run(self):
        super().run()
        compileUniversal()


class CompileInstall(setuptools.command.install.install):
    def run(self):
        super().run()
        compileUniversal()

# -------------------------------------------------------------

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

# requirements = [ ]
with open('requirements.txt') as f:
    requirements = f.read().splitlines()


setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', ]

setup(
    author="Matthew John Payne",
    author_email='matthewjohnpayne@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    description="MPC Advancer contains various functions for the advancing of particles (minor planets) around orbits.",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='mpcadvancer',
    name='mpcadvancer',
    packages=find_packages(include=['mpcadvancer']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/matthewjohnpayne/mpcadvancer',
    version='0.1.0',
    zip_safe=False,
    #cmdclass={'develop': CompileDevelop, 'install': CompileInstall}
)
