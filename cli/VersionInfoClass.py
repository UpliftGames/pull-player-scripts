import os
import json
import urllib.request

def request_live():
    with urllib.request.urlopen('https://clientsettings.roblox.com/v2/client-version/WindowsStudio') as dl_file:
        return json.loads(dl_file.read())

class VersionInfo:
    def __init__(self, version, guid):
        self.version = version
        self.guid = guid
        assert(self.__validate())

    def __validate(self):
        return (
            len(self.version) == 4
            and self.version[0] == 0
        )
    
    def __get_version_str(self):
        return '.'.join(map(lambda x : str(x), self.version))
    
    def get_wally_version(self):
        return '.'.join(map(lambda x : str(x), self.version[1:]))

    def to_json(self):
        return json.dumps({
            'version': '.'.join(map(lambda x : str(x), self.version)),
            'guid': self.guid,
        }, indent='\t')
    
    def to_file(self, path):
        with open(path, 'w') as f:
            f.write(self.to_json())
    
    def from_path(path):
        if os.path.exists(path):
            with open(path, 'r') as f:
                repo = json.loads(f.read())
                transformed_version = list(map(lambda x : int(x), repo['version'].split('.')))
                return VersionInfo(transformed_version, repo['guid'])
    
    def from_live():
        live = request_live()
        transformed_version = list(map(lambda x : int(x), live['version'].split('.')))
        return VersionInfo(transformed_version, live['clientVersionUpload'])
    
    def compare(self, info):
        v1 = self.__get_version_str()
        v2 = info.__get_version_str()

        if v1 == v2:
            return 0
        
        for i in range(len(self.version)):
            if self.version[i] == info.version[i]:
                continue
            return 1 if self.version[i] > info.version[i] else -1