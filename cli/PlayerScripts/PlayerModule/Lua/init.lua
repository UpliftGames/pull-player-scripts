--!strict

local StarterPlayer = game:GetService("StarterPlayer")
local StarterPlayerScripts = StarterPlayer:WaitForChild("StarterPlayerScripts")

local MODULE_NAME = "PlayerModule"

local module = {}

local patchedModule = script:WaitForChild("PlayerModulePatched")
local unpatchedModule = script:WaitForChild("PlayerModuleUnpatched")

patchedModule.Name = MODULE_NAME
unpatchedModule.Name = MODULE_NAME

function module.get(patched: boolean): ModuleScript
	if patched then
		return patchedModule
	end
	return unpatchedModule
end

function module.getCopy(patched: boolean): ModuleScript
	return module.get(patched):Clone()
end

function module.replace(playerModule: ModuleScript)
	local existing = StarterPlayerScripts:FindFirstChild(MODULE_NAME)
	if existing then
		existing:Destroy()
	end

	playerModule.Parent = StarterPlayerScripts
end

return module