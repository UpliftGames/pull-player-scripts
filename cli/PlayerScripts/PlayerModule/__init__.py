import os
from .Package import package

def main(pull, apply_package):
    src_path = pull('extracontent-scripts.zip', os.path.join(
        'PlayerScripts', 
        'StarterPlayerScripts', 
        'PlayerModule'
    ))

    if apply_package:
        src_path = package(src_path)

    return src_path