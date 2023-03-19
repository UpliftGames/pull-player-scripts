import os
from .Package import package

def main(pull, apply_package):
    src_path = pull('extracontent-scripts.zip', os.path.join(
        'PlayerScripts', 
        'StarterPlayerScriptsCommon', 
        'RbxCharacterSounds'
    ))

    os.rename(
        os.path.join(src_path, 'init.lua'),
        os.path.join(src_path, 'init.client.lua')
    )

    if apply_package:
        src_path = package(src_path)

    return src_path
