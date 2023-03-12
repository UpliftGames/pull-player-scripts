import os
import shutil
import zipfile
import urllib.request

def download_url(url, target_path):
    with urllib.request.urlopen(url) as dl_file:
        with open(target_path, 'wb') as out_file:
            out_file.write(dl_file.read())

def download_package(package_name, version_guid):
    url = 'https://setup.rbxcdn.com/{}-{}'.format(version_guid, package_name)
    download_url(url, package_name)

def convert_to_rojo_format(directory):
    for fname in os.listdir(directory):
        fpath = os.path.join(directory, fname)
        if os.path.isdir(fpath):
            lua_path = os.path.join(directory, fname + '.lua')
            if os.path.exists(lua_path):
                os.replace(lua_path, os.path.join(fpath, 'init.lua'))
                convert_to_rojo_format(fpath)
                os.replace(fpath, os.path.join(directory, fname.split('.', 1)[0]))
        elif fname.endswith('.robloxrc'):
            os.remove(fpath)

def extract_player_module(zip_path, target_path):
    with zipfile.ZipFile(zip_path, 'r') as zip:
        zip.extractall('tmp')

        convert_to_rojo_format(os.path.join('tmp', 'PlayerScripts', 'StarterPlayerScripts'))

        shutil.copytree(
            os.path.join('tmp', 'PlayerScripts', 'StarterPlayerScripts', 'PlayerModule'),
            target_path
        )

def pull(version_guid):
    target_path = 'PlayerModule'
    package_name = 'extracontent-scripts.zip'

    if os.path.exists(target_path):
        shutil.rmtree(target_path)

    download_package(package_name, version_guid)
    extract_player_module(package_name, target_path)

    if os.path.exists(package_name):
        os.remove(package_name)
    if os.path.exists('tmp'):
        shutil.rmtree('tmp')
    
    return target_path