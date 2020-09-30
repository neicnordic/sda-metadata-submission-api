from app import exceptions

"""
The list of objects, one of which have to be present in order to be able to upload the current object
"""
POSSIBLE_REFERENCE_OBJECTS = {
    'DATASET': ['ANALYSIS_REF', 'EXPERIMENT_REF'],
    'EXPERIMENT': ['STUDY_REF', 'SAMPLE_REF'],
    'ANALYSIS': ['STUDY_REF', 'SAMPLE_REF', 'RUN_REF'],
    'RUN': ['EXPERIMENT_REF'],
    'STUDY': [''],
    'SAMPLE': [''],
    'DAC': [''],
    'POLICY': ['']
}

"""
Schema URLs for objects
"""
SCHEMA_LOCATIONS = {
    'sample': 'ftp://ftp.sra.ebi.ac.uk/meta/xsd/sra_1_5/SRA.sample.xsd',
    'study': 'ftp://ftp.sra.ebi.ac.uk/meta/xsd/sra_1_5/SRA.study.xsd',
    'experiment': 'ftp://ftp.sra.ebi.ac.uk/meta/xsd/sra_1_5/SRA.experiment.xsd',
    'run': 'ftp://ftp.sra.ebi.ac.uk/meta/xsd/sra_1_5/SRA.run.xsd',
    'analysis': 'ftp://ftp.sra.ebi.ac.uk/meta/xsd/sra_1_5/SRA.analysis.xsd',
    'common': 'ftp://ftp.sra.ebi.ac.uk/meta/xsd/sra_1_5/SRA.common.xsd',
    'dac': 'ftp://ftp.sra.ebi.ac.uk/meta/xsd/sra_1_5/EGA.dac.xsd',
    'policy': 'ftp://ftp.sra.ebi.ac.uk/meta/xsd/sra_1_5/EGA.policy.xsd',
    'dataset': 'ftp://ftp.sra.ebi.ac.uk/meta/xsd/sra_1_5/EGA.dataset.xsd'
}

"""
The allowed file extensions
"""
ALLOWED_FILE_EXTENSIONS = ['xml']

"""
Custom error messages
"""
MISSING_FILE_NAME = 'No filename attached to posted file.'
MISSING_FILE_KEY = "No file keyword in POST request."
INVALID_XML = "XML not valid for the expected schema"
NOT_FOUND = "not found"
