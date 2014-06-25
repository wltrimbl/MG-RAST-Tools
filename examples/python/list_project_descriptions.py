#!/usr/bin/env python
'''This script retrieves the list of projects from the MG-RAST API'''

import urllib, json, sys, os

from mgrtools import GET_url, get_mgr_key

API_URL = "http://api.metagenomics.anl.gov/1"

CALL = "/project"

key = get_mgr_key()

# assign parameters
limit = "0"
offset = "0"

# http://api.metagenomics.anl.gov/1/project?verbosity=full&limit=0&order=id

# construct API call

parameters = {"order": "id", "limit": limit, "auth": key, "offset":offset, "verbosity":"full"}

base_url = API_URL + CALL + "?" + urllib.urlencode(parameters)
jsonobject = GET_url(base_url, user_agent="list_project_descriptions.py")

# convert the data from a JSON structure to a python data type, a dict of dicts.
jsonstructure = json.loads(jsonobject)

# unpack and display the data table
for item in jsonstructure["data"]:
    print "\t".join([item["id"], item["status"], item["name"], item["pi"], item["description"], item["created"], item["funding_source"]])
