from io import StringIO
from lxml import etree
from collections import OrderedDict, defaultdict
from flask import current_app
from pymongo import collection as pymongo_collection
from app import exceptions
from app.constants import SCHEMA_LOCATIONS, ALLOWED_FILE_EXTENSIONS, POSSIBLE_REFERENCE_OBJECTS, NOT_FOUND
from app.exceptions import CustomError
import re


def is_file_extension_allowed(filename):
    (name, extension) = filename.split(".")
    if extension.lower() in ALLOWED_FILE_EXTENSIONS:
        return True
    else:
        return False


def is_referenced_object_registered(xml_string, object_type, collection_name):
    reference_objects = POSSIBLE_REFERENCE_OBJECTS[object_type.upper()]
    for object in reference_objects:
        print(object)
        if "" in reference_objects:
            return True
        if "FILE" not in object and object in xml_string:
            obj_value = re.search(f'<{object}(.+?)<', xml_string).group(1)
            obj_value = obj_value.split("=", 1)[1].replace("/>", "")

            reference_document = collection_name.find_one({"alias": obj_value})
            if reference_document:
                return True
    return False


def is_valid_xml(xml_string, object_type):
    with current_app.open_resource(
            f'catalog/SRA.{object_type}.xsd') as schema_location:  # = SCHEMA_LOCATIONS[object_type]
        xml_schema_doc = etree.parse(schema_location)
        xml_schema = etree.XMLSchema(xml_schema_doc)
        xml_doc = etree.fromstring(xml_string)
        try:
            validity = xml_schema.validate(xml_doc)
            if validity is False:
                print("PARSE ERROR:", xml_schema.error_log)
        except:
            print("PROBLEM:", sys.exec_info()[0])
            print("PARSE ERROR:", xml_schema.error_log)

        return validity


def collection_writer(xml_string, object_type, collection_name):
    mongo_document = {'xml': xml_string, 'object_type': object_type, 'file_reference': ""}
    collection_name.insert(mongo_document)
    print("Records Successfully written in the database!")
    return True


def foldr(func, init, seq):
    if not seq:
        return init
    else:
        return func(seq[0], foldr(func, init, seq[1:]))
