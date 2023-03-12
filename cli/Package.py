import os
import shutil

lua_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lua')

def add_package_init(package_path):
    shutil.copy(
        os.path.join(lua_folder, 'init.lua'), 
        os.path.join(package_path, 'init.lua')
    )

def patch_camera_module(patched_player_module_path):
    shutil.copy(
        os.path.join(lua_folder, 'Patch.lua'),
        os.path.join(patched_player_module_path, 'Patch.lua')
    )

    camera_module_init_path = os.path.join(
        patched_player_module_path,
        'CameraModule', 
        'init.lua'
    )

    header = None
    with open(os.path.join(lua_folder, 'Header.lua'), 'r') as f:
        header = f.read()

    existing = None
    with open(camera_module_init_path, 'r') as f:
        existing = f.read()

    with open(camera_module_init_path, 'w') as f:
        f.write(header + '\n\n' + existing)

def make_package(should_package, player_module_path):
    package_path = 'src'

    if os.path.exists(package_path):
        shutil.rmtree(package_path)

    if not should_package:
        shutil.move(player_module_path, package_path)
    else:
        os.mkdir(package_path)
        unpatched_player_module_path = os.path.join(package_path, 'PlayerModuleUnpatched')
        patched_player_module_path = os.path.join(package_path, 'PlayerModulePatched')
        shutil.copytree(player_module_path, unpatched_player_module_path)
        shutil.move(player_module_path, patched_player_module_path)
        add_package_init(package_path)
        patch_camera_module(patched_player_module_path)
    
    return package_path

