The package has the following interface:

```Lua
-- returns the RbxCharacterSounds script
Package.get(patched: boolean): ModuleScript

-- returns a copy of the RbxCharacterSounds script
Package.getCopy(patched: boolean): ModuleScript

-- replaces the RbxCharacterSounds under StarterPlayer.StarterPlayerScripts 
-- with a copy and then returns that copy
Package.replace(patched: boolean): ModuleScript
```

When using the `--package` option the structure looks like this:

```
Package
	init.lua
	RbxCharacterSounds
		...
```