The package has the following interface:

```Lua
-- returns a copy of the version of the package
Package.getVersionInfo(): {[string]: string}

-- returns the RbxCharacterSounds script
Package.get(): LocalScript

-- returns a copy of the RbxCharacterSounds script
Package.getCopy(): LocalScript

-- replaces the RbxCharacterSounds under StarterPlayer.StarterPlayerScripts 
-- with the provided module script
Package.replace(rbxCharacterSounds: LocalScript)
```

When using the `--package` option the structure looks like this:

```
Package
	init.lua
	RbxCharacterSounds
		...
```