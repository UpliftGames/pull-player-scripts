import os
import argparse

from PullHelper import pull
from FileHelper import fmt_create
from VersionInfoClass import VersionInfo


import PlayerModule
import RbxCharacterSounds

def main():
    parser = argparse.ArgumentParser('a tool for pulling the roblox playerscripts in a rojo format.')

    subparsers = parser.add_subparsers(dest='cmd', help='sub-command help')

    player_module_parser = subparsers.add_parser('playermodule', help='pulls the playermodule')
    player_module_parser.add_argument('--package', action='store_true', help='attempt to package the playermodule in a wally friendly format')

    rbxcharactersounds_parser = subparsers.add_parser('rbxcharactersounds', help='pulls the rbxcharactersounds script')
    rbxcharactersounds_parser.add_argument('--package', action='store_true', help='attempt to package the rbxcharactersounds in a wally friendly format')

    file_creator_parser = subparsers.add_parser('project_add', help='creates/updates a number of files important extending the workflow of this tool')
    file_creator_parser.add_argument('--wally', nargs=3, type=str, metavar=('[author]', '[title]', '[version]'), help='create a wally toml in the root of the cwd')
    file_creator_parser.add_argument('--rojo', nargs=1, type=str, metavar=('[name]'), help='create a default.project.json in the root of the cwd')

    args = parser.parse_args()
    live_info = VersionInfo.from_live()

    def live_pull(package_name, extract_path):
        return pull(live_info.guid, package_name, extract_path)

    final_path = None
    if args.cmd == 'playermodule':
        final_path = PlayerModule.main(live_pull, args.package)
    elif args.cmd == 'rbxcharactersounds':
        final_path = RbxCharacterSounds.main(live_pull, args.package)
    elif args.cmd == 'project_add':
        if args.wally:
            fmt_create('wally.toml', args.wally)
        if args.rojo:
            fmt_create('default.project.json', args.rojo)
    
    if final_path:
        live_info.to_file(os.path.join(final_path, 'VersionInfo.json'))