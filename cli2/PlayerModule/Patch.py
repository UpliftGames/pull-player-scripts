import os
import shutil

lua_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lua')

def add_patch_init(package_path):
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

def patch(player_module_path):
    tmp_src_path = os.path.join(player_module_path, os.path.pardir, 'tmp')

    shutil.move(player_module_path, tmp_src_path)
    os.mkdir(player_module_path)

    unpatched_player_module_path = os.path.join(player_module_path, 'PlayerModuleUnpatched')
    patched_player_module_path = os.path.join(player_module_path, 'PlayerModulePatched')

    shutil.copytree(tmp_src_path, unpatched_player_module_path)
    shutil.move(tmp_src_path, patched_player_module_path)

    add_patch_init(player_module_path)
    patch_camera_module(patched_player_module_path)

    if os.path.exists(tmp_src_path):
        shutil.rmtree(tmp_src_path)
    
    return player_module_path

