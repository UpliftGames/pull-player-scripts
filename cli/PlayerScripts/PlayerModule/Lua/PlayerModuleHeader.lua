local modifiersModule = script:FindFirstChild("Modifiers")
local modifiers = modifiersModule and require(modifiersModule)

if modifiers then
	modifiers.apply()
end