import os
import json
import urllib.request

VERSION_LEN = 4
MAJOR_VERSION = 0

def request_live():
    try:
        with urllib.request.urlopen('https://clientsettings.roblox.com/v2/client-version/WindowsStudio') as dl_file:
            return json.loads(dl_file.read())
    except:
        pass

def request_repo():
    if os.path.exists('PulledStudioVersion.json'):
        with open('PulledStudioVersion.json', 'r') as f:
            try:
                return json.loads(f.read())
            except:
                pass

def transform(requested):
    if not requested:
        return None
    
    version = list(map(lambda x : int(x), requested['version'].split('.')))
    return {
        'version': version,
        'wally_version': version[1:],
        'guid': requested['clientVersionUpload'],
        'requested': requested,
    }

def validate(info):
    if info:
        if len(info['version']) != VERSION_LEN:
            return False, 'Version length was not expected.'
        elif info['version'][0] != MAJOR_VERSION:
            return False, 'Major version not supported.'
    return True

def compare(a, b):
    va = a['version']
    sa = '.'.join(map(lambda x : str(x), a))

    vb = b['version']
    sb = '.'.join(map(lambda x : str(x), b))

    if sa == sb:
        return 0
    
    for i in range(len(a)):
        if va[i] == vb[i]:
            continue
        return 1 if va[i] > vb[i] else -1

def get_status(force):
    live_info = transform(request_live())
    repo_info = transform(request_repo())

    assert(validate(live_info))
    assert(validate(repo_info))

    result = None
    if live_info and (not repo_info or force):
        result = live_info
    elif live_info and repo_info:
        outdated = compare(live_info, repo_info) == 1
        result = live_info if outdated else None

    return (result != None, result)