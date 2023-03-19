import os
import shutil

lua_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Lua')

def add_package_init(package_path):
    shutil.copy(
        os.path.join(lua_folder, 'init.lua'), 
        os.path.join(package_path, 'init.lua')
    )

def package(src_path):
    tmp_src_path = os.path.join(src_path, os.path.pardir, 'tmp')

    shutil.move(src_path, tmp_src_path)
    os.mkdir(src_path)
    shutil.move(tmp_src_path, os.path.join(src_path, 'RbxCharacterSounds'))

    add_package_init(src_path)

    if os.path.exists(tmp_src_path):
        shutil.rmtree(tmp_src_path)
    
    return src_path