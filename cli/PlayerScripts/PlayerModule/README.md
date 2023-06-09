The package has the following interface:

```Lua
-- returns a copy of the version of the package
Package.getVersionInfo(): {[string]: string}

-- returns either the patched or unpatched version the PlayerModule
Package.get(patched: boolean): ModuleScript

-- returns a copy of either the patched or unpatched version the PlayerModule
Package.getCopy(patched: boolean): ModuleScript

-- replaces the PlayerModule under StarterPlayer.StarterPlayerScripts 
-- with the provided module script
Package.replace(playerModule: ModuleScript)
```

## Patched CameraModule

When using the `--package` command two different copies of the CameraModule are generated. The structure looks something like this:

```
Package
	init.lua
	PlayerModuleUnpatched
		...
	PlayerModulePatched
		Patch.lua (new file)
		Modifiers.lua (new file)
		CameraModule
			init.lua (modified)
		ControlModule
			...
```

The `PlayerModuleUnpatched` is a completely unmodified version the PlayerModule and should work as long as Roblox themselves didn't push a release with broken PlayerModules.

The `PlayerModulePatched` however is a different story. This is a copy of the unmodified scripts with some slight additions that attempt to open up access to the CameraModule API which normally returns an empty lua table. These changes try to be very unassuming and work regardless of the changes Roblox makes, but there's always the possibility they will break and need some manual fixing. 

Since this is a open source project it's worth discussing how this module is "patched" so that in the event something does go wrong others have context on how it can be fixed.

### Patch Criteria

#### Modifiers.lua

A submodule is added to the patched `PlayerModule` which provides the ability to write custom code additions/modifications to the `PlayerModule`. The interface of this module looks like this:

```Lua
-- adds custom modifier module script to be run at a certain priority level
-- if no priority is specified then the code will be run at the end in no particular order
Modifiers.add(modifier: ModuleScript, priority: number?)
```

The modifier modules themselves are quite straightforward. They should return a function that accepts one argument: reference to the `PlayerModule` instance. For example a modifier might look like this:

```Lua
-- some module in the game that handles player control
local controlBindings = require(...)

return function (PlayerModule: ModuleScript)
	local controlObject = require(PlayerModule.ControlModule)

	controlBindings.setEnableCallback(function(enabled)
		if enabled then
			controlObject:Enable()
		else
			controlObject:Disable()
		end
	end)
end
```

#### Only header additions

Your first thought if asked to make the CameraModule API public might be to write a regex replace or modify lines in the existing source string so that the module doesn't return an empty table.

The problem with this approach is that it makes very strong assumptions about the future structure of the CameraModule. Some future update could completely change variables or move code around and that makes writing a patch using the above idea very likely to provide a broken result.

A safer approach is to come up with a way to patch the CameraModule without touching a single line that Roblox themselves have written. This can be done by prepending code to the top of the CameraModule. This ensures that our code runs first and can take control of the environment.

Currently control of the environment is used to overwrite `setmetatable`. At the time of writing there's only one call of this function in `CameraModule.new` and one of the arguments passed is the value we want to get ahold of.

The main concern of this approach is that it depends heavily on the fact that `semetatable` is only called once. We can of course compile of all the arguments passed into a list, but then it becomes a question of how to identify the value in that list that represents the CameraModule API. We don't want to make any assumptions about the form of this value because it may change. For now we're banking on the fact that in the context of the CameraModule the `setmetatable` function will only be called once.

#### Camera Module should return the API

If you're familiar with some of my other work on the CameraModule API you may know that I have already previously discovered a way to get the CameraModule api from an unpatched version of the PlayerModule.

```Lua
local CameraModule = ...
local TransparencyController = require(CameraModule.TransparencyController)

local oldTransparencyControllerNew = TransparencyController.new

local result = nil
local bind = Instance.new("BindableEvent")

TransparencyController.new = function(...)
	-- set this back its original value so it behaves as expected next time it's called
	TransparencyController.new = oldTransparencyControllerNew

	-- get the parent function and call it
	-- this is equivalent to calling `result = CameraModule.new()`
	local cameraModuleNew = debug.info(2, "f")
	result = cameraModuleNew()

	bind:Fire()
	bind.Event:Wait() -- yield forever!
end

-- the patch has been setup, now we wait!
task.spawn(function()
	require(CameraModule)
end)

while not result do
	bind.Event:Wait()
end

return result -- the public camera module api!
```

This method involves going into the `TransparencyController` (a dependency module of the CameraModule) and modifying one of its functions temporarily to get the `CameraModule.new` function then call and return its result.

This does work, but I chose not to use it in this case for a couple of reasons.

The first reason is that this makes assumptions about the existence of the `TransparencyController`. Who knows? This module could cease to exist, or where its called could be moved and the whole patch goes out the window.

The second reason is that this method creates a small memory leak. There are a number of benign event connections made before it's possible to hook in and apply a patch. These connection don't have any impact on result nor do they have significant performance impact, but they still exist. They're a small price to pay if you do need to hook in via this method, but if you don't have to then why bother?

The third and final reason is that using this method stops the original camera module from returning the proper result. In the above example I choose to yield forever in the original module so that no further memory leaks are created, this means that the module never returns! If you tried to require it from a different script you'd be waiting forever! The workaround I had for this was to rename the original module and create a proxy module that returns the `result` value instead. 

```
PlayerModule
	CameraModule (proxy)
		...
	_CameraModule (the real CameraModule)
	ControlModule
```

This comes with some risk because it means we're no longer respecting the parent-child hierarchy the original module was written for so there's a possibility of something breaking. You could of course just not move the children to the proxy module, but then other pieces of code in your game might break depending on what they assumed about the structure of the PlayerModule.