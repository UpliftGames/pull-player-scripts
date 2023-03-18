import argparse

from PullHelper import pull
from VersionInfoClass import VersionInfo

import PlayerModule
import RbxCharacterSounds

def main():
    parser = argparse.ArgumentParser('a tool for pulling the roblox playerscripts in a rojo format.')

    subparsers = parser.add_subparsers(dest='cmd', help='sub-command help')

    player_module_parser = subparsers.add_parser('playermodule', help='pulls the playermodule')
    player_module_parser.add_argument('--patch', action='store_true', help='attempt to patch the cameramodule so its api is public')

    rbxcharactersounds_parser = subparsers.add_parser('rbxcharactersounds', help='pulls the sound script')

    args = parser.parse_args()
    live_info = VersionInfo.from_live()

    def live_pull(package_name, extract_path):
        return pull(live_info.guid, package_name, extract_path)

    if args.cmd == 'playermodule':
        PlayerModule.main(live_pull, args.patch)
    elif args.cmd == 'rbxcharactersounds':
        RbxCharacterSounds.main(live_pull)

main()