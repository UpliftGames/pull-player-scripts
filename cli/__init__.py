import os
import json
import argparse

from .VersionInfo import get_status
from .Package import make_package
from .Wally import make_wally_toml
from .Pull import pull

def log(msg):
    print(msg)

def write_to_env(key, value):
    env_file = os.getenv('GITHUB_ENV')
    if env_file:
        with open(env_file, "a") as myfile:
            myfile.write('{}={}\n'.format(key, value))

def main():
    parser = argparse.ArgumentParser('A tool for pulling the Roblox PlayerModule in a rojo format.')
    parser.add_argument('--force', action='store_true', help='forcefully pull the playermodule even if the repository is up to date')
    parser.add_argument('--package', action='store_true', help='package the playermodule for easier use in game')
    parser.add_argument('--wally', nargs=2, type=str, metavar=('[author]', '[title]'), help='create a wally toml in the root of the cwd')
    parser.add_argument('--debugwallyv', type=str, help='set a debug wally version for testing')
    args = parser.parse_args()

    should_pull, ver_info = get_status(args.force)

    write_to_env('SHOULD_PULL', 'true' if should_pull else 'false')

    if should_pull:
        player_module_path = pull(ver_info['guid'])

        with open(os.path.join(player_module_path, 'VersionInfo.json'), 'w') as f:
            f.write(json.dumps({
                'version': ver_info['requested']['version'],
                'guid': ver_info['guid'],
            }, indent='\t'))

        make_package(args.package, player_module_path)

        with open('PulledStudioVersion.json', 'w') as f:
            f.write(json.dumps(ver_info['requested'], indent='\t'))
        
        if args.wally:
            author, title = tuple(args.wally)
            wally_version = '.'.join(map(lambda x : str(x), ver_info['wally_version']))
            if args.debugwallyv:
                wally_version = args.debugwallyv
            make_wally_toml('wally.toml', author, title, wally_version)
        
        write_to_env('VERSION', ver_info['requested']['version'])
        



