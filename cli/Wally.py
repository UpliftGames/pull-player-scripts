WALLY_TOML_FMT = '''[package]
name = "{author}/{title}"
version = "{version}"
registry = "https://github.com/UpliftGames/wally-index"
realm = "shared"

[dependencies]
'''

def make_wally_toml(target_path, author, title, version):
    with open(target_path, 'w') as f:
        f.write(WALLY_TOML_FMT.format(
            author=author, 
            title=title, 
            version=version
        ))

