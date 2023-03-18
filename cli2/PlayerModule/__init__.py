import os
from .Patch import patch

def main(pull, apply_patch):
    src_path = pull('extracontent-scripts.zip', os.path.join(
        'PlayerScripts', 
        'StarterPlayerScripts', 
        'PlayerModule'
    ))

    if apply_patch:
        src_path = patch(src_path)

    return src_path