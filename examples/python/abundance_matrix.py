#!/usr/bin/env python
'''This script retrieves a metagenome_statistics data structure from the MG-RAST API and
plots a graph using data from the web interface'''

import urllib, urllib2, json, sys, os

from mgrtools import GET_url, get_mgr_key

API_URL = "http://api.metagenomics.anl.gov/1"

CALL = "/matrix/organism"

key = get_mgr_key()

# assign parameters
metagenomes = ["mgm4447943.3", "mgm4447102.3"]
group_level = "domain"
result_type = "abundance"
source = "SEED"

# construct API call

parameters = {"group_level": group_level, "result_type": result_type, "auth":key, "source":source, "evalue":15}
base_url = API_URL + CALL + "?" + urllib.urlencode(parameters) +"&" + "&".join(["id=%s" % m for m in metagenomes])

jsonobject = GET_url(base_url)

# convert the data from a JSON structure to a python data type, a dict of dicts.
jsonstructure = json.loads(jsonobject)

# unpack and display the data table
cols = jsonstructure["columns"]
rows = jsonstructure["rows"]
data = jsonstructure["data"]

h = {(a, b) : int(c) for (a, b, c) in data}
sys.stdout.write("Taxon\t")
for j in range(0, len(cols)):
    sys.stdout.write(cols[j]["id"] +"\t")
print
for i in range(0, len(rows)):
    sys.stdout.write(str(rows[i]["id"])+"\t")
    for j in range(0, len(cols)):
        try:
            sys.stdout.write(str(h[(i, j)])+"\t")
        except KeyError:
            sys.stdout.write("0\t")
    sys.stdout.write("\n")

