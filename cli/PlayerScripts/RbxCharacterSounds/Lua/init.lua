--!strict

local StarterPlayer = game:GetService("StarterPlayer")
local StarterPlayerScripts = StarterPlayer:WaitForChild("StarterPlayerScripts")

local module = {}
local RbxCharacterSounds = script:WaitForChild("RbxCharacterSounds")
local versionInfo = require(script:WaitForChild("VersionInfo"))

local MODULE_NAME = RbxCharacterSounds.Name

function module.getVersionInfo(): {[string]: string}
	return table.clone(versionInfo)
end

function module.get(): ModuleScript
	return RbxCharacterSounds
end

function module.getCopy(): ModuleScript
	return module.get():Clone()
end

function module.replace(rbxCharacterSounds: ModuleScript)
	local existing = StarterPlayerScripts:FindFirstChild(MODULE_NAME)
	if existing then
		existing:Destroy()
	end

	rbxCharacterSounds.Parent = StarterPlayerScripts
end

return module