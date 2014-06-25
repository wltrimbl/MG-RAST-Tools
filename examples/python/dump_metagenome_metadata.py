#!/usr/bin/env python
'''This script retrieves a metagenome_statistics data structure from the MG-RAST API and
plots a graph using data from the web interface'''

import urllib, json, sys, os

from mgrtools import GET_url, get_mgr_key

def printall(js, elementlist, klist) :
      keys = klist
      for item in js["data"]:  
          print "ITEM: ", item
          if len(elementlist) == 1:
              datastem = item[elementlist[0]]
          elif len(elementlist) == 2: 
              datastem = item[elementlist[0]][elementlist[1]]
          else: 
              datastem = item[elementlist[0]][elementlist[1]][elementlist[2]]
          if type(datastem) == dict:
            for k in datastem.keys():
                if k not in keys: 
                   keys.append(k)
          elif type(datastem) == list: 
              for i in datastem:
                if i[0] not in keys: 
                   keys.append(i[0])
          else:
             assert False, "only dicts supported!"
      sortedkeys=keys
      print "#id\t" + "\t".join(sortedkeys)
      for item in js["data"]:
         print item["id"] + "\t",
         if len(elementlist) == 1:
              datastem = item[elementlist[0]]
         elif len(elementlist) == 2: 
              datastem = item[elementlist[0]][elementlist[1]]
         else: 
              datastem = item[elementlist[0]][elementlist[1]][elementlist[2]]
         if type(datastem) == list:  # have to get it in dict 
             newstem = {}
             for a,b in datastem:
                 newstem[a] = b
             datastem = newstem
         for k in sortedkeys :
             try:
                  print datastem[k] + "\t",
             except KeyError:
                  print "\t",
             except TypeError: # don't try if it's a data structure
                  print "\t",
         print
      return keys

# http://api.metagenomics.anl.gov//metagenome?limit=10&verbosity=metadata

API_URL = "http://api.metagenomics.anl.gov/1"

CALL = "/metagenome"

key = get_mgr_key()

# assign parameters
limit = "1000"
offset = "0"

# construct API call

parameters = {"limit": limit, "offset": offset, "verbosity": "metadata"}
base_url = API_URL + CALL + "?" + urllib.urlencode(parameters)
jsonobject = GET_url(base_url)

# convert the data from a JSON structure to a python data type, a dict of dicts.
jsonstructure = json.loads(jsonobject)

# unpack and display the data table
total_count = jsonstructure["total_count"]

sys.stderr.write("Total number of records: {:d}\n".format(total_count))
limit = 10

klist = []
for i in range(0, total_count / limit +1):
    parameters = {"limit": limit, "offset": i * limit, "verbosity" :"metadata"}
    base_url = API_URL + CALL + "?" + urllib.urlencode(parameters)
    jsonstructure = json.loads(GET_url(base_url, user_agent="dump_metagenome_metadata.py"))

    klist = printall(jsonstructure, ("metadata","sample"), klist) 

