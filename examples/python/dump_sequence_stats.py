#!/usr/bin/env python
'''This script retrieves a metagenome_statistics data structure from the MG-RAST API and
plots a graph using data from the web interface'''

import urllib, json, sys, os

from mgrtools import GET_url, get_mgr_key

def printsinglefield(js, fieldname):
    for item in js["data"]:
         try:
             field = item["statistics"]["sequence_stats"][fieldname]
         except KeyError:
             field = ""
         print item["id"]+ "\t" + field 

def printlist(js, header=False, keylist=None):
    if header:
      keys = set()
      for item in js["data"]:
          for k in item["statistics"]["sequence_stats"].keys():
              keys.add(k)
      print "#id\t" + "\t".join(sorted(keys))
      return sorted(keys)
    else:
      for item in js["data"]:
         print item["id"] + "\t",
         for k in keylist :
             try:
                  print item["statistics"]["sequence_stats"][k] + "\t",
             except KeyError:
                  print "\t",
         print

def printall(js, elementlist, klist) :
      keys = klist
      for item in js["data"]:
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
         print
      return keys

def printbrowsetable(js, header=False):
    if header:
	print "#",
	for k in sorted(js["data"][0]["statistics"]["sequence_stats"].keys()):
	    print k + "\t",
	print
    else:
      for item in js["data"]:
	 #print item["id"], item["project"][0], item["name"],
	 print item["id"], item["statistics"]["sequence_stats"]["bp_count_raw"], item["statistics"]["sequence_stats"]["sequence_count_raw"], item["sequence_type"], item["status"]

#  http://api.metagenomics.anl.gov/1/metagenome?verbosity=stats&limit=10&offset=0

API_URL = "http://api.metagenomics.anl.gov/1"

CALL = "/metagenome"

key = get_mgr_key()

# assign parameters
limit = "1"  # initial call
offset = "0"

# construct API call

parameters = {"limit": limit, "offset": offset, "auth": key }
base_url = API_URL + CALL + "?" + urllib.urlencode(parameters)
jsonobject = GET_url(base_url, user_agent="dump_sequence_stats.py")

# convert the data from a JSON structure to a python data type, a dict of dicts.
jsonstructure = json.loads(jsonobject)

# unpack and display the data table
total_count = jsonstructure["total_count"]

sys.stderr.write("Total number of records: {:d}\n".format(total_count))
limit = 1000

klist = []
for i in range(0, total_count / limit +1):
    parameters = {"limit": limit, "offset": i * limit, "verbosity" :"stats", "auth": key}
    base_url = API_URL + CALL + "?" + urllib.urlencode(parameters)
    jsonstructure = json.loads(GET_url(base_url))

    klist = printall(jsonstructure, ("statistics", "sequence_stats"), klist) 

