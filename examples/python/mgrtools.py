
def GET_url(url, user_agent="mgrtools"):
    import sys, urllib2
    sys.stderr.write("Retrieving %s\n" % url)
    try:
        opener = urllib2.urlopen(url)
    except urllib2.HTTPError, e:
        print "Error with HTTP request: %d %s\n%s" % (e.code, e.reason, e.read())
        sys.exit(255)
    opener.addheaders = [('User-agent', user_agent)]
    return(opener.read())

def get_mgr_key():
    import os
    try:
        key = os.environ["MGRKEY"]
    except KeyError:
        key = ""
    return key
