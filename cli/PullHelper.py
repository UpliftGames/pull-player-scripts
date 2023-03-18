import os
import shutil
import zipfile
import urllib.request

def download_url(url, target_path):
    with urllib.request.urlopen(url) as dl_file:
        with open(target_path, 'wb') as out_file:
            out_file.write(dl_file.read())

def download_package(target_path, package_name, version_guid):
    url = 'https://setup.rbxcdn.com/{}-{}'.format(version_guid, package_name)
    download_url(url, target_path)

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

def extract(zip_path, extract_path, target_path):
    with zipfile.ZipFile(zip_path, 'r') as zip:
        extracted_path = os.path.join(zip_path, os.path.pardir, 'extracted')
        zip.extractall(extracted_path)

        convert_to_rojo_format(os.path.join(extracted_path, extract_path, os.path.pardir))

        shutil.copytree(
            os.path.join(extracted_path, extract_path),
            target_path
        )

def pull(version_guid, package_name, extract_path):
    tmp_path = 'tmp'
    target_path = 'src'
    zip_path = os.path.join(tmp_path, package_name)

    if os.path.exists(target_path):
        shutil.rmtree(target_path)
    
    os.makedirs(tmp_path)

    download_package(zip_path, package_name, version_guid)
    extract(zip_path, extract_path, target_path)

    if os.path.exists(tmp_path):
        shutil.rmtree(tmp_path)
    
    return target_path