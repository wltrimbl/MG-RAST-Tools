#!/usr/bin/env python
'''This script retrieves a list of metagenomes from the MG-RAST API.'''

import urllib, json, sys, os

from mgrtools import GET_url, get_mgr_key

def printlist(js):
    '''prints essential fields from metagenome list'''
    for item in js["data"]:
        print "\t".join([item["id"], item["status"], item["created"], item["name"]])

# http://api.metagenomics.anl.gov//metagenome?limit=10000

API_URL = "http://api.metagenomics.anl.gov/1"

CALL = "/metagenome"

key = get_mgr_key()

# assign parameters
limit = "10"
offset = "0"

# construct API call

parameters = {"limit": limit, "offset": offset, "auth": key}
base_url = API_URL + CALL + "?" + urllib.urlencode(parameters)
jsonobject = GET_url(base_url, user_agent="list_all_metagenomes.py")

# convert the data from a JSON structure to a python data type, a dict of dicts.
jsonstructure = json.loads(jsonobject)

# unpack and display the data table
total_count = jsonstructure["total_count"]

sys.stderr.write("Total number of records: {:d}\n".format(total_count))

for i in range(0, total_count / 10000 +1):
    parameters = {"limit": 10000, "offset": i * 10000, "auth": key}
    base_url = API_URL + CALL + "?" + urllib.urlencode(parameters)
    jsonstructure = json.loads(GET_url(base_url))
    printlist(jsonstructure)
