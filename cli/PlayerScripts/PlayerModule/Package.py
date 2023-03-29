import os
import shutil

lua_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Lua')

def add_package_init(package_path):
    shutil.copy(
        os.path.join(lua_folder, 'init.lua'), 
        os.path.join(package_path, 'init.lua')
    )

def patch_player_module(patched_player_module_path):
    shutil.copy(
        os.path.join(lua_folder, 'Modifiers.lua'),
        os.path.join(patched_player_module_path, 'Modifiers.lua')
    )

    player_module_init_path = os.path.join(
        patched_player_module_path,
        'init.lua'
    )

    header = None
    with open(os.path.join(lua_folder, 'PlayerModuleHeader.lua'), 'r') as f:
        header = f.read()

    existing = None
    with open(player_module_init_path, 'r') as f:
        existing = f.read()

    with open(player_module_init_path, 'w') as f:
        f.write(header + '\n\n' + existing)

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
    with open(os.path.join(lua_folder, 'CameraModuleHeader.lua'), 'r') as f:
        header = f.read()

    existing = None
    with open(camera_module_init_path, 'r') as f:
        existing = f.read()

    with open(camera_module_init_path, 'w') as f:
        f.write(header + '\n\n' + existing)

def package(src_path):
    tmp_src_path = os.path.join(src_path, os.path.pardir, 'tmp')

    shutil.move(src_path, tmp_src_path)
    os.mkdir(src_path)

    unpatched_player_module_path = os.path.join(src_path, 'PlayerModuleUnpatched')
    patched_player_module_path = os.path.join(src_path, 'PlayerModulePatched')

    shutil.copytree(tmp_src_path, unpatched_player_module_path)
    shutil.move(tmp_src_path, patched_player_module_path)

    add_package_init(src_path)
    patch_player_module(patched_player_module_path)
    patch_camera_module(patched_player_module_path)

    if os.path.exists(tmp_src_path):
        shutil.rmtree(tmp_src_path)
    
    return src_path

