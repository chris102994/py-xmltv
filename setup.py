#!/usr/bin/env python

from distutils.core import setup
import subprocess
import os
import shutil
import sys
import pathlib

xsd_file = 'xmltv.xsd'
pkg_path = 'xmltv'
build_path = 'build'

xmltv_dtd_url = 'https://raw.githubusercontent.com/XMLTV/xmltv/master/xmltv.dtd'


def clean():
    if pathlib.Path(xsd_file).exists():
        print('-- Removing {}.'.format(xsd_file))
        os.remove(xsd_file)

    if pathlib.Path(pkg_path).exists():
        print('-- Removing {}.'.format(pkg_path))
        shutil.rmtree(pkg_path)

    if pathlib.Path(build_path).exists():
        print('-- Removing {}.'.format(build_path))
        shutil.rmtree(build_path)

def build():
    print('-- Installing Build Requirements.')
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'build_requirements.txt'])
    if not pathlib.Path(xsd_file).exists():
        print('[1/2] Building {} from the official dtd file from the URL: {} using the RELAX NG TRANG tool.'.format(xsd_file, xmltv_dtd_url))
        subprocess.Popen(['pytrang', '-I', 'dtd', '-O', 'xsd', xmltv_dtd_url,  xsd_file],
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE).wait()
    if not pathlib.Path(pkg_path).exists():
        print('[2/2] Building serialized data classes from the {} file generated in the last step.'.format(xsd_file))
        subprocess.Popen(['xsdata', 'generate', '--package', pkg_path, xsd_file],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE).wait()

if "build" in sys.argv:
    build()

if "clean" in sys.argv:
    clean()


setup(
    name="py-xmltv",
    description="An Auto-Generated Python Module for Reading and Writing XMLTV Files based on the official XMLTV XSD and DTD schema.",
    version='1.0',
    author="Chris102994",
    url="https://github.com/chris102994/py-xmltv",
    long_description='\n{}\n{}'.format(open('README.md').read(), open('CHANGELOG.md').read()).strip('\t'),
    classifiers=[
        'Development Status :: Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    requires=['xsdata'],
    license="LGPL-3.0+",
    packages=[pkg_path]
)
