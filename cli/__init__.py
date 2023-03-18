import os
import argparse

from .PullHelper import pull
from .FileHelper import fmt_create
from .VersionInfoClass import VersionInfo

from .PlayerScripts.PlayerModule import main as PlayerModule
from .PlayerScripts.RbxCharacterSounds import main as RbxCharacterSounds

def main():
    parser = argparse.ArgumentParser('a tool for pulling the roblox playerscripts in a rojo format.')

    subparsers = parser.add_subparsers(dest='cmd', help='sub-command help')

    # handle these as subparsers as the commands may differ if support for more playerscripts is added in the future
    player_module_parser = subparsers.add_parser('playermodule', help='pulls the playermodule')
    player_module_parser.add_argument('title', type=str, help='name of the project')
    player_module_parser.add_argument('author', type=str, help='author of the project')
    player_module_parser.add_argument('--package', action='store_true', help='attempt to package the playermodule in a wally friendly format')

    rbxcharactersounds_parser = subparsers.add_parser('rbxcharactersounds', help='pulls the rbxcharactersounds script')
    rbxcharactersounds_parser.add_argument('title', type=str, help='name of the project')
    rbxcharactersounds_parser.add_argument('author', type=str, help='author of the project')
    rbxcharactersounds_parser.add_argument('--package', action='store_true', help='attempt to package the rbxcharactersounds in a wally friendly format')

    args = parser.parse_args()
    live_info = VersionInfo.from_live()

    def live_pull(package_name, extract_path):
        return pull(live_info.guid, package_name, extract_path)

    final_path = None
    if args.cmd == 'playermodule':
        final_path = PlayerModule(live_pull, args.package)
    elif args.cmd == 'rbxcharactersounds':
        final_path = RbxCharacterSounds(live_pull, args.package)
    
    if final_path:
        live_info.to_file(os.path.join(final_path, 'VersionInfo.json'))

        fmt_create('wally.toml', [args.author, args.title, live_info.get_wally_version()])
        fmt_create('default.project.json', [args.title])