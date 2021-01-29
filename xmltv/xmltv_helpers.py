from typing import Type, TypeVar

from xmltv.models.xmltv import *
from xsdata.formats.dataclass.serializers import XmlSerializer
from xsdata.formats.dataclass.serializers.config import SerializerConfig
from xsdata.formats.dataclass.context import XmlContext
from xsdata.formats.dataclass.parsers import XmlParser
import pathlib

T = TypeVar("T")

def serialize_xml_from_file(
        xml_file_path: pathlib.Path,
        serialize_clazz: Optional[Type[T]]
):
    """
    Method to serialize XML data from a file.
    :param xml_file_path: A pathlib.path path object that leads to the targeted XML file.
    :param serialize_clazz: A class Object.
    :return: the serialized object.
    """
    parser = XmlParser(context=XmlContext())
    return parser.from_path(xml_file_path, serialize_clazz)

def write_file_from_xml(
        xml_file_path: pathlib.Path,
        serialize_clazz: Optional[Type[T]]
):
    """
    Method to write serialized XML data to a file.
    :param xml_file_path: A pathlib.path path object that the data will write to.
    :param serialize_clazz: A class Object.
    :return: N/A
    """
    serializer = XmlSerializer(config=SerializerConfig(
        pretty_print=True,
        encoding="UTF-8",
        xml_version="1.1",
        xml_declaration=False,
        schema_location="resources/xmltv.xsd",
        no_namespace_schema_location=None))

    with xml_file_path.open("w") as data:
        serializer.write(data, serialize_clazz)
