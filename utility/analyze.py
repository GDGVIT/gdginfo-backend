import pickle
import subprocess

def cache_analysis(org, repo, rd):
    print("[RUNNING cache_analysis]")

def get_cached_analysis(org, repo, redis):
    print("[RUNNING] get_cached_analysis")
    redis_key = org + ":" + repo
    try:
        unpacked_pickled_object = pickle.loads(redis.get(redis_key))
        return unpacked_pickled_object, None
    except:
        data, err = extract_analysis(org, repo)
        if err is not None:
            return data, err
        pickled_object = pickle.dumps(data)
        if not rd.set(redis_key, pickled_object):
            print("[ERROR] setting in redis: cache_response")
            return "Error setting redis cache", "ERROR"
        else:
            print("[COMPLETED] cache_response")
            return data, err
        
    finally:
        return unpacked_pickled_object, None

def extract_analysis(org, repo):

    print("[RUNNING] extract_analysis")
    url="https://github.com/" + org + "/" + repo
    path="./cloned/" + org + "_" + repo

    # Cloning repo
    process = subprocess.Popen(["git", "clone", url, path], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE)

    # Applying analysis
    process = subprocess.Popen(["gitinspector", "--format=html", path], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    # Removing repo
    process = subprocess.Popen(["rm", "-r", path], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE)
    _, stderr = process.communicate()
    if len(stderr) != 0:
        return stderr, "Error in removing clone"
    return stdout, None

def analyze(repo, org, redis):
    print("[RUNNING] analyze")
    if redis is None:
        data, err = extract_analysis(org, repo)
        return data, err
    else:
        data, err = get_cached_analysis(repo, org, redis)
        return data, err

