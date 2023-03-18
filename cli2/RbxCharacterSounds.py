import os

def main(pull):
    return pull('extracontent-scripts.zip', os.path.join(
        'PlayerScripts', 
        'StarterPlayerScriptsCommon', 
        'RbxCharacterSounds'
    ))