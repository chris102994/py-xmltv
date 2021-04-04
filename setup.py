#!/usr/bin/env python

from setuptools import setup
import subprocess
import os
import shutil
import sys
import pathlib

xmltv_pkg_dir = 'xmltv'
resources_dir = '{}/resources'.format(xmltv_pkg_dir)
xmltv_models_dir = '{}/models'.format(xmltv_pkg_dir)
xsd_file = '{}/xmltv.xsd'.format(resources_dir)
build_path = 'build'

xmltv_dtd_url = 'https://raw.githubusercontent.com/XMLTV/xmltv/master/xmltv.dtd'


def build():
    print('-- Installing Build Requirements.')
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'build_requirements.txt'])
    if not pathlib.Path(resources_dir).exists():
        print('-- Making the directory: {}.'.format(resources_dir))
        os.makedirs(resources_dir)
    if not pathlib.Path(xsd_file).exists():
        print('[1/2] Building {} from the official dtd file from the URL: {} using the RELAX NG TRANG tool.'.format(
            xsd_file, xmltv_dtd_url))
        subprocess.Popen(['pytrang', '-I', 'dtd', '-O', 'xsd', xmltv_dtd_url, xsd_file],
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE).wait()
    if not pathlib.Path(xmltv_models_dir).exists():
        print('[2/2] Building serialized data classes from the {} file generated in the last step.'.format(xsd_file))
        subprocess.Popen(['xsdata', 'generate', '--ns-struct', '--compound-fields', 'true', '--package', xmltv_models_dir, xsd_file],
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE).wait()


def clean():
    if pathlib.Path(xsd_file).exists():
        print('-- Removing {}.'.format(xsd_file))
        os.remove(xsd_file)

    if pathlib.Path(xmltv_models_dir).exists():
        print('-- Removing {}.'.format(xmltv_models_dir))
        shutil.rmtree(xmltv_models_dir)

    if pathlib.Path(build_path).exists():
        print('-- Removing {}.'.format(build_path))
        shutil.rmtree(build_path)

    if pathlib.Path('{}/__init__.py'.format(xmltv_pkg_dir)).exists():
        print('-- Removing {}.'.format('{}/__init__.py'.format(xmltv_pkg_dir)))
        os.remove('{}/__init__.py'.format(xmltv_pkg_dir))

    if pathlib.Path('py_xmltv.egg-info').exists():
        print('--Removing {}.'.format('py_xmltv.egg-info'))
        shutil.rmtree('py_xmltv.egg-info')

    if pathlib.Path('.pytest_cache').exists():
        print('--Removing {}.'.format('.pytest_cache'))
        shutil.rmtree('.pytest_cache')


def test():
    print('-- Installing Test Requirements.')
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pytest'])
    subprocess.check_call([sys.executable, '-m', 'pytest', 'tests/'])


if "build" in sys.argv:
    build()

if "clean" in sys.argv:
    clean()

if "test" in sys.argv:
    test()

setup(
    name="py-xmltv",
    description="An Auto-Generated Python Module for Reading and Writing XMLTV Files based on the official XMLTV XSD and DTD schema.",
    version='1.0.2',
    author="Chris102994",
    author_email="chris102994@yahoo.com",
    url="https://github.com/chris102994/py-xmltv",
    long_description='\n{}\n{}'.format(open('README.md').read(), open('CHANGELOG.md').read()).strip('\t'),
    long_description_content_type="text/markdown",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    requires=['xsdata'],
    license="LGPL-3.0+",
    packages=['xmltv', 'xmltv/models'],
    package_data={'': ['xmltv/resources/', 'xmltv/data/']},
    include_package_data=True
)
