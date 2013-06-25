import urllib2
import datetime
import sys
import os
import json

# grab todays date for the cache file
today = datetime.date.today()
dateString = today.strftime('%Y-%m-%d')
cacheFileName = os.path.join("cache", dateString + "_data.json")

# urls for the cdn
resURL = "http://cdnjs.com/packages.min.json"
downloadPath = "http://cdnjs.cloudflare.com/ajax/libs/%libname%/%version%/%file%"


def makeDir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def getURLandWriteToFile(url, fname):
    response = urllib2.urlopen(url)
    jsonData = response.read()
    f = open(fname, "w")
    f.write(jsonData)
    f.close()

def deleteOldCacheFiles():
    for the_file in os.listdir("cache"):
        file_path = os.path.join("cache", the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception, e:
            print e

def readConfig():
    # read in the config file
    f = open("conf.txt")
    while 1:
        l = f.readline().strip()
        if l == "":
            break;
        wanted.append(l)
        f.close

# check for the cache file if it is not there grab it
if not os.path.exists(cacheFileName):
    makeDir("cache")
    deleteOldCacheFiles()
    print "getting file"
    getURLandWriteToFile(resURL ,cacheFileName)

#read the data from this file and conver the json object
f = open(cacheFileName, "r")
jsonData = f.read()
f.close()
jsonData = json.loads(jsonData)

wanted = []
readConfig()

# make the fiels dir if it does not exist
makeDir("files")

for p in jsonData["packages"]:
    filefound = False
    if p["name"] in wanted:
        libname = p["name"]
        ver = p["assets"][0]["version"]
        for f in p["assets"][0]["files"]:
            # I know - very ugly but it works
            fileurl = downloadPath.replace("%libname%", libname)
            fileurl = fileurl.replace("%version%", ver)
            fileurl = fileurl.replace("%file%", f)
            jsfname = os.path.join("files", f)

            if not os.path.exists(jsfname):
                getURLandWriteToFile(fileurl, jsfname)
