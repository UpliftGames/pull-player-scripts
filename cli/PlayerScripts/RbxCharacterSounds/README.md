The package has the following interface:

```Lua
-- returns the RbxCharacterSounds script
Package.get(patched: boolean): ModuleScript

-- returns a copy of the RbxCharacterSounds script
Package.getCopy(patched: boolean): ModuleScript

-- replaces the RbxCharacterSounds under StarterPlayer.StarterPlayerScripts 
-- with the provided module script
Package.replace(rbxCharacterSounds: ModuleScript)
```

When using the `--package` option the structure looks like this:

```
Package
	init.lua
	RbxCharacterSounds
		...
```