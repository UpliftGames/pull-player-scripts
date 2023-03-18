# pull-player-scripts
A python tool for pulling the Roblox Player Scripts.

This is a work in progress!

## Command Line Interface

This tool can be used to pull different Roblox Player Scripts from the live version of the game into the current working directory. Most of the player scripts can also be pulled in a special package format that makes them easier to use in your games as dependencies through package managers such as [Wally](https://github.com/UpliftGames/wally).

### Global Options

These options can be specified when running the tool and are all optional.

* `--help`, `-h`
	* Prints help information about the tool and exits.
* `playermodule [title] [author]`
	* Pulls the PlayerModule and converts to a rojo format.
	* `--package` can optionally be included to attempt to pull the module in its package friendly format.
* `rbxcharactersounds [title] [author]`
	* Pulls the RbxCharacterSounds and converts to a rojo format.
	* `--package` can optionally be included to attempt to pull the module in its package friendly format.

## `--package` formats

Some of the playerscripts that can be pulled include the optional `--package` command. This command changes the format of the result so that it can be more easily used as a project dependency. This second aims to discuss the individual formats of each playerscript this tool can pull.
