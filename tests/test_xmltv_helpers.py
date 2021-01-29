import pytest
from xmltv import xmltv_helpers
from xmltv.models.xmltv import *
import pathlib
import os


xmltv_in_file = pathlib.Path('tests/data/test_guide.xml')
xmltv_out_file = pathlib.Path('test_write_file_from_xml.xml')


def teardown_module(module):
    if pathlib.Path(xmltv_out_file).exists():
        print('-- Removing {}.'.format(xmltv_out_file))
        os.remove(xmltv_out_file)

def test_serialize_xml_from_file():
    data = xmltv_helpers.serialize_xml_from_file(xmltv_in_file, Tv)
    assert data is not None  # Ensure the xml loads properly.
    assert type(data) is Tv  # Ensure the type is a Tv type.


def test_write_file_from_xml():
    data = xmltv_helpers.serialize_xml_from_file(xmltv_in_file, Tv)
    xmltv_helpers.write_file_from_xml(xmltv_out_file, data)
    assert os.path.exists(xmltv_out_file) and os.path.getsize(xmltv_out_file) > 0  # Ensure it writes a file that's not empty.
    data2 = xmltv_helpers.serialize_xml_from_file(xmltv_in_file, Tv)
    assert data == data2  # Ensure the data just written is the same as the data just read.
