import PyOpenColorIO as ocio

# Load the Houdini OCIO configuration file
houdini_config_path = '../houdini/houdini-config-v1.0.0_aces-v1.3_ocio-v2.1.ocio'
houdini_config = ocio.Config.CreateFromFile(houdini_config_path)

# Create a new OCIO configuration
config = ocio.Config.CreateRaw()

# Copy color spaces
color_spaces = houdini_config.getColorSpaces()
for cs in color_spaces:
    if cs.getName() == 'Apple Display P3 - Display':
        config.addColorSpace(cs)

# Copy display and views
displays = houdini_config.getDisplays()
for display in displays:
    if display == 'Apple Display P3 - Display':
        views = houdini_config.getViews(display)
        for view in views:
            color_space = houdini_config.getDisplayViewColorSpaceName(display, view)
            looks = houdini_config.getDisplayViewLooks(display, view)
            config.addDisplayView(display, view, color_space, looks)

# Copy view transforms
view_transforms = houdini_config.getViewTransforms()
for vt in view_transforms:
    config.addViewTransform(vt)

# Set the active displays and views
config.setActiveDisplays('Apple Display P3 - Display')
config.setActiveViews('Raw, ACES 1.0 - SDR Video, ACES 1.0 - SDR Video (D60 sim on D65), ACES 1.1 - HDR Video (1000 nits & Rec.2020 lim), ACES 1.1 - HDR Video (1000 nits & P3 lim), ACES 1.1 - HDR Cinema (108 nits & P3 lim), Un-tone-mapped')

# Save the configuration to a file
config_path = '../appleP3/apple_display_p3_config.ocio'
with open(config_path, 'w') as f:
    f.write(config.serialize())

print(f"Apple Display P3 OCIO configuration saved to: {config_path}")

