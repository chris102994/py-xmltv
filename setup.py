#!/usr/bin/env python

import os
from setuptools import setup
import sh
import shutil
import sys
import pathlib
from distutils.command.build_py import build_py
from distutils.cmd import Command

xmltv_pkg_dir = 'xmltv'
resources_dir = '{}/resources'.format(xmltv_pkg_dir)
xmltv_models_dir = '{}/models'.format(xmltv_pkg_dir)
xsd_file = '{}/xmltv.xsd'.format(resources_dir)
build_path = 'build'
xmltv_dtd_url = 'https://raw.githubusercontent.com/XMLTV/xmltv/master/xmltv.dtd'

class custom_clean(Command):
    description = """Custom Clean Commands"""
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        if pathlib.Path(xsd_file).exists():
            print('-- Removing {}.'.format(xsd_file))
            os.remove(xsd_file)

        if pathlib.Path(xmltv_models_dir).exists():
            print('-- Removing {}.'.format(xmltv_models_dir))
            shutil.rmtree(xmltv_models_dir)

        if pathlib.Path('.tox/').exists():
            print('-- Removing {}.'.format('.tox/'))
            shutil.rmtree('.tox/')

        if pathlib.Path('dist/').exists():
            print('-- Removing {}.'.format('dist/'))
            shutil.rmtree('dist/')

        if pathlib.Path(build_path).exists():
            print('-- Removing {}.'.format(build_path))
            shutil.rmtree(build_path)

        if pathlib.Path('py_xmltv.egg-info').exists():
            print('--Removing {}.'.format('py_xmltv.egg-info'))
            shutil.rmtree('py_xmltv.egg-info')

        if pathlib.Path('.pytest_cache').exists():
            print('--Removing {}.'.format('.pytest_cache'))
            shutil.rmtree('.pytest_cache')


class custom_build(build_py):
    description = """Custom Build Commands"""
    if not pathlib.Path(resources_dir).exists():
        print('-- Making the directory: {}.'.format(resources_dir))
        os.makedirs(resources_dir)
    if not pathlib.Path(xsd_file).exists():
        print('[1/2] Building {} from the official dtd file from the URL: {} using the RELAX NG TRANG tool.'.format(
            xsd_file, xmltv_dtd_url))
        try:
            sh.pytrang('-I', 'dtd', '-O', 'xsd', xmltv_dtd_url, xsd_file)
        except sh.ErrorReturnCode as error:
            print('Missing Files. This is likely java.', error)
            sys.exit(1)

    if not pathlib.Path(xmltv_models_dir).exists():
        print('[2/2] Building serialized data classes from the {} file generated in the last step.'.format(xsd_file))
        os.makedirs(xmltv_models_dir)
        try:
            sh.xsdata('generate', xsd_file)
        except sh.ErrorReturnCode as error:
            print('Error generating data class from the XSD file {}.'.format(xsd_file), error)
            sys.exit(1)


class custom_test(Command):
    description = """Custom Test Commands"""
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import pytest
        pytest.main(['tests/'])


setup(
    cmdclass={
        'clean': custom_clean,
        #'build_py': custom_build,
        'test': custom_test
    }
)

