#!/usr/bin/env python
'''This script retrieves a metagenome_statistics data structure from the MG-RAST API and
plots a graph using data from the web interface'''

import urllib, json, sys, os

from mgrtools import GET_url, get_mgr_key

# http://api.metagenomics.anl.gov//download/mgm4447943.3

API_URL = "http://api.metagenomics.anl.gov/1"

CALL = "/download/"

DATASET = "mgm4447943.3"

key = get_mgr_key()

# assign parameters

parameters = {"auth": key}

# construct API call

base_url = API_URL + CALL + DATASET + "?" + urllib.urlencode(parameters)
jsonobject = GET_url(base_url)

# convert the data from a JSON structure to a python data type, a dict of dicts.
jsonstructure = json.loads(jsonobject)

for record in jsonstructure:
    for k in ["file_type","stage_name", "url", "file_id", "id", "stage_id", "file_name"]:
        print record[k] + "\t",
    print 


