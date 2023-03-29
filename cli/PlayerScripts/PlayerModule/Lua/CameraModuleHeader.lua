local patchModule = script.Parent:FindFirstChild("Patch")
local patch = patchModule and require(patchModule)

local setmetatable = setmetatable
if patch then
	if patch.redirect() then
		return patch.result()
	end

	setmetatable = patch.setmetatable()
end