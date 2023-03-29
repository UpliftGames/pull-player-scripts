--!strict

local PlayerModule = script.Parent

local module = {}

function module.add(modifier: ModuleScript, priority: number?)
	local copy = modifier:Clone()
	copy:SetAttribute("Priority", priority)
	copy.Parent = script
end

function module.apply()
	local children = script:GetChildren() :: {ModuleScript}

	table.sort(children, function(a, b)
		local pa = a:GetAttribute("Priority") :: number?
		local pb = b:GetAttribute("Priority") :: number?

		if pa and pb then
			return pa < pb
		elseif pb then
			return false
		end

		return true			
	end)

	for _, child in children do
		local callback = require(child) :: (ModuleScript) -> ()
		callback(PlayerModule)
	end
end

return module