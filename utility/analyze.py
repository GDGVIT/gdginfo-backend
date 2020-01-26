import os
import json
import pickle
import subprocess

from bs4 import BeautifulSoup
from xml.etree.ElementTree import fromstring
from xmljson import badgerfish as bf

def cache_analysis(org, repo, rd, token):
    print("[RUNNING cache_analysis]")

def get_cached_analysis(org, repo, redis, token, fmt):
    print("[RUNNING] get_cached_analysis")
    redis_key = org + ":" + repo + ":" + fmt
    try:
        unpacked_pickled_object = pickle.loads(redis.get(redis_key))
        print("CACHE HIT")
        return unpacked_pickled_object, None
    except:
        data, err = extract_analysis(org, repo, token, fmt)
        if err is not None:
            return data, err
        pickled_object = pickle.dumps(data)
        if not redis.set(redis_key, pickled_object):
            print("[ERROR] setting in redis: cache_response")
            return "Error setting redis cache", "ERROR"
        else:
            print("[COMPLETED] cache_response")
            return data, err
        return data, err

def extract_analysis(org, repo, token, fmt):

    print("[RUNNING] extract_analysis")
    url="https://" + token + "@github.com/" + org + "/" + repo
    path="./cloned/" + org + "_" + repo

    # Call child process for:
    # Cloning
    # Analyzing
    # Removing
    data, err = childProcess(url, path, fmt)

    # Append analyzed file to log
    with open("analyzed.log", "a+") as f:
        f.seek(0, os.SEEK_SET)
        fileData = f.read()
        f.seek(2, os.SEEK_SET)
        if repo not in fileData:
            f.write(repo + "\n")
        else:
            print(repo + " already added in analyzed.log")

    return data, err

def analyze(repo, org, redis, token, fmt):
    print("[RUNNING] analyze")
    if redis is None:
        data, err = extract_analysis(org, repo, token, fmt)
        return data, err
    else:
        data, err = get_cached_analysis(org, repo, redis, token, fmt)
        return data, err


def childProcess(url, path, fmt):
    # Cloning repo
    process = subprocess.Popen(["git", "clone", url, path], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE)
    _, stderr = process.communicate()
    print(stderr)
    print("CLONED!!")

    watch_files = "java,c,cc,cpp,h,hh,hpp,py,glsl,rb,js,sql,go,rs,dart,kt,kts,md,html,css"
    # Applying analysis
    process = subprocess.Popen(["gitinspector", "--format=" + fmt, "-f", watch_files
        , "--grading", path], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if len(stderr) != 0:
        print(stderr)
        return stderr, "Error in applying analysis"
    print("ANALYZED!!")

    # Removing repo
    process = subprocess.Popen(["rm", "-r", path], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE)
    _, stderr = process.communicate()
    if len(stderr) != 0:
        return stderr, "Error in removing clone"
    print("REMOVED!!")

    if fmt == "html":
        soup=BeautifulSoup(stdout, "lxml")
        soup.find_all("div")[1].decompose()
        return str(soup), None

    soup=bf.data(fromstring(stdout))
    return json.dumps(soup), None
