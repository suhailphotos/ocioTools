import PyOpenColorIO as ocio

# Load the Houdini OCIO configuration file
houdini_config_path = '../houdini/houdini-config-v1.0.0_aces-v1.3_ocio-v2.1.ocio'
houdini_config = ocio.Config.CreateFromFile(houdini_config_path)

# Load the Blender OCIO configuration file
blender_config_path = '../blender/config.ocio'
blender_config = ocio.Config.CreateFromFile(blender_config_path)

# Function to copy displays and views from Houdini to Blender config
def copy_displays_and_views(houdini_config, blender_config):
    displays = houdini_config.getDisplays()
    for display in displays:
        if display == 'Apple Display P3 - Display':
            views = houdini_config.getViews(display)
            for view in views:
                color_space = houdini_config.getDisplayViewColorSpaceName(display, view)
                looks = houdini_config.getDisplayViewLooks(display, view)
                blender_config.addDisplayView(display, view, color_space, looks)
                print(f"Copied view '{view}' for display '{display}' with color space '{color_space}' and looks '{looks}'")
    return blender_config

# Function to copy color spaces from Houdini to Blender config
def copy_color_spaces(houdini_config, blender_config):
    color_spaces = houdini_config.getColorSpaces()
    for cs in color_spaces:
        if cs.getName() == 'Apple Display P3 - Display':
            blender_config.addColorSpace(cs)
    return blender_config

# Function to copy view transforms from Houdini to Blender config
def copy_view_transforms(houdini_config, blender_config):
    view_transforms = houdini_config.getViewTransforms()
    for vt in view_transforms:
        blender_config.addViewTransform(vt)
    return blender_config

# Function to update active displays and views
def update_active_displays_and_views(blender_config):
    active_displays = blender_config.getActiveDisplays().split(', ')
    if 'Apple Display P3 - Display' not in active_displays:
        active_displays.append('Apple Display P3 - Display')
        blender_config.setActiveDisplays(', '.join(active_displays))
    
    active_views = blender_config.getActiveViews().split(', ')
    new_views = [
        'ACES 1.0 - SDR Video',
        'ACES 1.0 - SDR Video (D60 sim on D65)',
        'ACES 1.1 - HDR Video (1000 nits & Rec.2020 lim)',
        'ACES 1.1 - HDR Video (1000 nits & P3 lim)',
        'ACES 1.1 - HDR Cinema (108 nits & P3 lim)',
        'Un-tone-mapped'
    ]
    for view in new_views:
        if view not in active_views:
            active_views.append(view)
    blender_config.setActiveViews(', '.join(active_views))

# Copy the relevant information
blender_config = copy_displays_and_views(houdini_config, blender_config)
blender_config = copy_color_spaces(houdini_config, blender_config)
blender_config = copy_view_transforms(houdini_config, blender_config)
update_active_displays_and_views(blender_config)

# Save the modified configuration directly to a new file
modified_blender_config_path = '../blender/modified_blender_config.ocio'
with open(modified_blender_config_path, 'w') as f:
    f.write(blender_config.serialize())

print(f"Modified Blender OCIO configuration saved to: {modified_blender_config_path}")
