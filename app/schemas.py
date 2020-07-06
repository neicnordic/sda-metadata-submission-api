from voluptuous import Schema, Required, Optional, Any


def transformToMongoQuery(value):
    return {"$in": value}


indicator_object = {
    Required('name'): str,
    Optional('type'): str
}

"""
    Schema for document to be inserted in DB
    As a minimum, the document must have a valid XML, an ID to which this object is related, its type, and a reference to 
    the data file that is described by this metadata. It could potentially also contain other fields.
"""
document_schema = Schema({
    Required("xml"): str,
    Required("type"): str,
    Optional("related_to"):str,
    Required("file_reference", default=""):str
    extra=True
)
