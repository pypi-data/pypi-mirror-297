__version__ = "0.3.4"
__author__ = "Bhavyahshree Navaneetha Krishnan"

import os
import requests
import tellurium as te
import tempfile
import ollama
from langchain_text_splitters import CharacterTextSplitter

import biomodelcache
import convert_sbml_to_antimony
import split_biomodels
import create_vector_db
import generate_response

# Import functions from other modules
from biomodelcache import BioModelCacheRetrieval
from convert_sbml_to_antimony import convert_sbml_to_antimony
from split_biomodels import split_biomodels
from create_vector_db import create_vector_db
from generate_response import generate_response


# Define __all__ to specify which names are publicly accessible
__all__ = ['biomodelcache', 'convert_sbml_to_antimony', 'split_biomodels','create_vector_db', 'generate_response', 'BioModelCacheRetrieval']
