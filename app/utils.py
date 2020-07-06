from io import StringIO
from lxml import etree
from collections import OrderedDict, defaultdict
from flask import current_app
from pymongo import collection as pymongo_collection
from app import exceptions
from app.constants import SCHEMA_LOCATIONS,ALLOWED_FILE_EXTENSIONS, POSSIBLE_REFERENCE_OBJECTS, NOT_FOUND
from app.exceptions import CustomError

def is_file_extension_allowed(filename):
    (name,extension) = filename.split(".")
    if extension.lower()  in ALLOWED_FILE_EXTENSIONS:
         return True
    else:
        return False

def is_referenced_object_registered(xml_string, object_type, collection_name):
    reference_objects = POSSIBLE_REFERENCE_OBJECTS[object_type.upper()]
    root = etree.parse(StringIO(xml_string))
    # root = etree.parse(StringIO(xml_string))
    # root = etree.fromstring(xml_string)
    for object in reference_objects:
        reference_name = root.XPath('//%s[@"refname"]/text()' %object)
        if reference_name != '':
            reference_document = collection_name.find_one({"reference_alias" : reference_name})
            if reference_document:
                return True
    return False

def is_valid_xml(xml_string, object_type):
    #metadata_string = StringIO(xml_string)
    with current_app.open_resource('catalog/SRA.experiment.xsd') as schema_location: #= SCHEMA_LOCATIONS[object_type]
      xml_schema_doc = etree.parse(schema_location)
      xml_schema = etree.XMLSchema(xml_schema_doc)
      xml_doc = etree.fromstring(xml_string)
      # xml_doc = etree.parse(xml_string)
      #xml_doc = etree.parse(metadata_string)
      try:
          validity = xml_schema.validate(xml_doc)
          print ("PARSE ERROR:",xml_schema.error_log)
      except:
          print ("PROBLEM:", sys.exec_info()[0])
      return validity

def collection_writer(xml_string, object_type,  db_name, collection_name):
    mongo_document = {}
    mongo_document['xml']=xml_string
    mongo_document['object_type'] = object_type
    mongo_document['file_reference'] = ""
    collection_name.insert(mongo_document)
    return True

def parse_query_params(query_params) -> dict:
    if 'year' in query_params:
        if type(query_params['year']) == list:
            query_params['year'] = [int(i) for i in query_params['year']]
        else:
            query_params['year'] = [int(query_params['year'])]
    if 'indicator' in query_params:
        for k, v in query_params['indicator'].items():
            query_params[f"indicator.{k}"] = v
        del query_params['indicator']
    for k in ['name', 'type']:
        if k in query_params:
            query_params[f"indicator.{k}"] = query_params[k]
            del query_params[k]

    return query_params


def generate_payload(query_params: OrderedDict, filters, collection: pymongo_collection, skip=0, limit=100) -> dict:
    """
    We want to generate a payload that confirms to the specs. There are two scenarios we can have for labels: (a) years
    and (b) country codes. We also want to offer the functionality of submitting multiple filters when requesting
    a data (instead of sending multiple requests).

    The format sent is roughly like this:

        {'Country Code': ['ISL', 'JAP', 'DEN'], 'Product': ['Grapes', 'Bananas'], 'Value Unit': ['kg']}

    In this example, we are actually using (a) years as the label, since it's not being included in the query. In
    addition, we are also giving back 3*2*1 = 6 value sets back, i.e. with all values with filters
    ['ISL', 'Grapes', 'kg'] being the first set.

    So we want to generate all combinations of the values, submitting a query to MongoDB for each one. We generate a
    dictionary of the actual plot values, with the actual query metadata (i.e. filter keys and values).

    Note that one of the requested formats in the FE is that missing values for a given set are filled with NaN, i.e.
    labels [2001, 2003, 2004] and values [1, 2, 3] become [2001, 2002, 2003, 2004] and [1, NaN, 2, 3]. Hence we need to
    keep track of the unique labels to create a range of years / list of countries.

    TODO:
        This is a bit restricted since we are just coding for years or countries. Possibly have it more broader
        functionality somehow? Depends on the frontend.

    :param query_params: The query parameters of the request, indicating which filters to apply when grabbing the data.
    :param collection: The current collection (filename).
    :return: The payload after grabbing the data and parsing it into a suitable format.
    """
    label_kind = "year" if ("country code" in query_params) or ("country" in query_params) else (
        "country" if "country" in query_params else "country code")
    unique_labels = set()
    documents = collection.find(query_params,
                                {'_id': False, 'display': False, 'file name': False, 'region': False,
                                 'income group': False, 'source': False})
    payload = {'graph_elements': []}
    full_response = [i for i in documents]
    group = defaultdict(list)

    if label_kind == 'year':
        for i in full_response:
            group[i['country code']].append(i)
        for key in group.keys():
            plot_values = OrderedDict({i[label_kind]: i['value'] for i in group[key]})
            unique_labels.update(set(plot_values.keys()))
            meta_data = group[key][0]

            del meta_data["value"]
            del meta_data["year"]
            payload_item = dict(query_metadata={**meta_data, 'value unit': documents.distinct('value unit')},
                                labels_and_values=plot_values)
            payload['graph_elements'].append(payload_item)
        if unique_labels:
            payload['labels'] = list(range(int(min(unique_labels)), int(max(unique_labels)) + 1))
        else:
            payload['labels'] = []
    else:
        for i in full_response:
            group[int(i['year'])].append(i)
        for key in group.keys():
            plot_values = OrderedDict({i[label_kind]: i['value'] for i in group[key]})
            unique_labels.update(set(plot_values.keys()))
            meta_data = group[key][0]

            del meta_data["value"]
            del meta_data["country code"]
            del meta_data["country"]

            payload_item = dict(query_metadata={**meta_data, 'value unit': documents.distinct('value unit')},
                                labels_and_values=plot_values)
            payload['graph_elements'].append(payload_item)
            payload['labels'] = sorted(list(unique_labels))

    total = len(payload["graph_elements"])

    payload["total"] = total
    limit = total if limit >= total else limit
    payload["count"] = limit
    payload["graph_elements"] = payload["graph_elements"][skip:limit]
    return payload


def generate_payload_from_average_groupby(filters, datapoint, result):
    group = list(map(lambda el: el["query_metadata"][f"{filters['type']}"], result["graph_elements"]))

    if datapoint["_id"][f"{filters['type']}"] not in group:
        (result["labels"]).add(datapoint['_id']["year"])
        result["graph_elements"].append({
            "query_metadata": {**filters, **datapoint['_id'], 'year': [datapoint['_id']['year']]},
            'values': [datapoint['average']]

        })
    else:
        index = group.index(datapoint["_id"][f"{filters['type']}"])
        (result["labels"]).add(datapoint['_id']["year"])
        (result["graph_elements"][index]['values']).append(datapoint['average'])
        (result["graph_elements"][index]["query_metadata"]['year']).append(datapoint['_id']["year"])

    return result


def foldr(func, init, seq):
    if not seq:
        return init
    else:
        return func(seq[0], foldr(func, init, seq[1:]))
