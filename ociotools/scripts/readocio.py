import PyOpenColorIO as ocio

# Load an OCIO configuration file
config = ocio.Config.CreateFromFile('../houdini/houdini-config-v1.0.0_aces-v1.3_ocio-v2.1.ocio')

# Print some basic information about the config
print(f"OCIO Config Version: {config.getMajorVersion()}.{config.getMinorVersion()}")
print(f"Default Display: {config.getDefaultDisplay()}")
print(f"Displays: {config.getDisplays()}")

# Access a specific display and its views
display = config.getDefaultDisplay()
views = config.getViews(display)
print(f"Views for Display '{display}': {views}")

# Access and print color spaces
color_spaces = config.getColorSpaces()
for cs in color_spaces:
    print(f"Color Space: {cs.getName()}")





